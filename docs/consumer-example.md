# Consumer Example

Here is an example of how to use the RZR Status Notify reusable workflow in your own repositories.

## Using Slack Bot Token

This setup dynamically routes notifications to a specific Slack channel using a single organisation-wide Slack Bot Token.

```yaml
name: Validation

on:
  schedule:
    - cron: "0 2 * * *"
  workflow_dispatch:

permissions:
  actions: read
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run build and tests
        run: echo "Replace this with the actual build"

  notify:
    runs-on: ubuntu-slim
    needs:
      - build
    if: always()
    uses: YOUR_ORG/.github/.github/workflows/rzr-notify-status.yml@main
    with:
      current_result: ${{ needs.build.result }}
      channel_context: Validation run
      slack_channel: "#team-a-builds" # Target channel
      mention_on_failure: "<!subteam^REPLACE_WITH_SLACK_USER_GROUP_ID>"
    secrets:
      slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
```

**Note**: The `notify` job must be a separate final job using `if: always()` so it runs after success or failure of the preceding jobs.
