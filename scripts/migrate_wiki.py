#!/usr/bin/env python3
# Usage: python3 scripts/migrate_wiki.py my-new-wiki/
# 脚本会自动完成：
# 1. 在 docs/en/ 和 docs/zh/ 创建 my-new-wiki 文件夹。
# 2. 移动文件（并自动剥离 zh/ 层级）。
# 3. 更新 docs/en/index.md，添加指向该 Wiki 概览页的链接。
# 4. 在 docs/en/.pages 和 docs/zh/.pages 中注册该目录。

import os
import shutil
import re
import argparse
from typing import Optional

def get_overview_file(directory: str) -> str:
    """尝试寻找最适合作为索引页的文件"""
    files = [f for f in os.listdir(directory) if f.endswith(".md")]
    # 优先级：1-overview.md > 1-xxx-overview.md > index.md > 第一个文件
    priority_patterns = [
        r"^1-overview\.md$",
        r"overview\.md$",
        r"^index\.md$"
    ]
    for pattern in priority_patterns:
        for f in files:
            if re.search(pattern, f, re.IGNORECASE):
                return f
    # 如果没找到，返回第一个带数字的文件或任意一个
    files.sort()
    return files[0] if files else "index.md"

def update_nav_pages(pages_path: str, wiki_name: str):
    """更新 .pages 文件中的 nav 列表"""
    if not os.path.exists(pages_path):
        with open(pages_path, "w", encoding="utf-8") as f:
            f.write("nav:\n  - index.md\n")
    
    with open(pages_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 检查是否已存在
    if any(wiki_name in line for line in lines):
        return

    # 找到 nav: 标记并插入
    with open(pages_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)
            if "nav:" in line:
                f.write(f"  - {wiki_name}\n")

def update_index_md(index_path: str, wiki_name: str, overview_file: str):
    """更新 docs/en/index.md 的列表"""
    if not os.path.exists(index_path):
        return

    display_name = wiki_name.replace("_", " ").replace("-", " ").title()
    new_entry = f"* [{display_name}]({wiki_name}/{overview_file})"
    
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if new_entry in content:
        return

    # 找到 ## Available Wikis 并在其后插入（按字母排序比较复杂，这里简单追加）
    pattern = r"(## Available Wikis\s*\n)"
    replacement = f"\\1{new_entry}\n"
    new_content = re.sub(pattern, replacement, content)
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)

def migrate(src_dir: str, wiki_name: Optional[str] = None):
    if not wiki_name:
        wiki_name = os.path.basename(src_dir.rstrip("/"))
    
    base_docs = "docs"
    dst_en = os.path.join(base_docs, "en", wiki_name)
    dst_zh = os.path.join(base_docs, "zh", wiki_name)
    
    print(f">>> Migrating {wiki_name} to docs/...")
    os.makedirs(dst_en, exist_ok=True)
    os.makedirs(dst_zh, exist_ok=True)
    
    # 1. 处理文件迁移
    src_zh = os.path.join(src_dir, "zh")
    items = os.listdir(src_dir)
    
    for item in items:
        src_item = os.path.join(src_dir, item)
        # 排除项
        if item == "zh":
            continue
        if item.endswith(".py") or item.endswith(".sh"):
            continue
            
        # 移动到 EN
        shutil.move(src_item, os.path.join(dst_en, item))
    
    # 处理 ZH
    if os.path.exists(src_zh):
        for zh_item in os.listdir(src_zh):
            shutil.move(os.path.join(src_zh, zh_item), os.path.join(dst_zh, zh_item))
        os.rmdir(src_zh)

    # 2. 更新导航
    overview = get_overview_file(dst_en)
    update_index_md(os.path.join(base_docs, "en", "index.md"), wiki_name, overview)
    update_nav_pages(os.path.join(base_docs, "en", ".pages"), wiki_name)
    
    # 如果有中文，也更新中文导航
    if os.listdir(dst_zh):
        update_nav_pages(os.path.join(base_docs, "zh", ".pages"), wiki_name)
    else:
        # 如果没中文内容，清理空目录
        os.rmdir(dst_zh)
        
    print(f"Successfully migrated {wiki_name}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate a wiki directory to docs/en and docs/zh structure.")
    parser.add_argument("src", help="Source wiki directory")
    parser.add_argument("--name", help="Override wiki name (optional)")
    args = parser.parse_args()
    
    migrate(args.src, args.name)
