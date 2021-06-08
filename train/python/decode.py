import torch
import librosa

from ctcdecode import CTCBeamDecoder

from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

 Prifysgol Bangor University

"""

def greedy_decode(logits):
    predicted_ids=torch.argmax(logits, dim=-1)
    return processor.batch_decode(predicted_ids)[0]

def lm_decode(lm_file_path, logits):
    
    vocab=processor.tokenizer.convert_ids_to_tokens(range(0, processor.tokenizer.vocab_size))
    space_ix = vocab.index('|')
    vocab[space_ix]=' '

    ctcdecoder = CTCBeamDecoder(vocab, 
        model_path=lm_file_path,
        alpha=1.3648747541523258,
        beta=0.441997826890268,
        cutoff_top_n=40,
        cutoff_prob=1.0,
        beam_width=100,
        num_processes=4,
        blank_id=processor.tokenizer.pad_token_id,
        log_probs_input=True
        )

    beam_results, beam_scores, timesteps, out_lens = ctcdecoder.decode(logits)
    return "".join(vocab[n] for n in beam_results[0][0][:out_lens[0][0]])

#
def main(audio_file, lm_file_path, **args):
    global processor
    global model

    organisation_name = "BangorUniversity"
    model_name = "wav2vec2-large-xlsr-53-ft-cy"
    huggingface_model = organisation_name + "/" + model_name
    model_path = huggingface_model

    processor = Wav2Vec2Processor.from_pretrained(model_path)
    model = Wav2Vec2ForCTC.from_pretrained(model_path)

    audio, rate = librosa.load(audio_file, sr=16000)
    inputs = processor(audio, sampling_rate=16_000, return_tensors="pt", padding=True)

    with torch.no_grad():
        logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits

    if not lm_file_path:
        output=greedy_decode(logits)
    else:
        output=lm_decode(lm_file_path, logits)

    print (output)


if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("--wav", dest="audio_file", required=True)
    parser.add_argument("--lm", dest="lm_file_path")
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
