import os
import io
import sys
import glob
import json
import yaml
import shlex
import subprocess

import torch
import torchaudio
import optuna
import text_preprocess

from pathlib import Path
from ctcdecode import CTCBeamDecoder
from datasets import load_dataset, load_metric, set_caching_enabled
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

from argparse import ArgumentParser, RawTextHelpFormatter


DESCRIPTION = """

Train and optimize a KenLM language model from HuggingFace's provision of the Welsh corpus by the OSCAR project.

"""

set_caching_enabled(False)


# Preprocessing the datasets.
def speech_file_to_array_fn(batch):
    batch["sentence"] = text_preprocess.cleanup(batch["sentence"]).strip() # + " "
    speech_array, sampling_rate = torchaudio.load(batch["path"])
    batch["speech"] = resampler(speech_array).squeeze().numpy()
    return batch


def decode(batch):
    inputs = processor(batch["speech"], sampling_rate=16_000, return_tensors="pt", padding=True)        
    with torch.no_grad():
       logits = model(inputs.input_values.to("cuda"), attention_mask=inputs.attention_mask.to("cuda")).logits

    beam_results, beam_scores, timesteps, out_lens = ctcdecoder.decode(logits)
    batch["pred_strings_with_lm"] = "".join(vocab[n] for n in beam_results[0][0][:out_lens[0][0]]).strip()

    return batch


def optimize_lm_objective(trial):    
    global ctcdecoder
    
    alpha = trial.suggest_uniform('lm_alpha', 0, 6)
    beta = trial.suggest_uniform('lm_beta',0, 5)

    try:
        binarylm_file_path=os.path.join(lm_model_dir, "lm.binary")
        ctcdecoder = CTCBeamDecoder(vocab, 
            model_path=binarylm_file_path,
            alpha=alpha,
            beta=beta,
            cutoff_top_n=40,
            cutoff_prob=1.0,
            beam_width=100,
            num_processes=4,
            blank_id=processor.tokenizer.pad_token_id,
            log_probs_input=True
        )
        result = test_dataset.map(decode)
        result_wer = wer.compute(predictions=result["pred_strings_with_lm"], references=result["sentence"])
        result_cer = cer.compute(predictions=result["pred_strings_with_lm"], references=result["sentence"])

        # clear tmp cache
        fileList = glob.glob("/tmp/**/cache-*.arrow", recursive=True)
        for filepath in fileList:
            try:
                os.remove(filepath)
            except OSError:
                print("Error deleting tmp cache file %s" % filepath)

        print(f"WER: {result_wer} | CER: {result_cer}")
        trial.report(result_wer, step=0)
        

    except Exception as e:
        print (e)
        raise

    finally:
        return result_wer 



def train(lm_dir, oscar_dataset_name):

    Path(lm_dir).mkdir(parents=True, exist_ok=True)    
    corpus_file_path = os.path.join(lm_dir, "corpus.txt")

    print ("\nLoading OSCAR {} dataset...".format(oscar_dataset_name))
    oscar_corpus = load_dataset("oscar", oscar_dataset_name)

    print ("\nExporting OSCAR to text file {}...".format(corpus_file_path))
    with open(corpus_file_path, 'w', encoding='utf-8') as corpus_file:
        for line in oscar_corpus["train"]:
            t = text_preprocess.cleanup(line["text"])
            corpus_file.write(t)

    # generate KenLM ARPA file language model
    lm_arpa_file_path=os.path.join(lm_dir, "lm.arpa")
    lm_bin_file_path=os.path.join(lm_dir, "lm.binary")

    cmd = "lmplz -o {n} --text {corpus_file} --arpa {lm_file}".format(n=5, corpus_file=corpus_file_path, lm_file=lm_arpa_file_path)
    print (cmd)

    subprocess.run(shlex.split(cmd), stderr=sys.stderr, stdout=sys.stdout)

    # generate binary version
    cmd = "build_binary trie -s {arpa_file} {bin_file}".format(arpa_file=lm_arpa_file_path, bin_file=lm_bin_file_path)
    print (cmd)

    subprocess.run(shlex.split(cmd), stderr=sys.stderr, stdout=sys.stdout)

    #
    os.remove(corpus_file_path)
    os.remove(lm_arpa_file_path)

    return lm_dir



def optimize(lm_dir, wav2vec_model_path):
    global processor
    global model
    global vocab
    global wer
    global cer
    global resampler
    global test_dataset
    global lm_model_dir

    lm_model_dir=lm_dir

    test_dataset = load_dataset("custom_common_voice.py", "cy", split="test")
    #test_dataset = load_dataset("common_voice", "cy", split="test")

    wer = load_metric("wer")
    cer = load_metric("cer")

    processor = Wav2Vec2Processor.from_pretrained(wav2vec_model_path)
    model = Wav2Vec2ForCTC.from_pretrained(wav2vec_model_path)

    model.to("cuda")

    resampler = torchaudio.transforms.Resample(48_000, 16_000)

    vocab=processor.tokenizer.convert_ids_to_tokens(range(0, processor.tokenizer.vocab_size))
    space_ix = vocab.index('|')
    vocab[space_ix]=' '

    print ("Preprocessing speech files")
    test_dataset = test_dataset.map(speech_file_to_array_fn)


    print ("Beginning alpha and beta hyperparameter optimization")
    study = optuna.create_study()
    study.optimize(optimize_lm_objective, n_jobs=1, n_trials=100)

    #
    lm_best = {'alpha':study.best_params['lm_alpha'], 'beta':study.best_params['lm_beta']}

    config_file_path = os.path.join(lm_model_dir, "config_ctc.yaml")
    with open (config_file_path, 'w') as config_file:
        yaml.dump(lm_best, config_file)

    print('Best params saved to config file {}: alpha={}, beta={} with WER={}'.format(config_file_path, study.best_params['lm_alpha'], study.best_params['lm_beta'], study.best_value))



def main(lm_root_dir, wav2vec2_model_path, **args):
    lm_file_path=train_kenlm(lm_root_dir, "unshuffled_deduplicated_cy")
    optimize_kenlm(lm_file_path, wav2vec2_model_path) 



if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--target_dir", dest="lm_root_dir", required=True, help="target directory for language model")
    parser.add_argument("--model", dest="wav2vec_model_path", required=True, help="acoustic model to be used for optimizing")
           
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

