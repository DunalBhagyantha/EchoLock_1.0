import os
from datetime import datetime

HISTORY_DIR = "data/chat_history"
os.makedirs(HISTORY_DIR, exist_ok=True)

def timestamp() -> str:
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def append_history(username: str, line: str):
    path = os.path.join(HISTORY_DIR, f"{username}.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def load_history(username: str, limit=50):
    path = os.path.join(HISTORY_DIR, f"{username}.txt")
    if not os.path.exists(path):
        return []
    lines = open(path, encoding="utf-8").read().splitlines()
    return lines[-limit:]
