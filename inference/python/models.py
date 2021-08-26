import os
import tarfile
import urllib.request
from urllib.parse import urlparse

from pathlib import Path
from tqdm import tqdm



class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

        
def default_root_dir():
    return os.path.join("/", "models")


def download_file(models_root_dir, model_name, version, file_name):
    # expecting model name as HuggingFace Model name e.g. techiaith/wav2vec2-xlsr-ft-cy
    # expecting file name within the HuggingFace model git repository e.g. kenlm.tar.gz

    model_file = os.path.join(models_root_dir, file_name)

    if Path(model_file).is_file():
        print ("Model file {} already downloaded.".format(model_file))
    else:
        print ("Downloading {} version {}".format(file_name, version))
        Path(models_root_dir).mkdir(parents=True, exist_ok=True)

        file_url = os.path.join("https://huggingface.co", model_name, "resolve", version, file_name)
        download_and_extract(file_url, model_file)

    return models_root_dir


def download_and_extract(file_url, output_file_path):
    
    #
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=file_url.split('/')[-1]) as t:
        urllib.request.urlretrieve(file_url, filename=output_file_path, reporthook=t.update_to)

    # extract.
    if output_file_path.endswith(".tar.gz"):
        print ("Extracting...")
        model_dir = Path(output_file_path).parent.absolute()
        tar = tarfile.open(output_file_path, "r:gz")
        tar.extractall(model_dir)
        tar.close()

    #Path(output_file_path).unlink()
