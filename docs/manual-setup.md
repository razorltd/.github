# Manual setup required

The following manual setup steps must be completed to enable Slack notifications. We use the **Slack Bot Token** method which allows a single Slack App token to post to any channel dynamically.

---

## Slack Bot Token Setup

### 1. Create Slack App & Token
1. Go to the [Slack App Directory](https://api.slack.com/apps) and click **Create New App** -> **From scratch**.
2. Under **OAuth & Permissions**, scroll down to **Scopes** -> **Bot Token Scopes** and add:
   - `chat:write`
   - `files:write` (Required for uploading detailed job summaries as attachments)
   - `channels:read` (Optional, required to resolve public channel names like `#channel-name` to IDs)
   - `groups:read` (Optional, required to resolve private channel names to IDs)
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

## State Store Repository (.status) Setup

To store workflow run statuses automatically, the workflow pushes JSON status files to a dedicated, private repository named `.status`.

### 1. Create Private Repository
Create a private repository in your organization called `.status` (e.g., `razorltd/.status`). Initialize it with at least one file (e.g., a default `README.md` or `.gitignore` file) so that the default branch (e.g., `main` or `master`) exists.

### 2. Generate GitHub Access Token
Generate a GitHub Access Token with write permissions to the `.status` repository:

1. Go to **Organization Settings** -> **Developer settings** -> **GitHub Apps** -> **New GitHub App**.
2. Give it a name (e.g. `RZR Status Store`).
3. Set **Homepage URL** to any URL (e.g., your `.github` repository URL).
4. Uncheck **Active** under **Webhook** (webhook is not needed).
5. In **Permissions** -> **Repository permissions** -> **Contents**: Select `Access: Read & write`.
6. Click **Create GitHub App**.
7. In the app settings page, copy the **App ID**.
8. Scroll down and click **Generate a private key**. Download the `.pem` private key file.
9. Click **Install App** in the left menu, install it on your organization, and select access only to the `.status` repository.


### 3. GitHub Organisation Settings
* Create an organization **variable** named `STATUS_APP_ID` with the App ID as the value.
* Create an organization **secret** named `STATUS_APP_PRIVATE_KEY` with the entire contents of the `.pem` private key file.

These credentials will be passed directly to the reusable workflow, which handles token generation internally.

---

## General Configurations

### 1. Consumer Repository Rollout
Update your workflow in each target repository to add the final `notify` job. Refer to `docs/consumer-example.md` for a configuration example.
