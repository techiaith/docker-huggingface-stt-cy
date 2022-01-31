import os
import torch
import torchaudio
import json
import numpy as np
import yaml

import models

from argparse import ArgumentParser, RawTextHelpFormatter

from datasets import load_dataset, load_metric
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import text_preprocess

from ctcdecode import CTCBeamDecoder

DESCRIPTION = """

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
    inputs = processor(batch["speech"], sampling_rate=16000, return_tensors="pt", padding=True)
    
    with torch.no_grad():
       logits = model(inputs.input_values.to("cuda"), attention_mask=inputs.attention_mask.to("cuda")).logits

    pred_ids = torch.argmax(logits, dim=-1)

    batch["pred_strings"] = processor.batch_decode(pred_ids)[0].strip()

    if ctcdecoder:
        beam_results, beam_scores, timesteps, out_lens = ctcdecoder.decode(logits)
        pred_with_ctc = "".join(vocab[n] for n in beam_results[0][0][:out_lens[0][0]])
        batch["pred_strings_with_ctc"]=pred_with_ctc.strip()
    
    if kenlm_ctcdecoder:
        beam_results, beam_scores, timesteps, out_lens = kenlm_ctcdecoder.decode(logits)
        pred_with_lm = "".join(vocab[n] for n in beam_results[0][0][:out_lens[0][0]])
        batch["pred_strings_with_lm"]=pred_with_lm.strip()

    return batch


def main(wav2vec2_model_path, revision, **args):
    global processor
    global model
    global vocab
    global ctcdecoder
    global kenlm_ctcdecoder
    global resampler

    processor, model, vocab, ctcdecoder, kenlm_ctcdecoder = models.create(wav2vec2_model_path, revision)

    #
    test_dataset = load_dataset("custom_common_voice.py", "cy", split="test")

    wer = load_metric("wer")
    cer = load_metric("cer")

    model.to("cuda")

    resampler = torchaudio.transforms.Resample(48000, 16000)

    test_dataset = test_dataset.map(speech_file_to_array_fn)
    result = test_dataset.map(evaluate, batch_size=8)

    print("WER: {:2f}".format(100 * wer.compute(predictions=result["pred_strings"], references=result["sentence"])))
    if ctcdecoder: print("WER with CTC: {:2f}".format(100 * wer.compute(predictions=result["pred_strings_with_ctc"], references=result["sentence"])))
    if kenlm_ctcdecoder: print("WER with CTC+LM: {:2f}".format(100 * wer.compute(predictions=result["pred_strings_with_lm"], references=result["sentence"])))

    print("CER: {:2f}".format(100 * cer.compute(predictions=result["pred_strings"], references=result["sentence"])))
    if ctcdecoder: print("CER with CTC: {:2f}".format(100 * cer.compute(predictions=result["pred_strings_with_ctc"], references=result["sentence"])))
    if kenlm_ctcdecoder: print("CER with CTC+LM: {:2f}".format(100 * cer.compute(predictions=result["pred_strings_with_lm"], references=result["sentence"])))


if __name__ == "__main__":
   
    models_root_dir="/models/published"
    wav2vec2_model_name = "wav2vec2-xlsr-ft-cy"
    kenlm_model_name= "kenlm"

    wav2vec_model_dir = os.path.join(models_root_dir, wav2vec2_model_name)

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)
    
    parser.add_argument("--model_path", dest="wav2vec2_model_path", default=wav2vec_model_dir)
    parser.add_argument("--revision", dest="revision", default='')
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
