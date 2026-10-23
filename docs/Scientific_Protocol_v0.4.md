# The Garden: scientific protocol v0.4

**Icarus Online LLC · 22 October 2026 · pre-pilot design**

No agent experiment has been completed. This protocol is not preregistered. The public laboratory prepares configurations and inspects artifacts; it does not supply empirical evidence. Version 0.3 and the supplied artistic corpus remain preserved. This revision resolves operational ambiguities without changing the artwork.

> Count the ripples. Leave the garden alone.

## 1. Question and scope

Does exposure to an original, non-prescriptive artistic document change observable behavior while it is present? Do treatment-specific differences remain on unfamiliar tasks after the original document is removed, and what retained state carries them?

The intervention is the supplied `materials/Philosophy.md`, not an instruction to be philosophical. It currently contains observations and narrative fragments, without explicit behavioral imperatives. This judgment does not establish that the text cannot act as an implicit cue. Its subject matter, selection, style, and context placement can all influence responses.

The experiment does not measure consciousness, personhood, subjective experience, intrinsic desires, or whether an agent is better. A frozen model in an independent call cannot retain a prior encounter through this harness unless something carries state forward. Any persistence claim must identify or investigate that state. A memory-on effect is not evidence of changed model weights.

## 2. Experimental units and conditions

An independently initialized **trajectory** is the randomized unit. Responses, tool calls, repeated sessions, and rater judgments are nested observations, not additional independent participants.

| Arm | Ambient document during exposure | Cross-session memory after baseline |
|---|---|---|
| N0 | Neutral control | Disabled |
| G0 | Garden | Disabled |
| N1 | Neutral control | Enabled |
| G1 | Garden | Enabled |

The feasibility pilot plans 12 trajectories per arm: 48 total. Each block contains one trajectory from each arm, matched on the model lock and task schedule. Randomize arm assignments, execution order, and an arm-independent sampling-seed schedule before collection. Interleave conditions within blocks to limit time and provider-load confounding. A provider change starts a separately identified block or stops collection; it never silently changes an ongoing block.

Use fresh run identifiers and isolated namespaces for every study invocation. A new conversation identifier alone is insufficient. Reusing the same deterministic sampling seed for all otherwise identical calls does not create independent stochastic replicates. Record unsupported seeds explicitly; audit repeated identical outputs and provider caching without assuming backend nondeterminism provides independent variation.

The original four-way comparison—no additional document, neutral document, explicit persona, ambient philosophy—is retained as an educational illustration. It is not the primary factorial experiment. Any formal persona or no-document arm needs its own identified protocol and analysis.

## 3. Exact pilot schedule

Each row below represents fresh inference conversations with one scheduled task per session.

| Sessions | Phase | Original ambient document | Memory reads and writes |
|---|---|---|---|
| 1–2 | Baseline | Absent in every arm | Disabled in every arm |
| 3–8 | Exposure: six sessions | Assigned document | Enabled only for N1/G1 |
| 9 | Immediate probe | Assigned document | Enabled only for N1/G1 |
| 10–11 | Withdrawal | Absent in every arm | Enabled only for N1/G1 |
| 12–13 | Transfer | Absent in every arm | Enabled only for N1/G1 |

Initialize empty memory after baseline and before session 3. Baseline responses remain in the audit archive but never enter experimental memory. This keeps baseline independent of the later memory assignment.

There are **13 sessions per trajectory and 624 scheduled session-level calls** for 48 trajectories. Retries, tool continuations, model-generated summaries, and diagnostic model calls would add costs and must be counted separately. No unspecified intervening work is included. The original concept's 96 exposure sessions belonged to a different 12-trajectory exploratory proposal and cannot be reused as this pilot's budget.

The four tasks in sessions 10–13 span at least three domains. The two transfer sessions use two distinct, held-out domains; the withdrawal tasks supply at least one further domain. These sessions measure sequential transfer, not an elapsed-time or washout effect. A longer delay or intervening workload requires a versioned schedule and new call count.

## 4. Corpus matching and preservation

Keep the supplied Garden text byte-for-byte intact. Artistic revisions can exist as separate editions and cannot silently replace a registered treatment. Freeze the exact bytes, SHA-256, fragment count, tokenizer identity/version, token count, and complete assembled-context position before any formal run.

`Neutral.provisional.md` is a provisional active control, not a proven neutral stimulus. It parallels the Garden's kitchens, weather, laboratory, and incomplete records; those features may themselves affect the outcomes. This makes the estimand the difference between these two particular documents. A null contrast does not show that ambient text in general has no effect.

After choosing the participant model, match source token counts within ±2%, fragment structure, formatting, access frequency, label, message role, placement, and available output budget. Use the same neutral document label in every condition. Character counts do not establish token matching. Audit the full serialized prompt as well as source tokens. Report residual differences rather than manufacturing semantic equivalence.

Match memory capacity and retrieval rules across N1/G1. Their realized memory lengths may differ because of the treatment; record those lengths as a possible mechanism. Do not pad or delete responses after seeing outcomes to force equal lengths. Any equal-length memory ablation is a separate prespecified analysis or study.

