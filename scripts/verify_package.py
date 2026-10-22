#!/usr/bin/env python3
"""Check internal research website links, required files, and write a release manifest."""
from pathlib import Path
from hashlib import sha256
import json
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1]
website=root/'index.html'
soup=BeautifulSoup(website.read_text(encoding='utf-8'),'html.parser')
assert 'Icarus Online Research Field Station' in soup.title.string
assert len(soup.select('button[data-source]')) == 10
assert len(soup.select('button[data-condition]')) == 4
assert all((root/'materials'/x).exists() for x in ['Philosophy.md','Neutral.provisional.md','Philosophy.seed.md'])
errors=[]
for a in soup.select('a[href]'):
 link=a.get('href','')
 if link.startswith('#'):
  if not soup.select_one(link): errors.append(f'Broken anchor: {link}')
 elif link and not link.startswith(('https:','http:','mailto:')):
  if not (root/link).exists():errors.append(f'Broken local path: {link}')
assert not errors,'; '.join(errors)
entries={}
for path in sorted(root.rglob('*')):
 if not path.is_file() or path.name=='RELEASE_MANIFEST.json' or '__pycache__' in path.parts:
  continue
 rel=path.relative_to(root).as_posix()
 b=path.read_bytes()
 entries[rel]={'sha256':sha256(b).hexdigest(),'bytes':len(b)}
manifest={'title':'The Garden - Icarus Online LLC Independent Research','release':'v0.3','release_status':'research_design_not_preregistered_no_agent_runs',
 'note':'These hashes inventory the package. They are NOT frozen preregistration corpus hashes or evidence of an experiment.',
 'file_count':len(entries),'files':entries}
(root/'RELEASE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Verified {len(entries)} files, all website links resolve, required study materials present.')
