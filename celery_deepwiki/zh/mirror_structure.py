import os
import shutil

SOURCE_DIR = '.'
TARGET_DIR = 'zh'
SKIP_DIRS = {TARGET_DIR, '.git', '.gemini', '__pycache__', '.idea', '.vscode'}

def mirror_structure():
    markdown_files = []
    
    if os.path.exists(TARGET_DIR):
        print(f"Directory {TARGET_DIR} already exists. Skipping creation to avoid accidental deletion, but will overwrite files.")
    else:
        os.makedirs(TARGET_DIR)

    for root, dirs, files in os.walk(SOURCE_DIR):
        # Filter out directories to skip
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        
        # Calculate relative path to mirror structure
        rel_path = os.path.relpath(root, SOURCE_DIR)
        if rel_path == '.':
            target_root = TARGET_DIR
        else:
            target_root = os.path.join(TARGET_DIR, rel_path)
            if not os.path.exists(target_root):
                os.makedirs(target_root)
        
        for file in files:
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(target_root, file)
            
            if file.lower().endswith('.md'):
                markdown_files.append((source_file_path, target_file_path))
            else:
                # Copy non-markdown files directly
                shutil.copy2(source_file_path, target_file_path)
                print(f"Copied: {file}")

    # Sort files for consistent processing order
    markdown_files.sort()
    
    print("\nFiles to translate:")
    for src, dst in markdown_files:
        print(f"{src} -> {dst}")

if __name__ == "__main__":
    mirror_structure()
