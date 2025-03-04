const { AtpAgent, RichText } = require("@atproto/api");

async function sendPost(text) {
	const agent = new AtpAgent({ service: "https://bsky.social" });
	await agent.login({
		identifier: "${{ env.PODRACING_IDENTIFIER }}",
		password: "${{ secrets.PODRACING_PASSWORD }}",
	});
	const richText = new RichText({ text });
	await richText.detectFacets(agent);
	await agent.post({
		text: richText.text,
		facets: richText.facets,
	});
}

sendPost("Hello from the Bluesky API!");
