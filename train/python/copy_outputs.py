import os
import glob
import shutil
import tarfile

from pathlib import Path

DESCRIPTION = """

 Prifysgol Bangor University

"""

TECHIAITH_RELEASE=os.environ["TECHIAITH_RELEASE"]

#
def copy_for_evaluation_or_publishing(source_dir, target_dir):
   
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    # copy json files
    for file in glob.glob(os.path.join(source_dir, r"*.json")):
        print ("Copying %s" % file)
        shutil.copy(file, target_dir)

    # copy config and model binary file 
    checkpoint_dir=glob.glob(os.path.join(source_dir, r"checkpoint-*"))[0]
    shutil.copy(os.path.join(checkpoint_dir, "config.json"), target_dir)
    shutil.copy(os.path.join(checkpoint_dir, "pytorch_model.bin"), target_dir)

    return target_dir 

#
def make_model_tarfile(model_name, source_dir, version=TECHIAITH_RELEASE): 
    output_dir = Path(source_dir).parent
    output_tar_file_path = os.path.join(output_dir, model_name.replace("/","_") + "." + version + ".tar.gz")
    with tarfile.open(output_tar_file_path, "w:gz") as tar:
        tar.add(source_dir, arcname="")

    return output_tar_file_path

