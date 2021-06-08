# docker-wav2vec2-xlsr-ft-cy

[(cliciwch yma os hoffwch ddarllen y README Cymraeg)](README.md)

This repository contains an implementation for easy training of speech 
recognition models and their provision via an online API with Docker.

Two types of models are supported. 

First, a pretrained multilingual acoustic model (wav2vec2) by Facebook AI and HuggingFace
is fine tuned for training an effective Welsh acoustic model.

However, the repository also contains scripts for training and utilising a KenLM 
language model for improving decoding results considerably.

The Welsh language dataset from Common Voice is used for fine tuning the acoustic model and for testing. 
The Welsh text corpus by the OSCAR project was used for training the language model.

## References

Alexei Baevski, H. Zhou, Abdel-rahman Mohamed, and Michael Auli 2020. *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations*. ArXiv, abs/2006.11477.

Rosana Ardila, Megan Branson, Kelly Davis, Michael Henretty, Michael Kohler, Josh Meyer, Reuben Morais, Lindsay Saunders, Francis M. Tyers, and Gregor Weber 2020. *Common Voice: A Massively-Multilingual Speech Corpus*. In LREC.

Pedro Javier Ortiz Suárez, Benoît Sagot, and Laurent Romary 2019. *Asynchronous pipelines for processing huge corpora on medium to low resource infrastructures.* In CMLC-7 (pp. 9 – 16). Leibniz-Institut für Deutsche Sprache.

