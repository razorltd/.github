# Organisation .github Repository

This repository contains organisation-wide default files, community health files, and shared automation. It serves as the single source of truth for repository configurations across the organisation.

## Contents

- **Organisation Profile**: Files in the `profile/` directory used to generate the public organisation profile page.
- **Shared GitHub Actions**: Reusable workflows stored in `.github/workflows/` that can be called by other repositories.
- **Community Health Files**: Default issue templates, PR templates, and contributing guidelines which apply to all repositories unless overridden locally.

## Shared GitHub Actions
## Nightly Status Notify

A reusable workflow that posts Slack notifications for nightly build status changes across private repositories. It notifies Slack when a scheduled nightly workflow fails, or when a previously failing nightly workflow recovers, avoiding repeated messages.

### How it is called

The workflow is called using `workflow_call`. See [docs/consumer-example.md](docs/consumer-example.md) for a full example.

```yaml
  notify:
    needs: [build]
    if: always()
    uses: YOUR_ORG/.github/.github/workflows/nightly-status-notify.yml@main
    with:
      watched_workflow_name: Nightly Validation
      current_result: ${{ needs.build.result }}
      channel_context: Nightly build
      mention_on_failure: "<!subteam^REPLACE_WITH_SLACK_USER_GROUP_ID>"
    secrets:
      slack_webhook_url: ${{ secrets.SLACK_BUILD_WEBHOOK }}
```

### Required Secret

- `slack_webhook_url`: A Slack Incoming Webhook URL. It's recommended to store this as an organisation secret named `SLACK_BUILD_WEBHOOK`.

### Required Manual Setup

See [docs/manual-setup.md](docs/manual-setup.md) for detailed manual setup instructions.

### Expected Notification Behaviour

- **Failure**: Posts to Slack when the previous result was not `failure` and the current result is `failure`.
- **Recovery**: Posts to Slack when the previous result was `failure` and the current result is `success`.
- **Ignored**: No notification is sent if the workflow continues to succeed or continues to fail.

### Example Rollout Checklist

1. Configure Slack Webhook.
2. Add Organisation Secret.
3. Identify Slack Group ID for mentions.
4. Add `notify` job to target repository workflow.
