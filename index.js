const { AtpAgent, RichText } = require("@atproto/api");

async function sendPost(text) {
	const agent = new AtpAgent({ service: "https://bsky.social" });
	await agent.login({
		identifier: "YOUR_IDENTIFIER_HERE",
		password: "YOUR_PASSWORD_HERE",
	});
	const richText = new RichText({ text });
	await richText.detectFacets(agent);
	await agent.post({
		text: richText.text,
		facets: richText.facets,
	});
}

sendPost("Hello from the Bluesky API!");
