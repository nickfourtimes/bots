const tracery = require("tracery-grammar");
const fs = require("fs");
const CRISIS_PROBABILITY = 0.05;

// some custom modifier functions using JS string manip
function lowercase(text) {
  return text.toLowerCase();
}
function uppercase(text) {
  return text.toUpperCase();
}

module.exports = {
  getText: function (cityParams) {
    // any and all JSON files we're using
    const sourceFiles = [
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
      "./words/weather.json"
    ];

    // import all the source files
    var allJson = [];
    for (const f of sourceFiles) {
      var j = JSON.parse(fs.readFileSync(f, "utf8"));
      allJson = { ...allJson, ...j };
    }

    // import our grammar and add some (base & custom) modifiers
    var grammar = tracery.createGrammar(allJson);
    grammar.addModifiers(tracery.baseEngModifiers);
    grammar.addModifiers({
      "lowercase": lowercase,
      "uppercase": uppercase
    });

    var starter = "";

    if (Math.random() < CRISIS_PROBABILITY) {
      starter = "#crisis#";

    } else if ("highway" in cityParams) {
      // check if the highway leads out of the city
      if (cityParams.highway.includes("tr")) {
        starter = "#highway-tr#";
      } else if (cityParams.highway.includes("bl")) {
        starter = "#highway-bl#";
      } else {
        starter = "#highway#";
      }

    } else {
      if ("cityLimit" in cityParams) {
        if (cityParams.cityLimit.includes("tl")) {
          // parkway drive & palm
          starter = "#cityLimit-tl#";
        } else if (cityParams.cityLimit.includes("t")) {
          // Xth & palm
          starter = "#cityLimit-t#";
        } else if (cityParams.cityLimit.includes("l")) {
          // parkway drive & FLOWER
          starter = "#cityLimit-l#";
        } else if (cityParams.cityLimit.includes("r")) {
          // clear water drive & FLOWER
          starter = "#cityLimit-r#";
        } else if (cityParams.cityLimit.includes("b")) {
          // Xth & river road
          starter = "#cityLimit-b#";
        }
      } else {
        // we may have more than one special (L or R or both), so comment on a random one
        if ("special" in cityParams) {
          starter = "#" + cityParams.special[Math.floor(Math.random() * cityParams.special.length)] + "#";
        } else {
          // if we get here, it's a very standard city block
          starter = "#standardGrid#";
        }
      }
    }

    return grammar.flatten(starter);
    // return grammar.flatten("#police#");
  }
};
