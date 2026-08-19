import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ideas import _jaccard_similarity
import json
import glob

def main():
    test = [
        [[["hel", "elo", "llo"], ["hel", "elo", "llo"]], 1.0],
        [[["abc"], ["ddd"]], 0.0],
        [[["abc"], ["abc", "ddd"]], 0.5],
        [[["abc", "bcd", "cde"], ["abc", "bcd", "cdf"]], 0.5],
        [[["hel", "elo", "llo"], ["hel", "ell", "llo", "lo ", "o w", " wo", "wor", "orl", "rld"]], 0.2]
    ]

    results = []

    completed = 0
    all = len(test)
    for i, answer in test:
        result = _jaccard_similarity(*i)
        #print(result)
        results.append([round(result, 3) == round(answer, 3), result, answer])
        if round(result, 3) == round(answer, 3):
            completed += 1
        #print(f"{"V" if round(result, 3) == round(answer, 3) else "X"} {round(result, 3)} {round(answer, 3)}")

    results.append((completed, all))

    return results

if __name__ == "__main__":
    main()


