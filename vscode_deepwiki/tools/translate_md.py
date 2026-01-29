#!/usr/bin/env python3
"""
Translate Markdown files into Simplified Chinese while preserving code blocks and inline code.

This script reads tools/translation_manifest.json for the list of files to process.
It writes translated files to zh/<original path> (creates directories as needed).

Translation backend: unofficial Google Translate HTTP endpoint. This is a best-effort machine translation.

Behavior:
- If target file already exists, the file is skipped (status set to 'skipped').
- Fenced code blocks (```...```) and inline code (`...`) are preserved and NOT translated.
- Other Markdown content is submitted for translation.
- Updates tools/translation_manifest.json with status, size, sha256 and writes tools/translation_log.json with detailed per-file records.

WARNING: This uses an unofficial translate endpoint and may be rate-limited. Use with care.
"""

import re
import json
import os
import sys
import hashlib
from pathlib import Path
from urllib.parse import quote_plus
import urllib.request
import time

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tools' / 'translation_manifest.json'
LOG = ROOT / 'tools' / 'translation_log.json'
ZH_ROOT = ROOT / 'zh'

if not MANIFEST.exists():
    print('Manifest not found:', MANIFEST)
    sys.exit(2)

with open(MANIFEST, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

files = manifest.get('files', [])

# Helpers
CODE_FENCE_RE = re.compile(r'(```[\s\S]*?```)', re.MULTILINE)
INLINE_CODE_RE = re.compile(r'(`[^`]+?`)', re.MULTILINE)


def protect_code(text):
    """Replace code fences and inline code with placeholders and return mapping."""
    placeholders = {}
    i = 0

    def repl_fence(m):
        nonlocal i
        key = f"__CODEBLOCK_{i}__"
        placeholders[key] = m.group(1)
        i += 1
        return key

    text = CODE_FENCE_RE.sub(repl_fence, text)

    # Now inline code
    def repl_inline(m):
        nonlocal i
        key = f"__INLINE_{i}__"
        placeholders[key] = m.group(1)
        i += 1
        return key

    text = INLINE_CODE_RE.sub(repl_inline, text)
    return text, placeholders


def restore_placeholders(text, placeholders):
    for k, v in placeholders.items():
        text = text.replace(k, v)
    return text


def sha256_bytes(b: bytes):
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()


def translate_text(text, src='en', tgt='zh-CN'):
    """Translate text using unofficial Google translate endpoint. Returns translated string."""
    if not text.strip():
        return text
    # The API can take limited length; chunk if necessary
    # We'll split by double newlines to try to preserve paragraph boundaries
    parts = text.split('\n\n')
    translated_parts = []

    for part in parts:
        if not part.strip():
            translated_parts.append(part)
            continue
        # URL encode
        q = quote_plus(part)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={src}&tl={tgt}&dt=t&q={q}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode('utf-8')
                # Response is a JS-style array, parse minimally
                # Typical: [[['translated text', 'orig', ...],...],...]
                # We'll extract all first elements
                m = re.findall(r'\[\[\["(.*?)"', body)
                if m:
                    translated = m[0]
                else:
                    # fallback: try to parse by splitting
                    translated = re.sub(r"\],.*", '', body)
                    translated = translated
                # Unescape sequences if any
                translated_parts.append(translated)
        except Exception as e:
            print('Translation error for part:', repr(e))
            # On error, fallback to original text to avoid data loss
            translated_parts.append(part)
        time.sleep(0.5)  # be gentle

    return '\n\n'.join(translated_parts)


log = []

for item in files:
    src = item.get('source')
    tgt = item.get('target')
    src_path = ROOT / src
    tgt_path = ROOT / tgt

    rec = {
        'source': src,
        'target': tgt,
        'status': 'pending',
        'bytes': 0,
        'sha256': '',
        'error': ''
    }

    try:
        if tgt_path.exists():
            rec['status'] = 'skipped'
            print('Skipping existing target:', tgt)
            item['status'] = 'skipped'
            log.append(rec)
            continue

        text = src_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            text = src_path.read_text(encoding='latin-1')
            rec['error'] = 'decoded-latin1'
        except Exception as e:
            rec['status'] = 'error'
            rec['error'] = 'read-error:' + str(e)
            log.append(rec)
            item['status'] = 'error'
            continue
    except Exception as e:
        rec['status'] = 'error'
        rec['error'] = 'read-error:' + str(e)
        log.append(rec)
        item['status'] = 'error'
        continue

    # Protect code blocks and inline code
    protected_text, placeholders = protect_code(text)

    # Translate the protected_text
    translated = translate_text(protected_text, src='en', tgt='zh-CN')

    # Restore placeholders
    final = restore_placeholders(translated, placeholders)

    # Ensure target directory exists
    tgt_path.parent.mkdir(parents=True, exist_ok=True)
    tgt_path.write_text(final, encoding='utf-8')

    b = final.encode('utf-8')
    rec['bytes'] = len(b)
    rec['sha256'] = sha256_bytes(b)
    rec['status'] = 'translated'
    item['status'] = 'translated'
    print('Translated:', src, '->', tgt)
    log.append(rec)

# Update manifest and write log
with open(MANIFEST, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

with open(LOG, 'w', encoding='utf-8') as f:
    json.dump(log, f, indent=2, ensure_ascii=False)

print('Done. Translated files:', sum(1 for r in log if r['status']=='translated'))
print('Skipped files:', sum(1 for r in log if r['status']=='skipped'))
print('Errors:', sum(1 for r in log if r['status']=='error'))
