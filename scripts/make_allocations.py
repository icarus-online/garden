#!/usr/bin/env python3
"""Reproducible blocked allocations. Planning only: never calls an AI provider."""
import argparse
import csv
import hashlib
import json
import secrets
from pathlib import Path

ARMS = ("N0", "G0", "N1", "G1")
ALGORITHM = "sha256-counter-rejection-fisher-yates-v1"

def seed_hash(seed):
    return int.from_bytes(hashlib.sha256(seed.encode("utf-8")).digest(), "big") or 1

class Generator:
    """Versioned byte-defined stream, unbiased bounded draws (no modulo bias)."""
    def __init__(self, seed):
        self.seed = seed.encode("utf-8")
        self.counter = 0
    def next(self):
        payload = b"garden-allocation-v1\0" + len(self.seed).to_bytes(8, "big") + self.seed + self.counter.to_bytes(8, "big")
        self.counter += 1
        return int.from_bytes(hashlib.sha256(payload).digest(), "big")
    def below(self, bound):
        limit = 2 ** 256 - (2 ** 256 % bound)
        while True:
            value = self.next()
            if value < limit:
                return value % bound
    def shuffle(self, arr):
        for j in range(len(arr) - 1, 0, -1):
            k = self.below(j + 1)
            arr[j], arr[k] = arr[k], arr[j]
        return arr

def make_allocations(seed, per_arm=12, experiment_id="allocation-preview"):
    if type(per_arm) is not int or not 1 <= per_arm <= 2000:
        raise ValueError("per_arm must be an integer in 1..2000")
    if not isinstance(seed, str) or not seed:
        raise ValueError("seed must be nonempty text")
    if not isinstance(experiment_id, str) or not experiment_id:
        raise ValueError("experiment_id must be nonempty text")
    prng = Generator(seed)
    scope = hashlib.sha256(json.dumps([experiment_id, seed], ensure_ascii=False).encode()).hexdigest()
    result = []
    for block in range(1, per_arm + 1):
        for arm in prng.shuffle(list(ARMS)):
            trajectory = f"T{len(result) + 1:04d}"
            result.append({"trajectory_id": trajectory, "block": block, "arm": arm,
                "ambient": "garden" if arm.startswith("G") else "neutral",
                "memory_enabled": arm.endswith("1"),
                "memory_namespace": f"{scope}/{trajectory}",
                "total_fresh_sessions_planned": 13})
    return result

def validate(items, per_arm):
    checks = [len(items) == per_arm * 4,
        len({x["trajectory_id"] for x in items}) == len(items),
        len({x["memory_namespace"] for x in items}) == len(items),
        all(sum(x["arm"] == arm for x in items) == per_arm for arm in ARMS),
        all({x["arm"] for x in items if x["block"] == block} == set(ARMS) for block in range(1, per_arm + 1)),
        all((x["ambient"] == "garden") == x["arm"].startswith("G") for x in items),
        all(x["memory_enabled"] == x["arm"].endswith("1") for x in items)]
    if not all(checks):
        raise ValueError("Invalid or contaminated allocation table")
    return True

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", help="Predeclared private seed; generated if omitted")
    ap.add_argument("--per-arm", type=int, default=12)
    ap.add_argument("--experiment-id", default="allocation-preview")
    ap.add_argument("--out-dir", type=Path, default=Path("runs/private"))
    args = ap.parse_args()
    seed = args.seed if args.seed is not None else secrets.token_hex(32)
    items = make_allocations(seed, args.per_arm, args.experiment_id)
    validate(items, args.per_arm)
    args.out_dir.mkdir(parents=True, exist_ok=False, mode=0o700)
    with (args.out_dir / "experimenter_allocations_PRIVATE.csv").open("w", newline="") as f:
        dw = csv.DictWriter(f, fieldnames=list(items[0]))
        dw.writeheader()
        dw.writerows(items)
    manifest = {"schema_version": "1.0", "status": "allocation_plan_only_NOT_experiment",
        "experiment_id": args.experiment_id, "seed_sha256": hashlib.sha256(seed.encode()).hexdigest(),
        "algorithm": ALGORITHM, "per_arm": args.per_arm, "independent_units": len(items),
        "sessions_per_unit": 13, "planned_minimum_sessions": len(items) * 13}
    (args.out_dir / "allocation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (args.out_dir / "allocation_seed_PRIVATE.txt").write_text(seed + "\n")
    for path in args.out_dir.iterdir():
        path.chmod(0o600)
    print(f"Created {len(items)} allocations in {args.out_dir}; private seed saved there. No inference performed.")

if __name__ == "__main__":
    main()
