import os
import glob
import shutil
import tarfile

from pathlib import Path

DESCRIPTION = """

 Prifysgol Bangor University

"""

#
def export_checkpoint(training_dir):
    # copy config and model binary file 
    checkpoint_dir=glob.glob(os.path.join(training_dir, r"checkpoint-*"))[0]
    shutil.copy(os.path.join(checkpoint_dir, "config.json"), training_dir)
    shutil.copy(os.path.join(checkpoint_dir, "pytorch_model.bin"), training_dir)
    shutil.rmtree(checkpoint_dir)


#
def copy_for_publishing(source_dir, target_dir):
    print ("Copying for evaluation or publishing")
    print (source_dir)
    print (target_dir)

    Path(target_dir).mkdir(parents=True, exist_ok=True)

    # copy json files
    for file in glob.glob(os.path.join(source_dir,'*')):
        if os.path.isfile(file): 
            print ("Copying %s" % file)
            shutil.copy(file, target_dir)

    return target_dir 

#
def make_model_tarfile(model_name, source_dir, output_dir):

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_tar_file_path = os.path.join(output_dir, model_name + ".tar.gz")
    print ("Creating {} ".format(output_tar_file_path))
    with tarfile.open(output_tar_file_path, "w:gz") as tar:
        tar.add(source_dir, arcname="")

    return output_tar_file_path

