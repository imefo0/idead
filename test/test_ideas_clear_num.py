import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ideas import _clear_num
import json

def main():
    test = [
        ["20260808", "20260808"],
        ["22--22--22", "222222"],
        ["123abc123abc", "123123"],
        ["2026-08-07", "20260807"],
        ["abcabcbcbdjfnksndfkjn3#(4", "34"]
    ]

    results = []

    completed = 0
    all = len(test)
    for i, answer in test:
        result = _clear_num(i)
        results.append([result == answer, result, answer])
        if result == answer:
            completed += 1

    results.append((completed, all))

    return results

if __name__ == "__main__":
    main()
