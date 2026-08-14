import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from main import _parse_value
import json
from io import StringIO

def main():

    test = [
        ["settings.all.warning_choice", "true", True],
        ["settings.ideas.format", "4", "4"],
        ["settings.ideas.search.max_results", "fff", "E: Invalid Type"],
        ["settings.ideas.search.table_columns", "['fff', 'score', 'name', 'abc']", ["fff", "score", "name", "abc"]],
        ["settings.settings", "akmsdfl", "E: No Path Found"],
        ["settings.all", "mmm", "E: No Path Found"]
    ]

    results = []


    completed = 0
    all = len(test)
    for path, value, answer in test:
        try:
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            result = _parse_value(value, path)
            parser = sys.stdout.getvalue()
            sys.stdout = old_stdout

            #if answer == result:
            #    print(f"ok: {result} --> {answer}")
            #    completed += 1
            #else:
            #    print(f" e: {result} -X> {answer}")
            results.append([answer == result, result, answer])

        except SystemExit:
            parser = sys.stdout.getvalue()
            sys.stdout = old_stdout

            #if parser.strip() == answer:
            #    print(f"ok: {parser.strip()} --> {answer}")
            #    completed += 1
            #else:
            #    print(f" e: {parser.strip()} -X> {answer}")
            results.append([parser.strip() == answer, parser.strip(), answer])

    #print(f"{completed}/{all} | {(completed/all*100):.0f}%")

    results.append((completed, all))



if __name__ == "__main__":
    main()
