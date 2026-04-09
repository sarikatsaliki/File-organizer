import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ai_logic import get_ai_category

class HybridHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory:
            if event.event_type in ['created', 'moved', 'modified']:
                filename = os.path.basename(event.src_path)

                # Skip system files and existing structure
                if filename in ["main.py", "ai_logic.py", "automation.py", ".env"] or "\\" in filename:
                    return

                # Wait for file handle to be released by OS
                time.sleep(1) 

                # Step 1: Extension-based sorting
                file_ext = os.path.splitext(filename)[1].lower()
                target_folder = None

                if file_ext in ['.mp3', '.wav', '.m4a', '.flac']:
                    target_folder = "Audio"
                elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
                    target_folder = "Images"
                elif file_ext in ['.mp4', '.mov', '.avi', '.mkv']:
                    target_folder = "Videos"
                elif file_ext in ['.zip', '.rar', '.7z', '.tar']:
                    target_folder = "Archives"

                # Step 2: AI Fallback
                if not target_folder:
                    target_folder = get_ai_category(filename)
                
                # Step 3: Move operation
                project_root = os.path.dirname(os.path.abspath(__file__))
                test_folder = os.path.join(project_root, "test_folder")
                target_dir = os.path.join(test_folder, target_folder)

                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                dest_path = os.path.join(target_dir, filename)

                try:
                    if os.path.exists(event.src_path):
                        shutil.move(event.src_path, dest_path)
                        print(f"Moved: {filename} -> {target_folder}")
                except Exception as e:
                    print(f"Error moving {filename}: {e}")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(project_root, "test_folder")
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    event_handler = HybridHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    print(f"Monitoring folder: {path}")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()