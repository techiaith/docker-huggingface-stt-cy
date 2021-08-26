import os
import torch
import librosa
import yaml
import datetime
import pandas

import models
import text_preprocess

import re

from pathlib import Path
from datasets import load_metric

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

 Prifysgol Bangor University

"""

wer = load_metric("wer")
predictions = list()
references = list()

tags_regex = '\[.*?\]'

class TestStatistics:

    def __init__(self):
        self.total_clips=0
        self.total_duration=0        
        self.average_wer=0
        self.dfResults=pandas.DataFrame(columns=['wav_filename', 'duration', 'prediction', 'reference', 'wer'])


    def calculate_wer(self, prediction, reference):        
        tmp_predictions=list()
        tmp_predictions.append(prediction)

        tmp_references=list()           
        tmp_references.append(reference)

        return 100*wer.compute(predictions=tmp_predictions, references=tmp_references)


    def add(self, clip_file_path, prediction, reference):        
        audio, rate = librosa.load(clip_file_path, sr=16000)
        duration=librosa.get_duration(y=audio, sr=rate)
        current_wer=self.calculate_wer(prediction, reference)
        
        self.total_clips+=1
        self.total_duration+=duration       

        self.dfResults.loc[self.total_clips] = [clip_file_path, duration, prediction, reference, current_wer]        
        self.average_wer=100 * wer.compute(predictions=self.dfResults['prediction'].tolist(), references=self.dfResults['reference'].tolist())

        print (clip_file_path)           
        print (reference)
        print (prediction)
        print ("%s, %s" % (current_wer, self.average_wer))
        print ()

       
    def print(self):
        print ("Test Statistics")
        print ("---------------")
        print ("No of Clips: %s" % self.total_clips)
        print ("Duration: {} hours ({} seconds).".format(datetime.timedelta(seconds=self.total_duration), self.total_duration))
        print ("WER with CTC+LM: {:2f}".format(self.average_wer))

        print ("")


    def save(self):
        print("Results saved to results.csv file")
        self.dfResults.to_csv("results.csv", encoding='utf-8', index=False)
        

    def get_average_wer(self):
        return self.average_wer


    def get_clips_count(self):
        return self.total_clips

#
#
def main(clips_dir, model_path, revision, **args):

    # iterate through each audio file and text. 
    processor, model, vocab, ctcdecoder, kenlm_ctcdecoder = models.create(model_path, revision)

    df = pandas.DataFrame(columns=['wav_filename', 'duration', 'prediction', 'reference', 'wer'])

    clips_dir_files = Path(clips_dir).glob('*.wav')
    test_stats = TestStatistics()
    
    for clip_file_path in clips_dir_files:
        audio, rate = librosa.load(clip_file_path, sr=16000)
        duration = librosa.get_duration(y=audio, sr=rate)

        inputs = processor(audio, sampling_rate=16_000, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits

        beam_results, beam_scores, timesteps, out_lens = kenlm_ctcdecoder.decode(logits)
        prediction = "".join(vocab[n] for n in beam_results[0][0][:out_lens[0][0]]) 
                        
        with open(str(clip_file_path).replace(".wav",".txt"),'r',encoding='utf-8') as reference_file:
            reference=reference_file.read()
            reference=text_preprocess.cleanup(reference)
    
        if not re.findall(tags_regex, reference):            
            test_stats.add(clip_file_path, prediction, reference)                        
    
    test_stats.print()
    test_stats.save()

   
if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("--clips_dir", dest="clips_dir", required=True)
    parser.add_argument("--model_path", dest="model_path", required=True)
    parser.add_argument("--revision", dest="revision", default='')
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
