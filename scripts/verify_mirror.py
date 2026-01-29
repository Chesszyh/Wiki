#!/usr/bin/env python3
"""
验证 zh/ 是否在目录与 Markdown 文件列表上镜像原始工作区（除 zh/ 自身）。

用法: python3 scripts/verify_mirror.py
"""
import os
from pathlib import Path

ROOT = Path('.').resolve()
ZH = ROOT / 'zh'

def collect_files(base: Path):
    files = set()
    for dirpath, dirnames, filenames in os.walk(base):
        rel = os.path.relpath(dirpath, base)
        for f in filenames:
            p = os.path.normpath(os.path.join(rel, f))
            if p.startswith('.' + os.sep):
                p = p[2:]
            files.add(p.replace('\\', '/'))
    return files

def main():
    if not ZH.exists():
        print('错误: zh/ 目录不存在')
        return

    # collect original files (excluding zh/)
    originals = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # skip zh
        if os.path.abspath(dirpath).startswith(str(ZH)):
            continue
        rel = os.path.relpath(dirpath, ROOT)
        for f in filenames:
            relp = os.path.normpath(os.path.join(rel, f))
            if relp.startswith('.' + os.sep):
                relp = relp[2:]
            originals.add(relp.replace('\\', '/'))

    mirror = collect_files(ZH)

    only_in_orig = sorted(originals - mirror)
    only_in_mirror = sorted(mirror - originals)

    if not only_in_orig and not only_in_mirror:
        print('验证通过：zh/ 与原始目录镜像一致（文件路径级别）。')
    else:
        print('验证发现不一致：')
        if only_in_orig:
            print(f'  仅在原始目录中: {len(only_in_orig)} 个示例')
            for p in only_in_orig[:20]:
                print('    ', p)
        if only_in_mirror:
            print(f'  仅在 zh/ 中: {len(only_in_mirror)} 个示例')
            for p in only_in_mirror[:20]:
                print('    ', p)

if __name__ == '__main__':
    main()
