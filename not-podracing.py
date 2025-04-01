import os
import requests
import sys

from atproto import Client
from dotenv import load_dotenv
from mastodon import Mastodon

# get vars
load_dotenv()

# Bluesky credentials
BSKY_USERNAME = os.getenv("PODRACING_BSKY_HANDLE")
BSKY_APP_PASSWORD = os.getenv("PODRACING_BSKY_PASSWORD")
BSKY_BASE_URL = os.getenv("BSKY_BASE_URL")

# Mastodon credentials
MASTO_ACCESS_TOKEN = os.getenv("PODRACING_MASTO_ACCESS_TOKEN")
MASTO_BASE_URL = os.getenv("MASTO_BASE_URL")


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
        vowels = ["a", "A", "e", "E", "i", "I", "o", "O", "u", "U"]
        if answer[0] in vowels:
            article = "An"
        else:
            article = "A"

        # *** THIS IS THE POST TEXT ***
        post_text = f"{article} {answer} is NOT podracing."
        return post_text


# poast!
post = get_post()
# print(post)

try:
    bsky = Client(BSKY_BASE_URL)
    bsky.login(BSKY_USERNAME, BSKY_APP_PASSWORD)
    bsky.send_post(post)
    print("Posted to Bluesky.")
except SystemError as e:
    print(f"Error posting to Bluesky: {e}")

try:
    masto = Mastodon(access_token=MASTO_ACCESS_TOKEN, api_base_url=MASTO_BASE_URL)
    masto.status_post(post)
    print("Posted to Mastodon.")
except SystemError as e:
    print(f"Error posting to Mastodon: {e}")
