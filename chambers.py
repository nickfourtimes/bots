import os
import requests
import sys

from atproto import Client
from dotenv import load_dotenv
from mastodon import Mastodon

# get vars
load_dotenv()

# Bluesky credentials
BLUESKY_USERNAME = os.getenv("CHAMBERS_BSKY_HANDLE")
BLUESKY_APP_PASSWORD = os.getenv("CHAMBERS_BSKY_PASSWORD")
BLUESKY_BASE_URL = os.getenv("https://bsky.social")

# Mastodon credentials
MASTO_ACCESS_TOKEN = os.getenv("CHAMBERS_MASTO_ACCESS_TOKEN")
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
        article = "A"
        first = answer[0]
        if first == "a" or first == "e" or first == "i" or first == "o" or first == "u":
            article = "An"

        # *** THIS IS THE POST TEXT ***
        post_text = f"{article} {answer} is NOT podracing."
        print(f"Post text: {post_text}")
        return post_text


# poast!
post = get_post()

try:
    bsky = Client(BLUESKY_BASE_URL)
    bsky.login(BLUESKY_USERNAME, BLUESKY_APP_PASSWORD)
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
