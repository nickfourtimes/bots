import json
import math
import random
import tracery
from tracery.modifiers import base_english

# get config vars
with open("lytton/config.json") as jfile:
    data = json.load(jfile)
    CRISIS_PROB = data["CRISIS_PROB"]


def lowercase(text):
    return text.toLowerCase()


def uppercase(text):
    return text.toUpperCase()


def get_text(cityParams):
    # any and all JSON files we're using
    sourceFiles = [
        "./lytton/words/tracery-data.json",
        "./lytton/words/clothes.json",
        "./lytton/words/containers.json",
        "./lytton/words/crimes.json",
        "./lytton/words/emoji.json",
        "./lytton/words/food.json",
        "./lytton/words/names.json",
        "./lytton/words/nouns.json",
        "./lytton/words/numbers.json",
        "./lytton/words/occupations.json",
        "./lytton/words/weather.json",
    ]

    # import all the source files
    all_json = {}
    for f in sourceFiles:
        with open(f, encoding="utf-8") as json_file:
            all_json = {**all_json, **json.load(json_file)}

    # import our grammar and add some (base & custom) modifiers
    grammar = tracery.Grammar(all_json)
    grammar.add_modifiers(base_english)
    grammar.add_modifiers({"lowercase": lowercase, "uppercase": uppercase})

    starter = ""

    if random.random() < CRISIS_PROB:
        starter = "#crisis#"

    elif "highway" in cityParams:
        # check if the highway leads out of the city
        if "tr" in cityParams["highway"]:
            starter = "#highway-tr#"
        elif "bl" in cityParams["highway"]:
            starter = "#highway-bl#"
        else:
            starter = "#highway#"

    else:
        if "cityLimit" in cityParams:
            if "tl" in cityParams["cityLimit"]:  # parkway drive & palm
                starter = "#cityLimit-tl#"
            elif "t" in cityParams["cityLimit"]:  # Xth & palm
                starter = "#cityLimit-t#"
            elif "l" in cityParams["cityLimit"]:  # parkway drive & FLOWER
                starter = "#cityLimit-l#"
            elif "r" in cityParams["cityLimit"]:  # clear water drive & FLOWER
                starter = "#cityLimit-r#"
            elif "b" in cityParams["cityLimit"]:  # Xth & river road
                starter = "#cityLimit-b#"
        else:
            # we may have more than one special (L or R or both), so comment on a random one
            if "special" in cityParams:
                starter = f"#{random.choice(cityParams["special"])}#"
            else:
                # if we get here, it's a very standard city block
                starter = "#standardGrid#"

    return grammar.flatten(starter)
