import os
import json
import random
import pandas as pd
import torch
import torchaudio
import librosa
import numpy as np
import soundfile as sf

import copy_outputs

from pathlib import Path
from datasets import Dataset, ClassLabel, load_dataset, load_metric, concatenate_datasets
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from transformers import Wav2Vec2CTCTokenizer, Wav2Vec2FeatureExtractor, Wav2Vec2Processor, Wav2Vec2ForCTC, TrainingArguments, Trainer

import text_preprocess


"""

Train an acoustic model by fine tuning the wav2vec2 large XLSR pre-trained models by Facebook for Welsh.

Much of the code in this file was lifted from a HuggingFace blog entry:

Fine-Tune XLSR-Wav2Vec2 for low-resource ASR with Transformers
https://huggingface.co/blog/fine-tune-xlsr-wav2vec2

by Patrick von Platen
"""


#
def remove_special_characters(batch):
    batch["sentence"] = text_preprocess.cleanup(batch["sentence"]) + " "
    return batch

def extract_all_chars(batch):
    all_text = " ".join(batch["sentence"])
    vocab = list(set(all_text))
    return {"vocab": [vocab], "all_text": [all_text]}

def show_random_elements(dataset, num_examples=10):
    assert num_examples <= len(dataset), "Can't pick more elements than there are in the dataset."
    picks = []
    for _ in range(num_examples):
        pick = random.randint(0, len(dataset)-1)
        while pick in picks:
            pick = random.randint(0, len(dataset)-1)
        picks.append(pick)

    df = pd.DataFrame(dataset[picks])
    print (df.to_html())


@dataclass
class DataCollatorCTCWithPadding:
    """
    Data collator that will dynamically pad the inputs received.
    Args:
        processor (:class:`~transformers.Wav2Vec2Processor`)
            The processor used for proccessing the data.
        padding (:obj:`bool`, :obj:`str` or :class:`~transformers.tokenization_utils_base.PaddingStrategy`, `optional`, defaults to :obj:`True`):
            Select a strategy to pad the returned sequences (according to the model's padding side and padding index)
            among:
            * :obj:`True` or :obj:`'longest'`: Pad to the longest sequence in the batch (or no padding if only a single
              sequence if provided).
            * :obj:`'max_length'`: Pad to a maximum length specified with the argument :obj:`max_length` or to the
              maximum acceptable input length for the model if that argument is not provided.
            * :obj:`False` or :obj:`'do_not_pad'` (default): No padding (i.e., can output a batch with sequences of
              different lengths).
        max_length (:obj:`int`, `optional`):
            Maximum length of the ``input_values`` of the returned list and optionally padding length (see above).
        max_length_labels (:obj:`int`, `optional`):
            Maximum length of the ``labels`` returned list and optionally padding length (see above).
        pad_to_multiple_of (:obj:`int`, `optional`):
            If set will pad the sequence to a multiple of the provided value.
            This is especially useful to enable the use of Tensor Cores on NVIDIA hardware with compute capability >=
            7.5 (Volta).
    """
    processor: Wav2Vec2Processor
    padding: Union[bool, str] = True
    max_length: Optional[int] = None
    max_length_labels: Optional[int] = None
    pad_to_multiple_of: Optional[int] = None
    pad_to_multiple_of_labels: Optional[int] = None

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        # split inputs and labels since they have to be of different lenghts and need
        # different padding methods
        input_features = [{"input_values": feature["input_values"]} for feature in features]
        label_features = [{"input_ids": feature["labels"]} for feature in features]

        batch = self.processor.pad(
            input_features,
            padding=self.padding,
            max_length=self.max_length,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors="pt",
        )
        with self.processor.as_target_processor():
            labels_batch = self.processor.pad(
                label_features,
                padding=self.padding,
                max_length=self.max_length_labels,
                pad_to_multiple_of=self.pad_to_multiple_of_labels,
                return_tensors="pt",
            )

        # replace padding with -100 to ignore loss correctly
        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)

        batch["labels"] = labels

        return batch


