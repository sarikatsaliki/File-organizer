import os
import requests
import time
from dotenv import load_dotenv

# 1. Initialize the environment loader
load_dotenv()

# 2. Fetch the token from your hidden .env file
# This is much safer than hardcoding the string!
TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

def get_ai_category(filename):
    """
    Connects to the Hugging Face Inference API to categorize a filename.
    Implements error handling for API latency and missing credentials.
    """
    if not TOKEN:
        print(" SECURITY ERROR: HF_TOKEN not found in .env file!")
        return "Others"

    headers = {"Authorization": f"Bearer {TOKEN.strip()}"}
    categories = ["Education", "Coding", "Personal", "Finance"]
    payload = {"inputs": filename, "parameters": {"candidate_labels": categories}}
    
    try:
        # Pinging the AI Model
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Handle "Model Loading" state (503 Service Unavailable)
        if response.status_code == 503:
            print(" AI model is warming up... Retrying in 15s.")
            time.sleep(15)
            return get_ai_category(filename)
            
        # Success state
        if response.status_code == 200:
            data = response.json()
            # Support for both single-result and list-result formats
            if isinstance(data, list): 
                data = data[0]
            
            # Extracting the most confident label
            return data.get("label") or data.get("labels")[0]
            
        return "Others"
    except Exception as e:
        print(f" AI Logic Exception: {e}")
        return "Others"