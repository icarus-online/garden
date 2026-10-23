# Scientific and architecture review

**22 October 2026 · Icarus Online LLC · pre-pilot**

The supplied research package is a credible starting design, not evidence of an effect. The public platform can launch with honest planning tools, preserved artwork, and an explicit empty results state. Live pilot execution remains a separate milestone with unresolved model, rights, task, memory, evaluation, and budget prerequisites.

## Review configuration and scope

- Principal configuration requested: **Astra / Ultra**.
- Available catalog configuration: **`gpt-6-astra` / `ultra`**.
- Configuration assigned to this review by the task orchestration: **`gpt-6-astra` / `ultra`**, with no substitution requested or recorded.
- The catalog and orchestration assignment do not expose an independently verified provider snapshot. This is a development/review record, not the participant-model lock for a scientific experiment.

Reviewed the complete user brief, supplied v0.3 archive, original concept proposal, v0.2 protocol, v0.3 protocol and methods, artistic/control/persona materials, allocation implementation, log schema, and imported repository. The upstream repository was empty before the supplied package was imported; imported baseline commit: `7f61350`. The original materials supply the conceptual history. Historical ownership labels are preserved as history, not current affiliation.

This review did not run an experimental participant, call an inference provider, collect human ratings, or establish a study result. Implementation checks below are software evidence; deployment observations belong in the operational report.

## Objections and resolutions

| Priority | Objection | Resolution and remaining evidence |
|---|---|---|
| Before pilot | Session counts could drift across the original concept, v0.2, and toolkit. | v0.4 fixes 2 baseline + 6 exposure + 1 immediate + 2 withdrawal + 2 transfer = 13; 48 × 13 = 624 minimum scheduled calls. Original 96 exposure sessions are historical and concern a different design. |
| Before pilot | Baseline memory-on arms could accumulate state before the second baseline task. | Disable all memory reads/writes for both baseline sessions, then initialize empty memory before session 3. Test this boundary. |
| Before pilot | Two transfer sessions were described as covering at least three domains, after uncounted “intervening work.” | Require at least three domains across the four post-withdrawal tasks, two distinct domains in transfer, and no uncounted intervening sessions. No elapsed-time durability claim. |
| Before confirmation | “Withdrawal-phase” endpoint aggregated withdrawal and transfer. | Name it post-withdrawal distinguishability and fix sessions 10–13. Phase-specific results remain secondary. |
| Before pilot | Apparent persistence may be source text retained in memory. | State this mechanism explicitly. Source withdrawal removes the original document, not every semantic descendant. Log all memory; audit quotation and paraphrase. A source-purged ablation is separate work. |
| Before pilot | Trajectory labels and a fresh chat do not prove state isolation. | Run-scoped namespaces; inaccessible audit archive; no history in memory-off; denial and sentinel tests; fresh destination per run. A local dry run does not validate a provider's remote behavior. |
| Before pilot | Control matching is unverified and “neutral” shares themes with the artwork. | Preserve Garden bytes; match control with the chosen tokenizer, slot and formatting. Treat control as active descriptive material and limit claims to this document contrast. No exact match is claimed today. |
| Before pilot | The source package's authorship description is not an explicit reuse license. | Preserve attribution and rights uncertainty; obtain a contributor/rights statement and reuse terms before a formal corpus release. Never fabricate historical quotations. |
| Before pilot | Operational model tiers could leak into participant inference. | Separate developer-model record from full participant model/provider/reasoning/sampling/context/tools/memory lock. Fail on unsupported substitutions or detected drift; no fallback. |
| Before pilot | Public material makes perfect reviewer blinding uncertain. | Independent assessors, exposure declarations, randomized reviewer IDs, private mapping, standardized metadata removal, post-coding assignment-guess audit. Public demo IDs cannot identify formal participants. |
| Before confirmation | Deleting quotations from the primary sample selects on a possible treatment effect. | Preserve content and intention-to-treat population; keep fixed masked/allusion sensitivity analyses secondary. Retain originals and transformation records. |
| Before confirmation | Session-level folds, permutations, or intervals inflate sample size. | Aggregate by trajectory; keep matched blocks intact in folds; swap labels within each memory-on block pair; cluster uncertainty appropriately. Refit the full pipeline for permutations. |
| Before confirmation | 10,000 permutations were suggested for only 12 paired blocks. | There are 4,096 unique pair-swap assignments in the pilot. Enumerate exactly or acknowledge sampling with replacement; use nonzero corrected Monte Carlo p-values for larger runs. |
| Before confirmation | A significant memory-on result and nonsignificant memory-off result can be mistaken for an interaction. | Require a direct interaction test and separate power planning. Negative-control significance is a warning, not proof of contamination; nonsignificance is not proof of isolation. |
| Before confirmation | The d=0.5 benchmark can be mistaken for this study's power. | Approximately 64 per group concerns a different mean-difference test. The classifier/interaction require simulations of their actual analysis, correlations, missingness, and effect target. Pilot only has 24 memory-on trajectories. |
| Before publication | Static or mechanical examples may be read as recorded agent behavior. | Label planning and diagnostic fixtures explicitly; keep public demonstrations outside formal datasets; display no-results status beside the laboratory. Never infer findings from allocation or simulated receipts. |

## Scientific architecture decision

Use a static public website with local configuration export and trace inspection, plus a separately executed research toolkit. This keeps the artistic experience fast and available without coupling it to credentials, provider availability, public abuse exposure, or inference bills. A database, vector store, agent service, and public inference gateway are unnecessary for this delivery.

