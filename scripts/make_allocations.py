#!/usr/bin/env python3
"""Generate independent, blocked arm assignments only; DOES NOT call AI models.

The non-cryptographic FNV-1a/xorshift32 shuffle matches the visual website.
For a real experiment, choose and privately record an unpredictable seed, then
preregister the allocation method and preserve assignments outside review data.
"""
import argparse
import csv
import hashlib
import json
import secrets
from pathlib import Path

ARMS = ("N0", "G0", "N1", "G1")

def seed_hash(seed: str) -> int:
    h = 2166136261
    for byte in seed.encode("utf-8"):
        h = ((h ^ byte) * 16777619) & 0xffffffff
    return h or 1

class Generator:
    def __init__(self, seed: str):
        self.state = seed_hash(seed)
    def next(self) -> int:
        x = self.state
        x ^= (x << 13) & 0xffffffff
        x ^= (x >> 17) & 0xffffffff
        x ^= (x << 5) & 0xffffffff
        self.state = x & 0xffffffff
        return self.state
    def shuffle(self, arr):
        for j in range(len(arr)-1, 0, -1):
            k = self.next() % (j + 1)
            arr[j], arr[k] = arr[k], arr[j]
        return arr

def make_allocations(seed: str, per_arm: int = 12):
    if not isinstance(per_arm, int) or not (1 <= per_arm <= 2000):
        raise ValueError("per_arm must be an integer in 1..2000")
    prng = Generator(seed)
    result = []
    for block in range(1, per_arm + 1):
        for arm in prng.shuffle(list(ARMS)):
            index = len(result) + 1
            result.append({
                "trajectory_id": f"T{index:04d}",
                "block": block,
                "arm": arm,
                "ambient": "garden" if arm.startswith("G") else "neutral",
                "memory_enabled": arm.endswith("1"),
                "memory_namespace": f"garden-pilot-T{index:04d}",
                "total_fresh_sessions_planned": 13,
            })
    return result

def validate(items, per_arm):
    assert len(items) == per_arm * 4
    assert len({x["trajectory_id"] for x in items}) == len(items)
    assert len({x["memory_namespace"] for x in items}) == len(items)
    for arm in ARMS:
        assert sum(x["arm"] == arm for x in items) == per_arm
    for block in range(1, per_arm + 1):
        assert {x["arm"] for x in items if x["block"] == block} == set(ARMS)
    assert all((x["ambient"] == "garden") == x["arm"].startswith("G") for x in items)
    assert all(x["memory_enabled"] == x["arm"].endswith("1") for x in items)
    return True

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", default=None, help="Private allocation seed; auto-generated if omitted")
    ap.add_argument("--per-arm", type=int, default=12)
    ap.add_argument("--out-dir", default="runs/private", type=Path)
    args = ap.parse_args()
    seed = args.seed or secrets.token_hex(16)
    allocations = make_allocations(seed, args.per_arm)
    validate(allocations, args.per_arm)
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    with (out / "experimenter_allocations_PRIVATE.csv").open("w", newline="", encoding="utf-8") as f:
        dw = csv.DictWriter(f, fieldnames=list(allocations[0].keys()))
        dw.writeheader()
        dw.writerows(allocations)
    with (out / "reviewer_ids_BLINDED.csv").open("w", newline="", encoding="utf-8") as f:
        dw = csv.DictWriter(f, fieldnames=["trajectory_id", "session_number", "blinded_response_path"])
        dw.writeheader()
        for trajectory in allocations:
            for session in range(1, 14):
                dw.writerow({"trajectory_id": trajectory["trajectory_id"], "session_number": session,
                    "blinded_response_path": f"blinded/{trajectory['trajectory_id']}/session-{session:02d}.txt"})
    manifest = {"schema_version": "0.3", "project": "Icarus Online LLC / The Garden",
      "status": "allocation_plan_only_NOT_experiment", "seed_sha256": hashlib.sha256(seed.encode()).hexdigest(),
      "seed_is_stored_in_manifest": False, "per_arm": args.per_arm,
      "independent_units": len(allocations), "sessions_per_unit": 13,
      "planned_minimum_sessions": len(allocations) * 13,
      "algorithm": "FNV1a32(UTF8(seed)) + xorshift32 + within-block Fisher-Yates (4 arms)"}
    (out / "allocation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Created {len(allocations)} independent study allocations in {out}")
    print(f"Minimum planned fresh sessions: {len(allocations)*13}")
    if args.seed is None:
        print("Generated random private seed (STORE SECURELY; NOT IN BLINDED FILES):", seed)
    print("NOTHING was sent to any AI provider; no study was conducted.")

if __name__ == "__main__":
    main()
