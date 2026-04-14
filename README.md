# AI-Driven Hybrid File Organizer

### 1. Problem Statement
Traditional organizers are context-blind. Sorting strictly by extension (e.g., all .pdf files into "Documents") fails to distinguish between technical lab reports, textbooks, and personal records.

### 2. Why I Built It
I needed a tool that could read filenames. This project combines local Python logic with NLP to differentiate between files like DBMS_Lab.pdf (Coding) and Savings_Statement.pdf (Finance) automatically.

### 3. Core Features
* **Event-Driven:** Uses watchdog for real-time folder monitoring.
* **Data-Driven:** Configuration managed via `config.json` for easy customization of file categories and extensions without touching the source code.
* **Hybrid Classification:**
  * Deterministic: O(1) dictionary lookup for media (Images, Audio).
  * Semantic: AI-powered analysis for documents using the Hugging Face Inference API.
* **Security:** API credentials managed via .env for safe deployment.

### 4. Architecture
The system utilizes a Hybrid Fall-through Architecture:

1. **Config Loader:** Loads `config.json` to decouple sorting rules from the execution logic.
2. **Observer:** Monitors the target folder for new file events.
3. **Fast Path:** Immediate extension check against a local dictionary dynamically built from JSON data.
4. **AI Fallback:** If the extension is ambiguous, the filename is sent to a BART-large-mnli model for classification.
5. **Execution:** shutil handles the physical move to the predicted destination with built-in collision and retry logic.

### 5. Future Planned Improvements
* Local LLM: Moving to Ollama for offline processing and privacy.
* Deep Scan: Classifying based on file content rather than just the title.
* GUI: A dashboard to monitor sorting accuracy and manual overrides.