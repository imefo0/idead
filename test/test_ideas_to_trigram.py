import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ideas import _to_trigram

def main():
    test = [
        ["1234567890", ["123", "234", "345", "456", "567", "678", "789", "890"]],
        ["abc", ["abc"]],
        ["''", ["''"]],
        ["%%%%", ["%%%", "%%%"]],
        ["hello world", ["hel", "ell", "llo", "lo ", "o w", " wo", "wor", "orl", "rld"]],
        ["+", ["+"]],
        ["yyoo", ["yyo", "yoo"]],
        ["", [""]]
    ]

    results = []

    completed = 0
    all = len(test)
    for i, answer in test:
        result = _to_trigram(i)
        #print(result)
        results.append([result == answer, result, answer])
        if result == answer:
            completed += 1

    results.append((completed, all))

    return results

if __name__ == "__main__":
    main()


