#!/usr/bin/env node
// smoke-test-auth.js — Slack auth.test smoke test

const TOKEN = require("fs").readFileSync("keys.env","utf-8")
  .match(/^SLACK_BOT_TOKEN\s*=\s*(.+)$/m)?.[1].trim();

if (!TOKEN) {
  console.error("SLACK_BOT_TOKEN not set — add it to keys.env or export it");
  process.exit(1);
}

async function smokeTest() {
  console.log("🔍 Calling auth.test...");

  const res = await fetch("https://slack.com/api/auth.test", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    console.error(`HTTP error: ${res.status} ${res.statusText}`);
    process.exit(1);
  }

  const data = await res.json();

  if (!data.ok) {
    console.error(`Slack error: ${data.error}`);
    process.exit(1);
  }

  console.log("Token is valid");
  console.log(`   User:  ${data.user} (${data.user_id})`);
  console.log(`   Team:  ${data.team} (${data.team_id})`);
  console.log(`   Bot ID: ${data.bot_id ?? "n/a"}`);
  console.log(`   URL:   ${data.url}`);
}

smokeTest().catch((err) => {
  console.error("Unexpected error:", err.message);
  process.exit(1);
});