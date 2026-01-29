# -*- coding: utf-8 -*-
"""
Automated translation helper (conservative).
This script creates zh/ translations for markdown files under the repo.
It performs limited, conservative translations and appends glossary entries the first time they appear (outside code fences and inline code).
"""
import os
import io
import re
import json
import hashlib

ROOT = "/home/chesszyh/Downloads/tests/vscode_deepwiki"
ZH_ROOT = os.path.join(ROOT, "zh")

# Conservative glossary with chosen Chinese equivalents.
GLOBAL_GLOSSARY = {
    "VS Code": "Visual Studio Code",
    "Monaco Editor": "Monaco 编辑器",
    "Electron": "Electron 运行时",
    "xterm.js": "xterm.js 终端模拟器",
    "TypeScript": "TypeScript 语言",
    "Extension Host": "扩展主机",
    "ExtensionHostStarter": "扩展主机启动器",
    "PtyHost": "PTY 主机",
    "PtyHostService": "PTY 主机服务",
    "Workbench": "工作台",
    "InstantiationService": "实例化服务",
    "ITextModel": "ITextModel 接口",
    "CodeApplication": "CodeApplication 应用",
    "ExtensionHost": "扩展主机",
    "CodeEditorService": "代码编辑器服务",
}

# Phrase translations for headings and common labels (conservative)
PHRASE_MAP = {
    "Overview": "概览",
    "Purpose": "目的",
    "Scope": "范围",
    "Multi-Process Architecture": "多进程架构",
    "Core Platform Components": "核心平台组件",
    "Major Subsystems": "主要子系统",
    "Execution Modes": "执行模式",
    "Dependency Management and Build System": "依赖管理与构建系统",
    "Service Initialization and Dependency Injection": "服务初始化与依赖注入",
    "Configuration System": "配置系统",
    "Navigation Guide": "导航指南",
    "Key Classes": "主要类",
    "Primary Location": "主要位置",
    "Location": "位置",
    "Details": "细节",
    "Sources": "来源",
    "Key Files": "关键文件",
    "Key Dependencies": "关键依赖",
    "Build Pipeline Overview": "构建流水线概览",
}

# Phrases to replace in non-code regions
COMMON_REPLACEMENTS = {
    "**Purpose**": "**目的**",
    "**Scope**": "**范围**",
    "**Sources**": "**来源**",
    "**Details**": "**细节**",
    "**Primary Location**": "**主要位置**",
    "**Location**": "**位置**",
    "**Key Classes**": "**主要类**",
}

# Files to skip (existing translations)
SKIP_EXISTING = set([
    os.path.join(ZH_ROOT, "1-overview.md"),
    os.path.join(ZH_ROOT, "2-build-system-and-development.md"),
])

# Collect source files
md_files = []
for root, dirs, files in os.walk(ROOT):
    # skip zh directory
    if root.startswith(ZH_ROOT):
        continue
    for f in files:
        if f.endswith('.md'):
            md_files.append(os.path.join(root, f))
md_files = sorted(md_files)

# We'll build manifest entries
translation_manifest = []
translation_glossary = {}  # original -> {"zh":..., "file":...}
summary = {"total": 0, "translated": 0, "skipped": 0, "errors": []}

# Maintain set of glossary terms that have been introduced
introduced = set()

# Helper: compute sha1

