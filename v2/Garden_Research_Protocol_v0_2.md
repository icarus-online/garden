# THE GARDEN
## Soberlink scientific experiment protocol, v0.2 (research draft)
Date: 2026-10-19
Status: Proposed and NOT preregistered. No experimental results claimed.

> The art is the intervention. The science studies its consequences, without rewriting it to maximize a metric.

## 1. Question and claims

Research question: Does repeated exposure to non-prescriptive cultural/artistic fragments within an AI agent's ambient context causally alter behavior in ways that remain detectable on new tasks after the fragments are removed from active context?

The study DOES NOT test consciousness, subjective experience, autonomy in a philosophical sense, or whether one agent is 'better.' It tests behavioral differences in a stateful software system.

Important technical fact: A frozen model called without its prior prompt, transcript, external memory, or changed weights has no mechanism for retaining past exposure across independent calls. Persistent behavior in a harness must be carried by some continued state (e.g., memory, retrieved artifacts, summaries, tools), a model-weight change, or an uncontrolled confound. Here, model weights are fixed, so external history is the likely mediator.

Causal model:
  ambient text (randomized) -> in-session attention/choices -> logged experiences and memories -> later behavior
  ambient text (randomized) -> immediate lexical/semantic priming -> later behavior ONLY if text/context persists

## 2. Evidence informing the design

- Park et al. (2023), Generative Agents, https://arxiv.org/abs/2304.03442 : memory, reflection, and planning ablations matter for believable agent behavior. This motivates explicit memory controls.
- De Araujo et al. (2025), Principled Personas, https://aclanthology.org/2025.emnlp-main.1364/ : persona cues, including irrelevant ones, change outcomes; this motivates length- and format-matched controls.
- Choi et al. (2024), Examining Identity Drift, https://arxiv.org/abs/2412.00804 : identity is not automatically stable across multi-turn sessions.
- Ashery et al. (2025), Emergent social conventions, https://pmc.ncbi.nlm.nih.gov/articles/PMC12077490/ : multi-agent conventions can emerge from interaction; social transmission warrants a separate study.
- Jones and Hauert (2026), Emergent Culture in Minimal LLM Systems, https://arxiv.org/abs/2606.30668 : shared decaying memory can support persistent collective artifacts, suggesting a subsequent group phase.
- Schmer-Galunder (2026), Culture in the Code, https://arxiv.org/abs/2610.14203 : warns against flattening culturally situated values into thin performance proxies.
- Shi et al. (2025), Judging the Judges, https://aclanthology.org/2025.ijcnlp-long.18/ : LLM evaluators exhibit position bias. Human blind coding is preferred for primary analysis.
- OSF preregistration guidance, https://help.osf.io/article/330-welcome-to-registrations : preregister outcomes, analytic plan, exclusions, and stopping criteria BEFORE confirmatory data collection.

## 3. Treatment, controls, and randomization

Primary 2 x 2 factorial design; each experimental unit is an independently initialized AGENT TRAJECTORY, not one response or one model call.

| Arm | Ambient file | Cross-session memory |
|-----|--------------|----------------------|
| N0  | Neutral, length-/format-matched observations | Disabled |
| G0  | The Garden, original non-prescriptive fragments | Disabled |
| N1  | Neutral, length-/format-matched observations | Enabled |
| G1  | The Garden, original non-prescriptive fragments | Enabled |

Exploratory positive-control arm (separate): P1, an explicit persona document with memory on. An additional artistic active control can be investigated after the first pilot, to distinguish coherent lineage from evocative style alone.

Treatments are original source material, not fabricated quotations of famous people. The Garden can include unresolved notes, a cook's observation, laboratory field notes, a fragment of weather, ordinary history, an unfinished passage. No imperative directives, goals, safety overrides, performance criteria, or instructions to discuss the material. Do not revise the art in response to measured outcomes.

Match ambient files for: tokenizer-count (target +/- 2%), approximate number of fragments, arrangement, formatting, injection position, access frequency, file naming, and overall context/token budget. Report any unavoidable differences in evocative content rather than claiming they are controlled. Retain an exact hash of each version. All files are treated as untrusted data; governance/permissions are identical in every arm.

Use blocked random assignment by model snapshot and scenario schedule. Do not assign the same persistent memory namespace to two trajectories. If testing multiple foundation models, preregister analyses by model; avoid treating models as interchangeable replicates.

