# The Garden - preregistration checklist (DRAFT)

Status: Template only. No preregistration has been submitted.

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
Lead investigator / affiliations:
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
