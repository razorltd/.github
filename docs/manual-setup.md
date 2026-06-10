# Manual setup required

The following manual setup steps must be completed to enable Slack notifications. We use the **Slack Bot Token** method which allows a single Slack App token to post to any channel dynamically.

---

## Slack Bot Token Setup

### 1. Create Slack App & Token
1. Go to the [Slack App Directory](https://api.slack.com/apps) and click **Create New App** -> **From scratch**.
2. Under **OAuth & Permissions**, scroll down to **Scopes** -> **Bot Token Scopes** and add:
   - `chat.postMessage`
   - `files:write` (Required for uploading detailed job summaries as attachments)
3. Click **Install to Workspace** at the top of the page.
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`).

### 2. GitHub Organisation Secret
Create a GitHub Actions organisation secret:
* **Name**: `SLACK_BOT_TOKEN`
* **Value**: The `xoxb-` token.
* **Access policy**: `Selected repositories` or `All repositories`.

### 3. Invite Bot to Channels
For each channel the bot should post to:
- Invite the bot to the channel using `/invite @YourBotName` (required for private channels, recommended for public channels). If the bot is not in the channel, the Slack API will return `not_in_channel` and the GitHub Action will fail, alerting you to the setup issue.

---

## General Configurations

### 1. Slack Mention Target
If failures should mention a Slack User Group, locate the Group ID in Slack and format it like:
`<!subteam^GROUP_ID>`

### 2. Consumer Repository Rollout
Update your workflow in each target repository to add the final `notify` job. Refer to `docs/consumer-example.md` for a configuration example.
