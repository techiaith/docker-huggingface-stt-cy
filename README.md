
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5270295.svg)](https://doi.org/10.5281/zenodo.5270295)


# docker-wav2vec2-cy

[(click here to read the README in English)](README_en.md)

Mae'r project yn datblygu ac yn darparu adnabod lleferydd Cymraeg a ddwyieithog gan ddefnyddio'r dull wav2vec2 [1], [2] a [3]. Defnyddir data o Mozilla Common Voice Cymraeg yn bennaf, gyda sgriptiau'r project hwn, i greu modelau sydd yn trawsgrifio unrhyw leferydd Cymraeg (a Saesneg) yn lledgywir. Mae modd i chi llwytho i lawr y modelau er mwyn defnyddio adnabod lleferydd ar eich cyfrifiadur neu o fewn projectau meddalwedd eich hunain.


## Defnyddio adnabod lleferydd Cymraeg

Mae'r adnoddau yn y ffolder 'inference' yn ei gwneud hi'n hawdd defnyddio modelau sydd wedi eu hyfforddi'n barod i drawsgrifio lleferydd Cymraeg o fewn ffeiliau sain fach neu fawr neu hyd yn oed o fewn fideos megis ar YouTube. Ewch i [inference/README.md](inference/README.md) am ragor o wybodaeth.


## Hyfforddi Modelau 

Mae'r adnoddau yn y ffolder 'train' yn hwyluso hyfforddi neu fireinio modelau acwsteg. Mae'r sgriptiau yn cynnwys modd hyfforddi modelau iaith yn ogystal er mwyn gwella cywirdeb canlyniadau trawsgrifio. Gweler [train/README.md](train/README.md) am ragor o wybodaeth.


## Diolchiadau

Diolch i'r cwmnïau, sefydliadau ac unigolion canlynol sydd wedi ein helpu i wireddu datrysiad adnabod lleferydd Cymraeg mor effeithiol.

 - Mozilla a phawb sydd wedi cyfrannu yn hael ac yn wirfoddol drwy gwefan [Common Voice](https://commonvoice.mozilla.org/), yn enwedig i Rhoslyn Prys (meddal.com) a ymgymerodd â nifer o ymgyrchoedd torfoli ar sail wirfoddol, i'r Mentrau Iaith, Cyngor Gwynedd, Llyfrgell Genedlaethol Cymru a weithiodd gyda Rhoslyn ar rai o'r ymgyrchoedd hyn, ac hefyd i Lywodraeth Cymru.
 - Facebook AI am rhannu'r ddull wav2vec2 yn ogystal a modelau amlieithog enfawr wedi'i rhag-hyfforddi. [wav2vec 2.0 - Learning the Structure of Speech from Raw Audio](https://ai.facebook.com/blog/wav2vec-20-learning-the-structure-of-speech-from-raw-audio/)
 - HuggingFace : [Fine-Tune XLSR-Wav2Vec2 for low-resource ASR with 🤗 Transformers](https://huggingface.co/blog/fine-tune-xlsr-wav2vec2)
 - Parlance Speech Recognition : (https://github.com/parlance/ctcdecode)
 - KenLM : (https://github.com/kpu/kenlm)
 

## Cyfeiriadau

[1] Alexei Baevski, H. Zhou, Abdel-rahman Mohamed, and Michael Auli. 2020. *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations*. ArXiv, abs/2006.11477.

[2] Alexis Conneau, Alexi Baevski, Ronan Collobert, Abdelrahman Mohamed and Michael Auli. 2020. *Unsupervised Cross-lingual Representation Learning for Speech Recognition*. ArXiv, abs/2006.13979.

[3] Arun Babu, Changhan Wang, Andros Tjandra, Kushal Lakhotia, Qiantong Xu, Naman Goyal, Kritika Singh, Patrick von Platen, Yatharth Saraf, Juan Pino, Alexei Baevski, Alexis Conneau and Michael Auli. 2021. *XLS-R: Self-supervised Cross-lingual Speech Representation Learning at Scale*. ArXiv, abs/2111.09296

[4] Rosana Ardila, Megan Branson, Kelly Davis, Michael Henretty, Michael Kohler, Josh Meyer, Reuben Morais, Lindsay Saunders, Francis M. Tyers, and Gregor Weber. 2020. *Common Voice: A Massively-Multilingual Speech Corpus*. In LREC.

[5] Pedro Javier Ortiz Suárez, Benoît Sagot, and Laurent Romary. 2019. *Asynchronous pipelines for processing huge corpora on medium to low resource infrastructures.* In CMLC-7 (pp. 9 – 16). Leibniz-Institut für Deutsche Sprache.



## Cydnabyddiaeth

Os defnyddiwch chi'r adnodd hwn, gofynnwn yn garedig i chi gydnabod a chyfeirio at ein gwaith. Mae cydnabyddiaeth o'r fath yn gymorth i ni sicrhau cyllid yn y dyfodol i greu rhagor o adnoddau defnyddiol i'w rhannu.

```
@software{dewi_bryn_jones_2021_5270295,
  author       = {Dewi Bryn Jones},
  title        = {{GitHub Repository: techiaith/docker-wav2vec2-cy Speech recognition for Welsh with wav2vec2.}},
  month        = aug,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {22.10},
  doi          = {10.5281/zenodo.5270295},
  url          = {https://doi.org/10.5281/zenodo.5270295}
}
```
