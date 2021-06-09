# docker-wav2vec2-xlsr-ft-cy

[(click here to read the README in English)](README_en.md)

 - [Hyfforddi modelau](#hyfforddi-modelau)
 - [Cynnal gweinydd eich hunain](#gweinydd-adnabod-lleferydd)

 
## Hyfforddi Modelau 

Mae'r project yma yn darparu amgylchedd Docker sy'n hwyluso hyfforddi neu fireinio
**modelau acwsteg** amlieithog enfawr newydd (wav2vec2) gan Facebook AI ac HuggingFace
ar gyfer wireddu adnabod lleferydd Cymraeg. (gweler [train/README.md](train/README.md))

Mae'r project hefyd yn cynnwys modd hyfforddi **model iaith** KenLM Cymraeg er mwyn gwella
canlyniadau yn sylweddol. 

Defnyddir data gan project Mozilla Common Voice ar gyfer hyfforddi ac i brofi adnabod
lleferydd. Defnyddir corpws testun Cymraeg gan project OSCAR i hyfforddi'r model iaith. 

Mae defnyddio'r ddau model ar y cyd ar set profi Common Voice Cymraeg, yn rhoi 
[cyfradd gwallau o 15%](train/README.md#gwerthuso)


## Gweinydd Adnabod Lleferydd

Mae'r project yn ogystal yn cynnwys modd i chi fedru darparu eich modelau arlein neu'n
lleol drwy API syml, neu i darparu API gyda modelau sydd eisoes wedi eu hyfforddi 
gan yr Uned Technolegau Iaith ym Mhrifysgol Bangor. 

Ewch i [server/README.md](server/README.md) ar rhagor o wybodaeth. 

Gellir gweld enghraifft o'r modelau newydd ar waith o fewn gwefan gwasanaeth Trawsgrifiwr ar-lein (https://trawsgrifiwr.techiaith.cymru/)


## Diolchiadau

Diolch i'r cwmniau, sefydliadau ac unigolion canlynol sydd wedi ein helpu i wireddu datrysiad adnabod lleferydd mor effeithiol..

 - Mozilla a phawb sydd wedi cyfrannu yn hael ac yn wirfoddol drwy gwefan [Common Voice](https://commonvoice.mozilla.org/), yn enwedig i Rhoslyn Prys (meddal.com) a ymgymerodd â nifer o ymgyrchoedd torfoli ar sail wirfoddol, i'r Mentrau Iaith, Cyngor Gwynedd, Llyfrgell Genedlaethol Cymru a weithiodd gyda Rhoslyn ar rai o'r ymgyrchoedd hyn, ac hefyd i Lywodraeth Cymru.
 - Facebook AI am y wav2vec2 cyntaf ac yna i HuggingFace: [Fine-Tune XLSR-Wav2Vec2 for low-resource ASR with 🤗 Transformers](https://huggingface.co/blog/fine-tune-xlsr-wav2vec2)
 - Parlance Speech Recognition am integreiddio CTC Decoder gyda PyTorch: (https://github.com/parlance/ctcdecode)
 

## Cyfeiriadau

Alexei Baevski, H. Zhou, Abdel-rahman Mohamed, and Michael Auli 2020. *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations*. ArXiv, abs/2006.11477.

Rosana Ardila, Megan Branson, Kelly Davis, Michael Henretty, Michael Kohler, Josh Meyer, Reuben Morais, Lindsay Saunders, Francis M. Tyers, and Gregor Weber 2020. *Common Voice: A Massively-Multilingual Speech Corpus*. In LREC.

Pedro Javier Ortiz Suárez, Benoît Sagot, and Laurent Romary 2019. *Asynchronous pipelines for processing huge corpora on medium to low resource infrastructures.* In CMLC-7 (pp. 9 – 16). Leibniz-Institut für Deutsche Sprache.



## Cydnabyddiaeth

Os defnyddiwch chi'r adnodd hwn, gofynnwn yn garedig i chi gydnabod a chyfeirio at ein gwaith. Mae cydnabyddiaeth o'r fath yn gymorth i ni sicrhau cyllid yn y dyfodol i greu rhagor o adnoddau defnyddiol i'w rhannu.

```
@misc{Jones2021,
  author = {Jones, Dewi Bryn},
  title = {Speech recognition for Welsh with fine tuned wav2vec2 and KenLM language models},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/techiaith/docker-wav2vec2-ft-cy}},
  commit = {}
}
```


