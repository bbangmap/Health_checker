const moment = require("moment");
const path = require("path");
const { IncomingWebhook } = require("@slack/webhook");

const webhookURL = process.env.SLACK_WEBHOOK;

function post(message) {
  hook(message);
}

async function hook(message) {
  const webhook = new IncomingWebhook(webhookURL, {});
  await webhook.send({
    text: message,
    attachments: [],
  });
}


module.exports = {
  post: post,
};