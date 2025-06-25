#utils.py

import os
import json
from datetime import datetime

def log_to_file(message: str, logfile="logs/app.log"):
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    with open(logfile, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def load_config(path="config.json"):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(data, path="config.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
