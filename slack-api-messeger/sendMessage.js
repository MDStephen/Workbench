#!/usr/bin/env node
// send-message.js — Post a message to #bench

const TOKEN = require("fs").readFileSync("keys.env", "utf-8")
  .match(/^SLACK_BOT_TOKEN\s*=\s*(.+)$/m)?.[1].trim();

if (!TOKEN) {
  console.error("SLACK_BOT_TOKEN not found in keys.env");
  process.exit(1);
}

async function sendMessage(text) {
  const res = await fetch("https://slack.com/api/chat.postMessage", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      channel: "C0ASC2ML3CN",
      text,
    }),
  });

  const data = await res.json();

  if (!data.ok) {
    console.error(`Slack error: ${data.error}`);
    process.exit(1);
  }

  console.log(`Message sent — ts: ${data.ts}`);
}

const info = `${new Date().toISOString()} | ${require("os").hostname()} | ${process.platform}`;

sendMessage(info);