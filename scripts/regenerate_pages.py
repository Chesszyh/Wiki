import os
from pathlib import Path
from natsort import natsorted

DOCS_DIR = Path('docs')
EN_DIR = DOCS_DIR / 'en'
ZH_DIR = DOCS_DIR / 'zh'

def generate_pages():
    print("Regenerating .pages files with combined natural sorting...")
    for lang_dir in [EN_DIR, ZH_DIR]:
        if not lang_dir.exists():
            continue
            
        for root, dirs, files in os.walk(lang_dir):
            root_path = Path(root)
            
            # Filter files
            # Exclude index.md from the sorted list (handle it separately)
            # Exclude _sidebar.md as it's likely configuration/metadata not meant for main nav
            md_files = [f for f in files if f.endswith('.md') and f != 'index.md' and f != '_sidebar.md']
            
            # Filter directories
            # Exclude hidden directories
            visible_dirs = [d for d in dirs if not d.startswith('.')]
            
            # Combine files and directories for sorting
            # We want to sort them based on their names naturally
            # e.g. "1-intro.md" comes before "2-setup"
            # "2-setup.md" and "2-setup/" ... natsort handles this well usually
            
            combined_items = md_files + visible_dirs
            combined_items = natsorted(combined_items)
            
            # Create .pages content
            content = "nav:\n"
            
            # Add index.md first if exists
            if 'index.md' in files:
                 content += "  - index.md\n"
                 
            for item in combined_items:
                content += f"  - {item}\n"
            
            # Write .pages
            # Only write if we have something to navigate
            if combined_items or 'index.md' in files:
                pages_file = root_path / ".pages"
                with open(pages_file, "w") as f:
                    f.write(content)
                # print(f"Updated {pages_file}")
                
    print(".pages regeneration complete.")

if __name__ == "__main__":
    generate_pages()