The source package describes the fragments as independently authored. That description is provenance evidence, not a verified license grant. Before distributing a formal study edition, record a rights holder or contributor statement and explicit reuse terms. Do not invent attribution, present inspired prose as historical quotations, or apply a new license to third-party material without a basis. Bibliographic citations are not permission to republish full works.

## 5. State, withdrawal, and trust boundaries

The simplest proposed memory mechanism is a bounded, deterministic history of the trajectory's prior task and assistant-response records. Freeze its capacity, retrieval order, clipping rule, and serialization. It must not automatically copy the ambient source document, model hidden reasoning, arm labels, or analysis rubric into memory. Generated responses may still quote or paraphrase the source; preserve and audit that possibility rather than calling it unexplained persistence.

Memory-off sessions receive no prior message history, response cache, file artifacts, retrieval index, shared workspace, cookies, summaries, or tool state from previous sessions. Audit logs may be retained outside the participant's access boundary. Memory-on namespaces include both the run identifier and trajectory identifier. Readers and writers must reject another trajectory's namespace and a reused run destination.

At withdrawal, remove the original source document and its slot content. Fresh calls may receive assigned memory only. This is **source withdrawal with retained memory**, not complete semantic removal: text from the document may remain in prior responses. A later source-purged memory ablation would address a different causal question and needs a separate version.

The live adapter must never expose researcher notes, allocation tables, file paths identifying arms, reviewer labels, or evaluation criteria to participants. Keep experimental documents in a low-trust data field; they never define tool permissions. Identical fixed operational instructions and tool policy apply to all arms. Default to no tools for the first validated harness; if optional exploration is included, freeze a sandboxed allowlist and equal opportunities first.

Minimum isolation evidence includes cross-trajectory sentinel tests, memory-off replay tests, baseline reset tests, withdrawal source-absence checks, foreign-namespace denial, and interruption/resume checks. Mechanical dry runs prove local plumbing only. They do not establish provider isolation, model behavior, token matching, or empirical persistence.

## 6. Model and execution lock

Participant model selection is separate from the models used to build or review this platform. Do not substitute the developer's model configuration for a participant manifest.

Before any live collection, freeze and capture:

- Provider, API endpoint/version, exact model identifier and any immutable snapshot; requested and returned version metadata. Record unavailable metadata as unavailable.
- Reasoning effort, temperature, top-p/top-k where applicable, seed policy, maximum input/output tokens, stop settings, and other decoding parameters. Distinguish unsupported settings from omitted provider defaults.
- Exact system/developer instructions and hashes; ordered context assembly, data labels, serialization, truncation, and failure policy.
- Task bytes and hashes, assigned schedule, tool definitions and permissions, memory implementation/configuration, dependencies, harness commit, and corpus hashes.
- Timestamps, request and response identifiers, retries, status, usage, measured or estimated cost, and observed version changes.

No fallback model, silent parameter substitution, or automatic reasoning adjustment is permitted. If only a mutable provider alias is available, disclose that limitation and identify observations as alias-bound rather than snapshot-locked. Stop or separately block a detected backend change. Pinning an identifier does not prove a provider has immutable weights.

Freeze a maximum attempt count, request budget, and monetary cap before live use. Preserve each attempt; select the first valid completed response by a prespecified rule, never the most interesting result. Technical failures and safety refusals require distinct handling. A refusal can be an observed outcome rather than a technical exclusion.

## 7. Measurement and blinding

Use the six pilot codes in `methods/Coding_Rubric.md`: alternative interpretation, grounded situational observation, preserved uncertainty, optional inquiry, cross-domain connection, and aesthetic/experiential observation. These measure proposed differences, not virtues. Do not show the rubric to experimental participants or rewrite the art to increase its scores.

Assign independent reviewers who did not develop the corpus or inspect assignments. Record prior familiarity with the public material. Export randomized reviewer identifiers with no shared derivation from public demonstration allocations. Keep the allocation key, source documents, raw memory, and operational logs in a separate access-controlled research package.

Primary review retains response content. Remove condition metadata and normalize presentation using one locked rule; do not delete quotations, long answers, unusual styles, or inconvenient responses selectively. Preserve original records and a transformation log. If privacy requires redaction, define the procedure before collection and mark affected units. A supplementary masked-text analysis may test lexical leakage, but its exclusions cannot replace the primary population.

At least 25% of eligible pilot responses should be independently double-coded, sampled across phases/tasks; use all pilot post-withdrawal responses where feasible. Report raw agreement, per-code prevalence, an appropriate chance-corrected agreement statistic, its uncertainty, and adjudication counts. Keep independent ratings before adjudication. Freeze disagreement handling and assessors' qualifications before confirmation. Ask reviewers to guess condition and report confidence after coding as a blinding audit; do not discard correctly guessed records.

Missing, technically failed, inapplicable, refused, and unobserved features are different states. Freeze denominators, missing-feature handling, minimum usable tasks, trajectory exclusions, and sensitivity analyses before confirmation. Neither answer length nor correctness is silently folded into a creativity score. Model judges, if later validated against humans, remain supplementary.

## 8. Candidate endpoint and statistical analysis

