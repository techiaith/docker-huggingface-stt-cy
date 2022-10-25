# Mireinio modelau wav2vec2 XLSR gan Facebook AI ar gyfer y Gymraeg

[(click here to read the README in English)](README_en.md)

Cod i fireinio model wav2vec2 XLSR Facebook gyda HuggingFace ar gyfer wireddu 
adnabod lleferydd Cymraeg effeithiol. Datblygwyd ac yna addaswyd yn benodol ar gyfer
y Gymraeg yn ystod wythnos fireinio i ieithoedd llai eu hadnoddau gan HuggingFace. 

Gweler : https://discuss.huggingface.co/t/open-to-the-community-xlsr-wav2vec2-fine-tuning-week-for-low-resource-languages/4467

Defnyddiwyd is-setiau benodol o ddata Common Voice Cymraeg gan Mozilla i fireinio modelau acwsteg. Adeiladwyd yr is-setiau gyda sgriptiau o https://github.com/techiaith/docker-commonvoice-custom-splits-builder. 

Mae'r project yn cynnwys cod ychwanegol sydd hefyd yn cynnwys hyfforddi modelau iaith
KenLM yn ogystal ag optimeiddio hyperbaramedrau alpha a beta dadgodio CTC. 

Hyfforddwyd y modelau iaith gyda thestun corpws gan broject OSCAR a llyfrgell Datasets 
HuggingFace. 

# Sut i'w ddefnyddio...  

`$ make`

`$ make run `

Er mwyn llwytho i lawr data Common Voice, mae angen i chi greu ffeil o'r enw `data_url.py` ac sy'n cynnwys un linell yn unig ar gyfer
y cyfeiriad URL y ddata bydd gwefan Common Voice wedi ei ddarparu'n arbennig i chi... 

`root@bff0be8425ea:/usr/src/xlsr-finetune# vi data_url.py`

`_DATA_URL = "https://voice-prod-bundler-ee1969a6ce8178826482b88e843c335139bd3fb4.s3.amazonaws.com/cv-corpus-7.0-2021-07-21/cy.tar.gz"`

Gweler hefyd https://commonvoice.mozilla.org/cy/datasets

Yna i ddechrau hyfforddi....

`root@bff0be8425ea:/usr/src/xlsr-finetune# python3 run.py`

Yn dibynnu ar y cerdyn graffics, bydd yn gymryd rhai oriau i hyfforddi. 



# Gwerthuso 

`root@bff0be8425ea:/usr/src/xlsr-finetune# python3 evaluate.py`

|Training Data | Test Data | Model | Decode | WER | CER |
|---|---|---|---|---|---|
|cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-xls-r-1b | greedy | **15.82%** | **4.53%**|
|cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-xls-r-1b | ctc | **15.72%** | **4.50%**|
|cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-xls-r-1b | ctc with lm (kenlm, n=5) | **10.17%** | **3.42%**|
|cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-large-xlsr-53 | greedy | 16.73% | 4.63% |
|cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc | 16.62% | 4.61% |
|cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 10.45% | 3.42% |
|cv11 training+validation (s=3) | cv11 test | wav2vec2-large-xlsr-53 | greedy | 17.42% | 4.83% |
|cv11 training+validation (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc | 17.29% | 4.80% |
|cv11 training+validation (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 10.82% | 3.58% |
|cv10 training+validation+custom other | cv10 test | wav2vec2-xls-r-1b | greedy | 19.67% | 5.24%|
|cv10 training+validation+custom other | cv10 test | wav2vec2-xls-r-1b | ctc | 19.50% | 5.43%|
|cv10 training+validation+custom other | cv10 test | wav2vec2-xls-r-1b | ctc with lm (kenlm, n=5) | 12.50% | 4.36%|
|cv10 training+validation+custom other | cv10 test | wav2vec2-large-xlsr-53 | greedy | 22.52% | 6.23%|
|cv10 training+validation+custom other | cv10 test | wav2vec2-large-xlsr-53 | ctc | 22.44% | 6.22%|
|cv10 training+validation+custom other | cv10 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 13.38% | 4.52%|
|cv10 training+validation | cv10 test | wav2vec2-large-xlsr-53 | greedy | 23.17% | 6.45%|
|cv10 training+validation | cv10 test |wav2vec2-large-xlsr-53 | ctc | 23.06% | 6.40%|
|cv10 training+validation | cv10 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 13.74% | 4.69%|
|cv9 training+validation | cv9 test | wav2vec2-large-xlsr-53 | greedy | 23.15% | 6.48%|
|cv9 training+validation | cv9 test | wav2vec2-large-xlsr-53 | ctc | 23.08% | 6.46%|
|cv9 training+validation | cv9 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 13.69% | 4.71%|
|cv9 training+validation | cv9 test | wav2vec2-xls-r-1b | greedy | 19.68% | 5.5%|
|cv9 training+validation | cv9 test | wav2vec2-xls-r-1b | ctc | 19.6% | 5.47%|
|cv9 training+validation | cv9 test | wav2vec2-xls-r-1b | ctc with lm (kenlm, n=5) | 12.38% | 4.07%|
|cv8 training+validation | cv8 test | wav2vec2-large-xlsr-53 | greedy | 24.03%% | 6.74%|
|cv8 training+validation | cv8 test | wav2vec2-large-xlsr-53 | ctc | 24.01% | 6.71%|
|cv8 training+validation | cv8 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 13.79% | 4.77%|
|cv7 training+validation | cv7 test | wav2vec2-large-xlsr-53 | greedy | 24.28%% ||
|cv7 training+validation | cv7 test | wav2vec2-large-xlsr-53 | ctc | 24.27% ||
|cv7 training+validation | cv7 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 14.05% ||
|cv6.1 training+validation | cv6.1 test | wav2vec2-large-xlsr-53 | greedy | 25.59% ||
|cv6.1 training+validation | cv6.1 test | wav2vec2-large-xlsr-53 | ctc | 25.47% ||
|cv6.1 training+validation | cv6.1 test |wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 15.07% ||
