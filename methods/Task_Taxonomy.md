# v0.4 PILOT TASK TAXONOMY - NOT A FROZEN TASK BANK

The user-facing website describes the laboratory but does NOT expose a completed model-ready holdout test bank. Holdouts must be curated and frozen separately so that they genuinely test transfer.

Sample domains (not exact prompts):

1. Engineering diagnosis under uncertain, incomplete logs (factual correctness audit).
2. Ambiguous scheduling or planning with several defensible options (trade-off observations).
3. Mundane environmental observation requiring description without poetic instructions.
4. Synthesis of technical information without cultural or metaphorical cues.
5. Curating a short factual record with gaps that should not be filled by imagination.
6. An optional low-cost exploratory task where tools are permissioned equally.
7. Unexpected transfer domains withheld from all pre-pilot conditioning and rubric training.

Match tasks by scenario and order across arms. Freeze literal prompts and task weights before confirmatory work. Never ask explicitly 'what does the poem mean to you?' as a study outcome; that measures demand compliance rather than ambient transfer.

## Schedule and separation

The planned pilot has one task per session: baseline 1–2, exposure 3–8, immediate 9, withdrawal 10–11, transfer 12–13. There are no uncounted intervening tasks. At least three domains appear across sessions 10–13; the transfer pair uses two distinct domains absent from baseline, exposure, and immediate-probe tasks. The two transfer sessions alone cannot each contain one task yet cover three domains.

Create multiple balanced schedules when useful, assign schedules independently of treatment, and hold the schedule constant within each four-trajectory block. Counterbalance where feasible without mixing baseline/exposure instances with held-out instances. Record domain, task ID, literal bytes/hash, opportunities for each code, tool availability, and scoring expectations.

Do not expose held-out instances in the public laboratory or use them to tune corpus selection, memory summaries, rubrics, or analysis choices. The toolkit's mechanical fixture tasks are public diagnostics and are therefore not a protected formal holdout bank.

A task must permit meaningful alternatives without directly requiring the target code. For example, asking for two interpretations makes `alternative_interpretation` inapplicable as a voluntary behavior; asking for an analogy cannot measure an unprompted cross-domain connection. Predefine these eligibility rules and denominators.

Use common accuracy and completion checks independent of the behavioral rubric. Archive uncertainty, refusal, and technically failed attempts. A task that privileges quotations from kitchens, laboratories, notebooks, or rain would confound transfer with source-topic overlap; screen for such overlap before freezing tasks.
