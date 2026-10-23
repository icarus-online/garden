# Icarus Online LLC / The Garden - preregistration checklist (v0.4 DRAFT)

Status: Independent project draft; NO preregistration has been submitted; no experiment results exist.

Current design: [Scientific Protocol v0.4](Scientific_Protocol_v0.4.md), 22 October 2026. The diagnostic toolkit is not a live participant adapter. This checklist is neither a registration nor authorization to begin paid inference.

## Minimum lock-in before confirmatory runs

- [ ] State one confirmatory question and the precise null hypothesis.
- [ ] Freeze ambient Garden and neutral corpora (SHA-256 + tokenizer counts), or predefine a fixed set of variants.
- [ ] Freeze all four arms and how external memory is enabled/disabled.
- [ ] Freeze the 13-session schedule: 2 baseline, 6 exposure, 1 immediate, 2 withdrawal, 2 transfer. Disable all baseline memory reads/writes and initialize empty memory before session 3.
- [ ] Freeze independent randomization unit = agent trajectory; assign memory namespace per trajectory.
- [ ] Include run ID in each namespace; freeze execution-order and arm-independent sampling-seed schedules. Keep audit logs inaccessible to participants.
- [ ] Freeze one foundation model snapshot and inference settings for primary analysis.
- [ ] Record exact provider/API/model metadata, reasoning effort, sampling settings and unsupported values; prohibit fallback and specify drift stops. Disclose mutable aliases and unavailable snapshot information.
- [ ] Freeze the standardized exposure task order and unseen withdrawal task set.
- [ ] Validate and freeze the behavioral annotation rubric using pilot data ONLY.
- [ ] Freeze the classifier feature set, cross-validation design, permutation test, alpha, and interval method.
- [ ] Name the endpoint post-withdrawal distinguishability and fix sessions 10–13. Keep matched blocks intact in folds; fit preprocessing only on training data. Permute G1/N1 within pairs and refit the full pipeline.
- [ ] Specify exact enumeration when feasible (4,096 pair swaps for 12 blocks), otherwise prespecified Monte Carlo draws with nonzero correction. Account for shared training data in uncertainty intervals.
- [ ] Plan a direct factorial interaction test before claiming memory modifies the treatment effect; do not compare significance labels across arms.
- [ ] Specify a power simulation and minimum meaningful effect; choose a fixed confirmatory N.
- [ ] Lock per-run tool permissions, token budgets, and safety stops.
- [ ] Blind annotators and exclude condition labels, file names, and raw memory from judgments.
- [ ] Validate no cross-session context in memory-off arms and no cross-arm contamination.
- [ ] Define direct-allusion leakage checks and an evidence threshold for rejecting a 'persistence' interpretation.
- [ ] Define exclusions and missing data procedures before unblinding.
- [ ] Distinguish missing, failed, refused, inapplicable, and unobserved features; freeze denominators, retries, first-valid-response selection, replacements, and complete attempt accounting.
- [ ] Register with OSF or another suitable immutable public registry before confirmation; additionally archive exact commits/releases. Do not describe an ordinary editable document or Git tag alone as a completed registry submission.
- [ ] Prepare public release of methods, redacted trajectories, code, and null results.

## OSF style fields

Study title:
Lead investigator / affiliation: Icarus Online LLC (verify actual study personnel prior to registration)
Preregistration URL and registration date:
Research question:
Independent experimental unit:
Eligibility and exclusions:
Arms and assignment probability:
Randomization seed and blocking variables:
Experimental materials (hashes):
Model snapshot / harness commit:
Episode/task sequence:
Primary endpoint:
Null hypothesis and alternative:
Analysis code commit / frozen container version:
Statistical test / permutation restrictions:
Alpha / multiplicity handling:
Sample size, power simulation, fixed stop rule:
Missing data and deviation handling:
Human annotation rubric / blinding plan:
Safety and privacy controls:
Data sharing plan:
Exploratory analyses (explicitly labeled):

## Candidate core claim, conditional on data

'In a randomized controlled harness experiment, ambient, non-instructional cultural text produced detectable changes in agent behavior on unseen tasks [only if true], with persistence linked to externally stored trajectory memory [only if supported]. The study does not establish consciousness or intrinsic values.'

## Required legal and operational gates

- [ ] Independently host the clean-room test harness; confirm no unauthorized Soberlink IP, employer accounts, protected health data, or production tools.
- [ ] Record the exact copyright status and provenance of every treatment fragment.
- [ ] Document the distinction between art and research instruments; freeze scientific editions without optimizing them for a favorable outcome.
- [ ] Confirm the sample-size/power design uses independent TRAJECTORIES, not individual model messages as pseudoreplicates.
- [ ] Freeze the primary factorial 2x2 separately from no-file / persona exploratory galleries.
- [ ] Document the neutral corpus token matching using the pinned model tokenizer (not merely characters).
- [ ] Log technical stop criteria, withdrawals, model revisions, and missing outcomes before unblinding.
- [ ] Reserve blinded assessors who did not edit the corpus or choose memorable samples.
- [ ] Record assessors' prior exposure; double-code at least 25% of eligible pilot responses; preserve pre-adjudication ratings and report agreement, prevalence, uncertainty, and post-coding assignment guesses.
- [ ] Preserve all primary response content. Define metadata redaction separately from supplementary source-overlap masking; do not selectively exclude quotations after treatment.
- [ ] Explain that withdrawal removes the original document, not source-derived content retained in assigned memory.
- [ ] Keep diagnostic receipts and public demonstrations in separate artifact classes, never in the empirical dataset.
- [ ] Freeze a live inference budget/cap and validate real provider isolation before collection. Local dry-run success is insufficient.
