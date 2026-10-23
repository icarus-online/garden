# Local research apparatus

This Python 3.10+ toolkit runs **mechanical dry runs only**. It makes zero network requests, has no inference credentials, and generates no agent responses or scientific findings. Its purpose is to test allocation, context assembly, bounded state, withdrawal, artifact integrity, and review-export structure before a separately authorized pilot. The published task prompts are fixtures; they cannot serve as a sealed study holdout bank.

From the repository root, with no third-party dependencies:

```sh
python3 -m unittest discover -s tests -v
python3 -m research validate research/configs/dry-run.example.json
python3 -m research run research/configs/dry-run.example.json --out runs/demo
python3 -m research verify runs/demo
python3 -m research blind runs/demo --out runs/review --key-out runs/reviewer-key_PRIVATE.json
python3 scripts/freeze_corpora.py --check methods/corpus_manifest.json
```

Output directories must be new. A second run needs another output path. `runs/` is ignored by Git; the full run includes private allocations, the allocation seed, source material, and contexts. Directory/file modes default to 0700/0600. Do not publish these files as a blinded dataset. The checksums detect accidental changes and verify internal consistency; they are not digital signatures against an attacker able to rewrite the whole bundle.

## Configuration and model lock

The checked-in example is locked to a local mechanical receipt generator, named `local-dry-run / mechanical-receipt-v1`, with explicit non-applicable reasoning and null sampling fields. No real model is selected. The strict configuration schema rejects additional fields, live providers, model changes, enabled tools, automatic fallback, and truncation. It records the operational instructions, context policy, bounded memory policy, source/task hashes, allocation seed, and protocol version.

The sibling `.lock.json` file hashes the canonical configuration and exact implementation files. A changed config, source corpus, task bank, model setting, or implementation stops execution. To prepare an intentional new diagnostic block, copy the example under a new name, update its `experiment_id` and explicit settings/source hashes, then create a **new** lock:

```sh
python3 -m research lock research/configs/my-diagnostic-block.json
python3 -m research validate research/configs/my-diagnostic-block.json
python3 -m research run research/configs/my-diagnostic-block.json --out runs/my-diagnostic-block
```

The lock command refuses an existing lock. Preserve earlier configs and locks with their artifacts; do not casually relock after unexpected drift. A live adapter needs a new reviewed schema and must validate actual returned provider/version metadata, isolate server-side state, and implement budget/permission gates. The current apparatus does not test those live properties.

## Schedule and state

Each trajectory receives exactly 13 fresh contexts: two baseline sessions, six exposure sessions, one immediate probe, two withdrawal sessions, and two transfer sessions. There are no hidden intervening sessions. Baseline reads and writes are disabled for **all** arms. State is reset immediately before the first exposure. The assigned Garden or neutral source appears in a common untrusted-data envelope only during sessions 3–9. The dry-run context is an unordered diagnostic object with system/developer instructions, memory, ambient data, and task fields; canonical JSON sorts its keys for hashing. It is not an API message sequence. A live adapter must separately freeze and test ordered message placement. Exceeding the byte budget stops the run instead of truncating.

Memory-disabled arms never read or write retained records. Memory-enabled arms retain at most the configured number of previous diagnostic receipts. A receipt includes only session number and task/context hashes plus an explicit no-inference notice and a null response. It is not an agent-generated memory or evidence of behavioral persistence. Each execution has a fresh 128-bit random identifier; each trajectory has its own registered namespace. No state is restored from disk. Disabled-state isolation is checked by comparing N0 and G0 post-withdrawal contexts for exact equality.

The intended scientific memory design remains a separate gate: pin a bounded task-plus-response record policy, exclude direct corpus insertion, log exact reads and writes, and test the live provider. Output retention can still preserve corpus quotations or paraphrases; withdrawal of the ambient file does not imply erasure of treatment from memory.

## Allocation and repeatability

`sha256-counter-rejection-fisher-yates-v1` takes UTF-8 seed bytes. Each draw hashes the concatenation of `garden-allocation-v1` followed by a NUL byte, the seed byte length as unsigned 64-bit big-endian, the seed, and a zero-based unsigned 64-bit big-endian draw counter. The digest is interpreted as a 256-bit big-endian integer. Rejection sampling discards values at or above `2^256 - (2^256 mod bound)`; accepted values modulo `bound` drive Fisher–Yates. Each successive block shuffles the ordered arms N0, G0, N1, G1. The test suite freezes a Unicode-seed golden vector.

This replaces the historical FNV/xorshift planning algorithm. Historical example allocations and the browser's educational visualization must retain their original algorithm labels; they are not interchangeable with runner allocations. All trajectories receive the same task schedule in this apparatus; task-order counterbalancing is not claimed.

Identical seeds/configs produce the same assignments, contexts, and receipts. Execution identifiers, namespaces, timestamps, and resulting run-level hashes deliberately differ between executions. The complete payload chain is reproducible; execution metadata records separate runs. A real stochastic provider would not inherit this bitwise repeatability guarantee.

Standalone allocations are also available:

```sh
python3 scripts/make_allocations.py --per-arm 12 --experiment-id pilot-plan-001 --out-dir runs/allocation-plan
```

Omitting `--seed` generates a 256-bit random seed and saves it in the private output directory. The seed is not printed. Preserve it securely before preregistration; the demonstration seed is public and unsuitable for concealing real assignments.

## Artifacts and review export

`manifest.json` captures the zero-inference status, exact config hash, model settings, source-code hashes, Git commit (which may precede uncommitted local changes), Python version, timestamps, trajectory/session counts, and every artifact hash. `manifest.sha256` covers the manifest. Implementation hashes, rather than the commit alone, identify the executed source. `traces.jsonl` contains a record for each completed diagnostic session; corresponding context and receipt files retain the full mechanical chain. An interrupted/failed run without a manifest is incomplete and cannot be verified or exported. Keep it for diagnosis and restart in a new directory.

`verify` checks file completeness and hashes, all expected trajectory/session pairs, assignment/model identity, full context reconstruction, source withdrawal, disabled-state isolation, exact memory reads/writes, and receipt consistency. A valid bundle has 624 diagnostic records for the 48-trajectory example, with zero model calls.

`blind` verifies the source first, shuffles records with a fresh private seed, assigns non-semantic review IDs, and exports only task prompts and null responses. The private join key must be outside both reviewer directory and source run. No arm labels, trajectory IDs, phases, memory, hashes, or source names appear in reviewer records. It is an **unrateable structural rehearsal**, not a validated blind evaluation. Real responses may reveal treatment through quotations or style, and task wording may reveal phase; that limitation requires preregistered review procedures and empirical audit.

The corpus inventory command compares exact bytes without editing the art. `--out NEW_FILE.json` writes a new inventory, and no flags prints it. Neither operation verifies model-token matching, quotation rights, or preregistration, and neither declares the provisional control ready for the pilot.
