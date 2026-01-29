#!/usr/bin/env python3
"""
创建 `zh/` 目录镜像：
- 递归遍历当前工作目录（不包含 zh/）
- 创建对应目录结构到 zh/
- 复制非 Markdown 文件到 zh/
- 复制 Markdown 文件到 zh/（作为初始占位，保留原文）
- 生成 translate_queue.txt 列出所有需要翻译的文件（相对路径）

用法: python3 scripts/mirror_and_prepare.py
"""
import os
import shutil
from pathlib import Path

ROOT = Path('.').resolve()
ZH = ROOT / 'zh'

EXCLUDE_DIRS = {'zh', '.git', '__pycache__'}


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return any(p in EXCLUDE_DIRS for p in parts)


def main():
    if not ZH.exists():
        ZH.mkdir()

    md_paths = []

    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT)
        if rel_dir == '.':
            rel_dir = ''
        # skip excluded top-level dirs
        if rel_dir.split(os.sep)[0] in EXCLUDE_DIRS:
            continue

        # create corresponding directory in zh/
        target_dir = ZH / rel_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        for fname in filenames:
            src = Path(dirpath) / fname
            # skip if the file is inside excluded dirs
            if should_skip(src):
                continue

            rel_path = Path(rel_dir) / fname if rel_dir else Path(fname)
            dest = ZH / rel_path

            # copy files: keep md files as-is (placeholders for translation)
            shutil.copy2(src, dest)

            if src.suffix.lower() == '.md':
                md_paths.append(str(rel_path))

    # write translate queue
    queue_file = ZH / 'translate_queue.txt'
    with queue_file.open('w', encoding='utf-8') as f:
        for p in sorted(md_paths):
            f.write(p.replace('\\', '/') + '\n')

    print(f"镜像已创建到: {ZH}")
    print(f"Markdown 文件数量: {len(md_paths)} (列表在 {queue_file})")


if __name__ == '__main__':
    main()
