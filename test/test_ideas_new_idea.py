import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ideas import test_new_idea
import json
import glob

def main():
    test = [
        [["test", "desc"], ["test", "desc"]],
        [["name", "--- desc ---"], ["name", "--- desc ---"]],
        [["uuid --- ---", "--- name: name ---"], ["uuid --- ---", "--- name: name ---"]],
        [["uuid: uuiddd ---123---", "---"], ["uuid: uuiddd ---123---", "---"]],
        [["final test --------------- --- --- --- --- desc: dd --- d: name: name: --- date: errrror", "ff--- --- ---"],
         ["final test --------------- --- --- --- --- desc: dd --- d: name: name: --- date: errrror", "ff--- --- ---"]
        ]
    ]

    results = []

    completed = 0
    all = len(test)
    for i, answer in test:
        uuid6 = test_new_idea(*i)
        with open(next((Path.home() / ".cache" / "idead" / "tests" / "ideas").glob(f"*{uuid6}*.md")), "r") as f:
            text = f.read().split("\n")
        result = [text[1][6:], text[-1]]
        #print(result)
        results.append([result == answer, result, answer])
        if result == answer:
            completed += 1

    results.append((completed, all))

    return results

if __name__ == "__main__":
    main()

