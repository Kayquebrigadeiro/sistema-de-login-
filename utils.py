import json
import time

def now_ts():
    return int(time.time())

def load_users(path):
    try:
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

def save_users(path, data):
    # salva com indent para leitura fácil
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)