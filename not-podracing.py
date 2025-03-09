import os

from dotenv import load_dotenv
from mastodon import Mastodon

load_dotenv()

ACCESS_TOKEN = os.getenv("PODRACING_MASTO_ACCESS_TOKEN")
CLIENT_KEY = os.getenv("PODRACING_MASTO_CLIENT_KEY")
CLIENT_SECRET = os.getenv("PODRACING_MASTO_CLIENT_SECRET")

masto = Mastodon(access_token=ACCESS_TOKEN, api_base_url="http://mastodon.social")

print(masto.toot("here goes nothing"))


# ************************************************************************* METHODS

# function doPost(res) {
# 	var wordnik_req =
# 		"http://api.wordnik.com:80/v4/words.json/randomWord?" +
# 		"hasDictionaryDef=false" +
# 		"&includePartOfSpeech=noun" +
# 		"&minCorpusCount=5000" +
# 		"&maxCorpusCount=-1" +
# 		"&minDictionaryCount=1" +
# 		"&maxDictionaryCount=-1" +
# 		"&minLength=4" +
# 		"&maxLength=100" +
# 		"&api_key=" +
# 		process.env.WORDNIK_API_KEY;

# 	var answer = "?";
# 	request(wordnik_req, (error, response, body) => {
# 		if (error || response.statusCode !== 200 || body == "") {
# 			console.error("wordnik error: " + error);
# 			res.send("null");
# 		} else {
# 			answer = JSON.parse(body);

# 			// get the correct article
# 			var article = "A";
# 			var first = answer.word.substr(0, 1);
# 			if (
# 				first === "a" ||
# 				first === "e" ||
# 				first === "i" ||
# 				first === "o" ||
# 				first === "u"
# 			) {
# 				article = "An";
# 			}

# 			// *** THIS IS THE POST TEXT ***
# 			var post_text = article + " " + answer.word + " is NOT podracing.";

# 			// *** MASTODON ***
# 			M.post("statuses", { status: post_text }, (err, data, response) => {
# 				if (error) {
# 					console.error(err);
# 				}
# 			});

# 			res.sendStatus(200);
# 		} // end of "else all is well with the response from Wordnik"
# 	});
# }
