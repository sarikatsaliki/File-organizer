import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from main import organize_folder

class DebugHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # This will print EVERY change Windows sees
        if not event.is_directory:
            print(f"🔍 [DEBUG] Event: {event.event_type} | Path: {event.src_path}")
            
            # If the file is created or moved in, try to organize
            if event.event_type in ['created', 'moved', 'modified']:
                print("✨ Attempting to organize...")
                time.sleep(1) # Wait for Windows to 'let go' of the file
                
                # Get the folder and run your main logic
                project_root = os.path.dirname(os.path.abspath(__file__))
                test_folder = os.path.join(project_root, "test_folder")
                organize_folder(test_folder)

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_folder")
    
    event_handler = DebugHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    print(f"🚀 DEBUG MODE STARTING...")
    print(f"📂 Watching: {path}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()