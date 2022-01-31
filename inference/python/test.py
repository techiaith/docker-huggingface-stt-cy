import os
import csv
import torch
import librosa
import yaml
import datetime
import pandas

import models
import text_preprocess

import re
import jiwer

from pathlib import Path

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

 Prifysgol Bangor University

"""


tags_regex = '\[.*?\]'

class TestStatistics:

    def __init__(self):
        self.total_clips=0
        self.total_ignored_clips=0

        self.total_duration=0        
        
        self.dfResults=pandas.DataFrame(columns=['wav_filename', 'duration', 'prediction', 'reference', 'wer', 'cer'])
        self.dfIgnoredResults=pandas.DataFrame(columns=['wav_filename', 'duration', 'prediction', 'reference', 'wer', 'cer'])


    def calculate_error_rates(self, prediction, reference):        

        cer_error = jiwer.cer(reference, prediction)
        wer_error = jiwer.wer(reference, prediction)

        return 100*wer_error, 100*cer_error


    def add(self, clip_file_path, prediction, reference):        
       
        print (clip_file_path)           
        print (reference)
        print (prediction)
        
        audio, rate = librosa.load(clip_file_path, sr=16000)
        duration=librosa.get_duration(y=audio, sr=rate)

        current_wer, current_cer=self.calculate_error_rates(prediction, reference)
    
        self.total_duration+=duration       
        
        # skip averaging if reference contains a (metadata) tag in square brackets
        if not re.findall(tags_regex, reference):
            self.total_clips+=1
            self.dfResults.loc[self.total_clips] = [clip_file_path, duration, prediction, reference, current_wer, current_cer]
        else:
            self.total_ignored_clips+=1
            self.dfIgnoredResults.loc[self.total_clips] = [clip_file_path, duration, prediction, reference, current_wer, current_cer]
            
        print ("WER: %s, CER: %s" % (current_wer, current_cer)) 
        print ("")

       
    def print(self):
       
        predictions = self.dfResults['prediction'].tolist()
        references = self.dfResults['reference'].tolist()

        average_wer=100 * jiwer.wer(hypothesis=predictions, truth=references)
        average_cer=100 * jiwer.cer(hypothesis=predictions, truth=references)

        #
        print ("Test Statistics")
        print ("---------------")
        print ("No of Clips: %s" % self.total_clips)        
        print ("Duration: {} hours ({} seconds).".format(datetime.timedelta(seconds=self.total_duration), self.total_duration))
        print ("WER with CTC+LM: {:2f}".format(average_wer))
        print ("CER with CTC+LM: {:2f}".format(average_cer))

        print ("No of ignored clips: %s" % self.total_ignored_clips)

        print ("")


    def save(self):
        print("Results saved to results.csv file")
        self.dfResults.to_csv("results.csv", encoding='utf-8', index=False)
        self.dfIgnoredResults.to_csv("results_ignored.csv", encoding='utf-8', index=False)
        

#
#
def main(testset_csv_file_path, model_path, revision, **args):

    # iterate through each audio file and text. 
    processor, model, vocab, ctcdecoder, kenlm_ctcdecoder = models.create(model_path, revision)
    test_stats = TestStatistics()

    testset_csv_parent_dir=Path(testset_csv_file_path).parent.absolute()

    with open(testset_csv_file_path, 'r', encoding='utf-8') as testset_csv_file:
        testset = csv.DictReader(testset_csv_file)
        for testfile in testset:
            clip_file_path = os.path.join(testset_csv_parent_dir, "clips", testfile["wav_filename"])
            
            audio, rate = librosa.load(clip_file_path, sr=16000)
            duration = librosa.get_duration(y=audio, sr=rate)

            inputs = processor(audio, sampling_rate=16_000, return_tensors="pt", padding=True)
            with torch.no_grad():
                logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits

            beam_results, beam_scores, timesteps, out_lens = kenlm_ctcdecoder.decode(logits)
            prediction = "".join(vocab[n] for n in beam_results[0][0][:out_lens[0][0]]) 
                                    
            reference=text_preprocess.cleanup(testfile["transcript"])
            test_stats.add(clip_file_path, prediction, reference)                        
    
    test_stats.print()
    test_stats.save()



if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("--test_csv", dest="testset_csv_file_path", required=True)
    parser.add_argument("--model_path", dest="model_path", required=True)
    parser.add_argument("--revision", dest="revision", default='')
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
