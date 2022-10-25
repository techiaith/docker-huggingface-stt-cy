
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5270295.svg)](https://doi.org/10.5281/zenodo.5270295)

# docker-wav2vec2-cy

[(cliciwch yma os hoffwch ddarllen y README Cymraeg)](README.md)

The project develops and provides Welsh and bilingual speech recognition using the wav2vec2 method [1], [2] and [3]. Data from Mozilla Common Voice Cymraeg has been mainly used, with the scripts of this project, to create models that transcribe any Welsh (and English) speech fairly accurately. You can download the models in order to use speech recognition on your computer or within your own software projects.

## How to Use the Welsh speech recognition models

The resources in the 'inference' folder make it easy to use models that have already been trained to transcribe Welsh speech with small or large audio files or even with videos such as on YouTube. Visit [inference/README_en.md](inference/README.md) for more information.

## Training your own models

The resources in the 'train' folder facilitate the training or refinement of acoustic models. The scripts also include a way to train language models in order to improve the accuracy of transcription results. See [train/README_en.md](train/README.md) for more information.

## Acknowledgements

Such effective wav2vec2+KenLM speech recognition models would not have been possible without the work and contributions of the following organisations and individuals..

 - Mozilla and everyone who has contributed their voices to [Common Voice](https://commonvoice.mozilla.org/) but in particular to Rhoslyn Prys (meddal.com) who undertook on a voluntary basis a number of crowdsourcing campaigns, to the Mentrau Iaith, Gwynedd Council, the National Library of Wales who worked with Rhoslyn on some of these campaigns, and to the Welsh Government.
 - Facebook AI for wav2vec2 and subsequently HuggingFace: [Fine-Tune XLSR-Wav2Vec2 for low-resource ASR with 🤗 Transformers](https://huggingface.co/blog/fine-tune-xlsr-wav2vec2)
 - Parlance Speech Recognition for their PyTorch CTC Decoder bindings and KenLM integration (https://github.com/parlance/ctcdecode)
 - KenLM : (https://github.com/kpu/kenlm)
 

## References

Alexei Baevski, H. Zhou, Abdel-rahman Mohamed, and Michael Auli 2020. *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations*. ArXiv, abs/2006.11477.

Rosana Ardila, Megan Branson, Kelly Davis, Michael Henretty, Michael Kohler, Josh Meyer, Reuben Morais, Lindsay Saunders, Francis M. Tyers, and Gregor Weber 2020. *Common Voice: A Massively-Multilingual Speech Corpus*. In LREC.

Pedro Javier Ortiz Suárez, Benoît Sagot, and Laurent Romary 2019. *Asynchronous pipelines for processing huge corpora on medium to low resource infrastructures.* In CMLC-7 (pp. 9 – 16). Leibniz-Institut für Deutsche Sprache.


## Acknowledging our work

If you use this resource, we kindly ask you to acknowledge and reference our work. Doing so helps us secure future funding to create more useful resources to share.

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
