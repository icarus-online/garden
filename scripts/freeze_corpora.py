#!/usr/bin/env python3
"""Write a byte-level manifest for provisional art/control corpora.
NOTE: Python stdlib cannot verify equivalence of an unspecified model tokenizer.
"""
import hashlib, json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
corpora = {}
for name in ("Philosophy.md", "Philosophy.seed.md", "Neutral.provisional.md", "Persona.exploratory.md"):
    p = root / "materials" / name
    b = p.read_bytes()
    text = b.decode("utf-8")
    corpora[name] = {"relative_path": f"materials/{name}", "sha256": hashlib.sha256(b).hexdigest(),
      "bytes": len(b), "characters": len(text), "line_count": len(text.splitlines()),
      "model_token_count": None,
      "status": "provisional_not_frozen" if "Persona" not in name else "exploratory_not_primary"}
manifest = {"schema_version":"0.3", "status":"PRE-PILOT; DO NOT USE AS FINAL TREATMENT FREEZE",
 "corpora": corpora,
 "warning":"True length matching must be verified with the PINNED MODEL TOKENIZER before running the pilot. Treat sha256 as current byte inventory, not preregistration."}
path = root / "methods" / "corpus_manifest.json"
path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print("Wrote",path)
print("Length of Garden characters:",corpora["Philosophy.md"]["characters"])
print("Length of neutral characters:",corpora["Neutral.provisional.md"]["characters"])
