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

# todo: get config vars

# /** randomly select how the city is going to be built */
# function chooseCityParams() {
#   var args = {};

#   // highways are just built different
#   if (Math.random() < HIGHWAY_PROB) {
#     // 25% chance, each, of top-right or bottom-left; 50% chance of straight through
#     var opt = ["tr", "bl", "nil", "nil"];
#     args.highway = opt[Math.floor(Math.random() * opt.length)];
#   } else {
#     // not a highway...

#     // ...but we could be on the outskirts of town
#     if (Math.random() < CITY_LIMIT_PROB) {
#       // randomly choose a city limit
#       var opt = ["tl", "t", "l", "r", "b"];
#       var choice = opt[Math.floor(Math.random() * opt.length)];
#       args.cityLimit = choice;
#     }

#     // maybe there are special buildings!
#     if (Math.random() < SPECIAL_PROB) {
#       // we're doing a special block or two!
#       var specialR = ["bertsPark", "jail"];
#       var specialL = [
#         "blueRoom",
#         "caffeineWino",
#         "commBldg",
#         "cottonCove",
#         "courthouse",
#         "hotel",
#         "lyttonPark",
#         "police",
#       ];

#       // we'll either have a special left, or right, or both
#       var allSpecial = [];
#       var rnd = Math.random();
#       if (rnd > 0.667) {
#         allSpecial.push(specialL[Math.floor(Math.random() * specialL.length)]);
#       } else if (rnd > 0.333) {
#         allSpecial.push(specialR[Math.floor(Math.random() * specialR.length)]);
#       } else {
#         allSpecial.push(specialR[Math.floor(Math.random() * specialR.length)]);
#         allSpecial.push(specialL[Math.floor(Math.random() * specialL.length)]);
#       }

#       args.special = allSpecial;
#     } // special buildings
#   } // no highways

#   return args;
# }

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
