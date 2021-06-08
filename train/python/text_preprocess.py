import re

chars_to_ignore_regex = '[\,\?\.\!\u00AC\;\:\"\\%\\\]'

# Preprocessing the datasets.
# We need to read the aduio files as arrays
def cleanup(sentence):
    sentence = re.sub(chars_to_ignore_regex, '', sentence).lower()
    sentence = sentence.replace('\u2013',"-")
    sentence = sentence.replace('\u2014',"-")
    sentence = sentence.replace('\u2018',"'")
    sentence = sentence.replace('ñ',"n")
    return sentence
