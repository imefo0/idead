import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get, set_value
import json
from io import StringIO
from unittest.mock import patch

def main():
    test = [
        ["y", True], #!
        ["n", False],
        ["c", False],
        ["yes", True],
        ["YeS", True],
        ["Y", True],
        [" yes ", True],
        [" y e s ", True],
        [" Y E s   ", True],
        [" y E    s", True],
        [" y\ne S  ", True],
        [" y \t\t\t e s", True],
        [" y  yy eess", False], # может и true
        ["\t\t\tnoo\t\t\t\t\n\n\t", False],
        ["\t\n\t\n\t\n", False]
    ]
    warning_choice = get()["settings"]["all"]["warning_choice"]
    if not warning_choice:
        set_value("settings.all.warning_choice", True)

    results = []

    completed = 0
    all = len(test)
    for i, answer in test:
        with patch('builtins.input', return_value=i):
            from ideas import _warning
            result = _warning("")
            results.append([result == answer, result, answer])
            if result == answer:
                completed += 1

    results.append((completed, all))

    set_value("settings.all.warning_choice", warning_choice)

    #for i in results: print(i)

    return results

if __name__ == "__main__":
    main()
