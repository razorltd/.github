# Organisation .github Repository

This repository contains organisation-wide default files, community health files, and shared automation. It serves as the single source of truth for repository configurations across the organisation.

## Contents

- **Organisation Profile**: Files in the `profile/` directory used to generate the public organisation profile page.
- **Shared GitHub Actions**: Reusable workflows stored in `.github/workflows/` that can be called by other repositories.
- **Community Health Files**: Default issue templates, PR templates, and contributing guidelines which apply to all repositories unless overridden locally.

## Shared GitHub Actions
### RZR Status Notify

A reusable workflow that posts Slack notifications for workflow run status changes across private repositories. It notifies Slack when a scheduled workflow fails, or when a previously failing workflow recovers, avoiding repeated messages.

[action](./.github/workflows/rzr-notify-status.yml)
[example](./docs/consumer-example.md)

### Optional Inputs

- `report-mode`: Determines when to send notifications. Options:
  - `on-change` (default): Only notify when the state changes (failure -> success, success -> failure).
  - `all`: Send a notification on every run (success or failure).
  - `all-failures`: Send a notification on every failure, and on recovery.
- `current_result`: Optional current workflow result (e.g., `success`, `failure`). If omitted, it will automatically query the GitHub API to scan all jobs in the run and determine the status.
- `artifacts`: Optional multi-line list of artifacts to link in the status UI. Format: `[Name](https://url)` (e.g. `[Playwright Report](https://example.com/report/index.html)`).

### Required Inputs

- `slack_channel`: Target Slack channel (e.g., `#build-status` or ID).
- `name`: A human-readable name/context, for example `Validation run`.
- `product`: The name of the product (e.g., `DataQI`).
- `status_app_id`: The GitHub App ID used to access the `.status` repository.

### NPM Audit Action

A composite action that runs `npm audit` in a specified directory, parses the vulnerability report, and outputs boolean flags, counts, and lists of vulnerable packages for each severity level.

[action](./.github/actions/npm-audit/action.yml)
[documentation](./docs/npm-audit-action.md)

---

## Organisation Setup
### Variables

- `STATUS_APP_ID`: The GitHub App ID. Recommended to store this as an organisation variable. **Required**.

### Secrets

- `slack_bot_token`: A Slack Bot User OAuth Token (`xoxb-...`) with `chat.postMessage`, `files:write`, and optionally `channels:read`/`groups:read` scopes. Recommended to store this as an organisation secret named `SLACK_BOT_TOKEN`. **Required**.
- `status_app_private_key`: The GitHub App private key (`.pem` file contents) with write access to the `.status` repository. Recommended to store this as an organisation secret named `STATUS_APP_PRIVATE_KEY`. **Required**.

### Required Manual Setup

See [docs/manual-setup.md](docs/manual-setup.md) for detailed manual setup instructions.