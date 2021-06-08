import os
import tarfile
import urllib.request
from urllib.parse import urlparse

from pathlib import Path
from tqdm import tqdm


DATA_URL = "http://techiaith.cymru/wav2vec2"
MODEL_VERSION=os.environ["MODEL_VERSION"]


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)
        

def download(model_name, version=MODEL_VERSION):
    # expecting model name as techiaith_bangor/kenlm-cy
    # expecting model name as techiaith_bangor/wav2vec2-xlsr-ft-cy
    model_dir = os.path.join("/","models", "server", model_name, version)
    if Path(model_dir).is_dir():
        print ("Model {} already downloaded.")
    else:
        print ("Downloading {} version {}".format(model_name, version))
        Path(model_dir).mkdir(parents=True, exist_ok=True)

        filename = model_name.replace("/","_") + "." + version + ".tar.gz"
        file_url = os.path.join(DATA_URL, filename)

        download_and_extract(file_url, model_dir)

    return model_dir


def download_and_extract(file_url, model_dir):
    
    #
    file_name = os.path.basename(urlparse(file_url).path)
    output_file_path = os.path.join(model_dir, file_name)
    
    #
    print (file_url)
    print (file_name)
    print (output_file_path)
    
    #
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=file_url.split('/')[-1]) as t:
        urllib.request.urlretrieve(file_url, filename=output_file_path, reporthook=t.update_to)

    # extract.
    print ("Extracting...")
    tar = tarfile.open(output_file_path, "r:gz")
    tar.extractall(model_dir)
    tar.close()

    Path(output_file_path).unlink()

