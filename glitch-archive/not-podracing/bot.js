const express = require("express");
const request = require("request");
const Mastodon = require("mastodon");
const Twitter = require("twit");

// ************************************************************************* CONFIG

const config = {
	masto: {
		access_token: process.env.MASTO_ACCESS_TOKEN,
		api_url: "https://botsin.space/api/v1/",
		client_key: process.env.MASTO_CLIENT_KEY,
		client_secret: process.env.MASTO_CLIENT_SECRET,
		timeout_ms: 60 * 1000,
	},

	// twitter: {
	//   consumer_key: process.env.TWITTER_CONSUMER_KEY,
	//   consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
	//   access_token: process.env.TWITTER_ACCESS_TOKEN,
	//   access_token_secret: process.env.TWITTER_ACCESS_TOKEN_SECRET,
	// },
};

const app = express();
const M = new Mastodon(config.masto);
// const T = new Twitter(config.twitter);

// ************************************************************************* METHODS

function doPost(res) {
	var wordnik_req =
		"http://api.wordnik.com:80/v4/words.json/randomWord?" +
		"hasDictionaryDef=false" +
		"&includePartOfSpeech=noun" +
		"&minCorpusCount=5000" +
		"&maxCorpusCount=-1" +
		"&minDictionaryCount=1" +
		"&maxDictionaryCount=-1" +
		"&minLength=4" +
		"&maxLength=100" +
		"&api_key=" +
		process.env.WORDNIK_API_KEY;

	var answer = "?";
	request(wordnik_req, (error, response, body) => {
		if (error || response.statusCode !== 200 || body == "") {
			console.error("wordnik error: " + error);
			res.send("null");
		} else {
			answer = JSON.parse(body);

			// get the correct article
			var article = "A";
			var first = answer.word.substr(0, 1);
			if (
				first === "a" ||
				first === "e" ||
				first === "i" ||
				first === "o" ||
				first === "u"
			) {
				article = "An";
			}

			// *** THIS IS THE POST TEXT ***
			var post_text = article + " " + answer.word + " is NOT podracing.";

			// // *** TWITTER ***
			// T.post("statuses/update", { status: post_text }, (err, data, response) => {
			//     if (err) {
			//       console.error(err)
			//     }
			// });

			// *** MASTODON ***
			M.post("statuses", { status: post_text }, (err, data, response) => {
				if (error) {
					console.error(err);
				}
			});

			res.sendStatus(200);
		} // end of "else all is well with the response from Wordnik"
	});
}

// ************************************************************************* WEB APP

app.use(express.static("public"));

app.all("/" + process.env.BOT_ENDPOINT, (req, res) => {
	doPost(res);
});

var listener = app.listen(process.env.PORT, function () {
	console.log("Your bot is running on port " + listener.address().port);
});
