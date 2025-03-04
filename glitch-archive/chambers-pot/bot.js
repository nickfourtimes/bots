const express = require("express");
const request = require("request");
const Mastodon = require("mastodon");

const fs = require("fs");
const nouns = JSON.parse(fs.readFileSync("./data/chambers-nouns.json"));
const adjs = JSON.parse(fs.readFileSync("./data/chambers-adjectives.json"));

// ************************************************************************* CONFIG

const config = {
	masto: {
		access_token: process.env.MASTO_ACCESS_TOKEN,
		api_url: "https://botsin.space/api/v1/",
		client_key: process.env.MASTO_CLIENT_KEY,
		client_secret: process.env.MASTO_CLIENT_SECRET,
		timeout_ms: 60 * 1000,
	},
};

const app = express();
const M = new Mastodon(config.masto);

// ************************************************************************* METHODS

function toTitleCase(str) {
	return str.replace(/\w\S*/g, function (txt) {
		return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
	});
}

function getPreamble() {
	var options = ["*cracks knuckles*", "hm.", "how about...", "could it be..."];

	return options[Math.floor(Math.random() * options.length)];
}

function getTitle() {
	var n1 = nouns["nouns"][Math.floor(Math.random() * nouns["nouns"].length)];
	var n2 = nouns["nouns"][Math.floor(Math.random() * nouns["nouns"].length)];
	var a1 = adjs["adjs"][Math.floor(Math.random() * adjs["adjs"].length)];

	// caps
	n1 = toTitleCase(n1);
	n2 = toTitleCase(n2);
	a1 = toTitleCase(a1);

	// get the correct article
	var article = "A";
	var first = n1.substr(0, 1);
	if (
		first === "a" ||
		first === "A" ||
		first === "e" ||
		first === "E" ||
		first === "i" ||
		first === "I" ||
		first === "o" ||
		first === "O" ||
		first === "u" ||
		first === "U"
	) {
		article = "An";
	}

	return `${article} ${n1} for the ${n2}-${a1}`;
}

function getPostamble() {
	var options = ["*crumples paper*", "*sips coffee*", "sigh."];

	return options[Math.floor(Math.random() * options.length)];
}

function composePost() {
	var post = "";

	var v = Math.random();

	// random chance of preamble
	if (v < 0.33333 || v > 0.66667) post = post.concat(`${getPreamble()}\n\n`);

	// the actual name of the book
	post = post.concat(`"${getTitle()}"`);

	// random chance of postamble
	if (v > 0.33333) post = post.concat(`\n\n${getPostamble()}`);

	// console.log(post);

	return post;
}

function doPost(res) {
	var text = composePost();

	// *** MASTODON ***
	M.post("statuses", { status: text }).then((resp) => {
		if (resp.data.id > 0) {
			console.log("good: " + resp.data.id);
		} else {
			console.error("error: " + resp.data);
		}
	});
}

// ************************************************************************* WEB APP

app.use(express.static("public"));

app.all("/" + process.env.BOT_ENDPOINT, (req, res) => {
	doPost(res);
	res.sendStatus(200);
});

var listener = app.listen(process.env.PORT, function () {
	console.log("Your bot is running on port " + listener.address().port);
});
