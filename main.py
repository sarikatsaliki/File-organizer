import os
import shutil

# mapping of extensions to their respective folders
EXTENSION_MAP = {
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
    ".pdf": "Documents", ".txt": "Documents", ".docx": "Documents",
    ".mp3": "Audio",
    ".zip": "Archives"
}

def organize_folder(folder_path):
    # Ensure the folder exists before scanning
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return

    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)

        # Skip if it's a directory (we only move files)
        if os.path.isdir(full_path):
            continue

        name, extension = os.path.splitext(file)
        ext = extension.lower()
        
        # Use 'Others' for unknown file types
        target = EXTENSION_MAP.get(ext, "Others")
        target_dir = os.path.join(folder_path, target)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        new_file_path = os.path.join(target_dir, file)

        # Only move if the file doesn't already exist in the target
        if not os.path.exists(new_file_path):
            shutil.move(full_path, new_file_path)
            print(f"✅ Moved: {file} -> {target}")

if __name__ == "__main__":
    # Test path (uses current directory)
    base_path = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(base_path, "test_folder")
    organize_folder(test_path)