import os
import shutil
from ai_logic import get_ai_category

SOURCE_DIR = "." 

# Fast mapping for non-ambiguous media
EXTENSION_MAP = {
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    ".mp3": "Audio", ".wav": "Audio",
    ".mp4": "Videos", ".mov": "Videos",
    ".zip": "Archives", ".rar": "Archives"
}

def organize_files():
    required_folders = ["Images", "Audio", "Videos", "Documents", "Education", "Coding", "Finance", "Archives", "Others"]
    
    for folder in required_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            
    for filename in os.listdir(SOURCE_DIR):
        # Ignore system/script files
        if filename in ["main.py", "ai_logic.py", "automation.py", ".env"] or os.path.isdir(filename):
            continue

        file_ext = os.path.splitext(filename)[1].lower()
        target_folder = EXTENSION_MAP.get(file_ext)

        # AI handles documents, code, and unknown types
        if not target_folder:
            target_folder = get_ai_category(filename)
        
        dest_path = os.path.join(SOURCE_DIR, target_folder, filename)
        
        try:
            shutil.move(filename, dest_path)
            print(f"Moved: {filename} -> {target_folder}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    organize_files()