# Model configuration and participant boundary

**22 October 2026 · development and review record**

The models used to build this platform are not experimental participants. No Garden participant inference has been run. The current toolkit accepts only a local mechanical diagnostic backend.

## Development assignments

The active collaboration catalog exposed `gpt-6-astra` with `ultra` and `high` reasoning settings. The user requested Astra / Ultra for principal scientific and architecture work, with separate implementation assignments. The supported configuration was selected; no unavailable-model substitution was necessary for these assignments.

| Responsibility | Requested configuration | Assigned configuration in this execution |
|---|---|---|
| Principal scientific/architecture review | Astra / Ultra | `gpt-6-astra`, `ultra` |
| Frontend implementation | Astra implementation tier | `gpt-6-astra`, `high` |
| Research toolkit and deployment implementation | Astra implementation tier | `gpt-6-astra`, `high` |
| Root coordination, integration and operations | Inherited active environment | Inherited configuration; exact model/backend version not independently attested here |

These are orchestration assignments and the catalog observed in the active session. They are not independent attestations of immutable provider weights or a hidden backend version. No such version is invented in this record. The principal review challenged the experimental design, reviewed the implementation and public claims, and recorded corrections in [Scientific Review](Scientific_Review.md).

Routine build, lint, type, packaging, browser, and Python tests execute ordinary software commands. They do not introduce a third experimental model or produce participant responses. Development-service usage is distinct from a study's inference budget.

Supplementary public-web QA used the connected Browser Use service with its
documented default `gpt-5.6-luna`; no model override was requested. The service's
actual backend/version was not independently attested. That browsing agent is a
development verification tool, never a Garden participant or a model judge of
experimental responses.

## Current executable diagnostic lock

The [example configuration](../research/configs/dry-run.example.json) and its sibling lock identify:

| Field | Value |
|---|---|
| Mode | `dry_run` |
| Provider | `local-dry-run` |
| Model identifier | `mechanical-receipt-v1` |
| Version | `1` |
| Reasoning effort | `not-applicable` |
| Temperature, seed, top-p, maximum output tokens | Explicit `null`; no sampling occurs |
| API transport / endpoint | `none` / `null` |
| API retries | `0` |
| Tools / permissions | Empty list / `none` |
| Context | `diagnostic-object-v1`; reject oversize input; 250,000-byte fixture limit |
| Memory | `bounded-diagnostic-receipts-v1`; six-record fixture capacity |
| Baseline | Reads/writes disabled; reset before exposure |

The example fixes corpus and task hashes, operational text, the allocation seed, and protocol version. Its lock additionally hashes exact implementation files. Validation rejects unsupported providers, model changes, unexpected settings, enabled tools, and lock drift. There is no provider endpoint or fallback path to activate accidentally.

Each diagnostic receipt states that no model was called and contains a null response. Returned diagnostic metadata is locally generated identity data, not a provider acknowledgement. The manifest reports zero inference calls. The lock and receipt mechanism test reproducibility and isolation boundaries; they cannot establish model behavior.

## Participant selection remains open

No Astra model, DigitalOcean model, or other provider has been selected for the controlled pilot. The public website does not imply otherwise. Choosing a participant requires a separate manifest, reviewed provider adapter, budget, and live isolation checks.

The participant lock must record exact provider/API/model identifiers; available snapshot and returned metadata; reasoning effort; sampling/seed settings; input/output limits; instructions; ordered context assembly and truncation; task/source hashes; tool permissions; memory implementation; software versions; and attempt/cost accounting. Explicitly distinguish unsupported settings, omitted defaults, and unavailable metadata.

Keep model and reasoning settings fixed within randomized blocks. Do not route around an unavailable model or silently lower reasoning effort. Stop on detected drift or treat affected observations as a separately declared block. A mutable alias must be described as mutable; catalog availability alone is insufficient to establish a stable experimental backend.

See [protocol v0.4](Scientific_Protocol_v0.4.md) and the [research roadmap](Research_Roadmap.md) for the remaining pilot and confirmatory gates.
