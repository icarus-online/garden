# Production launch acceptance — 23 October 2026

**The Garden is live at [garden.icarus.onl](https://garden.icarus.onl/).**
The [Icarus Online homepage](https://icarus.onl/) identifies it as independent,
experimental research and links to the website and public repository. This is
acceptance of the platform, not completion of an agent study.

## Reviewed source and release identity

| Surface | Verified source |
|---|---|
| Garden launch | `e4d2998d2b00cdbfb1ff5eda1b550fd8dc29a05c`, [PR #1](https://github.com/icarus-online/garden/pull/1) |
| Parent integration | `3fe72a518371e7e475ea8233f02dd17ff4c8836a`, [parent PR #4](https://github.com/icarus-online/icarus-onl/pull/4) |
| Original supplied package | `5f242997cc802707baaf7568cc7fdc6e0649cbab`; all 50 supplied files preserved |

The accepted launch archive SHA-256 is
`1ca452583fc7222baf11767635c09de966d88c2a0bfc04cdf502195945acdeb5`;
its release-manifest SHA-256 is
`54e6ef5a0f8dc37e845f129cbfadf3dd07e5af1bab0c2b3851034406d5dbc899`.
These identify the launch tested below. This report is a subsequent documentation
change; it does not claim to have existed in that earlier artifact. Consult
[health.json](https://garden.icarus.onl/health.json) and the
[public file manifest](https://garden.icarus.onl/artifact-manifest.json) for the
currently served revision. The follow-up containing this report also corrects
the 320-pixel layout issue described below. The corpus and research implementation
remain unchanged.

## Engineering and research checks

- `npm run check` passed: public build, HTML and Markdown links, file hashes,
  sensitive-data exclusions, syntax checks, JavaScript type checking,
  **29 research/allocation tests and six deployment tests**.
- The updated PR passed [GitHub CI](https://github.com/icarus-online/garden/actions/runs/39875202679).
  The merged revision also passed [main-branch CI](https://github.com/icarus-online/garden/actions/runs/39875723343),
  which packaged and uploaded its release artifact with 14-day retention.
  Downloading that artifact confirmed its archive and manifest are byte-identical
  to the accepted locally packaged production release.
  GitHub builds have read-only repository permissions and no production secret.
- Repeated packaging of the same reviewed source produced identical archive and
  manifest bytes. Deployment verified transfer hashes, archive expansion bounds,
  allowed paths, every public-file hash, and the exact source revision.
- A fresh extraction of the downloadable toolkit passed all six documented
  command groups, including tests, configuration validation, a full diagnostic
  run, verification, blind export, and corpus checking. It produced **48 × 13 =
  624 mechanical records**, 624 null-response reviewer records, and **zero model
  calls**. These are not empirical observations or rateable model responses.
- The preserved artistic corpus still has SHA-256
  `66aef59c6243289b7241b6fc7a8c64819ac8288ae8868946187c022a9ebef5e5`.
- The PR review bot identified malformed trace timestamps accepted by verification;
  principal review identified omitted toolkit documentation causing public links
  to fail. Principal review using the assigned Astra/Ultra configuration verified
  both resolutions. Timestamp
  regression tests and published Markdown-link checking now pass. Earlier
  methodological objections and limits are recorded in [Scientific Review](Scientific_Review.md).

## Public acceptance

Public checks at **00:05 UTC on 23 October 2026** verified:

| Check | Observed result |
|---|---|
| Authoritative DNS change | One Garden A record added; all 20 pre-existing records unchanged |
| Mail routing | MX and mail-related TXT records unchanged; mail delivery itself was not tested |
| DNSSEC | Route 53 signing preserved; public validating resolver returned authenticated Garden A and unchanged parent DS answers |
| TLS | Trusted hostname-valid certificate, expiring 20 January 2027; approximately 90 days remaining |
| Certificate management | Caddy successfully obtained the certificate; persistent storage and automatic renewal remain configured |
| Canonical routes | HTTP-to-HTTPS and `/index.html` redirects return 308 and preserve queries |
| Error handling | Missing paths, `.env`, `.git/config`, and asset-directory requests return genuine 404 responses |
| Headers | Strict same-origin CSP, HSTS, framing denial, nosniff, referrer and permissions policies; no cookie or server header |
| Public artifact | All 50 launch files match local manifest hashes; public manifest matches the accepted build |
| Parent homepage | Byte-identical to the reviewed parent build, with correct Garden/repository links |
| Existing public services | Parent responsible-AI page, Swampcat homepage, and professional homepage returned 200 with their pre-change content hashes |

Fifteen additional probes against the pinned production Caddy image passed
before activation, including unversioned-asset revalidation, no-store health and
error responses, historical HTML attachment headers, and query-preserving
redirects. The shared container runs with a read-only root and read-only Garden
mount, using its existing restricted capabilities and resource limits.

Production Chromium acceptance at **00:05:21–00:05:45 UTC** passed **20/20 grouped
checks and 12 axe scans with zero reported violations**. Home and Laboratory
were tested at **360, 390, 768, 1024, and 1440 pixels**. Checks covered all eight
Garden routes, keyboard/orbital interaction, conditions and phases, the separate
exploratory inspector, deterministic educational allocation and download, empty
trace views, deep links, reduced motion, disabled JavaScript, historical
attachments, and the parent listing at 390/1440 pixels. No horizontal overflow,
JavaScript/console error, cookie, or third-party request was observed.

Fresh browser contexts measured homepage first contentful paint at **276–392 ms**
and **15,728 transferred bytes** for the page and three resources. These are
unthrottled measurements from one testing host, not global performance guarantees
or mobile-device hardware benchmarks. The [earlier browser report](Browser_QA.md)
records the broader local 66-check matrix, corrections, and accessibility limits.

Supplementary Browser Use inspection confirmed public navigation, Laboratory
controls and empty results, and the parent listing. It identified clipping at
320 pixels, below the original requested test matrix. The release follow-up
addresses that finding with wrapping navigation and a shrinkable hero/orbital
layout below 351 pixels, and extends the reusable browser matrix to 320 pixels.
The focused regression passed **35/35 checks and 34 clean axe scans**: all eight
pages at 320/360/390/1440 pixels, two additional Laboratory panes at 320 pixels,
and keyboard access to Archive. Document widths matched their viewports and
every navigation link remained visible. Screenshots at 320 and 360 pixels were
visually reviewed. Styles at 360 pixels and above are unchanged by this fix.

## Operations, cost, and remaining limits

The release reuses the existing corporate DigitalOcean host and Caddy edge.
It adds **$0 fixed monthly compute commitment**: no new Droplet, resize, database,
paid monitor, or inference provider was provisioned. Shared DNS/traffic/storage
usage can still affect the existing bill. The audited host plan is $6/month;
that is an existing shared cost, not a new Garden-only invoice. See [Costs](Costs.md).

Both GitHub workflows report `active`. The public-health workflow is installed
on `main` with a six-hour schedule and a 14-day certificate-expiry threshold.
The initial manual production checker passed; the first scheduled execution and
the owner's failed-workflow notification delivery were still unverified when this
acceptance record was written. The Icarus Online project owner owns monitoring
and should check subsequent runs and notification preferences. No custom email
or Slack alert channel was configured. A source schedule is not an uptime SLA.

The original parent image, service configuration, edge configuration, DNS
snapshot, and exact inverse Garden DNS change are retained in owner-restricted
deployment storage. The static installer retains release receipts and previous
targets for atomic content rollback. Installer rollback behavior was tested
locally; a live rollback was not deliberately triggered. See [Deployment](Deployment.md)
for promotion, recovery, retention, and monitoring procedures.

The connected GitHub app successfully published and merged the work. The local
credential broker still rejects this newly added repository; its permission
configuration was not changed. This does not block the connected publication path.

No study is preregistered, no participant model is selected, and no live inference
is enabled. Remaining pilot gates include corpus reuse terms, tokenizer-based
control matching, a reviewed provider adapter and fixed model configuration,
audited live state isolation, sealed held-out tasks, independent human reviewers,
and a bounded approved budget. Confirmatory research additionally needs a frozen
analysis plan and justified power calculation. See the [research roadmap](Research_Roadmap.md).
