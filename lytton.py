import os
import json
import math
import random

from atproto import Client
from dotenv import load_dotenv
from mastodon import Mastodon

from lytton.words.lytton_tracery import get_text

# get env vars
load_dotenv()

# Bluesky credentials
BSKY_USERNAME = os.getenv("LYTTON_BSKY_HANDLE")
BSKY_APP_PASSWORD = os.getenv("LYTTON_BSKY_PASSWORD")
BSKY_BASE_URL = os.getenv("BSKY_BASE_URL")

# Mastodon credentials
MASTO_ACCESS_TOKEN = os.getenv("LYTTON_MASTO_ACCESS_TOKEN")
MASTO_BASE_URL = os.getenv("MASTO_BASE_URL")

# get config vars
with open("./lytton/config.json") as jfile:
    data = json.load(jfile)
    CITY_LIMIT_PROB = data["CITY_LIMIT_PROB"]
    HIGHWAY_PROB = data["HIGHWAY_PROB"]
    SPECIAL_PROB = data["SPECIAL_PROB"]


# randomly select how the city is going to be built
def chooseCityParams():
    args = {}

    # highways are just built different
    if random.random() < HIGHWAY_PROB:
        # 25% chance, each, of top-right or bottom-left 50% chance of straight through
        opt = ["tr", "bl", "nil", "nil"]
        args["highway"] = opt[math.floor(random.random() * len(opt))]

    else:  # not a highway...

        # ...but we could be on the outskirts of town
        if random.random() < CITY_LIMIT_PROB:
            # randomly choose a city limit
            opt = ["tl", "t", "l", "r", "b"]
            choice = opt[math.floor(random.random() * len(opt))]
            args["cityLimit"] = choice

        # maybe there are special buildings!
        if random.random() < SPECIAL_PROB:
            # we're doing a special block or two!
            specialR = ["bertsPark", "jail"]
            specialL = [
                "blueRoom",
                "caffeineWino",
                "commBldg",
                "cottonCove",
                "courthouse",
                "hotel",
                "lyttonPark",
                "police",
            ]

            # we'll either have a special left, or right, or both
            all_special = []
            rnd = random.random()
            if rnd > 0.667:
                all_special.append(specialL[math.floor(random.random() * specialL.length)])
            elif rnd > 0.333:
                all_special.append(specialR[math.floor(random.random() * specialR.length)])
            else:
                all_special.append(specialR[math.floor(random.random() * specialR.length)])
                all_special.append(specialL[math.floor(random.random() * specialL.length)])

            args["special"] = all_special

    return args


params = chooseCityParams()

# poast!
post = "foo"

print(get_text(params))

# try:
#     bsky = Client(BSKY_BASE_URL)
#     bsky.login(BSKY_USERNAME, BSKY_APP_PASSWORD)
#     bsky.send_post(post)
#     print("Posted to Bluesky.")
# except SystemError as e:
#     print(f"Error posting to Bluesky: {e}")

# try:
#     masto = Mastodon(access_token=MASTO_ACCESS_TOKEN, api_base_url=MASTO_BASE_URL)
#     masto.status_post(post)
#     print("Posted to Mastodon.")
# except SystemError as e:
#     print(f"Error posting to Mastodon: {e}")
