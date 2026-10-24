# The Garden

**Icarus Online LLC · independent research · v0.4 · pre-pilot**

Can exposure to art, philosophy, and cultural context produce observable,
persistent differences in AI-agent behavior without prescribing a persona?

[Enter the Garden](https://garden.icarus.onl/) ·
[Explore the Laboratory](https://garden.icarus.onl/laboratory.html) ·
[Read protocol v0.4](docs/Scientific_Protocol_v0.4.md)

The Garden is both an artistic environment and an experimental apparatus. The
artwork has no obligation to produce a significant result. The research must be
able to distinguish evidence from a compelling story.

**No agent study has been run. No empirical findings are claimed. This project
is not preregistered.** The public laboratory demonstrates experimental structure
and exports educational plans. The local harness produces explicitly labeled
mechanical diagnostics with **zero model calls**. It cannot run live inference.

## Explore and reproduce

Requires Node.js 22 or newer and Python 3.10 or newer. Clone with history: the
build includes the original source snapshot from its preserved Git commit.

```sh
git clone https://github.com/icarus-online/garden.git
cd garden
npm ci
npm run check
npm run serve
```

The preview runs at `http://127.0.0.1:4178`. No account, runtime secret, database,
inference provider, remote font, analytics, or cookie is required.

```sh
npx playwright install --with-deps chromium
npm run qa:browser
```

Browser QA covers responsive layouts, accessibility, keyboard operation, motion
preferences, navigation, and functional laboratory controls. See the dated
[browser report](docs/Browser_QA.md) for executed evidence and limitations.

The research toolkit uses the Python standard library:

```sh
python3 -m research validate research/configs/dry-run.example.json
python3 -m research run research/configs/dry-run.example.json --out runs/example
python3 -m research verify runs/example
```

See [the complete toolkit guide](research/README.md) for locking a changed
configuration, private allocations, blind exports, and integrity checks. A lock
records the exact implementation as well as configuration and source hashes.
Changing the implementation invalidates old locks deliberately.

## What lives here

| Surface | Source | Purpose |
|---|---|---|
| Public experience | `site/` | Eight static pages, local artwork, interactive Garden and Laboratory |
| Artistic corpus | `materials/` | Original fragments, preserved byte-for-byte |
| Scientific protocol | `docs/Scientific_Protocol_v0.4.md`, `methods/` | Pilot design, coding, preregistration preparation, limitations |
| Local apparatus | `research/`, `scripts/`, `tests/` | Locked configuration, seeded allocation, isolation, trace validation |
| Operations | `deploy/`, `docs/Deployment.md` | Serving, immutable artifacts, atomic promotion, rollback and monitoring |
| Provenance | `archive/`, `v2/`, root `index.html`, `preview/` | Preserved earlier designs and dated QA artifacts |
| Generated output | `dist/`, `.release/`, `runs/`, `.qa/` | Ignored build, release, private diagnostics and test artifacts |

The root `index.html` and original Python site builder are historical v0.3
artifacts; current website source is `site/`. The original `RELEASE_MANIFEST.json`
describes that source package. Current builds generate their own hashed manifest.

## Scientific boundary

The primary feasibility pilot plans 48 independent trajectories, balanced across
Garden/neutral exposure × memory enabled/disabled. Thirteen sessions per
trajectory produce **624 scheduled session-level calls**, before any retries or
additional inference. Repeated responses are not independent experimental units.

Baseline memory is disabled in all arms and reset before exposure. Withdrawal
removes the original document; memory may still retain its influence or wording.
The original no-document/neutral/persona/philosophy comparison is a separate
educational demonstration. Neither demonstration is empirical evidence.

The shipped control is provisional, example tasks are public, and diagnostic
memory is not an inference-memory implementation. An actual pilot requires a
validated provider adapter, exact model lock, token matching, audited isolation,
sealed held-out tasks, corpus reuse terms, independent reviewers, and an explicit
budget. Confirmation additionally requires a powered sample and frozen public
preregistration. See [the research roadmap](docs/Research_Roadmap.md) and
[scientific review](docs/Scientific_Review.md).

The [pilot decision packet](docs/Pilot_Readiness_Packet.md) turns those gates into
assigned deliverables, an adapter-validation matrix and an unfilled cost worksheet.
It is preparation only and does not authorize or enable participant inference.

## Deployment and custody

Production design reuses the existing Icarus static web host with an isolated
Garden root and automatic HTTPS. Git owns source, the build manifest owns artifact
identity, and live acceptance establishes deployed state. See
[architecture](docs/Architecture.md), [deployment and rollback](docs/Deployment.md),
[costs](docs/Costs.md), and [production acceptance](docs/Release_Validation.md)
for verified operational status and remaining limits.

The project is independent Icarus Online LLC research. Historical employer
references are provenance, not ownership, sponsorship, endorsement, or permission
to use proprietary materials. No employer code or data is included. The supplied
artwork is preserved; no blanket third-party license is inferred. See
[provenance and reuse](docs/Provenance.md).

**Count the ripples. Leave the garden alone.**
