# NPM Audit Action

The NPM Audit action is a reusable composite GitHub Action that runs `npm audit` on a specified path, parses the output, and provides structured outputs. This makes it easier to parse vulnerabilities and configure conditional logic in workflows.

## Path
`uses: razorltd/.github/.github/actions/npm-audit@main`

## Inputs

| Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **`path`** | String | The directory path to run `npm audit` in. | `.` |

## Outputs

| Name | Type | Description |
| :--- | :--- | :--- |
| **`hasCritical`** | Boolean | `true` if critical vulnerabilities were found, `false` otherwise. |
| **`hasHigh`** | Boolean | `true` if high vulnerabilities were found, `false` otherwise. |
| **`hasModerate`** | Boolean | `true` if moderate vulnerabilities were found, `false` otherwise. |
| **`hasLow`** | Boolean | `true` if low vulnerabilities were found, `false` otherwise. |
| **`criticalCount`** | Number | Number of critical vulnerabilities found. |
| **`highCount`** | Number | Number of high vulnerabilities found. |
| **`moderateCount`** | Number | Number of moderate vulnerabilities found. |
| **`lowCount`** | Number | Number of low vulnerabilities found. |
| **`criticalVulnerabilities`** | JSON Array | Array of package names with critical vulnerabilities (e.g. `["cookie", "express"]`). |
| **`highVulnerabilities`** | JSON Array | Array of package names with high vulnerabilities. |
| **`moderateVulnerabilities`** | JSON Array | Array of package names with moderate vulnerabilities. |
| **`lowVulnerabilities`** | JSON Array | Array of package names with low vulnerabilities. |
| **`vulnerabilitiesArtifacts`** | String | A multi-line markdown link list of found vulnerabilities formatted for the status notifier. |

## Example Usage

Here is how to integrate this action in your repository workflow:

```yaml
name: Security Audit

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  check-security:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v5

      - name: Set up Node
        uses: actions/setup-node@v6
        with:
          node-version: '20'

      - name: Audit project
        id: audit
        uses: razorltd/.github/.github/actions/npm-audit@main
        with:
          path: '.'

      - name: Report Results
        run: |
          echo "Has Critical: ${{ steps.audit.outputs.hasCritical }}"
          echo "Has High: ${{ steps.audit.outputs.hasHigh }}"
          echo "Vulnerable Packages: ${{ steps.audit.outputs.highVulnerabilities }}"
```
