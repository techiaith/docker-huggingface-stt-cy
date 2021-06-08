import os
import train_wav2vec2
import train_kenlm
import copy_outputs

"""

Execute all steps for training both an acoustic and languege model for Welsh

"""

if __name__ == "__main__":

    organisation = "techiaith_bangor"
    models_root_dir = "/models"
    wav2vec2_model_name = "wav2vec2-xlsr-ft-cy"
    kenlm_model_name = "kenlm-cy"

    print ("\nTraining acoustic model...")
    wav2vec2_model_path = train_wav2vec2.train(models_root_dir, wav2vec2_model_name)
    #wav2vec2_model_dir = os.path.join(models_root_dir, wav2vec2_model_name)

    print ("\n\nTraining KenLM language model...")    
    lm_model_dir = train_kenlm.train(models_root_dir, kenlm_model_name, "unshuffled_deduplicated_cy")
    #lm_model_dir = os.path.join(models_root_dir, kenlm_model_name)

    print ("\n\nOptimizing KenLM language model...")
    train_kenlm.optimize(lm_model_dir, wav2vec2_model_dir)

    print ("Packaging to tar.gz files")
    wav2vec2_archive_file_path = copy_outputs.make_model_tarfile("{}/{}".format(organisation, wav2vec2_model_name), wav2vec2_model_dir)
    kenlm_archive_file_path = copy_outputs.make_model_tarfile("{}/{}".format(organisation, kenlm_model_name), lm_model_dir)

    print ("Files for publication ready at {} and {}".format(wav2vec2_archive_file_path, kenlm_archive_file_path))
