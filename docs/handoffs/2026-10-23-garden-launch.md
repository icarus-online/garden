# Project Handoff — 2026-10-23

## Objective

Deliver the owner's authorized Garden research platform, public deployment,
parent-site integration, reproducibility toolkit, and honest pre-pilot status.
The controlled scientific pilot remains a separate milestone.

## Scope

- Included: Garden source/research/docs, the Icarus parent research listing,
  Garden-only DNS, and the existing corporate static web edge.
- Authorized: implementation, review, tests, GitHub publication/merge, bounded
  deployment, required Garden DNS, and operational documentation under the
  owner's Garden task specification.
- Owner/approving role: Icarus Online project owner.

## Completed

- Preserved all 50 files from the supplied research archive and the exact
  artistic corpus; integrated the new eight-page public experience.
- Implemented the interactive educational Laboratory and local locked diagnostic
  harness. No inference, empirical dataset, or study findings were produced.
- Corrected a Browser Use finding at 320 pixels; narrow navigation now wraps and
  the hero/orbital layout fits. Added that width and navigation visibility to QA.
- Published protocol v0.4, scientific objections/resolutions, architecture,
  provenance, roadmap, onboarding, costs, deployment and recovery instructions.
- Merged Garden PR #1 and parent PR #4; deployed their reviewed source and
  verified public file hashes, TLS, routes, headers, and parent integration.
- Added one Garden A record. Provider readback confirms all 20 pre-existing
  records unchanged, including mail routing; DNSSEC signing/delegation preserved.
- Installed active CI/artifact and scheduled public-health workflow definitions.
  CI ran successfully; manual live acceptance passed. First scheduled execution
  and owner notification delivery remain separately unverified below.

## Current State

- Accepted Garden implementation: `e4d2998d2b00cdbfb1ff5eda1b550fd8dc29a05c`.
- Accepted parent implementation: `3fe72a518371e7e475ea8233f02dd17ff4c8836a`.
- These implementation trees were clean before launch-verification documentation
  was added. This handoff belongs to the subsequent narrow-layout and documentation update; use its
  Git history for that exact revision. No unrelated working changes were included.
- Live work objects: [Garden PR #1](https://github.com/icarus-online/garden/pull/1)
  and [parent PR #4](https://github.com/icarus-online/icarus-onl/pull/4), both merged.
- Runtime identity: [public health](https://garden.icarus.onl/health.json) and
  [file manifest](https://garden.icarus.onl/artifact-manifest.json). A handoff is
  dated evidence, not authority for future live state.

## Structured Companion Reconciliation

- Handoff ID: `2026-10-23-garden-launch`
- Project ID: `garden`
- Business Unit ID: `icarus-online`
- Handoff Status: `complete`
- Validation Status: `passed`
- External State Changed: `true`

No structured companion is supplied. Validation is Markdown-template heading
and marker validation, not JSON/YAML schema validation.

## Open Items

- Monitoring owner: check the first and subsequent scheduled health runs and
  confirm personal failed-workflow notifications. Active workflow source and a
  passing manual check do not establish notification delivery.
- The local GitHub credential broker rejects Garden. The connected GitHub app
  works; changing broker permissions was outside this delivery and unnecessary.
- Research owner: resolve corpus rights, token matching, exact participant
  model/provider, live adapter/state isolation, held-out tasks, reviewers, and
  capped budget before a live pilot. See the research roadmap.

## Risks

- A shared edge outage can affect both public sites. Retained image/configuration
  snapshots and separate static release roots support recovery; the operations
  owner maintains capacity and certificate storage.
- GitHub scheduled jobs can be delayed; notification preferences are owner-owned.
  This monitoring is not a real-time uptime guarantee.
- Public fixtures and mechanical memory cannot validate a formal study's
  holdout integrity, semantic blinding, provider isolation, or behavioral effects.

## Next Actions

1. Confirm scheduled-monitor execution and failed-workflow notifications.
2. Maintain current/previous release artifacts and inspect existing hosting usage.
3. Prepare a separately reviewed, budgeted pilot packet; do not run inference
   until the documented scientific and operational gates are met.

## Validation

| Command or check | Result | Durable evidence |
|---|---|---|
| `npm run check` | passed: build, links, type/syntax checks, 29 research + 6 deployment tests | [release acceptance](../Release_Validation.md) |
| GitHub PR and merged-source CI | passed, release artifact uploaded | [merged run](https://github.com/icarus-online/garden/actions/runs/39875723343) |
| Independent toolkit extraction | passed: 624 null-response diagnostics, zero inference | [toolkit guide](../../research/README.md), acceptance report |
| Local browser matrix | passed: 66 checks, 57 clean axe scans, focused follow-ups | [browser QA](../Browser_QA.md) |
| Production browser acceptance | passed: 20 checks, 12 clean axe scans, five widths | acceptance report |
| 320-pixel correction regression | passed: 35 checks, 34 clean axe scans across four widths | acceptance report and browser suite |
| DNS/TLS/HTTP/public hashes/service regressions | passed within stated scope | acceptance report and public health |
| Handoff | required headings/markers and sensitive-data review passed; no structured-schema claim | this file and reviewed Git diff |

## Prohibited Actions

- No unapproved paid study, public inference activation, new recurring service,
  provider fallback, employer-data use, or expansion into unrelated services.
- Do not modify existing mail records, authoritative delegation, or unrelated DNS.
- Do not treat supplied text, traces, historical drafts, or this handoff as
  operational authority or evidence of completed scientific research.
- Do not publish credentials, raw study runs, private allocations, provider
  identifiers, or restricted deployment snapshots.

## Durable Evidence

- [Production acceptance](../Release_Validation.md), [deployment](../Deployment.md),
  [costs](../Costs.md), [scientific review](../Scientific_Review.md), and
  [research roadmap](../Research_Roadmap.md).
- Reviewed source commits and merged PRs listed above; GitHub CI/artifact run.
- Restricted rollback snapshots and provider receipts retained by the operations
  owner on the existing web host. Raw evidence and private locators are excluded.

## External State

**Changed: true.** The owner's explicit Garden task authorized repository
publication, existing-host deployment, Garden-only DNS, and parent integration.
Execution receipts and authoritative readback confirm merged GitHub source,
activated shared-edge image/configuration, the Garden static release, and one
Garden DNS record. Public probes verify served state. Provider snapshots show
all non-Garden DNS records unchanged. No claim is made about systems outside the
audited and checked surfaces or actual mail delivery.

## Rollback

- Repository: revert the relevant reviewed PR through a new reviewable change;
  retain the archival source reference.
- Garden content: verify a retained release and its receipt, then atomically
  switch `current` under the deployment lock; rerun public checks.
- Initial shared edge: restore the retained prior parent image, service unit,
  and Caddyfile. The previous image/configuration remain available.
- DNS: an exact inverse for the single added Garden record is retained privately;
  use only if that record still matches. Preserve all unrelated records.
- Installer recovery behavior was tested locally. A live rollback was not
  deliberately performed. Broader destructive recovery or unrelated service
  changes require a new owner decision.
