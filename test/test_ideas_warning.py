import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get, set_value
import json
from io import StringIO

def main():

    test = [
        ["enter y", True],
        ["enter n", False],
        ["enter c", False]
    ]

    warning_choice = get()["settings"]["all"]["warning_choice"]
    if not warning_choice:
        set_value("settings.all.warning_choice", True)

    results = []

    completed = 0
    all = len(test)
    for msg, answer in test:
        from ideas import _warning
        result = _warning(msg)

        results.append([result == answer, result, answer])

        if result == answer: completed += 1

    results.append((completed, all))

    set_value("settings.all.warning_choice", warning_choice)

    for i in results: print(i)

if __name__ == "__main__":
    main()
