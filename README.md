# Organisation .github Repository

This repository contains organisation-wide default files, community health files, and shared automation. It serves as the single source of truth for repository configurations across the organisation.

## Contents

- **Organisation Profile**: Files in the `profile/` directory used to generate the public organisation profile page.
- **Shared GitHub Actions**: Reusable workflows stored in `.github/workflows/` that can be called by other repositories.
- **Community Health Files**: Default issue templates, PR templates, and contributing guidelines which apply to all repositories unless overridden locally.

## Shared GitHub Actions
### Nightly Status Notify

A reusable workflow that posts Slack notifications for nightly build status changes across private repositories. It notifies Slack when a scheduled nightly workflow fails, or when a previously failing nightly workflow recovers, avoiding repeated messages.

[action](./.github/workflows/nightly-status-notify.yml)
[example](./docs/consumer-example.md)

## Organisation Setup
### Secrets

- `slack_webhook_url`: A Slack Incoming Webhook URL. It's recommended to store this as an organisation secret named `SLACK_BUILD_WEBHOOK`.

### Required Manual Setup

See [docs/manual-setup.md](docs/manual-setup.md) for detailed manual setup instructions.