import os
import requests
import sys

from atproto import Client
from dotenv import load_dotenv
from mastodon import Mastodon

# get vars
load_dotenv()

# Bluesky credentials
BSKY_USERNAME = os.getenv("LYTTON_BSKY_HANDLE")
BSKY_APP_PASSWORD = os.getenv("LYTTON_BSKY_PASSWORD")
BSKY_BASE_URL = os.getenv("BSKY_BASE_URL")

# Mastodon credentials
MASTO_ACCESS_TOKEN = os.getenv("LYTTON_MASTO_ACCESS_TOKEN")
MASTO_BASE_URL = os.getenv("MASTO_BASE_URL")


# poast!
post = "foo"

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
