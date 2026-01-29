#!/usr/bin/env python3
"""
Verify that zh/ mirrors the repository's Markdown files.
Usage: python tools/verify_zh_structure.py
Exits with code 0 if OK, non-zero if differences found.
"""
import os
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
source_root = repo_root
target_root = repo_root / 'zh'

# Load manifest if present
import json
manifest_path = repo_root / 'tools' / 'translation_manifest.json'
manifest = None
if manifest_path.exists():
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except Exception:
        manifest = None

# Gather source md files
source_md = [p.relative_to(source_root).as_posix() for p in source_root.rglob('*.md')]
source_md = sorted([s for s in source_md if not s.startswith('zh/') and not s.startswith('tools/')])

# Gather target md files
if not target_root.exists():
    print('zh/ directory does not exist. Nothing to verify.')
    sys.exit(2)

target_md = [p.relative_to(target_root).as_posix() for p in target_root.rglob('*.md')]
target_md = sorted(target_md)

# If manifest exists, find files marked as skipped (already existed) and exclude them from required list
skipped = set()
if manifest:
    for f in manifest.get('files', []):
        if f.get('status') == 'skipped':
            skipped.add(f.get('target'))

# Compute expected target paths from source paths
expected_targets = [os.path.join(*Path(p).parts) for p in source_md]
expected_targets = ['/'.join([str('')]) if False else '/'.join(parts) for parts in [Path(p).parts for p in source_md]]
# But we need them relative under zh/
expected_targets = [p for p in source_md]

# Now find missing and extra
missing = []
for src in source_md:
    tgt = str(src)
    if tgt in skipped:
        continue
    tgt_path = target_root / tgt
    if not tgt_path.exists():
        missing.append(tgt)

extra = []
for tgt in target_md:
    if tgt not in source_md:
        extra.append(tgt)

if not missing and not extra:
    print('OK: zh/ mirrors source Markdown files (accounting for skipped files).')
    sys.exit(0)

print('Differences detected:')
if missing:
    print('\nMissing files in zh/:')
    for m in missing:
        print(' -', m)
if extra:
    print('\nExtra files in zh/:')
    for e in extra:
        print(' -', e)

sys.exit(1)
