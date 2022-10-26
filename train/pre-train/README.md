# Rhag hyfforddi modelau adnabod lleferydd 

[(**click here to read the README in English**)](README_en.md)

Ar y moment, mae'r modelau adnabod lleferydd Cymraeg gorau o'r repo hwn wedi eu creu drwy fireinio modelau mae Facebook/Meta AI wedi eu rhag-hyfforddi o sain leferydd wahanol ieithoedd, gan gynnwys mymryn o Gymraeg, yn unig (h.y. heb angen trawsgrifiadau hefyd). Yn y papur gwreiddiol ar y dull wav2vec2 ["wav2vec2: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477) gan Alexei Baevski, Henry Zhou, Abdelrahman Mohamed a Michael Auli, profwyd bod modd cael WER cyn lleied â 4.8 ar set profi Saesneg LibriSpeech ar ôl rhag-hyfforddi ar 53,000 awr o sain lleferydd Saesneg yn unig. Yn y ffolder hwn rydym am greu sgriptiau i greu modelau sylfaenol penodol i’r Gymraeg mewn ymgais i ostwng sgorau WER hyd yn oed ymhellach.

Mae'r gwaith yn defnyddio lawer ar adnoddau a dogfennaeth gan y cwmni HuggingFace:  

https://github.com/huggingface/transformers/tree/main/examples/pytorch/speech-pretraining

Dim ond model cychwynnol/arbrofol sydd wedi ei rhag-hyfforddi gyda'r sgriptiau hyn hyd yn hyn, gan ddefnyddio lleferydd Saesneg o is-setiau lleiaf LibriSpeech (`validation` a `test`), ac yna 184 awr a 47 munud o leferydd Cymraeg sydd wedi ei chrafu o amryw o fideos ar YouTube. Mae'r sgript [`build_youtube_playlists_corpus.sh](../../inference/python/build_youtube_playlists_corpus.sh) yn rhestru'r playlists defnyddiwyd i nodi ba fideos defnyddir. Mae hefyd ar gael o wefan HuggingFace o 

https://huggingface.co/techiaith/wav2vec2-base-cy

Megis prawf cysyniad yw'r gwaith hyd yn hyn, hyd nes byddwn ni wedi casglu miloedd o oriau o leferydd Cymraeg, yn hytrach na channoedd. Ar ol fireinio'r model o'r sgriptiau rhag-hyfforddi hyn ('wav2vec2-base-cy'), gweler [run_base-cy.sh](../fine-tune/python/run_base-cy.sh) gwelwyd WER uchel gyda set profi Common Voice yn ogystal ar set profi o fideos YouTube rydyn ni wedi eu drawsgrifio'n gywir.

|  Set Profi 	|   WER	|  CER 	|   WER (+LM)	|  CER(+LM) 	|    
|---	|---	|---	|---	|---	|
|   CV10	|   94.83	|   83.55	|   92.31	|   82.25	|
|   YouTube	|   95.43	|   90.26	|   93.60	|   89.33	|


