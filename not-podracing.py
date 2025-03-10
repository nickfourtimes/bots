import os
import requests
import sys

from dotenv import load_dotenv
from mastodon import Mastodon

# get vars
load_dotenv()
ACCESS_TOKEN = os.getenv("PODRACING_MASTO_ACCESS_TOKEN")
BASE_URL = os.getenv("MASTO_BASE_URL")


def get_post():
    wordnik_req = (
        "http://api.wordnik.com:80/v4/words.json/randomWord?"
        + "hasDictionaryDef=false"
        + "&includePartOfSpeech=noun"
        + "&minCorpusCount=5000"
        + "&maxCorpusCount=-1"
        + "&minDictionaryCount=1"
        + "&maxDictionaryCount=-1"
        + "&minLength=4"
        + "&maxLength=100"
        + "&api_key="
        + os.getenv("WORDNIK_API_KEY")
    )

    response = requests.get(wordnik_req)

    try:
        response = requests.get(wordnik_req)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

	# todo better error handling
    if response.status_code != 200 or response.json == "":
        print(f"wordnik error: {response.raise_for_status()}", file=sys.stderr)
    else:
        answer = response.json()["word"]

        # get the correct article
        article = "A"
        first = answer[0]
        if first == "a" or first == "e" or first == "i" or first == "o" or first == "u":
            article = "An"

        # *** THIS IS THE POST TEXT ***
        post_text = f"{article} {answer} is NOT podracing."
        print(f"Post text: {post_text}")
        return post_text


# poast!
masto = Mastodon(access_token=ACCESS_TOKEN, api_base_url=BASE_URL)
masto.status_post(get_post())
