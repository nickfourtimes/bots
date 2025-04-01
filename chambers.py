import json
import os
import random
import string

from atproto import Client
from dotenv import load_dotenv
from mastodon import Mastodon

# get vars
load_dotenv()

# Bluesky credentials
BSKY_USERNAME = os.getenv("CHAMBERS_BSKY_HANDLE")
BSKY_APP_PASSWORD = os.getenv("CHAMBERS_BSKY_PASSWORD")
BSKY_BASE_URL = os.getenv("BSKY_BASE_URL")

# Mastodon credentials
MASTO_ACCESS_TOKEN = os.getenv("CHAMBERS_MASTO_ACCESS_TOKEN")
MASTO_BASE_URL = os.getenv("MASTO_BASE_URL")

# get our words
with open("chambers/chambers-nouns.json", "r") as noun_file:
    noun_list = json.load(noun_file)
with open("chambers/chambers-adjectives.json", "r") as adj_file:
    adj_list = json.load(adj_file)


def get_preamble():
    options = ["*cracks knuckles*", "hm.", "how about...", "could it be..."]
    return random.choice(options)


def get_title():
    n1 = random.choice(noun_list["nouns"])
    n2 = random.choice(noun_list["nouns"])
    a1 = random.choice(adj_list["adjs"])

    # caps
    n1 = string.capwords(n1)
    n2 = string.capwords(n2)
    a1 = string.capwords(a1)

    # get the correct article
    article = "A"
    vowels = ["A", "a", "E", "e", "I", "i", "O", "o", "U", "u"]
    first = n1[0]
    if any(vowel in first for vowel in vowels):
        article = "An"

    return f"{article} {n1} for the {n2}-{a1}"


def get_postamble():
    options = ["*crumples paper*", "*sips coffee*", "sigh."]
    return random.choice(options)


def compose_post():
    post = ""

    v = random.random()

    # random chance of preamble
    if v < 0.33333 or v > 0.66667:
        post += f"{get_preamble()}\n\n"

    # the actual name of the book
    post += f'"{get_title()}"'

    # random chance of postamble
    if v > 0.33333:
        post += f"\n\n{get_postamble()}"

    # console.log(post)

    return post


# poast!
post = compose_post()
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
