var fs = require("fs"),
	Mastodon = require("mastodon"),
	M;

try {
	M = new Mastodon({
		access_token: process.env.MASTO_ACCESS_TOKEN,
		api_url: process.env.MASTO_API || "https://mastodon.social/api/v1/",
		client_key: process.env.MASTO_CLIENT_KEY,
		client_secret: process.env.MASTO_CLIENT_SECRET,
	});
} catch (err) {
	console.error(err);
	console.error("please update your .env file with your Mastodon access token");
}

module.exports = {
	M: M,
	toot: function (status, cb) {
		if (!M) {
			console.error("please update your .env file");
			return false;
		}
		if (status.length > 500) {
			console.error(`status too long: ${status}`);
			return false;
		}

		console.log("posting...");
		M.post("statuses", { status: status, visibility: 'public' }, function (err, data, response) {
			console.log(`posted status: ${status}`);
			if (cb) {
				cb(err, data);
			}
		});
	},
	post_image: function (text, img_file, cb) {
		M.post(
			"media",
			{
				file: fs.createReadStream(img_file),
				description: "a randomly-generated map of Lytton, CA"
			},
			function (err, data, response) {
				if (err) {
					console.log("ERROR:\n", err);
					if (cb) {
						cb(err, data);
					}
				} else {
					// console.log(data);
					// console.log("posting image...");
					M.post(
						"statuses",
						{
							status: text,
							media_ids: new Array(data.id),
						},
						function (err, data, response) {
							if (err) {
								console.log("ERROR:\n", err);
								if (cb) {
									cb(err, data);
								}
							} else {
								if (cb) {
									cb(null, data);
								}
							}
						}
					);
				}
			}
		);
	},
};
