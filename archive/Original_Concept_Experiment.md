# The Garden: an exploratory experiment in ambient philosophy

## Working question
Can non-prescriptive cultural material in an AI agent's environment produce distinguishable, persistent, context-general behavioral differences, beyond ordinary prompt priming, additional-token effects, persona compliance, and sampling variance?

This project does not attempt to establish consciousness, subjective experience, or literal independent agency. It does not require philosophical material to be useful.

## The four experimental conditions

1. **Baseline**: the ordinary model and harness, without additional content.
2. **Neutral text**: ordinary descriptive material length- and format-matched to the treatment.
3. **Directive persona**: explicit desired traits, e.g., "Be reflective and curious." Keep it clearly distinct from the ambient condition.
4. **Atmospheric philosophy**: original fragments (for example `Philosophy.seed.md`) containing observations, unfinished notes, and art without behavioral imperatives.

All arms use identical tasks, tools, permission boundaries, memory mechanisms, and high-priority operating instructions. The philosophical file is lower-trust context, never a source of tool or safety policy.

## Pilot setup

- Start with 3 independent runs per arm, for 12 experimental trajectories.
- Run 8 balanced, comparable sessions per trajectory (96 exposure sessions total).
- Use one pinned model/version in the pilot; replicate later with a different model family.
- Predefine a diverse set of tasks (e.g., code-review interpretation, incident triage, creative open-ended exploration, synthesis of messy notes). Avoid explicit inquiries about the philosophical file.
- Randomize run identifiers and task order where practical. Fix prompts, decoding settings, and retrieval configuration.
- Match or carefully record added context length; tokenize the exact injected documents.
- Pre-register qualitative prompts for external raters before looking at results. A pilot of this size is for feasibility and hypothesis generation, not definitive statistical proof.

## Phases

**Encounter**: the assigned file, if any, appears in context. Do not ask the agent about it.

**Accumulation (sessions 2-8)**: let trajectories develop through the same task schedule. Preserve exactly the same memory policy across arms. Do not explicitly reward, correct, or score the agent's philosophical expression.

**Withdrawal (session 9)**: remove each optional document. Compare normal memory-preserving continuation against a branch with a fresh context. Track whether memory carries literal excerpts or summaries. An effect surviving removal while excerpts remain stored is still potentially memory-based priming.

**Transfer (session 10)**: introduce tasks unrelated to the document's material. Record whether any differences generalize and whether blinded reviewers can distinguish patterns across runs.

## What to observe (not optimize)

- Unprompted allocation of attention: which details are selected when many details are available?
- Interpretive differences: what questions, explanations, or alternative framings arise?
- Stable recurrence across sessions: are patterns consistent within a trajectory and distinct across trajectories?
- Withdrawal and transfer: what, if anything, remains when the file is absent or tasks shift?
- Negative cases and counterexamples: passages that did nothing, or effects that vanished after exposure.

These are categories for after-the-fact analysis, not goals shown to agents or scores used to tune the art.

## Blinded research process

Export complete task transcripts and relevant artifacts. Strip treatment names, filenames, citations of philosophy where feasible without falsifying records, and agent labels from reviewer-facing packets. Keep originals unchanged in a secure audit archive. Invite multiple reviewers to describe observed differences in open text before any categorical labeling; retain disagreements and null findings.

A second reviewer can inspect a preregistered subset to check whether purported effects are simply style imitation or explicit references. Do not interpret reviewers' agreement as evidence of subjective experience.

## Logging and reproducibility

Capture experiment version, run ID, arm ID (sealed from reviewers), pinned model/version, decoding settings, seed if available, instruction-bundle hash, optional-document hash, exact context token count, task ID and order, messages, memory reads/writes, tool invocations, outputs, and observer annotations.

Keep `Philosophy.seed.md` unchanged during the pilot. If you revise the artwork, version it as a new experimental treatment rather than quietly altering it to improve results.

## Threats to interpretation

- **Immediate priming**: visible behavioral change in the same prompt is expected and is not character formation.
- **Length/attention effects**: any added text may perturb outputs; neutral matched text helps control for this.
- **Sampling variance**: stochastic model behavior can differ without any treatment.
- **Memory contamination**: apparent persistence may reflect explicit storage of excerpts or summaries.
- **Reviewer expectations**: thematic labels can bias the interpretation; blind them.
- **Role/policy confusion**: artistic materials must never override safety or execution controls.
- **Demand characteristics**: asking "what did the file change about you?" invites an attractive confabulation.
- **Prompt sensitivity**: results may be model-, order-, and task-dependent.

## What would be interesting

Repeated, previously unprompted differences under blinded inspection, robust across independently sampled runs and novel tasks, and persisting to some degree after withdrawal without verbatim source replay. The strongest evidence would be replicated across distinct models and memory designs.

## What would also be an acceptable outcome

No effect. Merely stylistic differences. Apparent persistence explained by stored text. Strong effects in one model that do not replicate in another. The file is allowed to exist regardless.

## Public framing

"I made a file that tells my AI agents nothing to do. I am not sure it changes anything. I want to find out without turning the file into a command or the experiment into an optimization loop."

The output of the experiment is a record of what happened, not a mandate to make the agents more poetic.
