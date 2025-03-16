import json
import random
import tracery

# get config vars
with open("lytton/config.json") as jfile:
    j = json.loads(jfile)
    print(j)
    CRISIS_PROB = j["CRISIS_PROB"]


def lowercase(text):
    return text.toLowerCase()


def uppercase(text):
    return text.toUpperCase()


def get_text(cityParams):
    # any and all JSON files we're using
    sourceFiles = [
        "./words/tracery-data.json",
        "./words/clothes.json",
        "./words/containers.json",
        "./words/crimes.json",
        "./words/emoji.json",
        "./words/food.json",
        "./words/names.json",
        "./words/nouns.json",
        "./words/numbers.json",
        "./words/occupations.json",
        "./words/weather.json",
    ]

    # import all the source files
    allJson = []
    for f in sourceFiles:
        with open(f) as json_file:
            allJson.append(json.load(json_file))

    # import our grammar and add some (base & custom) modifiers
    grammar = tracery.createGrammar(allJson)
    grammar.addModifiers(tracery.baseEngModifiers)
    grammar.addModifiers({"lowercase": lowercase, "uppercase": uppercase})

    starter = ""

    if random.random() < CRISIS_PROB:
        starter = "#crisis#"

    elif "highway" in cityParams:
        # check if the highway leads out of the city
        if cityParams.highway.includes("tr"):
            starter = "#highway-tr#"
        elif cityParams.highway.includes("bl"):
            starter = "#highway-bl#"
        else:
            starter = "#highway#"

    else:
        if "cityLimit" in cityParams:
            if cityParams.cityLimit.includes("tl"):  # parkway drive & palm
                starter = "#cityLimit-tl#"
            elif cityParams.cityLimit.includes("t"):  # Xth & palm
                starter = "#cityLimit-t#"
            elif cityParams.cityLimit.includes("l"):  # parkway drive & FLOWER
                starter = "#cityLimit-l#"
            elif cityParams.cityLimit.includes("r"):  # clear water drive & FLOWER
                starter = "#cityLimit-r#"
            elif cityParams.cityLimit.includes("b"):  # Xth & river road
                starter = "#cityLimit-b#"
        else:
            # we may have more than one special (L or R or both), so comment on a random one
            if "special" in cityParams:
                starter = (
                    "#"
                    + cityParams.special[
                        Math.floor(random.random() * cityParams.special.length)
                    ]
                    + "#"
                )
            else:
                # if we get here, it's a very standard city block
                starter = "#standardGrid#"

    return grammar.flatten(starter)
