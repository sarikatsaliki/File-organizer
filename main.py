import os
import shutil  # <-- 1. Add this (it stands for 'shell utilities')

folder_path = "test_folder"
files = os.listdir(folder_path)

for file in files:
    # This line prevents the script from trying to "move" a folder into itself
    if os.path.isdir(os.path.join(folder_path, file)):
        continue

    name, extension = os.path.splitext(file)
    ext = extension.lower()

    # 2. Decide the folder name
    if ext in [".jpg", ".png", ".jpeg"]:
        target = "Images"
    elif ext in [".txt", ".pdf", ".docx"]:
        target = "Documents"
    elif ext == ".mp3":
        target = "Audio"
    else:
        target = "Others"

    # 3. Create the folder if it doesn't exist
    target_dir = os.path.join(folder_path, target)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    new_file_path = os.path.join(target_dir, file)
        # 4. SAFETY CHECK: What if the file is already there?
    if os.path.exists(new_file_path):
        print(f"Skipping {file} - already exists in {target}")
        continue

    # 4. MOVE THE FILE
    # (Move from 'test_folder/file' to 'test_folder/target/file')
    shutil.move(os.path.join(folder_path, file), os.path.join(target_dir, file))
    
    print(f"Moved {file} -> {target}")