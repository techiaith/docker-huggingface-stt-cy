import os
import sys
import glob
import yaml
import torch
import librosa

from datetime import timedelta

import numpy as np
import json

import models

from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from vadSplit import VadSplit

from ctcdecode import CTCBeamDecoder


DESCRIPTION = """

(c) Prifysgol Bangor University

"""

class SpeechToText:

    def __init__(self, models_root_dir='', wav2vec2_model_path='', version='', language_model_path='', split_only=False):

        self.split_only = split_only

        print ("split_only: ", split_only)
        
        if self.split_only==False:
            if len(wav2vec2_model_path)==0:
                self.wav2vec2_model_path = os.environ["WAV2VEC2_MODEL_NAME"]

            # @todo - improve. 
            if len(language_model_path)==0:
                self.language_model_path = os.path.join(os.environ["WAV2VEC2_MODEL_NAME"], "kenlm")

            #
            if len(version)==0:
                self.version=os.environ["MODEL_VERSION"]
            
            #
            self.processor, self.model, self.vocab, self.ctcdecoder, self.kenlm_ctcdecoder = models.create(self.wav2vec2_model_path, self.version)
            
            self.device = "cpu"
            if torch.cuda.is_available():
                self.device="cuda"
                self.model.cuda()
            
            print ("wav2vec loaded to device %s" % self.device)



    def get_model_name(self):
        return self.wav2vec2_model_path

    def get_language_model(self):
        return self.language_model_path

    def get_model_version(self):
        return self.version
   
    def get_device(self):
        return self.device


    def split_frames(self, frames, aggressiveness):
        
        for audio_segment in split(frames, aggressiveness=aggressiveness):
            
            audio_segment_buffer, audio_segment_time_start, audio_segment_time_end = audio_segment

            audio_segment_time_start = audio_segment_time_start / 1000
            audio_segment_time_end = audio_segment_time_end / 1000
            audio_segment_duration = audio_segment_time_end - audio_segment_time_start

            #print (audio_segment_duration, len(audio_segment_buffer), aggressiveness)

            if audio_segment_duration>100.0 and aggressiveness<4:              
                self.split_frames(audio_segment_buffer, aggressiveness+1)
            else:
                yield audio_segment_buffer, audio_segment_time_start, audio_segment_time_end


    def transcribe(self, wav_file_path, max_segment_length=15, max_segment_words=14, withlm=False):
        
        print ("Processing: %s" % wav_file_path)

        wav_audio, rate = librosa.load(wav_file_path, sr=16000)

        time_start = 0.0
        time_end = librosa.get_duration(y=wav_audio,sr=rate)
        
        vadSplitter = VadSplit()
        for audio_segment in vadSplitter.split_audio_file(wav_file_path):
            audio_segment_buffer, audio_segment_time_start, audio_segment_time_end = audio_segment
            if self.split_only==True:
                yield "", audio_segment_time_start, audio_segment_time_end, None
            else:
                # Run stt on the chunk that just completed VAD
                audio = np.frombuffer(audio_segment_buffer, dtype=np.int16)

            # timings into seconds. 
            audio_segment_time_start = audio_segment_time_start / 1000
            audio_segment_time_end = audio_segment_time_end / 1000

            # Run stt on the chunk that just completed VAD
            audio = np.frombuffer(audio_segment_buffer, dtype=np.int16)

            features = self.processor(audio, sampling_rate=16_000, return_tensors="pt", padding=True)
            with torch.no_grad():
                logits = self.model(features.input_values.to(self.device, dtype=torch.float32), attention_mask=features.attention_mask.to(self.device)).logits

            transcription, alignment, timesteps = self.ctc_decode(logits, withlm) 
            
            #
            # for when voice activated splitting fails to ensure no split/segment is more than 
            # a set number of seconds, we can use the alignments from the CTC results to 
            # produce segments with a given time and/or word count. 
            # 
            timestep_length = (audio_segment_time_end - audio_segment_time_start) / timesteps
            for a in alignment:
                a[1] = ((a[1] * timestep_length) + audio_segment_time_start)
                aligned_words = self.aligned_words(alignment, timestep_length)

            if len(aligned_words) > 0:
                for transcription, seg_start, seg_end, seg_alignment in self.segment(aligned_words, max_segment_length, max_segment_words):                    
                    yield transcription, seg_start, seg_end, seg_alignment
            

    def ctc_decode(self, logits, withlm):

        if withlm:
            beam_results, beam_scores, timesteps, out_lens = self.kenlm_ctcdecoder.decode(logits)
        else:
            beam_results, beam_scores, timesteps, out_lens = self.ctcdecoder.decode(logits)

        # beam_results - Shape: BATCHSIZE x N_BEAMS X N_TIMESTEPS A batch containing the series 
        # of characters (these are ints, you still need to decode them back to your text) representing 
        # results from a given beam search. Note that the beams are almost always shorter than the 
        # total number of timesteps, and the additional data is non-sensical, so to see the top beam 
        # (as int labels) from the first item in the batch, you need to run beam_results[0][0][:out_len[0][0]].
        beam_string = "".join(self.vocab[n] for n in beam_results[0][0][:out_lens[0][0]])
       
        # beam_scores - Shape: BATCHSIZE x N_BEAMS A batch with the approximate CTC score of each beam 
        # If this is true, you can get the model's confidence that the beam is correct with 
        # p=1/np.exp(beam_score).
        score = 0.0 #float(beam_scores[0][0].item()) / 100
 
        # timesteps : BATCHSIZE x N_BEAMS : the timestep at which the nth output character has peak probability. 
        # Can be used as alignment between the audio and the transcript.
        alignment = list()
        for i in range(0, out_lens[0][0]):        
            alignment.append([beam_string[i], int(timesteps[0][0][i])] )

        return beam_string, alignment, int(beam_results.shape[2]) 


    def greedy_decode(self, logits):
        predicted_ids = torch.argmax(logits, dim=-1)
        return self.processor.batch_decode(predicted_ids)[0]
        

    def aligned_words(self, char_alignments, timestep_length):
        word_alignments = list()

        word = ''
        w_start = 0.0
        w_end = 0.0        

        for c, ts in char_alignments:
            if c != " ":
                if len(word)==0:
                    word = c
                    w_start=ts
                    w_end=ts+timestep_length
                else:
                    word = word + c
                    w_end = ts
            else:                
                word_alignments.append({'word':word, 'start':w_start, 'end':ts})
                word=''

        if (len(word)>0):
            word_alignments.append({'word':word, 'start':w_start, 'end':w_end})

        return word_alignments


    def segment(self, word_alignments, segment_max_length, segment_max_words):
                
        segment_alignments = list()
        
        segment_text = ''
        segment_start = word_alignments[0]['start']
        segment_end = word_alignments[0]['end']

        for a in word_alignments:

            # if the segment has reached a maximum number of words
            if len(segment_alignments)>segment_max_words:             
                yield segment_text, segment_start, segment_end, segment_alignments
                segment_text = a['word']
                segment_start = a['start']
                segment_end = a['end']
                segment_alignments = list()
                segment_alignments.append(a)

            elif a['start'] > segment_start + segment_max_length:
                yield segment_text, segment_start, segment_end, segment_alignments
                segment_text = a['word']
                segment_start = a['start']
                segment_end = a['end']
                segment_alignments = list()
                segment_alignments.append(a)

            else:
                segment_text = segment_text + ' ' + a['word']
                segment_text = segment_text.strip()
                segment_end = a['end']
                segment_alignments.append(a)
                    
        yield segment_text, segment_start, segment_end, segment_alignments

