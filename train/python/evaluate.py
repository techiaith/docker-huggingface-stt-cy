import os
import torch
import torchaudio
import json
import numpy as np
import yaml

from datasets import load_dataset, load_metric
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import text_preprocess

from ctcdecode import CTCBeamDecoder


"""

Much of the code in this file was lifted from a HuggingFace blog entry:

Fine-Tune XLSR-Wav2Vec2 for low-resource ASR with Transformers
https://huggingface.co/blog/fine-tune-xlsr-wav2vec2

by Patrick von Platen

An implementation of a CTC (Connectionist Temporal Classification) beam search decoder with
KenLM language models support from https://github.com/parlance/ctcdecode has been added.
 
"""


# Preprocessing the datasets.
# We need to read the aduio files as arrays
def speech_file_to_array_fn(batch):
    batch["sentence"] = text_preprocess.cleanup(batch["sentence"]).strip() # + " "
    speech_array, sampling_rate = torchaudio.load(batch["path"])
    batch["speech"] = resampler(speech_array).squeeze().numpy()
    return batch

def evaluate(batch):
    inputs = processor(batch["speech"], sampling_rate=16_000, return_tensors="pt", padding=True)
    
    with torch.no_grad():
       logits = model(inputs.input_values.to("cuda"), attention_mask=inputs.attention_mask.to("cuda")).logits

    pred_ids = torch.argmax(logits, dim=-1)

    batch["pred_strings"] = processor.batch_decode(pred_ids)[0].strip()

    beam_results, beam_scores, timesteps, out_lens = ctcdecoder.decode(logits)
    pred_with_ctc = "".join(vocab[n] for n in beam_results[0][0][:out_lens[0][0]])
    batch["pred_strings_with_ctc"]=pred_with_ctc.strip()

    beam_results, beam_scores, timesteps, out_lens = ctcdecoder_withlm.decode(logits)
    pred_with_lm = "".join(vocab[n] for n in beam_results[0][0][:out_lens[0][0]])
    batch["pred_strings_with_lm"]=pred_with_lm.strip()

    return batch


#
test_dataset = load_dataset("common_voice", "cy", split="test")

wer = load_metric("wer")

models_root_dir="/models"
wav2vec2_model_name = "wav2vec2-xlsr-ft-cy"
kenlm_model_name= "kenlm-cy"

wav2vec_model_dir = os.path.join(models_root_dir, wav2vec2_model_name)
processor = Wav2Vec2Processor.from_pretrained(wav2vec_model_dir)
model = Wav2Vec2ForCTC.from_pretrained(wav2vec_model_dir)

model.to("cuda")

resampler = torchaudio.transforms.Resample(48_000, 16_000)

vocab=processor.tokenizer.convert_ids_to_tokens(range(0, processor.tokenizer.vocab_size))
space_ix = vocab.index('|')
vocab[space_ix]=' '

# load alpha, betas. 
kenlm_model_dir=os.path.join(models_root_dir, kenlm_model_name)
with open(os.path.join(kenlm_model_dir, "config_ctc.yaml"), 'r') as config_file:
    ctc_lm_params=yaml.load(config_file, Loader=yaml.FullLoader)

ctcdecoder = CTCBeamDecoder(vocab, 
        model_path='', 
        alpha=0,
        beta=0,
        cutoff_top_n=40,
        cutoff_prob=1.0,
        beam_width=100,
        num_processes=4,
        blank_id=processor.tokenizer.pad_token_id,
        log_probs_input=True
        )

ctcdecoder_withlm = CTCBeamDecoder(vocab, 
        model_path=os.path.join(kenlm_model_dir, "lm.binary"),
        alpha=ctc_lm_params['alpha'],      # 1.3648747541523258,
        beta=ctc_lm_params['beta'],        # 0.441997826890268,
        cutoff_top_n=40,
        cutoff_prob=1.0,
        beam_width=100,
        num_processes=4,
        blank_id=processor.tokenizer.pad_token_id,
        log_probs_input=True
        )

test_dataset = test_dataset.map(speech_file_to_array_fn)

result = test_dataset.map(evaluate, batch_size=8)

#for r in result:
#    if r["pred_strings"]!=r["pred_strings_with_lm"]:
#        if (r["pred_strings_with_lm"]==r["sentence"]):
#            print ("CORRECT\n{}\n{}\n{}\n\n".format(r["pred_strings_with_lm"], r["pred_strings"], r["sentence"]))
#        else:
#            print ("INCORRECT\n{}\n{}\n{}\n\n".format(r["pred_strings_with_lm"], r["pred_strings"], r["sentence"]))


print("WER: {:2f}".format(100 * wer.compute(predictions=result["pred_strings"], references=result["sentence"])))
print("WER with CTC: {:2f}".format(100 * wer.compute(predictions=result["pred_strings_with_ctc"], references=result["sentence"])))
print("WER with CTC+LM: {:2f}".format(100 * wer.compute(predictions=result["pred_strings_with_lm"], references=result["sentence"])))

