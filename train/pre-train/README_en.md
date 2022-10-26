# Pre-training speech recognition models 

[(**cliciwch yma i ddarllen y README yn Gymraeg**)](README.md)

At the moment, the best Welsh speech recognition models from this repo have been created by fine-tuning models that Facebook/Meta AI have pre-trained from only the sounds of speech in different languages, including some Welsh. (i.e. without also need transcripts) In the original paper on the wav2vec2 method ["wav2vec2: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477) by Alexei Baevski, Henry Zhou, Abdelrahman Mohamed and Michael Auli, it was proved that it is possible to get a WER as low as 4.8 on the LibriSpeech English testing if a model is first pre-trained with 53,000 hours of English speech audio alone. In this folder we want to create scripts to pre-train models with Welsh (and some English) speech alone in an attempt to lower scores WER even further in subsequent fine-tuned models. 

The work draws heavily on resources and documentation from the HuggingFace:

https://github.com/huggingface/transformers/tree/main/examples/pytorch/speech-pretraining

Only an initial/experimental base model has been pre-trained with these scripts so far, using English speech from LibriSpeech's minimal subsets (`validation` and `test`), and 184 hours and 47 minutes of Welsh speech from various videos on YouTube. The script [`build_youtube_playlists_corpus.sh](../../inference/python/build_youtube_playlists_corpus.sh) lists the playlists used to identify which videos are used. The resulting pre-trained base model is available from the HuggingFace website from

https://huggingface.co/techiaith/wav2vec2-base-cy

The work so far is a proof of concept. Until we have collected thousands of hours of Welsh speech, rather than hundreds, the WER scores, after fine-tuning the model, see [run_base-cy.sh](../fine-tune/python/run_base-cy.sh), as seen below, will remain very high. We tested with the Welsh Common Voice test set as well as on a test set of YouTube videos with transcriptions we have corrected.

|  Set Profi 	|   WER	|  CER 	|   WER (+LM)	|  CER(+LM) 	|    
|---	|---	|---	|---	|---	|
|   CV10	|   94.83	|   83.55	|   92.31	|   82.25	|
|   YouTube	|   95.43	|   90.26	|   93.60	|   89.33	|