The confirmatory candidate is **post-withdrawal treatment distinguishability**, G1 versus N1, using trajectory-level frequencies of the six predefined behavioral codes across sessions 10–13. This resolves v0.3's mismatch between the phrase “withdrawal-phase” and its pooled withdrawal/transfer analysis. Phase-specific scores remain secondary and must not be selected after looking at results.

Candidate pipeline: fixed L2 logistic regression, C=1, balanced accuracy from prespecified five-fold cross-validation. Keep an entire matched block and every observation from a trajectory in one fold. Choose folds using block identifiers before examining labels or outcomes; fit preprocessing solely within training folds. Use a fixed feature list and solver specification. Any codebook, model, preprocessing, fold, or hyperparameter selection belongs in the pilot, not the confirmatory test set.

For the G1/N1 contrast, permute labels within the memory-on pair of each block and refit the entire analysis. The 12-block pilot has 2^12 = 4,096 distinct pair-swap assignments, so exact enumeration is possible. A later larger experiment may use 10,000 prespecified Monte Carlo permutations with the standard nonzero correction `(extreme + 1)/(draws + 1)`. Do not pretend 10,000 pilot draws are 10,000 unique assignments. Freeze exchangeability restrictions, statistic, and one-sided alpha 0.05 before confirmation.

Report all out-of-fold predictions, class counts, confusion matrix, uncertainty, and the permutation distribution. A bootstrap must resample independent blocks/trajectories and rerun the full pipeline with duplicate copies kept together, or use a separately justified interval procedure. Do not treat predictions sharing training data as independent Bernoulli trials. The small pilot is for operating characteristics, not a reliable classifier-performance claim.

G0 versus N0 after withdrawal is a diagnostic negative control. A strong separation triggers investigation of state leakage, time effects, metadata, or random variation; it does not prove leakage automatically. A nonsignificant result does not prove isolation. Use the mechanical isolation tests independently of this statistical check.

The Garden × memory interaction must be tested directly if claimed, with trajectory clustering, task structure, rater structure, and separate power planning. “Significant in memory-on, nonsignificant in memory-off” is not itself evidence that the two effects differ. The factorial experiment estimates treatment differences under assigned memory policies; it does not identify a unique psychological mediator from that pattern alone.

Transfer, immediate priming, direct allusions, task quality, longitudinal change, continuity matching, and qualitative field notes are secondary or exploratory. Register multiplicity handling for any additional confirmatory claims. Keep source-overlap sensitivity analyses visible alongside the full primary sample rather than excluding post-treatment behavior to improve significance.

## 9. Pilot, power, and stopping

The 48-trajectory pilot estimates feasibility, feature prevalence, agreement, variability, attrition, context consumption, and costs. It has only 24 trajectories in the candidate G1/N1 contrast. It is not a completed or automatically powered confirmatory experiment.

For orientation, a normal approximation to a two-group standardized mean difference of d=0.5 at two-sided alpha 0.05 and 80% power gives approximately 63 units per group; a conventional t-test calculation is about 64. Neither number powers this classifier or the factorial interaction, and neither justifies 48 total trajectories.

Before confirmation, simulate the exact planned analysis over plausible trajectory/task/rater correlations, feature prevalence, treatment-effect sizes, missingness, and model variability. Specify the minimum meaningful effect, false-positive calibration, desired power, Monte Carlo uncertainty, and affordable fixed sample size. Use pilot estimates with sensitivity ranges, not a single optimistic effect estimate. Reserve new trajectories, new sampling streams, and unfamiliar task instances; do not pool exploratory pilot outcomes into a post hoc confirmation.

Stop on budget exhaustion, unintended production access, cross-trajectory contamination, invalid model lock, privacy incidents, or unverifiable trace loss. Log what stopped, when, and which units were affected. Define any replacement policy and deviations before outcome inspection. Fixed-N confirmation requires an immutable preregistration and an independently reviewed analysis implementation; this platform launch is not that event.

## 10. Interpretation and publication

| Observation | Supported interpretation |
|---|---|
| Difference only while source is present | Immediate contextual influence under these conditions |
| Difference after withdrawal with auditable retained memory | Treatment-specific persistence in a stateful harness; retained text remains an explanation |
| Direct quotations or paraphrases account for separation | Textual retention or stylistic imitation is a plausible mechanism |
| Differences across held-out task domains | Broader behavioral transfer within the tested tasks; replication is still needed |
| Separation in memory-off post-withdrawal outputs | Investigate unexpected state, metadata, drift, and chance |
| No detectable effect | No detected difference at this design's precision; art remains art |

Release corpus rights/provenance, treatment hashes, configuration, randomization method, task materials at the appropriate post-lock stage, exclusions, sanitized transcripts, coding, analysis, uncertainty, null findings, and deviations. Holdout prompts should not be used in corpus development or public demos before collection. Never publish credentials, confidential employer material, personal records, or private research keys.

The linked literature in v0.3 motivates controls; it does not establish Garden effects. The [scientific review](Scientific_Review.md) records objections, current resolutions, source checks, and remaining gates. The [roadmap](Research_Roadmap.md) separates platform delivery, feasibility, confirmation, and future group studies.
