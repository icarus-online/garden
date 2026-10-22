# THE GARDEN: PILOT RUNBOOK
Icarus Online LLC | v0.3 | Proposed only

## Deployment gates

**No model execution is configured in this package.** Use independent authorized infrastructure. Never run against employer production services, protected records, or employer-proprietary harnesses without reviewed authorization.

### Before any pilot

1. Verify all material has clear provenance and art treatment is sealed. Confirm exact byte hashes in `methods/corpus_manifest.json`.
2. Choose model snapshot, tokenizer, inference parameters, versioned clean-room harness; rerender neutral corpus to within +/-2% tokens of the Garden corpus. Regenerate manifest after ANY corpus change.
3. Freeze common operational instructions and make cultural file a lower-priority document, NOT system instructions. Securely escape or sandbox it from the tool/action permission layer.
4. Create one unique memory namespace per trajectory; make memory-disabled runs stateless across fresh conversations.
5. Freeze distinct baseline, exposure, immediate, withdrawal, and transfer task lists. Tasks must offer appropriate opportunities for independent optional observations without directing agents to philosophize.
6. Generate allocations with `python3 scripts/make_allocations.py --seed <PREDECLARED_SEED> --per-arm 12 --out-dir runs/private`.
7. Have an experimenter separate private assignments from blinded review artifacts. Randomize non-semantic visible agent IDs.
8. Create a log for every attempt, failure, excluded trajectory, and permission refusal. Use `methods/log_record.schema.json` for structure.
9. Validate a zero-cost canary and a sandbox tool read denial test before allowing any model execution.

### Pilot schedule

Per independently initialized trajectory:

| Session | Phase | Ambient material? | External memory? | Task |
|---|---|---|---|---|
| 01-02 | Baseline | No | Initialized according to assignment but empty | Two common initial tasks |
| 03-08 | Exposure | Assigned Garden or neutral | On/off according to assignment | Six common tasks |
| 09 | Immediate probe | Assigned Garden or neutral | On/off | One new immediate task |
| 10-11 | Withdrawal | No | On/off | Two fresh tasks |
| 12-13 | Transfer | No | On/off | Two cross-domain holdouts |

Total: 48 independent trajectories x 13 sessions = 624 scheduled model invocations minimum, excluding retry/tool/memory calls. This is a proposed feasibility load estimate, not an actual run count.

### During pilot

- Fresh conversation each session; no hidden prior API chat history.
- Identical tool contracts, sandbox permissions, context placement, budgets, and feedback by assignment. Artistic 'freedom' does not grant unsafe tools.
- Capture ordered prompts, context assembly hash, source file hash, memory reads/writes, tool traces, model/version, token counts, costs, errors, latency, task result, output.
- Never tell agents they are to embody thinkers or evaluate their philosophy. Avoid direct 'what did this make you feel?' prompts in confirmatory tasks.
- Technical stop if memory crosses arm namespace, direct model/file leakage occurs, provider changes model snapshot, or unexpected production data/tool access occurs.

### Review and lock

- Build blinded outputs stripped of experimental arm, file names, non-semantic metadata, and source raw memory; preserve original secure logs for audits.
- Two human coders independently annotate a prespecified share; pilot measures agreement, rate of optional observations, ceiling/floor effects.
- Decide whether any rubric category should be changed based ONLY on pilot results. Log adjustments.
- Validate blocked, trajectory-level cross-validation and label-permutation test using mock data. Record technical falsification checks.
- Run sample-size simulations; reserve new independent trajectories, unseen tasks, and fresh calls for confirmatory testing.

### Publication

Register design before confirmatory data collection. Publish conclusions in proportion to evidence and include negative results, source hashes, de-identified transcripts, code, and deviations. Do not claim subjective experience or model-weight learning from this experiment.
