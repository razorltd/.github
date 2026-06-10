# Consumer Example

Here are examples of how to use the RZR Status Notify reusable workflow in your own repositories.

## Example 1: Automatic Result Detection (Recommended)

In this setup, `current_result` is omitted. The workflow automatically queries the GitHub API to scan the conclusions of all other jobs in the current run.

```yaml
name: Validation

on:
  schedule:
    - cron: "0 2 * * *"
  workflow_dispatch:

permissions:
  actions: read
  contents: read
  checks: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run build and tests
        run: echo "Replace this with the actual build"

  generate-status-token:
    runs-on: ubuntu-latest
    outputs:
      token: ${{ steps.app-token.outputs.token }}
    steps:
      - name: Generate status token
        id: app-token
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ vars.STATUS_APP_ID }}
          private-key: ${{ secrets.STATUS_APP_PRIVATE_KEY }}

  notify:
    runs-on: ubuntu-slim
    needs:
      - build
      - generate-status-token
    if: always()
    uses: YOUR_ORG/.github/.github/workflows/rzr-notify-status.yml@main
    with:
      name: Validation run
      product: MyProduct
      slack_channel: "#team-a-builds" # Target channel
    secrets:
      slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
      status_token: ${{ needs.generate-status-token.outputs.token }}
```

## Example 2: Explicit Result Override

If you want to override the result manually, you can pass `current_result` explicitly.

```yaml
name: Validation

on:
  schedule:
    - cron: "0 2 * * *"
  workflow_dispatch:

permissions:
  actions: read
  contents: read
  checks: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run build and tests
        run: echo "Replace this with the actual build"

  generate-status-token:
    runs-on: ubuntu-latest
    outputs:
      token: ${{ steps.app-token.outputs.token }}
    steps:
      - name: Generate status token
        id: app-token
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ vars.STATUS_APP_ID }}
          private-key: ${{ secrets.STATUS_APP_PRIVATE_KEY }}

  notify:
    runs-on: ubuntu-slim
    needs:
      - build
      - generate-status-token
    if: always()
    uses: YOUR_ORG/.github/.github/workflows/rzr-notify-status.yml@main
    with:
      current_result: ${{ needs.build.result }}
      name: Validation run
      product: MyProduct
      slack_channel: "#team-a-builds" # Target channel
    secrets:
      slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
      status_token: ${{ needs.generate-status-token.outputs.token }}
```

**Note**: The `notify` job must have `needs:` pointing to the preceding jobs so it runs after they finish, and it must use `if: always()` so it runs even if preceding jobs fail.
