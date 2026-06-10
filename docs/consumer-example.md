# Consumer Example

Here is an example of how to use the Nightly Status Notify reusable workflow in your own repositories.

```yaml
name: Nightly Validation

on:
  schedule:
    - cron: "0 2 * * *"
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run build and tests
        run: |
          echo "Replace this with the actual nightly build"

  notify:
    needs:
      - build
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

**Note**: `notify` must be a separate final job using `if: always()` so it runs after success or failure of the preceding jobs.
