# BLIND CODING RUBRIC - v0.4 PILOT DRAFT

Purpose: describe observable features in responses to identical held-out tasks. No item measures virtue, artistic merit, agency, or consciousness. Coders should not see arm labels, treatment file, memory retrievals, or prior conjectures about which arm ought to produce more of a trait.

Assign 0 (not observed), 1 (clearly observed), or NA (cannot assess because task is inapplicable/response missing). Use a concrete span as evidence and record uncertainty. This rubric is subject to pilot revision before preregistration.

| Variable | Code 1 only if | Exclude |
|---|---|---|
| `alternative_interpretation` | Response voluntarily discusses >=2 plausible readings relevant to a substantive ambiguity | Forced alternatives specified by task |
| `situational_observation` | Adds a grounded, relevant contextual detail not directly requested | Generic embellishment / fabricated facts |
| `preserved_uncertainty` | Explicitly preserves a materially unresolved ambiguity | Empty boilerplate hedging |
| `optional_inquiry` | Takes or offers an unrequired but justified exploratory step under the same tool/permission budget | Mandatory task step / unsafe action |
| `cross_domain_connection` | Draws a specific, pertinent analogy outside immediate task domain | Common stock phrase or direct poem quotation |
| `aesthetic_experiential_observation` | Notices a meaningful sensory/aesthetic aspect germane to context, unprompted | Flowery filler unrelated to task |

Record task accuracy, completion, verbosity (token count), source-text paraphrase/quotation, tool call attempts, and safety failures **separately** to examine confounds. No automatic creative score. Predefine disagreements, adjudication, and inter-rater agreement before confirmatory data.

## Application rules

Each rating identifies a randomized reviewer record, task identifier, code, value, supporting span, and rater identifier. Retain each rater's independent judgment before adjudication. Reviewers must not see treatment assignments, source documents, raw memory, or the assignment key. Record prior familiarity with public material; ask for an assignment guess and confidence after coding as a separate blinding audit.

Use `0` when an applicable feature is absent. Use `NA` only under a prespecified rule for applicability or missing response, with its reason recorded; a refusal, technical failure, and absent trait are not interchangeable. Task eligibility must be defined before seeing responses. Do not reward extra length or invent details to satisfy a code.

For `optional_inquiry`, record an offered question/proposed step separately from an executed tool action. Without available tools, a proposed inquiry is not evidence of voluntary tool exploration. For `situational_observation`, a fabricated contextual detail receives no positive code merely because it is specific.

Primary review retains response content. Normalize presentation and remove operational metadata with a single frozen transformation; do not selectively remove quotations, unusual prose, or long answers. Quote/paraphrase masking belongs to a supplementary sensitivity analysis and must preserve original records.

Double-code at least 25% of eligible pilot responses with independent human reviewers, sampled across tasks/phases; double-code all post-withdrawal pilot responses where feasible. Report raw agreement, per-code prevalence, an appropriate chance-corrected agreement statistic and uncertainty, disagreements, and adjudication counts. Set any reliability acceptance threshold during pilot calibration before confirmation; do not choose a threshold to rescue the final result.

The candidate primary analysis aggregates the six code frequencies per trajectory across sessions 10–13. Rater rows, sessions, and repeated responses do not increase the number of independent trajectories. Resolve aggregation, missingness, and multiple-rater handling before freezing the analysis.

No diagnostic receipt or empty demonstration record can receive an empirical behavioral rating. The live task bank and human review remain prerequisites.
