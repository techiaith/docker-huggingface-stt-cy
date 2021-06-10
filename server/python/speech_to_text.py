#!/bin/env python3
import os
import sys
import glob
import yaml
import torch

from datetime import timedelta

import numpy as np
import json

from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from vadSplit import read_frames_from_file, split

from ctcdecode import CTCBeamDecoder


DESCRIPTION = """

© Prifysgol Bangor University

"""

class SpeechToText:

    def __init__(self, acoustic_model_path, language_model_path):

        print ("Initialising processor...")
        self.processor = Wav2Vec2Processor.from_pretrained(acoustic_model_path)

        print ("Initialising wav2vec ctc model...")
        self.model = Wav2Vec2ForCTC.from_pretrained(acoustic_model_path)
                
        print ("Initialising vocab...")
        self.vocab=self.processor.tokenizer.convert_ids_to_tokens(range(0, self.processor.tokenizer.vocab_size))
        space_ix = self.vocab.index('|')
        self.vocab[space_ix]=' '

        with open(os.path.join(language_model_path, "config_ctc.yaml"), 'r') as config_file:
            ctc_lm_params=yaml.load(config_file, Loader=yaml.FullLoader)

        print ("Initialising ctc with lm decoder...")
        self.ctcdecoder = CTCBeamDecoder(self.vocab,
            model_path=os.path.join(language_model_path, "lm.binary"),
            alpha=ctc_lm_params['alpha'],
            beta=ctc_lm_params['beta'],
            cutoff_top_n=40,
            cutoff_prob=1.0,
            beam_width=10,
            num_processes=4,
            blank_id=self.processor.tokenizer.pad_token_id,
            log_probs_input=True
        )

    

    def transcribe(self, wav_file_path, aggressiveness=2):
        frames = read_frames_from_file(wav_file_path)
        i=0
        for segment in split(frames, aggressiveness=aggressiveness):

            segment_buffer, time_start, time_end = segment

            # Run stt on the chunk that just completed VAD
            audio = np.frombuffer(segment_buffer, dtype=np.int16)
            inputs = self.processor(audio, sampling_rate=16_000, return_tensors="pt", padding=True) # Batch size 1

            with torch.no_grad():
                logits = self.model(inputs.input_values, attention_mask=inputs.attention_mask).logits

            transcription, alignment, timesteps = self.ctc_withlm_decode(logits)
            timestep_length = (time_end - time_start) / timesteps
            for a in alignment:
                a[1] = ((a[1] * timestep_length) + time_start) / 1000
            
            yield transcription, alignment, time_start, time_end


    def ctc_withlm_decode(self, logits):
        beam_results, beam_scores, timesteps, out_lens = self.ctcdecoder.decode(logits)

        # beam_results - Shape: BATCHSIZE x N_BEAMS X N_TIMESTEPS A batch containing the series 
        # of characters (these are ints, you still need to decode them back to your text) representing 
        # results from a given beam search. Note that the beams are almost always shorter than the 
        # total number of timesteps, and the additional data is non-sensical, so to see the top beam 
        # (as int labels) from the first item in the batch, you need to run beam_results[0][0][:out_len[0][0]].
        beam_string = "".join(self.vocab[n] for n in beam_results[0][0][:out_lens[0][0]])
        
        # timesteps : BATCHSIZE x N_BEAMS : the timestep at which the nth output character has peak probability. 
        # Can be used as alignment between the audio and the transcript.
        alignment = list()
        for i in range(0, out_lens[0][0]):        
            alignment.append([beam_string[i], int(timesteps[0][0][i])] )

        return beam_string, alignment, int(beam_results.shape[2]) 



    def greedy_decode(self, logits):
        predicted_ids = torch.argmax(logits, dim=-1)
        return self.processor.batch_decode(predicted_ids)[0]
        
