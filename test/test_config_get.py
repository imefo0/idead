import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get, folder_config
import json

def main():
    results = []

    completed = 0
    all = 1
    result = get()
    answer = (folder_config / "config.json").read_text()
    results.append([result == answer, result, answer])
    if result == answer:
        completed += 1

    results.append((completed, all))

    return results

if __name__ == "__main__":
    main()