# Garden deployment and operations

**Updated 22 October 2026, before production acceptance.** This document describes the selected release procedure and installed workflow configuration. Its existence is not proof of a live deployment or a successful workflow run. The execution owner must record the deployed revision, artifact digest, dated DNS/TLS/HTTP checks, and actual workflow-run results in the release record. The operative definitions are `.github/workflows/ci.yml` and `.github/workflows/monitor.yml`; files under `deploy/workflows/` remain reference templates.

The parent-site Garden listing was merged in [Icarus Online PR #4](https://github.com/icarus-online/icarus-onl/pull/4) at source revision `3fe72a518371e7e475ea8233f02dd17ff4c8836a`. This establishes the reviewed source integration, not proof that this revision has reached the deployed parent site.

## Selected host and boundaries

Reuse the existing corporate `icarus-onl-web-01` DigitalOcean Droplet and its Caddy 2 edge. The read-only audit reported a $6/month 1-vCPU/1-GB host with approximately 512 MB available memory and 21 GB available disk. These are observations from the preparation session, not reserved capacity. No additional Droplet, database, inference service, or paid monitoring product is required for this static website.

The corporate container remains responsible for ports 80/443, certificate automation, and the existing parent site. Its established global configuration and parent virtual hosts must be preserved. The Garden adds a separate read-only mount, `/opt/garden:/srv/garden:ro`, and the Garden-only virtual hosts in `deploy/Caddyfile.garden`. The Caddy process runs as UID 1000; release directories/files are readable as 0755/0644. Certificate data/config volumes remain writable under the existing deployment. No Garden process listens on another port and no runtime provider credentials enter the static build.

The mount must include the whole `/opt/garden` directory because `current` is a relative symlink into `releases/`. Mounting only the symlink target would defeat later atomic switches. Caddy has no directory browsing enabled. Only the built public artifact is installed, with explicit rejection of source/private paths and links. The site's public toolkit ZIP intentionally contains reviewed research source; it contains no study runs or credentials.

The selected approach avoids another application service and preserves the authoritative zone's DNSSEC configuration. DigitalOcean App Platform was evaluated during the audit; its [documented custom-domain DNSSEC restriction](https://docs.digitalocean.com/products/app-platform/how-to/manage-domains/) was an additional reason to prefer the existing host. No nameserver or mail-service change is part of this deployment.

## Build and review an immutable artifact

Use Node 22+ (the installed CI workflow selects Node 24), Python 3.10+, and the committed lockfile. From a clean checkout:

```sh
npm ci
npx playwright install --with-deps chromium
npm run check
python3 -m unittest discover -s deploy -p 'test_*.py' -v
npm run qa:browser
python3 scripts/package_release.py
sha256sum .release/manifest.json
```

The build embeds the full Git revision in `health.json` and `artifact-manifest.json`. Packaging refuses an uncommitted checkout or a stale build revision. It produces `.release/garden.tar.gz` and `.release/manifest.json`; the latter records the archive hash, byte length, and source revision. Preserve the reviewed manifest SHA-256 and full revision through an authenticated operator channel. Hashes prove consistency with that trusted record; they do not replace artifact authenticity or code review.

The installed `Garden CI and release artifact` workflow runs on pull requests, pushes to `main`, and manual dispatch. It pins third-party actions to specific commits, checks the application/research/installer/browser suites, and packages and uploads a release artifact for non-PR runs. It has only `contents: read`, no production credentials, and no deployment step. Source installation, a passing run for the exact revision, and required branch-protection checks are separate facts. Local `npm run check` has passed during preparation; successful remote CI and artifact availability must be confirmed from the actual GitHub run before relying on them.

The browser suite starts and cleans up its own Garden preview by default, so CI does not depend on another repository or a manually started server. Parent-site checks run only when an explicit `PARENT_QA_URL` is supplied. An unconfigured parent suite is recorded as skipped, not passed. See the [browser QA record](Browser_QA.md) for executed local coverage and limits.

## Promote a release

Transfer the reviewed archive, manifest, and reviewed installer to the existing host using the operator's established authenticated administration path. Do not add a new broadly privileged CI key just to automate promotion. Verify the full source revision and manifest hash again on the host, then run:

```sh
python3 deploy/install_release.py \
  --archive /path/to/garden.tar.gz \
  --manifest /path/to/manifest.json \
  --manifest-sha256 REVIEWED_MANIFEST_SHA256 \
  --revision REVIEWED_FULL_GIT_REVISION \
  --root /opt/garden
```

The installer first verifies the manifest and archive bytes, then extracts into a staging directory under `/opt/garden/releases`. It rejects traversal, links, special/sparse files, extended tar metadata, duplicate paths, hidden/private source paths, unexpected file types, excess file counts, and size-limit violations. Limits are 64 MiB compressed, 128 MiB decompressed including tar metadata, 16 MiB per file, and 5,000 entries. It verifies every public file against the internal manifest and checks the health identity and disabled-inference status before making the release visible.

A process lock serializes installs. A relative symlink replacement atomically changes `current`; earlier releases remain intact. Deployment receipts under `/opt/garden/.deployment-records/` preserve the prior target and hashes outside the served directory. The installer does not change Caddy, Docker, DNS, or the parent site. It refuses an already existing release rather than overwriting it. A host or filesystem failure can still interrupt a deployment; inspect `current` and its receipt before retrying.

For the initial mount and virtual-host addition, snapshot the existing container configuration and Caddyfile privately. Add the mount through the existing corporate deployment method and append the Garden snippet while leaving all parent blocks unchanged. Validate the **complete candidate** with the host's exact Caddy binary/image before replacement. Caddy's admin API is disabled here, so `caddy reload` is not a supported assumption: use the established container recreation/restart mechanism with rollback available. The initial container operation may briefly affect the shared edge and must be followed by parent-site checks. Subsequent Garden releases normally need only the static symlink switch.

The Garden snippet gives HTTP redirects, HTTPS responses, and custom 404 responses the same security headers. `/index.html` redirects to `/` while preserving its query. Scripts/styles load from the same origin; no inline execution is allowed. The two original historical HTML pages are served as attachments because they retain inline code; opening a downloaded copy locally preserves the original experience without weakening production CSP. Their bytes also remain in the original downloadable ZIP. There are no analytics cookies or request access-log directives. Existing Caddy operational/certificate logs remain under corporate retention policy.

## DNS, certificates, and launch verification

At preparation time Garden returned NXDOMAIN. The execution owner verified the existing Route 53 public zone and its authoritative nameservers, recorded 20 pre-change records privately, and observed DNSSEC signing. Recheck that evidence immediately before the change. Add only the record required for `garden.icarus.onl` to reach the selected Droplet. An A record is appropriate for the audited stable IPv4 host; add AAAA only after separately verifying IPv6 reachability and ownership. Do not change apex nameservers, MX, SPF, DKIM, DMARC, or unrelated records.

Caddy's existing automated HTTPS setup obtains and renews the Garden certificate after public DNS and port reachability are correct. Keep its persistent certificate storage and port 80/443 access intact. Do not replace certificates manually or disable DNSSEC to accommodate a different hosting product. [Caddy automatic HTTPS](https://caddyserver.com/docs/automatic-https) documents the renewal and challenge requirements.

After promotion and DNS propagation:

```sh
python3 scripts/check-production.py \
  --host garden.icarus.onl \
  --expected-ip VERIFIED_DROPLET_IPV4 \
  --expected-revision DEPLOYED_FULL_GIT_REVISION
```

The checker validates resolver addresses, certificate trust/hostname and remaining lifetime, homepage identity, release health, canonical redirects, security headers, absence of cookies/server disclosure, custom missing-file responses, blocked private paths, and absence of directory browsing. It does not verify authoritative-zone change scope or mail service. Separately compare the complete post-change zone snapshot with the private baseline, verify all non-Garden records unchanged, and check the parent site's HTTPS/navigation/research listing. Keep private snapshots and any administrative diagnostics out of the public repository.

## Rollback and recovery

Read the previous release target from the deployment receipt. Verify the selected release's internal hashes with `verify_release` from the reviewed installer and compare its artifact-manifest SHA-256 against the stored deployment receipt. Then, under the same installation lock, create a new relative symlink and atomically replace `current`. For example, with a validated literal release directory name:

```sh
flock /opt/garden/.install.lock sh -c 'ln -s releases/VALIDATED_PREVIOUS_RELEASE /opt/garden/.rollback-next && mv -Tf /opt/garden/.rollback-next /opt/garden/current'
```

A pre-existing `.rollback-next` makes this command fail safely; inspect it rather than overwriting it blindly. Re-run the public checker using the previous release revision and confirm the parent site. No DNS change is normally needed for a content rollback. If the initial shared-container configuration fails, restore the privately saved corporate container/Caddyfile configuration using its established procedure; a content rollback cannot repair a missing mount or invalid Caddy configuration.

Retain at least the current and previous known-good releases plus their trusted manifests. The installer deliberately does not auto-delete releases. Periodically inspect free disk space; delete an older release only after confirming neither `current` nor the selected rollback target refers to it. Preserve the exact build inputs and release artifacts independently of this shared host. There is no newly configured database or research-state backup in this static deployment.

## Monitoring ownership

The installed `.github/workflows/monitor.yml` defines `Garden public health`: the public checker runs on manual dispatch and is scheduled at minute 17 every six hours (`17 */6 * * *`, UTC). Its job has a five-minute timeout, read-only repository permissions, and no cloud credentials. The checker fails if the certificate has fewer than 14 days remaining. The source schedule is configured; the first successful manual or scheduled run and ongoing execution must still be evidenced separately.

GitHub may delay scheduled workflows; this is not a real-time uptime SLA. An owner must enable/check failed-workflow notifications and periodically verify scheduled runs are actually occurring. No custom email/Slack delivery is configured by this repository, and notification delivery has not been established by the workflow file alone.

Before marking operations complete, record the monitoring owner, activation state, first successful scheduled/manual check, deployed revision, latest DNS/TLS evidence, and rollback target. A passing manual probe does not prove recurring monitoring is active.
