# Manual setup required

The following manual setup steps must be completed to enable Slack notifications.

### 1. Slack App and Webhook

The user must:
* Create or select a Slack app.
* Enable Incoming Webhooks.
* Add a webhook for the target Slack channel, probably `#build-status`.
* Copy the webhook URL.

### 2. GitHub Organisation Secret

The user must create a GitHub Actions organisation secret:

`SLACK_BUILD_WEBHOOK`

Value:

`the Slack webhook URL`

Access policy:

`Selected repositories`

or:

`All repositories`

depending on organisational preference.

### 3. Slack Mention Target

If failures should mention a group, the user must provide the Slack user group ID.

Preferred format:

`<!subteam^GROUP_ID>`

(Replace GROUP_ID with the actual group ID)

### 4. Consumer Repository Rollout

The user or a repo-maintenance agent must update each nightly workflow to add the final `notify` job.
