import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get_nested
import json

def main():
    test = [
        [
            [{"a": {"b": "321", "x": "2+5-321"}}, ["a", "b"]],
            "321"
        ],
        [
            [{"a": {"b": {"e": "1", "x": 17}}}, ["a", "b", "e", "x"]],
            None
        ]
    ]

    results = []

    completed = 0
    all = len(test)
    for i, answer in test:
        result = get_nested(*i)
        results.append([result == answer, result, answer])
        if result == answer:
            completed += 1

    results.append((completed, all))
    #print(results)
    return results

if __name__ == "__main__":
    main()


