#!/usr/bin/env python3
"""Inventory corpus bytes without modifying the art. This is not a formal study freeze.

Print JSON, write a NEW manifest with --out, or check a previous inventory with
--check. Matching model-token counts and provenance approval remain pilot gates.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('Philosophy.md', 'Philosophy.seed.md', 'Neutral.provisional.md', 'Persona.exploratory.md')

def inventory():
    corpora = {}
    for name in NAMES:
        data = (ROOT / 'materials' / name).read_bytes()
        text = data.decode('utf-8')
        corpora[name] = {'relative_path':f'materials/{name}','sha256':hashlib.sha256(data).hexdigest(),
            'bytes':len(data),'characters':len(text),'line_count':len(text.splitlines()),
            'model_token_count':None,'status':'exploratory_not_primary' if 'Persona' in name else 'provisional_not_frozen'}
    return {'schema_version':'1.0','status':'byte_inventory_NOT_formal_treatment_freeze','corpora':corpora,
        'warning':'No model tokenizer selected; byte hashes do not establish token matching, licensing clearance, or preregistration.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--out',type=Path)
    group.add_argument('--check',type=Path)
    args = parser.parse_args()
    current = inventory()
    if args.check:
        previous = json.loads(args.check.read_text())
        for name, source in current['corpora'].items():
            if previous['corpora'].get(name, {}).get('sha256') != source['sha256']:
                parser.exit(2, f'Corpus drift: {name}\n')
        print('All four corpus byte hashes match. Token matching and formal freeze remain unverified.')
    elif args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open('x', encoding='utf-8') as stream:
            stream.write(json.dumps(current, indent=2) + '\n')
        print(f'Wrote byte inventory to {args.out}; not a formal treatment freeze.')
    else:
        print(json.dumps(current, indent=2))

if __name__ == '__main__':
    main()