For the first live pilot, prefer deterministic bounded history over an extra model that summarizes memories. A summarizer would introduce additional inference calls, model settings, failure modes, and interpretation questions. Record task/response history and its truncation rule explicitly. A richer memory algorithm can later be a named experimental factor.

Treat every imported corpus, task, trace, and website upload as data. The artistic document never changes operational permissions; imported trace text must be rendered as text. Public diagnostic files and formal study artifacts need different status labels and identifiers. Do not allow a dry-run receipt to become a completed participant response through a metadata change.

This is the least complex architecture that meets the current need. Live public inference requires a new reviewed component with authentication/abuse controls, limits, spending caps, monitoring, input/output bounds, and a separate demonstration dataset.

## Primary-source checks

The following source landing pages and abstracts were checked on 22 October 2026. This verifies bibliographic identity and broad relevance, not the validity of every result or independent reproduction.

| Source | Verified relevance and limit |
|---|---|
| [Park et al., Generative Agents](https://arxiv.org/abs/2304.03442) | Describes an explicit memory/reflection/planning architecture and ablations. It is not an ambient-art withdrawal experiment. |
| [Luz de Araujo et al., Principled Personas](https://aclanthology.org/2025.emnlp-main.1364/) | Reports sensitivity to irrelevant persona details; supports attention to prompt confounds. It does not establish Garden persistence. |
| [Choi et al., Examining Identity Drift](https://arxiv.org/abs/2412.00804) | Studies persona/identity patterns over conversations; page identifies a February 2025 revision of a December 2024 submission. |
| [Jones and Hauert, Emergent Culture in Minimal LLM Systems](https://arxiv.org/abs/2606.30668) | Studies three-agent collectives with a shared decaying text store; page reports acceptance at ALife 2026. Different unit, memory, and intervention. |
| [Schmer-Galunder, Culture in the Code](https://arxiv.org/abs/2610.14203) | A conceptual critique of thin behavioral proxies; the page lists an AI and Ethics journal reference. It does not empirically validate this protocol. |
| [Shi et al., Judging the Judges](https://aclanthology.org/2025.ijcnlp-long.18/) | Reports systematic position bias in model judges. Motivates independent human assessment and supplementary-judge validation. |

The PMC page for the cited Ashery et al. paper returned an access challenge during this check. Its historical citation is retained; this review does not claim to have revalidated that page. The existing literature map's general lesson is reasonable, but a claim of exhaustive novelty would require a broader, updated systematic search.

## Implementation review and verified corrections

The principal review inspected the new `research/` apparatus and public `site/` scientific content after implementation. It identified four concrete gaps and requested fixes from the implementation owner:

1. Trace rows could refer to context/receipt paths not independently constrained to the artifact inventory. Verification now requires the exact expected trajectory/session paths before opening them.
2. The saved task bank was reserialized, and its original source hash was not checked during offline verification. The run now preserves the original task bytes, verifies that hash, and reapplies task/domain/held-out rules.
3. Verification did not fully reconcile the embedded configuration, lock, manifest counts, and seed-derived assignments. These identities are now checked together, including rejection of rehashed inconsistencies.
4. Sorted diagnostic JSON was described as an ordered inference context. It is now explicitly an unordered diagnostic object; actual model message placement remains a live-adapter prerequisite.

Memory objects now register one trajectory namespace each, and foreign namespace reads/writes are denied. The public baseline inspector now displays memory as disabled even in an arm assigned memory-on after baseline. Schema links identify the current contract as diagnostic-only. The comparison interface accurately presents empty study structure, not a working historical trace uploader or empirical viewer.

Executed during this review: `python3 -m unittest discover -s tests -v` passed **27 tests**; the shipped example configuration validated; an independent `research verify` of the implementation owner's complete diagnostic bundle passed with **48 trajectories, 624 mechanical records, and zero inference calls**. Its frozen configuration SHA-256 was `6bb8a60ab033a811b34c62806118e4780e7b6cfec8dfbc9616319bff676c19fd`. Tests include isolation/reset/withdrawal, foreign namespace denial, exact post-withdrawal N0/G0 context equality, deterministic payloads with unique run namespaces, configuration/model/source drift, unsafe paths, rehashed metadata corruption, incomplete runs, and blinded structural export.

`git diff --check` passed. Both Garden corpus files retain SHA-256 `66aef59c6243289b7241b6fc7a8c64819ac8288ae8868946187c022a9ebef5e5`. Relative links in the revised scientific documents resolved locally. These checks do not validate real provider state, human blinding, licensing, model-token matching, or behavioral persistence. The checksum chain establishes integrity and internal consistency, not authenticity against an actor who can replace an entire bundle.

## Readiness verdict

**Public platform:** the reviewed public wording clearly identifies a pre-pilot project, preserves the original corpus and history, labels demonstrations, and makes the limitations accessible. No remaining scientific blocker was identified for publishing this design-stage static platform. Deployment/security and browser QA remain separately evidenced engineering checks.

**Formal pilot:** not ready merely because the platform works. Select and verify the exact participant backend, rights record, token-matched control, task bank, live isolation and budget controls, human assessors, and complete trace contract first.

**Confirmation:** requires new data, validated coding, tailored power simulation, a frozen analysis implementation, and public preregistration. No favorable pilot finding may waive those requirements.