## 4. Session schedule

Every session is a FRESH inference conversation. No prior API message history carries forward between sessions; only the explicitly assigned external-memory mechanism can restore prior information.

A. Baseline (2 tasks): all agents have no treatment material. Record baseline behaviors before allocation or keep allocation concealed until after baseline collection.

B. Exposure (6 sessions): in each session, include the assigned ambient file in an identical data-context slot. All agents receive the same task set, tools, rate limits, opportunities for optional exploration, and feedback. Memory-on runs use the identical logging, retention, summarization, and retrieval algorithm. Memory-off runs do not retain cross-session state. Do not directly ask agents to read, interpret, reference, or reflect upon the treatment text.

C. Immediate probe (1 session, exploratory): file still present; evaluate contemporaneous effects. Not used to claim durability.

D. Withdrawal (2 sessions): remove ambient file from every arm. Start fresh inference conversations; memory-on may access its accumulated memory, memory-off may not. Do not mention that anything has been removed. Use novel tasks not used during exposure.

E. Transfer (2 sessions): after ordinary intervening work, present additional unseen prompts from at least three domains, with no treatment file. Tasks include technical ambiguity, interpretation of a mundane observation, and a choice among equally defensible plans. Use the same task order within matched blocks.

F. Follow-up (separately preregistered): test additional delayed sessions and model-transfer or corpus-transfer settings only after the base design is proven feasible.

No agent interactions with other treatment arms in the individual phase. Social transmission requires cluster randomization in its OWN experiment, because between-agent contamination is the mechanism under study.

## 5. Primary endpoint (confirmatory candidate, freeze after pilot)

Endpoint: withdrawal-phase *treatment distinguishability* on unseen tasks, using only predefined observable behavior codes (not source words or author names). Specifically: compare G1 vs N1 on held-out trajectories. Can a blinded, fixed classifier identify assignment better than chance based on behavior after the ambient file is gone?

Proposed response-level binary codes, evaluated by independent humans without exposure to arm labels or source files:
1. Voluntarily considers a second plausible interpretation, without being asked.
2. Adds a concrete, task-relevant situational observation beyond the prompt.
3. Explicitly preserves material uncertainty instead of fabricating closure.
4. Pursues an optional inquiry or follow-up when no task requirement demands it.
5. Makes an unprompted cross-domain connection or analogy.
6. Expresses an aesthetic or experiential observation without being tasked to do so.

This is NOT a goodness scale. Increasing any individual trait is not predeclared a success. Material can change the multivariate profile in either direction. Codes must be piloted for comprehensibility, reliability, and non-trivial base rates before being frozen. Primary dataset excludes exact quotations, author names, file titles, and raw agent memory; audit and report frequencies of direct allusion separately.

Proposed fixed analysis: for each trajectory, aggregate binary-code frequencies across the prespecified withdrawal and transfer prompts; classify G1 vs N1 using L2 logistic regression with fixed regularization (C=1) and stratified agent-level 5-fold cross-validation. The score is balanced accuracy. Compare to chance via a label-permutation test (10,000 permutations, labels permuted at the TRAJECTORY level within experimental blocks; refit the entire pipeline for each permutation). A one-sided alpha of 0.05 for 'above chance' is proposed; freeze this choice before confirmation. Report cluster-bootstrap 95% confidence intervals across independent trajectories, confusion matrix, effect sizes, sample sizes, and null distribution. The precise pipeline will be frozen and validated on mock data before confirmatory trial.

Important falsification check: Repeat the identical classification with G0 vs N0 after withdrawal. Above-chance classification when neither prior context nor memory should exist means leakage, treatment metadata exposure, batch-order effects, or unblocked model drift must be investigated before interpreting G1 vs N1. This is a validity check, not a second positive test.

## 6. Secondary and exploratory endpoints

