# docker-wav2vec2-xlsr-ft-cy

[(cliciwch yma os hoffwch ddarllen y README Cymraeg)](README.md)

 - [Training your own models](#training)
 - [Host a speech recognition server](#speech-recognition-server)


## Training

This repository provides a Docker environment for training or fine-tuning
pre-trained multilingual (wav2vec2) acoustic models by Facebook AI and 
HuggingFace that implements Welsh language speech recognition (see (gweler [train/README.md](train/README_en.md))

This repository also provides a means to train and utilise KenLM based language models that significantly improves recognition results. 

The Welsh language dataset from Common Voice is used for fine tuning the acoustic model and for testing. The Welsh text corpus by the OSCAR project was used for training the language model.

Evaluating both models on the Welsh Common Voice test set gives a [word error rate of 15%](train/README_en.md#evaluation)

## Speech Recognition server

This repository also contains a simple API server implementation for hosting your trained models locally or online, or for hosting models trained by Bangor University's Language Technologies Unit. 

Go to [server/README.md](server/README_en.md) for more information.

The models can be found in action in a transcription service website - Trawsgrifiwr Ar-lein (https://trawsgrifiwr.techiaith.cymru)

## Acknowledgements

Such effective wav2vec2+KenLM speech recognition models would not have been possible without the work and contributions of the following organisations and individuals..

 - Mozilla and everyone who has contributed their voices to [Common Voice](https://commonvoice.mozilla.org/) but in particular to Rhoslyn Prys (meddal.com) who undertook on a voluntary basis a number of crowdsourcing campaigns, to the Mentrau Iaith, Gwynedd Council, the National Library of Wales who worked with Rhoslyn on some of these campaigns, and to the Welsh Government.
 - Facebook AI for wav2vec2 and subsequently HuggingFace: [Fine-Tune XLSR-Wav2Vec2 for low-resource ASR with 🤗 Transformers](https://huggingface.co/blog/fine-tune-xlsr-wav2vec2)
 - Parlance Speech Recognition for their PyTorch CTC Decoder bindings and KenLM integration (https://github.com/parlance/ctcdecode)
 

## References

Alexei Baevski, H. Zhou, Abdel-rahman Mohamed, and Michael Auli 2020. *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations*. ArXiv, abs/2006.11477.

Rosana Ardila, Megan Branson, Kelly Davis, Michael Henretty, Michael Kohler, Josh Meyer, Reuben Morais, Lindsay Saunders, Francis M. Tyers, and Gregor Weber 2020. *Common Voice: A Massively-Multilingual Speech Corpus*. In LREC.

Pedro Javier Ortiz Suárez, Benoît Sagot, and Laurent Romary 2019. *Asynchronous pipelines for processing huge corpora on medium to low resource infrastructures.* In CMLC-7 (pp. 9 – 16). Leibniz-Institut für Deutsche Sprache.

## Acknowledging our work

If you use this resource, we kindly ask you to acknowledge and reference our work. Doing so helps us secure future funding to create more useful resources to share.

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