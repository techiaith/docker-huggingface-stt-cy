import os

import numpy as np
import pandas
import scipy.io.wavfile as wav

from python_speech_features import mfcc

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

© Prifysgol Bangor University

"""

N_CONTEXT=9


def audiofile_to_input_vector(audio_filename, numcep, numcontext):
    r"""
    Given a WAV audio file at ``audio_filename``, calculates ``numcep`` MFCC features
    at every 0.01s time step with a window length of 0.025s. Appends ``numcontext``
    context frames to the left and right of each time step, and returns this data
    in a numpy array.
    """
    # Load wav files
    fs, audio = wav.read(audio_filename)

    # Get mfcc coefficients
    features = mfcc(audio, samplerate=fs, numcep=numcep, winlen=0.032, winstep=0.02, winfunc=np.hamming)

    # Add empty initial and final contexts
    empty_context = np.zeros((numcontext, numcep), dtype=features.dtype)
    features = np.concatenate((empty_context, features, empty_context))

    return features


def is_feasible_transcription(wavfile, transcription):
    aftiv_length=audiofile_to_input_vector(wavfile, 26, N_CONTEXT).shape[0] - 2*N_CONTEXT
    return aftiv_length > len(transcription)


def main(clips_dir, **kwargs):
    print("validating clips in %s" % clips_dir)
  
    dfValid = pandas.DataFrame(columns=['wav_filename', 'wav_filesize', 'transcript', 'parent_wavfile_name'])

    clips_file_path = os.path.join(clips_dir, "clips.csv")
    dfAudio = pandas.read_csv(clips_file_path)

    i=0
    for index, row in dfAudio.iterrows():    
        wav_file_path=os.path.join(clips_dir, row['wav_filename'])
        if is_feasible_transcription(wav_file_path, row['transcript']):
            dfValid.loc[i] = [row['wav_filename'], row['wav_filesize'], row['transcript'], row['parent_wavfile_name']]
            i+=1

    valid_clips_csv=os.path.join(clips_dir, "clips.valid.csv")
    with open(valid_clips_csv, 'a') as csvfile:
        dfValid.to_csv(csvfile, encoding='utf-8', mode='a', index=False, header=csvfile.tell()==0)

    print ("%s valid audio file noted in %s" % (str(i), valid_clips_csv))


if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)
    
    parser.add_argument("--clips_dir", dest="clips_dir", required=True)

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))