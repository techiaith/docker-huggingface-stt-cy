import os
import publish
import train_kenlm
import train_wav2vec2

from evaluate import evaluate
from pathlib import Path

"""

Execute all steps for training both an acoustic and languege model for Welsh

"""

if __name__ == "__main__":

    perform_training_wav2vec2 = True
    perform_training_kenlm = True
    perform_optimize_kenlm = True

    organisation = "techiaith"
    models_root_dir = "/models"
    wav2vec2_model_name = "wav2vec2-xlsr-ft-cy"
    language="cy"
    kenlm_model_name = "kenlm"

    wav2vec2_model_dir = os.path.join(Path.home(), wav2vec2_model_name)
    lm_model_dir = os.path.join(Path.home(), kenlm_model_name)

    if perform_training_wav2vec2:
        print ("\nTraining acoustic model...")
        wav2vec2_model_dir = train_wav2vec2.train(wav2vec2_model_dir, language)
        evaluate(wav2vec2_model_dir, '')

    if perform_training_kenlm:
        print ("\n\nTraining KenLM language model...")    
        lm_model_dir = train_kenlm.train(lm_model_dir, "unshuffled_deduplicated_cy")
    
    if perform_optimize_kenlm:
        print ("\n\nOptimizing KenLM language model...")
        print (lm_model_dir)
        train_kenlm.optimize(lm_model_dir, wav2vec2_model_dir)

    print ("Packaging for publishing...")
    publish_dir = os.path.join(models_root_dir, "published", wav2vec2_model_name)

    if perform_training_kenlm or perform_optimize_kenlm: kenlm_archive_file_path = publish.make_model_tarfile(kenlm_model_name, lm_model_dir, publish_dir)    
    if perform_training_wav2vec2: publish_dir = publish.copy_for_publishing(wav2vec2_model_dir, publish_dir)
    
    print ("Files for publication ready at {}".format(publish_dir))