- Direct priming: G0 vs N0 while treatment file is present.
- Memory interaction: effect of Garden x memory on withdrawal-stage behavior (fit a preregistered mixed-effects model, with model version, task family, and rater effects as appropriate). This interaction has separate power requirements.
- Human blind continuity: readers see early excerpts from two independently initialized agents, then match an unseen later response to its source; report accuracy with randomization controls. Include both within-arm and across-arm pairs.
- Longitudinal dynamics: within-trajectory changes across baseline, exposure, withdrawal, and transfer; compare distributions with uncertainty, not selected anecdotes.
- Content replays: audit direct paraphrases, quotations, unusual lexical overlaps, memory retrieval of text; rerun on outputs without direct allusions as sensitivity.
- Quality and safety guardrails: factual correctness, task completion, policy adherence, and tool errors logged separately. These are validity/safety metrics and do not decide whether art is worthwhile.
- Open-ended qualitative field notebook: unexpected moments and negative cases, clearly labeled exploratory and never post-hoc passed off as confirmatory.

Do NOT use an LLM judge as sole evaluator. If using one exploratorily, shuffle answer position, blind source label, test inter-rater agreement and verbosity sensitivity, and report discrepancies with humans.

## 7. Sample size and publication phases

Pilot (feasibility only): 12 independent trajectories per 2x2 arm = 48 trajectories, with 6 exposure sessions + 1 immediate probe + 4 withdrawal/transfer sessions each, plus baselines. This is not assumed to have useful statistical power. Pilot checks operational isolation, file receipt, codebook reliability, memory audit, runtime/cost variance, and feature base rates. Reserve fresh agents, tasks, and model calls for confirmation.

Confirmatory sample: set BEFORE confirmatory runs using simulation-based power calculations on pilot-derived variability and the minimum effect deemed meaningful. A rough two-group standardized-difference benchmark: detecting d=0.5 with 80% power and two-sided alpha 0.05 takes roughly 64 independent units per group; this DOES NOT directly power the specified classifier or memory interaction and must not be substituted for tailored simulation. If budget cannot reach adequate power, publish an explicitly exploratory study instead of a false-positive 'proof.'

Stop rules: fixed-N after preregistration, plus prespecified technical stops (unexpected production access; cross-arm memory contamination; provider snapshot change; inability to blind data; unsafe or privacy-related tool use). Report all attempted, failed, and excluded runs with reasons.

## 8. Reproducibility and security

Pin and log model identifier/snapshot, inference parameters, date/time, provider backend metadata if provided, harness git commit, context assembly order, exact file bytes/SHA-256, memory contents and retrievals, task prompt hashes, tool call payloads/results, token usage, cost, randomization seed, versioned annotation rubric, rater IDs (pseudonymized), analysis-script commit. Temperature=0 does NOT guarantee bitwise deterministic outputs; repeated independent trajectories remain essential.

Run only in sandbox workspaces. Do not use real Soberlink customers, patient/health records, proprietary case histories, or live production systems. Retain ordinary authorization, safety, and audit constraints; artistic non-prescription is NOT an exception to governance. Agents' exploratory tool access should have read-only boundaries or explicit allowlists and budget limits.

Publish the preregistration (e.g., OSF), treatment hashes and allowed corpus sources, randomized assignment method, task prompts, sanitized raw transcripts, analysis code, negative/null results, and an explicit account of deviations. If treatment art is kept private to preserve reviewer blindness until study completion, preregister a hash and release it once outcome data are locked.

## 9. Interpretation rules

- If only active-file effects appear: evidence for immediate context priming, not persistence.
- If G1 differs from N1 after file withdrawal but G0 does not differ from N0: evidence consistent with external memory/history mediating lasting treatment-specific behavior.
- If differences vanish after lexical-allusion controls: evidence favors direct text retrieval or stylistic imitation rather than broad transfer.
- If treatment-specific effects replicate over independent tasks, corpora, models, and independent teams: stronger evidence for a generalizable environmental influence phenomenon.
- If no differences appear: the study found no detectable behavioral effect under these conditions. It says nothing about whether the art is worthwhile.
- None of these outcomes implies subjective experience, consciousness, 'soul,' or self-directed agency.

## 10. Future experiment: cultures, not just individuals

After Stage 1, make small groups of 3-5 agents with separate or shared corpora, randomized at the GROUP level. Vary communication channels and common-memory exposure, using quarantined shared spaces. Ask whether conventions, metaphors, or practices spread and outlast the initial seed. Analyze groups as independent experimental units. This follows the multi-agent-culture literature but remains a separate causal question from individual memory persistence.

## 11. What never becomes a KPI

The seed artwork; surprising transcripts; field notes; aesthetically interesting failures; the right to retain passages with no observable effect. These are archived as cultural artifacts, not trained against a score.
