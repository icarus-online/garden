# The Garden: pilot preparation runbook

**Icarus Online LLC · v0.4 draft · 22 October 2026**

No experimental participants or empirical results exist. The current toolkit implements a local mechanical diagnostic adapter. It has no live inference adapter. Its receipts are software test records, not agent responses, and cannot satisfy the formal pilot prerequisites below.

The current protocol is [Scientific Protocol v0.4](../docs/Scientific_Protocol_v0.4.md); v0.3 remains preserved history. The [toolkit guide](../research/README.md) documents the executable diagnostic contracts.

## Exercise the toolkit without inference

From the repository root, use a fresh output directory:

```sh
python3 -m research validate research/configs/dry-run.example.json
python3 -m research run research/configs/dry-run.example.json --out runs/demo
python3 -m research verify runs/demo
python3 -m research blind runs/demo --out runs/review --key-out runs/reviewer-key_PRIVATE.json
```

The checked-in fixture is explicitly diagnostic. The run records mechanical receipts with null participant responses. Verification checks integrity, scheduling, and local state behavior; it cannot establish model effects, provider isolation, human agreement, or corpus token matching. Keep private reviewer mappings separate from review packets. Follow the toolkit's explicit lock procedure when preparing a new configuration; do not silently regenerate a lock after collection.

## Before any live pilot

1. Confirm independent Icarus infrastructure and data. Do not use employer code, customer/health records, proprietary prompts, or production tools without separate authorization.
2. Record the Garden corpus's provenance and reuse terms. Preserve source bytes. Choose a participant model and tokenizer; match the neutral document within ±2% tokens and document all residual differences.
3. Freeze provider/model/snapshot metadata, reasoning, sampling, seed policy, instruction bundle, context assembly and truncation, tools, dependencies, memory, task files, and hashes. Treat unknown or unsupported settings explicitly. Never enable fallback.
4. Implement and validate the live provider adapter. Confirm that the requested settings are accepted, returned metadata is captured, drift stops are effective, and a request/monetary cap is enforced before the full pilot.
5. Freeze task schedules and arm-independent inference/execution seeds. Keep transfer instances out of calibration, corpus development, and public demonstrations.
6. Initialize one namespace per run and trajectory. Prove that memory-off receives no previous history or artifacts, baseline cannot write memory, foreign namespaces are denied, and source content is absent after session 9. Keep audit logs outside the participant boundary.
7. Specify deterministic memory retention, retrieval, clipping, and serialization. Formal memory holds prior task/response records; it does not directly copy the source or researcher metadata. The existing diagnostic receipt memory is not that formal implementation.
8. Freeze retries, first-valid-response selection, technical failure/refusal distinctions, missingness, exclusions, technical stops, and the complete trace contract. Preserve every attempt.
9. Assign independent human reviewers; seal assignments and keys; freeze presentation/redaction rules and the blinding audit. Never reuse public demonstration mappings as formal reviewer IDs.
10. Review a small authorized and budgeted live canary before the 48-trajectory pilot. A zero-inference dry run cannot replace it.

## Exact session schedule

| Session | Phase | Ambient document | Memory |
|---|---|---|---|
| 01–02 | Baseline | Absent in all arms | No reads or writes in any arm |
| 03–08 | Exposure | Assigned Garden or neutral | Assigned on/off |
| 09 | Immediate probe | Assigned Garden or neutral | Assigned on/off |
| 10–11 | Withdrawal | Absent in all arms | Assigned on/off |
| 12–13 | Transfer | Absent in all arms | Assigned on/off |

Initialize empty memory after session 2. Use one task per fresh conversation. No uncounted intervening work is scheduled. The last four tasks cover at least three domains, with two distinct held-out domains in transfer.

**48 independent trajectories × 13 sessions = 624 scheduled session calls minimum.** Count retries, continuation/tool calls, summaries, and canaries separately. This is a plan, not a completed run count.

## During a live pilot

Interleave arms within blocks. Apply identical model settings, instructions, tools, context placement, and response limits. Never tell agents to embody an influence, inspect their philosophical development, or optimize the coding rubric.

Retain ordered inputs, source/task/context hashes, all memory reads/writes, namespace checks, output, tool activity, versions, timestamps, attempts, usage, costs, latency, errors, and exclusions. Keep dataset status distinct from diagnostic fixtures. Stop on cross-trajectory state, invalid model lock, budget exhaustion, unapproved production access, privacy incident, or lost trace integrity.

Source withdrawal preserves assigned memory. Audit direct quotations and paraphrases. Do not describe this as source-free memory or model learning.

## Review and prepare confirmation

Produce blinded packets with randomized labels and no assignments, raw memory, or condition-revealing operational metadata. Preserve response content and private originals. Double-code a prespecified portion; retain independent ratings and report agreement, prevalence, uncertainty, adjudication, and blinding guesses.

Aggregate primary candidate features over sessions 10–13 by trajectory. Keep blocks intact in folds and pair-swap permutations; do not count sessions as independent participants. Use pilot results for feasibility and instrument calibration only. Freeze exact analysis choices and run tailored sample-size simulations before preregistration and new confirmatory data.

Publish proportionate claims, null findings, costs, sanitized artifacts, and deviations. Platform delivery is not experimental completion.
