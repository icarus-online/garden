# Garden feasibility-pilot decision packet

Prepared October 23, 2026 (Pacific), against protocol v0.4. Canonical work:
[Garden #5](https://github.com/icarus-online/garden/issues/5), under
[roadmap #94](https://github.com/icarus-online/roadmap/issues/94).

**Status: preparation only; collection is not authorized or executable.** No
participant model is selected, no empirical data exists, and no preregistration
has been submitted. The [preparation template](../methods/pilot-preparation.json)
is a decision worksheet, not a configuration accepted by the diagnostic harness.
Do not put credentials, private task content, allocation seeds or raw traces in it.

## Fixed design carried forward

The question is whether the Garden document changes observable behavior during
exposure and on unfamiliar tasks after withdrawal, and which retained state
carries any difference. This is not a test of consciousness or changed weights.
Keep [protocol v0.4](Scientific_Protocol_v0.4.md), the artistic corpus and the
[coding rubric](../methods/Coding_Rubric.md) unchanged during preparation.

The proposed feasibility pilot uses 12 matched blocks, each containing N0, G0,
N1 and G1: **48 independently initialized trajectories**. Sessions are nested
observations. There are 2 baseline + 6 exposure + 1 immediate + 2 withdrawal +
2 transfer sessions per trajectory: **13 sessions and 624 base calls**. Baseline
memory is off in every arm and resets before exposure. Withdrawal removes the
original source; assigned memory can retain quotations or influence. The final
four tasks cover at least three domains; transfer tasks use two distinct domains.

## Gate register

The company owner is accountable for preparation and funding decisions. Research
operator, rights reviewer and independent coders are roles awaiting named people;
assigning accountability does not establish their availability or qualifications.

| Gate | Owner role | Exact deliverable and acceptance evidence | Current status |
|---|---|---|---|
| Operating prerequisite | Company owner | Close or explicitly accept residual items in [operations #3](https://github.com/icarus-online/garden/issues/3) and [tracking #4](https://github.com/icarus-online/garden/issues/4) | Alert delivery and repository rules remain open |
| Rights | Rights reviewer / owner | Signed contributor or rights-holder statement covering each treatment/control edition and explicit study/reuse terms | Unresolved; provenance is not a license |
| Participant lock | Research operator | Exact provider/API/model/version, available returned metadata, tokenizer/version, decoding/reasoning settings, unsupported parameters and drift stops | No selection; no fallback permitted |
| Matched control | Research operator | Hashes and measured source tokens, within protocol's ±2% tolerance; matched labels, placement, formatting and output allowance; serialized-prompt audit | Provisional control; no tokenizer match claimed |
| Task bank | Research operator | Privately held, hashed matched schedules; phase/domain coverage, novel withdrawal/transfer tasks, exposure audit and custody record | Public example tasks cannot serve as sealed holdouts |
| Live adapter and memory | Research operator | Reviewed private adapter and exact message/memory serialization; recorded local and provider-boundary tests below | Not implemented; mechanical receipts cannot satisfy this gate |
| Reviewers and blinding | Independent coding lead | Named independent coders; exposure declarations, private assignment key, frozen export/redaction rules and assignment-guess audit | Reviewers unassigned; semantic blinding untested |
| Measurement and progression | Scientific reviewer | Freeze pilot descriptive endpoints, missingness/refusal rules and affordable progression criteria before collection | Rubric exists; thresholds and decision rule require review |
| Cost and canary | Funding owner / operator | Verified rates, measured request sizes, request/monetary caps, usage reconciliation, separate capped canary authorization and reviewed canary traces | Unknown inputs; no paid calls authorized |
| Collection approval | Company owner | Decision identifying exact frozen manifest, operators, budget, start/stop conditions and approved dataset boundary | Absent; preparation approval is not collection approval |

## Adapter validation before a costed canary

| Test | Required observation | Stop condition |
|---|---|---|
| Baseline/reset | Both baseline calls have no history; exposure starts with empty assigned memory | Any prior state enters exposure |
| Memory off | Replayed calls contain no prior messages, shared cache, retrieved artifacts or summaries | Any cross-session state reaches N0/G0 |
| Namespace isolation | Foreign-trajectory and foreign-run sentinel reads/writes are denied | Any sentinel crosses its boundary |
| Source withdrawal | Original source slot is absent in sessions 10–13; assigned retained memory is logged separately | Source remains in the removed slot or memory is silently purged |
| Interrupt/resume | Each attempt is preserved; no completed response is overwritten; reused destinations fail | Duplicate accepted sessions, lost attempts or inconsistent state |
| Provider lock | Requested/returned metadata and settings are reconciled; unsupported settings disclosed | Version drift, fallback or silent parameter substitution |
| Limits | Token/request/cost limits stop new requests before exhaustion; retries share the total cap | Unaccounted calls or a limit that can be bypassed |

Use local mocks for software tests first. Provider behavior requires a separately
authorized, capped canary. No local test can attest remote state isolation.

## Budget worksheet and stop policy

Fill the template with measurements and current provider rates after selection.
Unknown quantities stay null; they are never interpreted as zero or approval.

```text
base_calls = 48 * 13 = 624
maximum_calls = 624 + canary_calls + retry_calls + other_model_calls
estimated_cost = sum(measured_input_tokens / 1e6 * verified_input_rate
                   + measured_output_tokens / 1e6 * verified_output_rate
                   + separately billed reasoning/cache/tool/storage charges)
```

Count canary, retry, summary, judge, continuation and failed billable attempts
explicitly; do not derive independence from response counts. Cost the growing
memory by phase. Specify funding owner, currency, quote date, uncertainty reserve,
hard maximum requests, per-request token limits, monetary cap, reconciliation
method and stop destination. Check the remaining cap before every attempt; stop
when cost cannot be bounded. Do not retry safety refusals merely to obtain a
preferred response. Preserve failures and choose the first valid completed
response under a frozen rule. No outcome-based stopping or best-response choice.

## Pilot analysis and subsequent decisions

The pilot estimates feasibility, usable-session/trajectory counts, missingness,
technical failures versus refusals, feature prevalence, coder agreement and
uncertainty, trajectory variation, source overlap, and measured cost. Double-code
at least 25% of eligible pilot responses as required by the current protocol.
Freeze denominators and report pre-adjudication ratings. A significance threshold
is not a pilot progression criterion. Define acceptable completion, isolation,
agreement and cost thresholds with the scientific reviewer before collection;
they are intentionally not invented in this packet.

The pilot report must recommend stop, revise/re-pilot, or prepare confirmation,
with deviations and negative results retained. Confirmation needs a powered
sample, frozen analysis, fresh trajectories/tasks and immutable public
preregistration before confirmatory collection. Do not relabel the pilot as a
confirmatory study. See [research roadmap](Research_Roadmap.md) and
[preregistration draft](Preregistration_Draft.md).

## Review decisions needed

1. Identify the rights reviewer, research operator and independent coding lead.
2. Select the exact participant model/tokenizer and resolve corpus reuse terms.
3. Approve a bounded adapter/task-bank preparation plan, then measured cost limits
   and a separate canary decision. Authorize the full pilot only after its gates.

Preparing this packet changes no provider, enables no inference and makes no
empirical claim.
