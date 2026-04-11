### 1. The Trigger: Event-Driven Monitoring
The script uses the `watchdog` library to act as a background service. Instead of checking the folder manually, it "subscribes" to operating system signals.
* **Mechanism:** When a file is dropped into the folder, the OS triggers a `created` event.
* **Safety Delay:** A `time.sleep(1)` is implemented to ensure the file is fully downloaded and "released" by the OS before the script attempts to move it.

### 2. Tier 1: Deterministic Classification (The Fast Path)
This is the "Rules" layer. It uses a Python Dictionary (`EXTENSION_MAP`) for instant sorting.
* **Efficiency:** This is an O(1) lookup, meaning the speed is constant regardless of how many files you have.
* **Use Case:** We use this for media files (JPG, MP3, MP4) because their destination is fixed and doesn't require "thinking" or context.

### 3. Tier 2: Semantic Classification (The AI Path)
If a file has an ambiguous extension (like .pdf, .txt, or .py), the logic "falls through" to the AI layer.
* **NLP Intelligence:** The filename is sent to the Hugging Face Inference API (`bart-large-mnli`). 
* **Context Awareness:** Unlike Tier 1, the AI understands the "meaning" of the words. It knows "Operating_Systems.pdf" belongs in Education, while "script.py" belongs in Coding.
* **Zero-Shot Learning:** The model is flexible; it can classify files into our specific folders without needing to be "trained" on our personal data first.

### 4. The Execution: I/O Operations
Once the destination is decided, the script handles the physical organization:
* **Self-Healing:** It checks if the destination folder exists; if not, it uses `os.makedirs` to create it on the fly.
* **Atomic Move:** It uses `shutil.move` to relocate the file.
* **Error Handling:** The process is wrapped in `try-except` blocks. If the internet is down or a file is "in use," the script prints an error instead of crashing, allowing the watchdog to keep monitoring.