def speech_file_to_array_fn(batch):
    speech_array, sampling_rate = torchaudio.load(batch["path"])
    batch["speech"] = speech_array[0].numpy()
    batch["sampling_rate"] = sampling_rate
    batch["target_text"] = batch["sentence"]
    return batch


def resample(batch):
    batch["speech"] = librosa.resample(np.asarray(batch["speech"]), 48_000, 16_000)
    batch["sampling_rate"] = 16_000
    return batch


def prepare_dataset(batch):
    # check that all files have the correct sampling rate
    assert (
        len(set(batch["sampling_rate"])) == 1
    ), f"Make sure all inputs have the same sampling rate of {processor.feature_extractor.sampling_rate}."

    batch["input_values"] = processor(batch["speech"], sampling_rate=batch["sampling_rate"][0]).input_values
                                        
    with processor.as_target_processor():
        batch["labels"] = processor(batch["target_text"]).input_ids

    return batch


def compute_metrics(pred):
    pred_logits = pred.predictions
    pred_ids = np.argmax(pred_logits, axis=-1)

    pred.label_ids[pred.label_ids == -100] = processor.tokenizer.pad_token_id

    pred_str = processor.batch_decode(pred_ids)

    # we do not want to group tokens when computing the metrics
    label_str = processor.batch_decode(pred.label_ids, group_tokens=False)
    wer = wer_metric.compute(predictions=pred_str, references=label_str)

    return {"wer": wer}


