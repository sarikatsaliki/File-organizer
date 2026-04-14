import time
import os
import shutil
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ai_logic import get_ai_category
with open('config.json', 'r') as f:
    config = json.load(f)
EXTENSIONS = config['extensions']
RETRIES = config['settings']['retries']
DELAY = config['settings']['delay']

class HybridHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Process only files and specific event types
        if not event.is_directory and event.event_type in ['created', 'moved']:
            filename = os.path.basename(event.src_path)

            # Skip system/script files
            if filename in ["main.py", "ai_logic.py", "automation.py", ".env"]:
                return

            # Step 1: Determine destination
            target_folder = self.get_destination(filename)
            
            # Step 2: Move with error handling
            self.execute_safe_move(event.src_path, target_folder, filename)

    def get_destination(self, filename):
        file_ext = os.path.splitext(filename)[1].lower()
        
        for category, ext_list in EXTENSIONS.items():
            if file_ext in ext_list:
                return category
        # AI-based sorting (Brain)
        print(f"Analyzing: {filename}")
        return get_ai_category(filename)

    def execute_safe_move(self, src, folder, name):
        project_root = os.path.dirname(os.path.abspath(__file__))
        dest_dir = os.path.join(project_root, "test_folder", folder)
        
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Handle existing files (Rename if duplicate)
        dest_path = os.path.join(dest_dir, name)
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(name)
            dest_path = os.path.join(dest_dir, f"{base}_{int(time.time())}{ext}")

        # Retry loop to handle "File in use" errors
        for i in range(RETRIES):
            try:
                if os.path.exists(src):
                    shutil.move(src, dest_path)
                    print(f"Sorted: {name} -> {folder}")
                    return
            except PermissionError:
                time.sleep(DELAY) # Wait for OS to release file
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(project_root, "test_folder")
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    observer = Observer()
    observer.schedule(HybridHandler(), path, recursive=False)
    observer.start()

    print(f"Monitoring: {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()