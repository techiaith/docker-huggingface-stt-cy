import os
import datasets

from pathlib import Path

_DESCRIPTION = """\
YouTubeDataset is a dataset built internally at Bangor University but
which can be built by anyone using the scripts at :

inference/python/build-youtube_playlists_corpus.sh

that downloads all videos from selected playlists, extracts 
audio and segments into short clips containing speech.
"""

from dataset_url import URL
_DL_URL = URL


class YouTubeDatasetConfig(datasets.BuilderConfig):

    def __init__(self, name,  **kwargs):
        description = f"Dataset of clippings from YouTube"
        super(YouTubeDatasetConfig, self).__init__(
            name=name, version=datasets.Version("1.0",""), 
            description=description,
            **kwargs
        )


class YouTubeDataset(datasets.GeneratorBasedBuilder):
    
    def _info(self):

        features=datasets.Features(
            {
                "audio": datasets.Audio(sampling_rate=16_000),                    
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None
        )

    def _split_generators(self, dl_manager):
        dl_path=dl_manager.download_and_extract(_DL_URL)
                
        abs_path_to_data = os.path.join(dl_path)
        abs_path_to_clips = os.path.join(abs_path_to_data, "clips")

        generated_splits=[
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(abs_path_to_data, "clips.tsv"),
                    "path_to_clips": abs_path_to_clips,
                },
            ),
        ]
        return generated_splits


    def _generate_examples(self, filepath, path_to_clips):

        with open(filepath, encoding='utf-8') as f:
            lines = f.readlines()
            header_line = lines[0]
            
            for id_, line in enumerate(lines[1:]):
                field_values = line.strip().split("\t")
                audio_file_path=os.path.join(path_to_clips, field_values[0])
                with open(audio_file_path ,'rb') as audio_file:
                    audio = {"path": audio_file_path, "bytes":audio_file.read()}
                    yield id_, { "audio": audio }