def train(models_root_dir, model_name):

    global processor
    global tokenizer
    global model
    global wer_metric

    language = "cy"    

    # CV 6.1 (cy) training+dev set provides approximately 16 hours of unique sentence recordings.
    #
    dataset_name="common_voice"
    training_split="train+validation"

    # Or use an alternative training set - all validated Common Voice recordings minus recordings 
    # of sentences present in the test set. 
    # (in CV 6.1 the validated set ammounts to 24 hours with some sentences having been recorded 
    #  multiple times by multiple speakers.)
    #
    #dataset_name-"custom_common_voice.py"
    #training_split="validated"

    output_dir=os.path.join(Path.home(), model_name)

    print (output_dir, language, model_name) 

    print ("\nLoading %s datasets" % dataset_name)
    if dataset_name=="custom_common_voice.py":
        common_voice_validated = load_dataset(dataset_name, language, split=training_split)

        df_validated = common_voice_validated.to_pandas()
        df_test = common_voice_test.to_pandas()
        test_sentences = df_test['sentence'].tolist()

        df_train = df_validated[~df_validated['sentence'].isin(test_sentences)]
        df_train = df_train.set_index('path')

        common_voice_train = Dataset.from_pandas(df_train)
    else:
        common_voice_train = load_dataset(dataset_name, language, split=training_split)

    #
    common_voice_test = load_dataset(dataset_name, language, split="test")


    print ("\nRemoving unnecessary columns")
    common_voice_train = common_voice_train.remove_columns(["accent", "age", "client_id", "down_votes", "gender", "locale", "segment", "up_votes"])
    common_voice_test = common_voice_test.remove_columns(["accent", "age", "client_id", "down_votes", "gender", "locale", "segment", "up_votes"])


    print ("\nRemoving unnecesary characters from sentences ")
    common_voice_train = common_voice_train.map(remove_special_characters)
    common_voice_test = common_voice_test.map(remove_special_characters)


    print ("\nExtracting tokens and saving to vocab.%s.json" % language)
    vocab_train = common_voice_train.map(extract_all_chars, batched=True, batch_size=-1, keep_in_memory=True, remove_columns=common_voice_train.column_names)
    vocab_test = common_voice_test.map(extract_all_chars, batched=True, batch_size=-1, keep_in_memory=True, remove_columns=common_voice_test.column_names)

    vocab_list = list(set(vocab_train["vocab"][0]) | set(vocab_test["vocab"][0]))

    vocab_dict = {v: k for k, v in enumerate(vocab_list)}

    vocab_dict["|"] = vocab_dict[" "]
    del vocab_dict[" "]

    vocab_dict["[UNK]"] = len(vocab_dict)
    vocab_dict["[PAD]"] = len(vocab_dict)
    print(len(vocab_dict))
    print(vocab_dict)

    with open('vocab.%s.json' % language, 'w') as vocab_file:
        json.dump(vocab_dict, vocab_file)

    print ("\nConstructing tokenizer")
    tokenizer = Wav2Vec2CTCTokenizer("./vocab.%s.json" % language, unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")

    print ("\nFeature Extractor") 
    feature_extractor = Wav2Vec2FeatureExtractor(feature_size=1, sampling_rate=16000, padding_value=0.0, do_normalize=True, return_attention_mask=True)

    print ("\nConstructing Processor")
    processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)
    processor.save_pretrained(output_dir)

    print ("\nCreating array from speech files")
    common_voice_train = common_voice_train.map(speech_file_to_array_fn, remove_columns=common_voice_train.column_names)
    common_voice_test = common_voice_test.map(speech_file_to_array_fn, remove_columns=common_voice_test.column_names)
    
    print ("\nDownsampling all speech files")
    common_voice_train = common_voice_train.map(resample)
    common_voice_test = common_voice_test.map(resample)

    print ("\nPreparing the training dataset")
    common_voice_train = common_voice_train.map(prepare_dataset, remove_columns=common_voice_train.column_names, batch_size=8, num_proc=4, batched=True)

    print ("\nPreparing validation set")
    common_voice_test = common_voice_test.map(prepare_dataset, remove_columns=common_voice_test.column_names, batch_size=8, num_proc=4, batched=True)

    print ("\nSetting up data collator")
    data_collator = DataCollatorCTCWithPadding(processor=processor, padding=True)

    wer_metric = load_metric("wer")

    print ("\nLoading pre-trained facebook/wav2vec2-large-xlsr model")
    # see https://huggingface.co/transformers/model_doc/wav2vec2.html?highlight=mask_time_prob#transformers.Wav2Vec2Config
    model = Wav2Vec2ForCTC.from_pretrained(
        "facebook/wav2vec2-large-xlsr-53",
        activation_dropout=0.055,
        attention_dropout=0.055,
        hidden_dropout=0.047,
        feat_proj_dropout=0.04,
        mask_time_prob=0.082,
        layerdrop=0.041,
        gradient_checkpointing=True, 
        ctc_loss_reduction="mean", 
        pad_token_id=processor.tokenizer.pad_token_id,
        vocab_size=len(processor.tokenizer)
    )

    model.freeze_feature_extractor()

    # see https://huggingface.co/transformers/main_classes/trainer.html?highlight=group_by_length#transformers.TrainingArguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        group_by_length=True,
        per_device_train_batch_size=16,
        gradient_accumulation_steps=2,
        evaluation_strategy="steps",
        num_train_epochs=30,
        save_steps=400,
        eval_steps=400,
        logging_steps=400,
        learning_rate=3e-4,
        warmup_steps=400,
        save_total_limit=1,
    )

    print ("\nConstructing trainer")
    trainer = Trainer(
        model=model,
        data_collator=data_collator,
        args=training_args,
        compute_metrics=compute_metrics,
        train_dataset=common_voice_train,
        eval_dataset=common_voice_test,
        tokenizer=processor.feature_extractor,
    )

    print ("\nTraining...")
    trainer.train()

    print ("\n\nModel trained. See %s" % output_dir)

    print ("\n\nCopying files to models directory..")
    output_model_dir = os.path.join(models_root_dir, model_name)
    return copy_outputs.copy_for_evaluation_or_publishing(output_dir, output_model_dir)


if __name__ == "__main__":
    train()

