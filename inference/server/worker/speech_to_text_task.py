from pathlib import Path
from celery import Celery, Task

from speech_to_text import SpeechToText


class SpeechToTextTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.model:
            print("Loading SpeechToText model") 
            self.model = SpeechToText()

        return self.run(*args, **kwargs)

