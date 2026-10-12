# Razor on-prem static publishing

Build on an ordinary runner, upload a directory artifact, then call
`.github/workflows/publish-static-site.yml`. The publisher does not checkout
caller code or execute anything from the artifact. It uses the runner scale set
`razor-onprem-staticapp-publishers` and `/srv/sites` mounted by the GitOps PRs.
No Cloudflare token or Kubernetes credentials are required in caller repositories.

## GitHub setup

Restrict the publisher runner group to selected trusted private/internal repos.
If available, restrict selected workflow access to
`razorltd/.github/.github/workflows/publish-static-site.yml@refs/heads/main`.
Eligible repositories share write access to all sites. Use distinct site names
and protect caller workflows/branches. No site registry, environment, variable
or repository secret is required. Pass a site name and artifact name; the first
publish creates its directory. Per-site Cloudflare DNS and office-IP-or-AAD
Access setup is still needed before external access.

## Proposed dataqi-agent caller

The existing internal docs build uses Node 24, `npm ci --ignore-scripts`, an
audit, and `npm run build` under `docs/internal`, producing `docs/internal/dist`.
Keep those build checks and upload the output instead of deploying it to Azure.
The caller should only publish the approved source ref, not an arbitrary checkout.
The existing public-docs path should retain its current deployment separately.

After the build steps in the ordinary build job:

```yaml
- uses: actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7
  with:
    name: internal-docs-static
    path: docs/internal/dist/
    if-no-files-found: error
    retention-days: 7
```

Add a separate dependent job (replace the reference with the reviewed workflow
commit; use `main` only if selected-workflow policy requires that reference):

```yaml
publish:
  needs: build-internal-docs
  permissions:
    actions: read
    contents: read
  uses: razorltd/.github/.github/workflows/publish-static-site.yml@main
  with:
    site-name: dataqi-internal-docs
    site-hostname: dataqi-internal-docs.razor.co.uk
    artifact-name: internal-docs-static
```

Only push and manual-dispatch runs are eligible. Artifacts must come from the
same run. Optional `site-hostname` changes the reported URL only; the default is
`<site-name>-internal.razor.co.uk`. A custom hostname needs a matching NGINX alias
in GitOps as well as DNS and Access. It does not change the content directory.
No secrets inheritance is needed. Existing Azure-specific routing or
authentication config does not configure NGINX: test generated URL paths,
redirects and any SPA requirements during the separately approved migration.

## Release behaviour and limits

Root index.html is required; symlinks and special files are rejected.
Files receive 0644 and directories 0755. Publishing uses Bash and standard
Linux tools (`cp`, `find`, `chmod`, `ln`, `mv`).
Complete releases are staged on NFS, then the relative current symlink is
atomically replaced. Current content remains intact on a failed copy.

GitHub concurrency is repository-scoped. Keep the dedicated scale set at
maxRunners=1: that serialises writers across repositories. An older run cannot
replace a newer successful release; reruns have their own attempt number.
Do not add other writers or increase scale without a storage-side lock design.

After successful publication, keep the three newest releases (including current)
and delete older numeric release directories. Optional `keep-releases` accepts
2–20; default 3. The current release is never pruned. This bounds version count,
not byte usage; monitor NFS capacity because large artifacts can still fill it.
Failed copies clean their staging directory without replacing current content.
Keeping old release directories alone does not preserve unversioned asset URLs after a
switch: sites needing that must publish release-qualified assets or explicitly
retain old hashed assets. Rollback is a separately authorised atomic replacement
of current with a previous release; an older workflow rerun is not a rollback.

The workflow reports successful filesystem publication, not externally verified
Cloudflare reachability. Test office access, off-network AAD login, denied
unauthenticated access, both NGINX replicas and NFS visibility during the pilot.
