import json
import requests

from external_api_urls import PUNCTUATION_API_URL

def restore_punctuation_and_truecase(raw_text):

    try:
        params = {'text': raw_text }
        response = requests.get(PUNCTUATION_API_URL, params=params, timeout=360)
        result = response.json()
        return result['restored_text']
    except:
        print("Restore punctuation API exception")
        return raw_text

