# Mireinio modelau wav2vec2 ar gyfer y Gymraeg

[**(click here to read the README in English)**](README_en.md)

Mae sgriptiau i fireinio amrywiaeth o fodelau sydd wedi eu rhag-hyfforddi ac ar gael o hwb modelau HuggingFace. 

 - `run_xlsr-large-53.sh` - i fireinio modelau cyntaf wav2vec2 amlieithog gan Facebook : [facebook/wav2vec2-large-xlsr-53](https://huggingface.co/facebook/wav2vec2-large-xlsr-53) yn ogystal a chreu ac optimeiddio model iaith KenLM
 - `run_xls-r-1b.sh` - i fireinio modelau wav2vec2 amlieithog mwy : [facebook/wav2vec2-xls-r-1b](https://huggingface.co/facebook/wav2vec2-xls-r-1b) yn ogystal a chreu ac optimeiddio model iaith KenLM
 - `run_en_cy.sh` - mireinio [facebook/wav2vec2-large-xlsr-53](https://huggingface.co/facebook/wav2vec2-large-xlsr-53) ar gyfer model adnabod lleferydd acwstig yn unig ond yn ddwyieithog.
 - `run_base-cy.sh` - mireinio model arbrofol sydd wedi ei rhag-hyfforddi gan uned techiaith gyda rhagor o sain lleferydd Cymraeg yn ogystal a chreu ac optimeiddio model iaith KenLM ategol.
  
Datblygwyd y sgriptiau cyntaf ar gyfer y Gymraeg yn ystod [wythnos fireinio i ieithoedd llai eu hadnoddau gan HuggingFace](https://discuss.huggingface.co/t/open-to-the-community-xlsr-wav2vec2-fine-tuning-week-for-low-resource-languages/4467). 

Adeiladwyd a ddefnyddiwyd is-setiau ein hunain o ddata Common Voice Cymraeg a Saesneg gan Mozilla ar gyfer mireinio'r modelau mwyaf effeithiol. Gweler https://github.com/techiaith/docker-commonvoice-custom-splits-builder. 

Mae'r project yn cynnwys sgriptiau i hyfforddi modelau iaith KenLM gyda thestun o [gorpws broject OSCAR ar wefan Datasets HuggingFace](https://huggingface.co/datasets/oscar) a'u optimeiddio o fewn ddull dadgodio CTC. (rydym wedi integreiddio [Parlance CTC Decode](https://github.com/parlance/ctcdecode) gyda HuggingFace i alluogi wella canlyniadau gyd chymorth modelau iaith)


# Sut i'w ddefnyddio...  

`$ make`

`$ make run `

Er mwyn llwytho i lawr data Common Voice, mae angen i chi greu ffeil Python i gynnwys yr URL. Mae enghraifft/templed i'w weld yn y ffeil [`cv_version.template.py`](cv_version.template.py) . Nodwch enw'r ffeil (heb yr estyniad `.py`) o fewn y sgript hoffwch ei ddefnyddio i hyfforddi. e.e. o fewn y sgript mireinio wav2vec2-large-xlsr-53 gan Facebook,  `run_xlsr-large-53.sh`, newidiwch yr enw ar gyfer `CV_CONFIG_FILE`.

(disgwylir eich bod wedi llwytho'r set(iau) data Common Voice o'u wefan ac wedi lleoli'r ffeil `.tar.gz` ar weinydd `http` lleol eich hunain)

Yna i ddechrau hyfforddi, dewisich unrhyw un o'r pedwar sgript "run"

`root@d702159be82f:/xlsr-ft-train# ./run_xlsr-large-53.sh`

Yn dibynnu ar y cerdyn graffics, bydd yn gymryd rhai oriau i hyfforddi. 


# Gwerthuso 

Bydd y sgriptiau yn werthuso'r modelau yn ystod hyfforddi. Dyma'r canlyniadau ar ol i pob cam gwblhau

|Language | Training Data | Test Data | Model | Decode | WER | CER |
|---|---|---|---|---|---|---|
| CY |cv11 training+validation (s=max) | cv11 test | wav2vec2-large-xlsr-53 | greedy | **6.04%** | **1.88%** |
| CY |cv11 training+validation (s=max) | cv11 test | wav2vec2-large-xlsr-53 | ctc | **6.01%** | **1.88%** |
| CY |cv11 training+validation (s=max) | cv11 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | **4.05%** | **1.49%** |
| CY |cv11 training+validation (s=max) | bangor custom | wav2vec2-large-xlsr-53 | greedy | 37.46% | 14.11% |
| CY |cv11 training+validation (s=max) | bangor custom | wav2vec2-large-xlsr-53 | ctc | 37.18% | 14.08% |
| CY |cv11 training+validation (s=max) | bangor custom | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 31.51% | 14.84% |
| CY+EN |cv11 training+validation cy+en (s=max) | cv11 test cy+en | wav2vec2-large-xlsr-53 | greedy | 17.07% | 7.32% |
| CY+EN |cv11 training+validation cy+en (s=max) | cv11 test cy| wav2vec2-large-xlsr-53 | greedy | 7.13% | 2.2% |
| CY+EN |cv11 training+validation cy+en (s=max) | cv11 test en| wav2vec2-large-xlsr-53 | greedy | 27.54% | 11.6% |
| CY+EN |cv11 training+validation (s=max) | bangor custom | wav2vec2-large-xlsr-53 | greedy | 40.76% | 15.42% |
| CY+EN |cv11 training+validation (s=max) | bangor custom | wav2vec2-large-xlsr-53 | ctc | 40.47.18% | 15.34% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-xls-r-1b | greedy | 15.82% | 4.53% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-xls-r-1b | ctc | 15.72% | 4.50% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-xls-r-1b | ctc with lm (kenlm, n=5) | 10.17% | 3.42% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-large-xlsr-53 | greedy | 16.73% | 4.63% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc | 16.62% | 4.61% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 10.45% | 3.42% |
| CY |cv11 training+validation (s=3) | cv11 test | wav2vec2-large-xlsr-53 | greedy | 17.42% | 4.83% |
| CY |cv11 training+validation (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc | 17.29% | 4.80% |
| CY |cv11 training+validation (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 10.82% | 3.58% |

Allwedd:

- "custom other" : is-set ychwanegol sydd wedi ei greu gyda recordiadau o frawddegau unigryw o fewn 'other.tsv' yn Common Voice. h.y. heb i neb wrando eto a'u cadarnhau
- "s=3" : yr uchafswm ar y nifer o recordiadau mesul frawddeg unigryw o fewn Common Voice
- "s=max" : uchafswm eitha uchel, fel caniateir pob un recordiad o frawddeg yn y is-set.
- "bangor custom" : set profi trawsgrifiadau gan Prifysgol Bangor: https://git.techiaith.bangor.ac.uk/data-porth-technolegau-iaith/corpws-profi-adnabod-lleferydd/-/tree/master/data/trawsgrifio