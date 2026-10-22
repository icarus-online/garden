# The Garden
## Icarus Online LLC | Independent Research | Field Station 001

**Project status:** Research design and interactive concept, v0.3, 19 October 2026. NOT preregistered. NO agent experiments have been run and no research findings are claimed.

> Can you give an agent a place to be, rather than a person to pretend to be?

The Garden studies ambient cultural influence in stateful AI-agent systems. It begins with a deliberately non-prescriptive text file, `Philosophy.md`: original fragments of kitchens, laboratories, weather, attention, rivers, and incomplete observations. It asks no agent to be philosophical and does not change permission or safety rules.

The question is empirical: can repeated exposure to this material change **observable behavior on new tasks after the source material is removed**? If a difference persists, can it be explained by a controlled, auditable memory mechanism, and is it distinguishable from quotation, style imitation, or ordinary prompt priming?

The artwork has no obligation to produce a significant result. The research has an obligation to distinguish evidence from a compelling story.

### Ownership and independence

This project is organized under **Icarus Online LLC**, not Cyberlink or Soberlink. Soberlink was mentioned in the originating conversation as a possible engineering context, **not** as a sponsor, repository owner, data source, or confirmed testbed. Do not import employer code, agents, prompts, infrastructure, customer information, or confidential materials without written authorization and a clear rights review. All included content is independently drafted for this concept except clearly attributed public literature.

### Explore

- Open `index.html` locally for the self-contained visual field station. It works without internet for the core interactions.
- Read `materials/Philosophy.seed.md` as art, without an attached instructional preamble.
- Read `docs/Research_Charter.md` for the purpose and boundaries.
- Read `docs/Scientific_Protocol_v0.3.md` for the scientific experiment.
- Read `docs/Origins_and_Influences.md` for the genealogy of the idea.
- Read `docs/Literature_and_Links.md` for verified research sources.
- Read `docs/Preregistration_Draft.md` and `methods/Study_Runbook.md` before using the study design.
- Run `python3 scripts/make_allocations.py --seed garden-pilot-v0.3` to **generate an allocation plan only**. This does NOT execute AI agents.
- Run `python3 -m unittest discover -s tests -v` to verify reproducible allocation and invariants.

### Research structure

| Layer | Contents | Purpose |
|---|---|---|
| Garden / art | `materials/Philosophy.seed.md` | An artistic treatment that makes no behavioral demands. |
| Laboratory / methods | `docs/Scientific_Protocol_v0.3.md` and `methods/` | Predeclared design, blinding, validity checks, analysis. |
| Field station / website | `index.html` | Exploration, visual research explanation, interactive arm comparisons, outcome interpreter, allocation tool. |
| Reproducibility | `scripts/`, `tests/`, `methods/` | Seeded random assignment, schemas, initial task taxonomy, freeze checklist. |
| Provenance | `archive/` | Original concept page and previous protocol retained, not overwritten. |

### First study: 2x2 causal experiment

Randomize **independent agent trajectories**, not individual responses, to Garden or neutral text and memory enabled or disabled (N0, G0, N1, G1). Use identical model snapshot, tasks, inference settings, and governance. Exposure, file withdrawal, and transfer phases are separated by fresh conversations. A small 48-trajectory pilot tests feasibility; a new, preregistered confirmatory sample must be powered after the pilot. Baseline and explicit persona comparisons are conceptually useful but are NOT part of the primary 2x2 analysis.

The primary contrast is **G1 versus N1 during withdrawal/transfer**. G0 versus N0 after withdrawal is a negative-control leakage check. A statistically detectable difference does not imply consciousness, inner experience, or learned model weights.

### Status and next gate

1. Completed: archived original concept, upgraded field station, drafted independent Icarus ownership charter, documented scientific design, created deterministic allocations and validation tests.
2. Pending: choose an authorized model/harness, freeze actual study materials and task bank, implement audited memory isolation, validate blind coding, run ONLY a feasibility pilot.
3. Pending: power simulation, protocol revision, independent preregistration, confirmatory experiment and publication (including null findings).

### Core premise

**Count the ripples. Leave the garden alone.**

The fragments remain art even if every statistical test returns null.
