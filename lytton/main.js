// ************************************************************************* CHOOSE CITY PARAMETERS

const HIGHWAY_PROB = 0.3;
const CITY_LIMIT_PROB = 0.25;
const SPECIAL_PROB = 0.15;

/** randomly select how the city is going to be built */
function chooseCityParams() {
  var args = {};

  // highways are just built different
  if (Math.random() < HIGHWAY_PROB) {
    // 25% chance, each, of top-right or bottom-left; 50% chance of straight through
    var opt = ["tr", "bl", "nil", "nil"];
    args.highway = opt[Math.floor(Math.random() * opt.length)];
  } else {
    // not a highway...

    // ...but we could be on the outskirts of town
    if (Math.random() < CITY_LIMIT_PROB) {
      // randomly choose a city limit
      var opt = ["tl", "t", "l", "r", "b"];
      var choice = opt[Math.floor(Math.random() * opt.length)];
      args.cityLimit = choice;
    }

    // maybe there are special buildings!
    if (Math.random() < SPECIAL_PROB) {
      // we're doing a special block or two!
      var specialR = ["bertsPark", "jail"];
      var specialL = [
        "blueRoom",
        "caffeineWino",
        "commBldg",
        "cottonCove",
        "courthouse",
        "hotel",
        "lyttonPark",
        "police",
      ];

      // we'll either have a special left, or right, or both
      var allSpecial = [];
      var rnd = Math.random();
      if (rnd > 0.667) {
        allSpecial.push(specialL[Math.floor(Math.random() * specialL.length)]);
      } else if (rnd > 0.333) {
        allSpecial.push(specialR[Math.floor(Math.random() * specialR.length)]);
      } else {
        allSpecial.push(specialR[Math.floor(Math.random() * specialR.length)]);
        allSpecial.push(specialL[Math.floor(Math.random() * specialL.length)]);
      }

      args.special = allSpecial;
    } // special buildings
  } // no highways

  return args;
}

// ************************************************************************* WEB APP

const express = require("express");
const app = express();
app.use(express.static("public"));

const map = require("./maps/map-gen.js");
const masto = require("./masto.js");
const tracery = require("./words/tracery-gen.js");

// respond to endpoint -- generate a city & make a post
// todo maybe actually schedule this instead of using an endpoint
app.get("/" + process.env.BOT_ENDPOINT, (req, res) => {
  // generate the map & get it
  const cityParams = chooseCityParams();

  map(cityParams, res, function (err, image) {
    if (err) {
      console.error("could not render map: " + err);
    } else {
      const articleText = tracery.getText(cityParams);
      masto.post_image(articleText, image.path, function (err, data) {
        if (err) {
          console.error("could not post image: ", err);
        } else {
          // console.log("posted.");
          console.log(data.url);
        }
      });
    }
  });

  res.sendStatus(200);
});

// // test: uncomment to just test the map-generation algorithm
// app.get("/maps", (req, res) => {
//   // generate the map & get it
//   const cityParams = chooseCityParams();

//   map(cityParams, res, function (err, image) {
//     if (err) {
//       console.error("could not render map: " + err);
//     } else {
//       res.type("png");
//       res.send(image.data);
//     }
//   });
// });

// // test: uncomment to just test the text-generation algorithm
// app.get("/text", (req, res) => {
//   const cityParams = chooseCityParams();
//   const txt = tracery.getText(cityParams);
//   res.send(txt);
// });

// start the server and listen for requests :)
var listener = app.listen(process.env.PORT, function () {
  console.log("Your bot is running on port " + listener.address().port);
});
