import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from main import _parse_value
import json
from io import StringIO

def main():

    #test = [
    #    ["settings.all.warning_choice", "true", True],
    #    ["settings.ideas.format", "4", "4"],
    #    ["settings.ideas.search.max_results", "fff", "E: Invalid Type"],
    #    ["settings.ideas.search.table_columns", "['fff', 'score', 'name', 'abc']", ["fff", "score", "name", "abc"]],
    #    ["settings.settings", "akmsdfl", "E: No Path Found"],
    #    ["settings.all", "mmm", "E: No Path Found"]
    #]

    test = [
        # ===== 1. BOOLEAN (bool) =====
        ["settings.all.warning_choice", "true", True],
        ["settings.all.warning_choice", "false", False],
        ["settings.all.warning_choice", "True", True],      # с большой буквы
        ["settings.all.warning_choice", "False", False],    # с большой буквы
        ["settings.all.warning_choice", "TRUE", True],      # капс
        ["settings.all.warning_choice", "FALSE", False],    # капс
        ["settings.all.warning_choice", "yes", "E: Invalid Type"],   # не bool
        ["settings.all.warning_choice", "1", "E: Invalid Type"],     # не bool
        ["settings.all.warning_choice", "0", "E: Invalid Type"],     # не bool
        
        # ===== 2. INTEGER (int) =====
        ["settings.ideas.search.max_results", "5", 5],
        ["settings.ideas.search.max_results", "0", 0],
        ["settings.ideas.search.max_results", "-1", -1],
        ["settings.ideas.search.max_results", "100", 100],
        ["settings.ideas.search.max_results", "999999", 999999],
        ["settings.ideas.search.max_results", "5.5", "E: Invalid Type"],   # float
        ["settings.ideas.search.max_results", "abc", "E: Invalid Type"],   # строка
        ["settings.ideas.search.max_results", "", "E: Invalid Type"],      # пусто
        
        # ===== 3. FLOAT (если есть в конфиге) =====
        # ["settings.ideas.some_float", "3.14", 3.14],
        # ["settings.ideas.some_float", "0.0", 0.0],
        # ["settings.ideas.some_float", "abc", "E: Invalid Type"],
        
        # ===== 4. STRING (str) =====
        ["settings.ideas.format", "md", "md"],
        ["settings.ideas.format", "txt", "txt"],
        ["settings.ideas.format", "json", "json"],
        ["settings.ideas.format", "", ""],          # пустая строка
        ["settings.ideas.format", "   ", "   "],    # пробелы
        ["settings.ideas.format", "Markdown", "Markdown"],
        
        # ===== 5. LIST (list) =====
        ["settings.ideas.search.table_columns", "['number', 'score', 'date']", ['number', 'score', 'date']],
        ["settings.ideas.search.table_columns", "['a','b','c']", ['a','b','c']],
        ["settings.ideas.search.table_columns", "[]", []],   # пустой список
        ["settings.ideas.search.table_columns", "['1', 2, 'three']", ['1', 2, 'three']],  # смешанный
        ["settings.ideas.search.table_columns", "['fff', 'score', 'name', 'abc']", ['fff', 'score', 'name', 'abc']],
        ["settings.ideas.search.table_columns", "(1,2,3)", "E: Invalid Type"],   # кортеж
        ["settings.ideas.search.table_columns", "{'a':1}", "E: Invalid Type"],   # словарь
        ["settings.ideas.search.table_columns", "['a', 'b'", "E: Invalid Type"], # синтаксическая ошибка
        
        # ===== 6. НЕСУЩЕСТВУЮЩИЙ ПУТЬ (No Path Found) =====
        ["settings.nonexistent", "anything", "E: No Path Found"],
        ["settings.ideas.nonexistent", "anything", "E: No Path Found"],
        ["settings.ideas.search.nonexistent", "anything", "E: No Path Found"],
        ["settings.ideas.search.max_results.nonexistent", "anything", "E: No Path Found"],
        ["", "anything", "E: No Path Found"],  # пустой путь
        ["settings", "anything", "E: No Path Found"],  # путь указывает на словарь
        
        # ===== 7. ПУТЬ УКАЗЫВАЕТ НА СЛОВАРЬ (не конечный) =====
        ["settings", "anything", "E: No Path Found"],
        ["settings.ideas", "anything", "E: No Path Found"],
        ["settings.ideas.search", "anything", "E: No Path Found"],
        
        # ===== 8. НЕИЗВЕСТНЫЙ ТИП (если путь есть, но тип не поддерживается) =====
        # Если в конфиге есть поле с типом, который не обрабатывается
        # ["settings.ideas.unknown_type", "value", "E: Invalid Type"],
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

            if answer == result: completed += 1
            results.append([answer == result, result, answer])

        except SystemExit:
            parser = sys.stdout.getvalue()
            sys.stdout = old_stdout

            #if parser.strip() == answer:
            #    print(f"ok: {parser.strip()} --> {answer}")
            #    completed += 1
            #else:
            #    print(f" e: {parser.strip()} -X> {answer}")
            if parser.strip() == answer: completed += 1
            results.append([parser.strip() == answer, parser.strip(), answer])

    #print(f"{completed}/{all} | {(completed/all*100):.0f}%")

    results.append((completed, all))

    return results

if __name__ == "__main__":
    main()
