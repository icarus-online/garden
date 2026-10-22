# Icarus Online LLC / The Garden - preregistration checklist (DRAFT)

Status: Independent project draft; NO preregistration has been submitted; no experiment results exist.

## Minimum lock-in before confirmatory runs

- [ ] State one confirmatory question and the precise null hypothesis.
- [ ] Freeze ambient Garden and neutral corpora (SHA-256 + tokenizer counts), or predefine a fixed set of variants.
- [ ] Freeze all four arms and how external memory is enabled/disabled.
- [ ] Freeze independent randomization unit = agent trajectory; assign memory namespace per trajectory.
- [ ] Freeze one foundation model snapshot and inference settings for primary analysis.
- [ ] Freeze the standardized exposure task order and unseen withdrawal task set.
- [ ] Validate and freeze the behavioral annotation rubric using pilot data ONLY.
- [ ] Freeze the classifier feature set, cross-validation design, permutation test, alpha, and interval method.
- [ ] Specify a power simulation and minimum meaningful effect; choose a fixed confirmatory N.
- [ ] Lock per-run tool permissions, token budgets, and safety stops.
- [ ] Blind annotators and exclude condition labels, file names, and raw memory from judgments.
- [ ] Validate no cross-session context in memory-off arms and no cross-arm contamination.
- [ ] Define direct-allusion leakage checks and an evidence threshold for rejecting a 'persistence' interpretation.
- [ ] Define exclusions and missing data procedures before unblinding.
- [ ] Register with OSF or archive an immutable, timestamped git commit / signed release.
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
