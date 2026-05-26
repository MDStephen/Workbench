// bolt-app.js — Slack Bolt app, Socket Mode, listens for @mentions

const { App } = require("@slack/bolt");
const fs = require("fs");
const TOKEN = require("fs").readFileSync("keys.env", "utf-8")
  .match(/^SLACK_BOT_TOKEN\s*=\s*(.+)$/m)?.[1].trim();

if (!TOKEN) {
  console.error("SLACK_BOT_TOKEN not found in keys.env");
  process.exit(1);
}

function getEnv(key) {
  const val = fs.readFileSync("keys.env", "utf-8")
    .match(new RegExp(`^${key}\\s*=\\s*(.+)$`, "m"))?.[1].trim();
  if (!val) { console.error(`${key} not found in keys.env`); process.exit(1); }
  return val;
}

const app = new App({
  token: getEnv("SLACK_BOT_TOKEN"),
  appToken: getEnv("SLACK_APP_TOKEN"),
  socketMode: true,
});

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

app.event("app_mention", async ({ event, say }) => {
  console.log(`Mention from ${event.user}: ${event.text}`);
  await say(`<@${event.user}>Received : ${event.text}`);
});

app.command("/localserver", async ({ command, ack, say }) => {
  await ack(); // must ack within 3 seconds or Slack shows an error
  console.log(`Command from ${command.user_name}: ${command.text}`);
  const info = `${new Date().toISOString()} | ${require("os").hostname()} | ${process.platform}`;
  await say(`<@${command.user_id}>${info}${command.text}`);
});

app.command("/test", async ({ command, ack, client }) => {
  await ack();

  await client.views.open({
    trigger_id: command.trigger_id,
    view: {
      type: "modal",
      callback_id: "my_modal",
      title: { type: "plain_text", text: "My Modal" },
      submit: { type: "plain_text", text: "Submit" },
      close: { type: "plain_text", text: "Cancel" },
      blocks: [
        {
          type: "input",
          block_id: "input_block",
          label: { type: "plain_text", text: "Enter something" },
          element: {
            type: "plain_text_input",
            action_id: "input_value",
          },
        },
      ],
    },
  });
});

app.view("my_modal", async ({ view, ack, body }) => {
  await ack();
  const value = view.state.values.input_block.input_value.value;
  console.log(`Modal submitted by ${body.user.id}: ${value}`);
  sendMessage(`Modal input successfully received: <${value}>`);
});

(async () => {
  await app.start();
  console.log("Bolt app running — listening for mentions");
})();