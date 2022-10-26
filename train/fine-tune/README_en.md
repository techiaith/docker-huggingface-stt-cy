# Fine tune wav2vec2 models for Welsh

[**(cliciwch yma os hoffwch ddarllen y README Cymraeg)**](README.md)

These are scripts to fine-tune a variety of pre-trained models that are available from HuggingFace's model hub.

 - `run_xlsr-large-53.sh` - to fine-tune the first multilingual wav2vec2 models from Facebook : [facebook/wav2vec2-large-xlsr-53](https://huggingface.co/facebook/wav2vec2-large-xlsr-53) as well as create and optimize supporting KenLM language models
 - `run_xls-r-1b.sh` - to fine-tune more multilingual wav2vec2 models - [facebook/wav2vec2-xls-r-1b](https://huggingface.co/facebook/wav2vec2-xls-r-1b) as well as create and optimize supporting KenLM language models
 - `run_en_cy.sh` - fine-tune  [facebook/wav2vec2-large-xlsr-53](https://huggingface.co/facebook/wav2vec2-large-xlsr-53) for bilingual acoustic speech recognition models.
 - `run_base-cy.sh` - fine-tuning an experimental model pre-trained by techiaith with more Welsh speech audio as well as create and optimize supporting KenLM language models
  
The first scripts for Welsh were developed during [a fine-tuning week for low resource languages by HuggingFace](https://discuss.huggingface.co/t/open-to-the-community-xlsr-wav2vec2-fine-tuning-week-for-low-resource-languages/4467).

Our own subsets of Welsh and English Common Voice data were built and used by Mozilla for refining the most effective models. See https://github.com/techiaith/docker-commonvoice-custom-splits-builder.

The project includes scripts to train KenLM language models with text from the [OSCAR project corpus on the HuggingFace Datasets website](https://huggingface.co/datasets/oscar) and optimize alpha and beta CTC decoding hyperparameters. (We have integrated [Parlance CTC Decode](https://github.com/parlance/ctcdecode) to improve recognition results with the support of a language model)


# How to use...

`$ make`

`$ make run `
`
In order to download and import the Common Voice data, you need to create a Python file to contain a URL to its `.tar.gz` file. An example/template can be found in the file [`cv_version.template.py`](cv_version.template.py). Enter the name of the file (without the `.py` extension) into the variable `CV_CONFIG_FILE` inside the script you would like to use for training.

(it is expected that you have downloaded the Common Voice dataset(s) from the official website and re-located the `.tar.gz` file to your own local `http` server)

Then to start training, choose any of the four "run" scripts. E.g.

`root@d702159be82f:/xlsr-ft-train# ./run_xlsr-large-53.sh`

Depending on the graphics card, it will take a few hours to train.


# Evaluation

The scripts will evaluate the models during the training. Here are the results after each step is complete:

|Language | Training Data | Test Data | Model | Decode | WER | CER |
|---|---|---|---|---|---|---|
| CY |cv11 training+validation (s=max) | cv11 test | wav2vec2-large-xlsr-53 | greedy | **6.04%** | **1.88%** |
| CY |cv11 training+validation (s=max) | cv11 test | wav2vec2-large-xlsr-53 | ctc | **6.01%** | **1.88%** |
| CY |cv11 training+validation (s=max) | cv11 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | **4.05%** | **1.49%** |
| CY+EN |cv11 training+validation cy+en (s=max) | cv11 test cy+en | wav2vec2-large-xlsr-53 | greedy | 17.07% | 7.32% |
| CY+EN |cv11 training+validation cy+en (s=max) | cv11 test cy| wav2vec2-large-xlsr-53 | greedy | 7.13% | 2.2% |
| CY+EN |cv11 training+validation cy+en (s=max) | cv11 test en| wav2vec2-large-xlsr-53 | greedy | 27.54% | 11.6% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-xls-r-1b | greedy | 15.82% | 4.53% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-xls-r-1b | ctc | 15.72% | 4.50% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-xls-r-1b | ctc with lm (kenlm, n=5) | 10.17% | 3.42% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-large-xlsr-53 | greedy | 16.73% | 4.63% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc | 16.62% | 4.61% |
| CY |cv11 training+validation+custom other (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 10.45% | 3.42% |
| CY |cv11 training+validation (s=3) | cv11 test | wav2vec2-large-xlsr-53 | greedy | 17.42% | 4.83% |
| CY |cv11 training+validation (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc | 17.29% | 4.80% |
| CY |cv11 training+validation (s=3) | cv11 test | wav2vec2-large-xlsr-53 | ctc with lm (kenlm, n=5) | 10.82% | 3.58% |

Key:

- "custom other" : an additional subset created from recordings of unique sentences in 'other.tsv' in Common Voice. i.e. recordings that no-one has yet listened to and validated. 
- "s=3" : the maximum number of recordings per unique sentence within Common Voice
- "s=max" : quite a high maximum, so that every single recording of a sentence is allowed in the permitted
