import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import resolve_templates
import json

def main():
    test = [
        [
            {"a": {"b": "2", "c": "5"}, "bb": {"cccc": "321", "dd": "{a.b}+{a.c}-{bb.cccc}"}},
            {"a": {"b": "2", "c": "5"}, "bb": {"cccc": "321", "dd": "2+5-321"}},
        ],
        [
            {"a": {"b": "c", "c": "b"}, "c": {"b": "r", "e": "f"}, "r": {"f": "hello"}, "e": "{{{a.b}.{a.c}}.{c.e}}"},
            {"a": {"b": "c", "c": "b"}, "c": {"b": "r", "e": "f"}, "r": {"f": "hello"}, "e": "hello"}
        ],
        [
            {"a": {"b": "abc", "c": "ddd"}, "f": "{a.c}", "r": {"a": "{f} ~ {a.b}"}},
            {"a": {"b": "abc", "c": "ddd"}, "f": "ddd", "r": {"a": "ddd ~ abc"}}
        ]
    ]

    results = []

    completed = 0
    all = len(test)
    for i, answer in test:
        result = resolve_templates(i)
        results.append([result == answer, result, answer])
        if result == answer:
            completed += 1

    results.append((completed, all))
    #print(results)
    return results

if __name__ == "__main__":
    main()

