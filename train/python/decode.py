import os
import torch
import librosa
import yaml
import numpy as np

from ctcdecode import CTCBeamDecoder

from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

 Prifysgol Bangor University

"""

def greedy_decode(logits):
    predicted_ids=torch.argmax(logits, dim=-1)
    return processor.batch_decode(predicted_ids)[0]

def lm_decode(ctc_matrix):

    kenlm_model_name= "kenlm-cy"
    kenlm_model_dir=os.path.join(models_root_dir, kenlm_model_name)
    with open(os.path.join(kenlm_model_dir, "config_ctc.yaml"), 'r') as config_file:
       ctc_lm_params=yaml.load(config_file, Loader=yaml.FullLoader)

    vocab=processor.tokenizer.convert_ids_to_tokens(range(0, processor.tokenizer.vocab_size))
    space_ix = vocab.index('|')
    vocab[space_ix]=' '

    ctcdecoder = CTCBeamDecoder(vocab, 
        model_path=os.path.join(kenlm_model_dir, "lm.binary"),
        alpha=ctc_lm_params['alpha'],
        beta=ctc_lm_params['beta'],
        cutoff_top_n=40,
        cutoff_prob=1.0,
        beam_width=10,
        num_processes=4,
        blank_id=processor.tokenizer.pad_token_id,
        log_probs_input=False
        )

    beam_results, beam_scores, timesteps, out_lens = ctcdecoder.decode(ctc_matrix)
  
    # beam_results - Shape: BATCHSIZE x N_BEAMS X N_TIMESTEPS A batch containing the series 
    # of characters (these are ints, you still need to decode them back to your text) representing 
    # results from a given beam search. Note that the beams are almost always shorter than the 
    # total number of timesteps, and the additional data is non-sensical, so to see the top beam 
    # (as int labels) from the first item in the batch, you need to run beam_results[0][0][:out_len[0][0]].
    beam_string = "".join(vocab[n] for n in beam_results[0][0][:out_lens[0][0]])
   
    # beam_scores - Shape: BATCHSIZE x N_BEAMS A batch with the approximate CTC score of each beam
    score = float(beam_scores[0][0].item()) / 100
 
    # timesteps : BATCHSIZE x N_BEAMS : the timestep at which the nth output character has peak probability. 
    # Can be used as alignment between the audio and the transcript.
    alignment = list()
    for i in range(0, out_lens[0][0]):        
        alignment.append([beam_string[i], int(timesteps[0][0][i])] )

    return beam_string, alignment, score, int(beam_results.shape[2]) 

#
def main(audio_file, **args):
    global models_root_dir
    global processor
    global model

    models_root_dir="/models"
    wav2vec2_model_name = "wav2vec2-xlsr-ft-cy"
    wav2vec2_model_path = os.path.join(models_root_dir, wav2vec2_model_name)

    processor = Wav2Vec2Processor.from_pretrained(wav2vec2_model_path)
    model = Wav2Vec2ForCTC.from_pretrained(wav2vec2_model_path)

    audio, rate = librosa.load(audio_file, sr=16000)

    inputs = processor(audio, sampling_rate=16_000, return_tensors="pt", padding=True)

    with torch.no_grad():
        logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits

    print("Greedy decoding: " + greedy_decode(logits))

    ctc_matrix = torch.softmax(logits, dim=-1)
    text, alignment, score, timesteps = lm_decode(ctc_matrix)
    timestep_length = librosa.get_duration(audio) / timesteps
    for a in alignment:
        a[1] = a[1] * timestep_length  

    print("LM decoding (with alignments): " + text)
    print("Score: " + str(score))
    print("Alignment:" + str(alignment))


if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("--wav", dest="audio_file", required=True)
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
