# Mireinio modelau wav2vec2 XLSR gan Facebook AI ar gyfer y Gymraeg

[(click here to read the README in English)](README_en.md)

Cod i fireinio model wav2vec2 XLSR Facebook gyda HuggingFace ar gyfer wireddu 
adnabod lleferydd Cymraeg effeithiol. Datblygwyd ac yna addaswyd yn benodol ar gyfer
y Gymraeg yn ystod wythnos fireinio i ieithoedd llai eu hadnoddau gan HuggingFace. 

Gweler : https://discuss.huggingface.co/t/open-to-the-community-xlsr-wav2vec2-fine-tuning-week-for-low-resource-languages/4467

Defnyddiwyd data Common Voice Cymraeg gan Mozilla i fireinio modelau acwsteg.

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

Ar GeForce RTX 2080, mae'n cymryd hyd at 13 awr.



# Gwerthuso 

`root@bff0be8425ea:/usr/src/xlsr-finetune# python3 evaluate.py`

|Training Data | Test Data | Model | Decode | WER |
|---|---|---|---|---|
|cv6.1 training+validation | cv6.1 test | wav2vec2 ft cy | greedy | 25.59% |
|cv6.1 training+validation | cv6.1 test | wav2vec2 ft cy | ctc | 25.47% |
|cv6.1 training+validation | cv6.1 test | wav2vec2 ft cy | ctc with lm (kenlm, n=5) | **15.07%** |