def sha1_of_text(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()

# Helper: split into code fence and non-code segments
code_fence_re = re.compile(r'(^```.*?$\n.*?^```\n?)', re.MULTILINE | re.DOTALL)
inline_code_re = re.compile(r'(`[^`]*`)')

# Term match boundaries: ensure we match whole words or punctuation boundaries

def make_term_regex(term):
    # escape
    t = re.escape(term)
    return re.compile(r'(?<![`\w\-./])(' + t + r')(?![`\w\-./])')

TERM_REGEXES = {t: make_term_regex(t) for t in GLOBAL_GLOSSARY.keys()}

# Process each file
for src in md_files:
    summary['total'] += 1
    # Build target path
    rel = os.path.relpath(src, ROOT)
    target = os.path.join(ZH_ROOT, rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    if target in SKIP_EXISTING or os.path.exists(target) and os.path.basename(target) in ["1-overview.md","2-build-system-and-development.md"]:
        translation_manifest.append({
            "original_path": src,
            "translated_path": target,
            "status": "skipped - exists",
            "translator": "Claude Code",
            "glossary_entries": [],
            "sha1": None,
        })
        summary['skipped'] += 1
        continue
    try:
        with io.open(src, 'r', encoding='utf-8') as fh:
            text = fh.read()
    except Exception as e:
        summary['errors'].append({"file": src, "error": str(e)})
        translation_manifest.append({
            "original_path": src,
            "translated_path": target,
            "status": "error",
            "translator": "Claude Code",
            "glossary_entries": [],
            "sha1": None,
        })
        continue

    # Split into segments by code fences; keep fences intact
    parts = []
    last = 0
    for m in code_fence_re.finditer(text):
        start, end = m.span()
        if start > last:
            parts.append((False, text[last:start]))
        parts.append((True, text[start:end]))
        last = end
    if last < len(text):
        parts.append((False, text[last:]))

    per_file_glossary = []

    # Process non-code parts
    new_parts = []
    for is_code, seg in parts:
        if is_code:
            new_parts.append(seg)
            continue
        s = seg
        # Replace common bolded headings like **Purpose** etc
        for k, v in COMMON_REPLACEMENTS.items():
            s = s.replace(k, v)
        # Replace heading titles if line starts with #
        def repl_heading(m):
            hashes = m.group(1)
            title = m.group(2).strip()
            new_title = PHRASE_MAP.get(title, title)
            return f"{hashes} {new_title}"
        s = re.sub(r'^(\#{1,6})\s+(.*)$', repl_heading, s, flags=re.MULTILINE)

        # Translate image alt text outside code
        def repl_img(m):
            alt = m.group(1)
            path = m.group(2)
            # simple translation: if alt is English words, attempt mapping via PHRASE_MAP
            new_alt = PHRASE_MAP.get(alt, alt)
            return f'![{new_alt}]({path})'
        s = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', repl_img, s)

        # For each glossary term, find first occurrence outside inline code
        for term, zh in GLOBAL_GLOSSARY.items():
            if term in introduced:
                continue
            # search in s but not inside inline code
            pieces = inline_code_re.split(s)
            rebuilt = []
            found = False
            for i, piece in enumerate(pieces):
                if i % 2 == 1:
                    # inside inline code, leave
                    rebuilt.append(piece)
                    continue
                # search for term
                regex = TERM_REGEXES[term]
                m = regex.search(piece)
                if m and not found:
                    # append translation after the term
                    # only if the term is not inside backticks (we're in non-inline piece)
                    def _rep(mg):
                        return mg.group(1) + '（' + zh + '）'
                    piece = regex.sub(_rep, piece, count=1)
                    found = True
                    introduced.add(term)
                    translation_glossary[term] = {"zh": zh, "file": src}
                    per_file_glossary.append({"original": term, "zh": zh})
                rebuilt.append(piece)
            s = ''.join(rebuilt)
        new_parts.append(s)

    new_text = ''.join(new_parts)

    # Final minimal cleanups: replace some English labels
    label_map = {
        "**Key Classes**": "**主要类**",
    }
    for k, v in label_map.items():
        new_text = new_text.replace(k, v)

    # Write file
    try:
        with io.open(target, 'w', encoding='utf-8') as fh:
            fh.write(new_text)
    except Exception as e:
        summary['errors'].append({"file": target, "error": str(e)})
        translation_manifest.append({
            "original_path": src,
            "translated_path": target,
            "status": "error_write",
            "translator": "Claude Code",
            "glossary_entries": per_file_glossary,
            "sha1": None,
        })
        continue

    sha1 = sha1_of_text(new_text)
    translation_manifest.append({
        "original_path": src,
        "translated_path": target,
        "status": "translated",
        "translator": "Claude Code",
        "glossary_entries": per_file_glossary,
        "sha1": sha1,
    })
    summary['translated'] += 1

# Write zh/translation_manifest.json
os.makedirs(ZH_ROOT, exist_ok=True)
with io.open(os.path.join(ZH_ROOT, 'translation_manifest.json'), 'w', encoding='utf-8') as fh:
    json.dump(translation_manifest, fh, indent=2, ensure_ascii=False)

# Write zh/translation_glossary.json
with io.open(os.path.join(ZH_ROOT, 'translation_glossary.json'), 'w', encoding='utf-8') as fh:
    json.dump(translation_glossary, fh, indent=2, ensure_ascii=False)

# Update tools/translation_manifest.json (merge safely)
TOOLS_DIR = os.path.join(ROOT, 'tools')
os.makedirs(TOOLS_DIR, exist_ok=True)
tools_manifest_path = os.path.join(TOOLS_DIR, 'translation_manifest.json')
existing_tools = []
if os.path.exists(tools_manifest_path):
    try:
        with io.open(tools_manifest_path, 'r', encoding='utf-8') as fh:
            loaded = json.load(fh)
            # Support two formats: a dict with a 'files' list (existing tool manifest), or a direct list
            if isinstance(loaded, dict) and 'files' in loaded and isinstance(loaded['files'], list):
                existing_tools = loaded['files']
            elif isinstance(loaded, list):
                existing_tools = loaded
            else:
                existing_tools = []
    except Exception:
        existing_tools = []
# Merge by original_path
existing_map = {e['original_path']: e for e in existing_tools if isinstance(e, dict) and 'original_path' in e}
for e in translation_manifest:
    existing_map[e['original_path']] = e
merged = list(existing_map.values())
with io.open(tools_manifest_path, 'w', encoding='utf-8') as fh:
    # write as a list for simplicity
    json.dump(merged, fh, indent=2, ensure_ascii=False)

# Write summary to /tmp
summary['total'] = summary['total']
summary['glossary_count'] = len(translation_glossary)
with io.open('/tmp/translation_agent_summary.json', 'w', encoding='utf-8') as fh:
    json.dump(summary, fh, indent=2, ensure_ascii=False)

print('Done')
