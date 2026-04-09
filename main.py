import os
import shutil
from ai_logic import get_ai_category

# 1. SETUP: Where are the files?
# Use "." to scan the current folder where the script is
SOURCE_DIR = "." 

# 2. THE SIMPLE MAP (Fast & Local)
EXTENSION_MAP = {
    ".jpg": "Personal",
    ".png": "Personal",
    ".mp4": "Personal",
    ".py": "Coding",
    ".cpp": "Coding",
    ".java": "Coding",
    ".xlsx": "Finance",
    ".csv": "Finance"
}

def organize_files():
    required_folders = ["Education", "Coding", "Personal", "Finance", "Others"]
    
    for folder in required_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f" Created missing folder: {folder}")
    print("Starting File Organizer...")
    
    # Loop through every file in the folder
    for filename in os.listdir(SOURCE_DIR):
        # Skip the scripts themselves!
        if filename in ["main.py", "ai_logic.py", "test_ai.py"]:
            continue
            
        # Skip folders
        if os.path.isdir(os.path.join(SOURCE_DIR, filename)):
            continue

        print(f"\n🔍 Processing: {filename}")
        
        # --- PHASE 1: Check Extension (Speed) ---
        file_ext = os.path.splitext(filename)[1].lower()
        target_folder = EXTENSION_MAP.get(file_ext)

        # --- PHASE 2: Ask AI (The Brain) ---
        if not target_folder:
            print(f" Extension '{file_ext}' unknown. Asking AI...")
            target_folder = get_ai_category(filename)
        
        # --- PHASE 3: Move the File ---
        dest_path = os.path.join(SOURCE_DIR, target_folder, filename)
        
        try:
            shutil.move(filename, dest_path)
            print(f" Moved to -> {target_folder}")
        except Exception as e:
            print(f" Could not move {filename}: {e}")

if __name__ == "__main__":
    organize_files()