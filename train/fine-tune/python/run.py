import os
import json
import argparse

import publish
import train_kenlm
import train_wav2vec2

from pathlib import Path
from evaluate import evaluate

"""

Execute all steps for training both an acoustic and languege model for Welsh

"""

def parse_args():
    parser = argparse.ArgumentParser(description="Finetune a wav2vec2 pre-trained model for speech recognition")

    parser.add_argument(
        "--session-id",
        type=str,
        required=True,
        help="an id that should be given for the training session (str)",
    )
    parser.add_argument(
        "--language",
        type=str,
        required=True,
        help="language(s) we are training for (str)",
    )
    parser.add_argument(
        "--training-dir",
        type=str,
        required=True,
        help="directory where training should be conducted"
    )

    parser.add_argument(
        "--train-wav2vec2",
        action='store_true',
        help="flag whether a new wav2vec2 acoustic model should be trained (bool)",
    )
    parser.add_argument(
        "--no-train-wav2vec2",
        dest="train_wav2vec2",
        action='store_false'
    ),
    parser.set_defaults(train_wav2vec2=True)

    parser.add_argument(
        "--train-kenlm",
        action="store_true",
        help="flag whether a new KenLM language model should be trained (bool)",
    )
    parser.add_argument(
        "--no-train-kenlm",
        dest="train_kenlm",
        action='store_false'
    ),
    parser.set_defaults(train_kenlm=True)

    parser.add_argument(
        "--optimize-kenlm",
        action='store_true',
        help="flag whether the last KenLM model should be optimized (bool)",
    )
    parser.add_argument(
        "--no-optimize-kenlm",
        dest="optimize_kenlm",
        action='store_false'
    ),
    parser.set_defaults(train_optimize=True)

    parser.add_argument(
        "--pre-trained-model-name",
        type=str,
        required=True,
        help="name of pretrained model from HuggingFace models hub (str)",
    )
    parser.add_argument(
        "--training-split-name",
        type=str,
        required=True,
        help="name of split for training (str)",
    )
    parser.add_argument(
        "--test-split-name",
        type=str,
        required=True,
        help="name of split for testing (str)",
    )    
    parser.add_argument(
        "--oscar-text-corpus-name",
        type=str,
        default=None,
        help="name of language specific OSCAR text corpus (str)",
    )

    args = parser.parse_args()
    return args


def main():
    
    args = parse_args()

    perform_training_wav2vec2 = args.train_wav2vec2
    perform_training_kenlm = args.train_kenlm
    perform_optimize_kenlm = args.optimize_kenlm

    pretrained_model_name = args.pre_trained_model_name
    
    session_id = args.session_id
    training_dir = args.training_dir
    logging_dir = os.path.join("/", "logs", session_id)

    Path(training_dir).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(training_dir, 'commandline_args.txt'), 'w') as f:
         json.dump(args.__dict__, f, indent=2)

    #
    if perform_training_wav2vec2:
        print ("\nTraining acoustic model in {}".format(training_dir))
        wav2vec2_model_dir = train_wav2vec2.train(training_dir, logging_dir, 
                                                  args.language,
                                                  args.pre_trained_model_name, 
                                                  args.training_split_name, 
                                                  args.test_split_name)
        #evaluate(training_dir, '')

    if perform_training_kenlm:
        print ("\n\nTraining KenLM language model...")    
        lm_model_dir = train_kenlm.train(training_dir, "unshuffled_deduplicated_cy")
    
    if perform_optimize_kenlm:
        print ("\n\nOptimizing KenLM language model...")
        print (lm_model_dir)
        train_kenlm.optimize(lm_model_dir, wav2vec2_model_dir)

    #print ("Packaging for publishing...")
    #publish_dir = os.path.join(models_root_dir, "published", wav2vec2_model_name)

    #if perform_training_kenlm or perform_optimize_kenlm: kenlm_archive_file_path = publish.make_model_tarfile(kenlm_model_name, lm_model_dir, publish_dir)    
    #if perform_training_wav2vec2: publish_dir = publish.copy_for_publishing(wav2vec2_model_dir, publish_dir)
    
    #print ("Files for publication ready at {}".format(publish_dir))


if __name__ == "__main__":
    main()
