# Fine tune Facebook AI wav2vec2 XLSR for Welsh

[(cliciwch yma os hoffwch ddarllen y README Cymraeg)](README.md)

Code for fine tuning Facebook AI's wav2vec2 XLSR acoustic models with HuggingFace for
Welsh language speech recognition. The original code was first developed and 
subsequently specialized for Welsh during the HuggingFace Fine tuning week for lesser resourced languages:

https://discuss.huggingface.co/t/open-to-the-community-xlsr-wav2vec2-fine-tuning-week-for-low-resource-languages/4467

Welsh language data from Mozilla Common Voice was used for fine tuning acoustic models. 

Additional code in this repo adds training of a KenLM language model and optimization 
of alpha and beta hyperparameters for CTC decoding. 

The Welsh language text corpus provided by the OSCAR project via HuggingFace Datasets was used
for training the languge model.


# How to use...

`$ make`

`$ make run `
`
In order to download the Common Voice data, you will need to create a file named `data_url.py` that contains only one line
for the data's URL provided to you be the Common Voice website...

`root@bff0be8425ea:/usr/src/xlsr-finetune# vi data_url.py`

`_DATA_URL = "https://voice-prod-bundler-ee1969a6ce8178826482b88e843c335139bd3fb4.s3.amazonaws.com/cv-corpus-7.0-2021-07-21/cy.tar.gz"`

See also https://commonvoice.mozilla.org/cy/datasets

Then to start training....

`root@bff0be8425ea:/usr/src/xlsr-finetune# python3 run.py`

Depending on your graphics card, it will take some hours to train.


# Evaluation

`root@bff0be8425ea:/usr/src/xlsr-finetune# python3 evaluate.py`

|Training Data | Test Data | Model | Decode | WER | CER |
|---|---|---|---|---|---|
|cv9 training+validation | cv9 test | wav2vec2-xlsr-ft-cy | greedy | 23.09% | 6.43%|
|cv9 training+validation | cv9 test | wav2vec2-xlsr-ft-cy | ctc | 23.01% | 6.41%|
|cv9 training+validation | cv9 test | wav2vec2-xlsr-ft-cy | ctc with lm (kenlm, n=5) | 13.74% | 4.85%|
|cv9 training+validation | cv9 test | wav2vec2-xls-r-1b-ft-cy | greedy | **19.68%** | **5.5%**|
|cv9 training+validation | cv9 test | wav2vec2-xls-r-1b-ft-cy | ctc | **19.6%** | **5.47%**|
|cv9 training+validation | cv9 test | wav2vec2-xls-r-1b-ft-cy | ctc with lm (kenlm, n=5) | **12.38%** | **4.07%**|
|cv8 training+validation | cv8 test | wav2vec2-xlsr-ft-cy | greedy | 24.03%% | 6.74%|
|cv8 training+validation | cv8 test | wav2vec2-xlsr-ft-cy | ctc | 24.01% | 6.71%|
|cv8 training+validation | cv8 test | wav2vec2-xlsr-ft-cy | ctc with lm (kenlm, n=5) | 13.79% | 4.77%|
|cv7 training+validation | cv7 test | wav2vec2-xlsr-ft-cy | greedy | 24.28%% ||
|cv7 training+validation | cv7 test | wav2vec2-xlsr-ft-cy | ctc | 24.27% ||
|cv7 training+validation | cv7 test | wav2vec2-xlsr-ft-cy | ctc with lm (kenlm, n=5) | 14.05% ||
|cv6.1 training+validation | cv6.1 test | wav2vec2-xlsr-ft-cy | greedy | 25.59% ||
|cv6.1 training+validation | cv6.1 test | wav2vec2-xlsr-ft-cy | ctc | 25.47% ||
|cv6.1 training+validation | cv6.1 test | wav2vec2-xlsr-ft-cy | ctc with lm (kenlm, n=5) | 15.07% ||
