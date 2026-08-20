#!/usr/bin/env python3

from pathlib import Path
import sys
from datetime import datetime # now = datetime.now().strftime("%Y-%m-%d %H:%M")
import uuid
from config import *
from ideas import *
from typing import Any
import test.test

command = sys.argv[1:]
data = get()

# если нету using то в выводе (не показывать ошикбу) написать "пока нет описания"
# TODO: еще надо добавить в классы конфигурации идей (а щас функции, сейчас буду делать рефактор что бы все было в классах) проверку версии чтобы не вызывать ошибку а писать E: Config Version Deprecated
# TODO: добавить плагины и их поддержку
# TODO: добавить описание ошибки и решение
# TODO: добавить:
# idead config settings.ideas.search.max_results 10  # set по умолчанию
# idead config settings.ideas.search.max_results     # get по умолчанию
# TODO: добавить гайды

def _parse_command(path: list(str), data):
    # path: config.arg.get
    #print(keys)
    
    keys = path.copy()
    # преобразуем 

    if keys and keys[0] == "idead":
        keys = keys[1:]

    if keys and keys[0] == "config":
        if len(keys) >= 2 and keys[1] not in ["reset", "update"]:
            keys[1] = "arg"

    for i in range(len(keys)-1):
        if keys[i] in ["--date", "--time", "--uuid", "--name"]:
            keys[i+1] = "arg"

    if keys and keys[-1] == "arg":
        keys.pop()

    result = []
    for part in keys:
        if part.startswith("--"):
            result.append("flags")
            result.append(part)
        else:
            result.append("subcmds")
            result.append(part)

    for i in range(len(result)-1, -1, -1):
        #print(result[i], end=" ")
        if result[i] == "subcmds" and result[i-1] == "arg":
            del result[i]

    keys = result.copy()

    #print()
    #print(keys)
    #return

    # получаем значение
    current = data

    # Проходим по всем ключам, создавая пустые словари при необходимости
    for key in ["helper", *keys]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]

    # Если дошли до конца — забираем about и using
    about = current.get("about", "")
    using = current.get("using", "")

    print(f"using: {using}\nabout: {about}")

def _parse_value(value: str, path: str):
    with open((Path(__file__).resolve().parent / "default_config.json"), "r") as f:
        default_data = json.load(f)

    # 1. Проверяем существование пути
    keys = path.split(".")
    current = default_data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            print(f"E: No Path Found")
            sys.exit()
    
    # 2. Получаем ожидаемый тип
    expected = current
    
    # 3. Если ожидаемый тип — словарь, значит путь не конечный
    if isinstance(expected, dict):
        print(f"E: No Path Found")
        sys.exit()
    
    # 4. Преобразуем значение в нужный тип
    expected_type = type(expected)
    
    try:
        if expected_type is bool:
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
            else:
                raise ValueError
        elif expected_type is int:
            return int(value)
        elif expected_type is float:
            return float(value)
        elif expected_type is str:
            return value
        elif expected_type is list:
            # Для списков используем ast.literal_eval
            import ast
            try:
                parsed = ast.literal_eval(value)
                if isinstance(parsed, list):
                    return parsed
                else:
                    raise ValueError
            except:
                raise ValueError
        else:
            # Неизвестный тип — просто возвращаем строку
            return value
    except (ValueError, TypeError):
        print(f"E: Invalid Type")
        sys.exit()

def main():
    # TODO: добавить переменные для обозначения флагов
    # TODO: добавить поддержку удаления идеи сразу с несколькими флагами
    if len(command) > 0:
        if "--help" in command:
            del command[command.index("--help")]
            _parse_command(command, data)
            return

        if command[0] == "init":
            init()
        elif command[0] == "new":
            if command[1] == "idea":
                new_idea(command[2], command[3])
        elif command[0] == "remove":
            if command[1] == "idea":
                if "--date" in command[2:] or "--time" in command[2:]:
                    if "--date" in command[2:] and "--time" in command[2:]:
                        remove_idea_by_date(command[command.index("--date")+1], command[command.index("--time")+1])
                    elif "--date" in command[2:]:
                        remove_idea_by_date(date=command[command.index("--date")+1])
                    elif "--time" in command[2:]:
                        remove_idea_by_date(time=command[command.index("--time")+1])
                else:
                    if "--uuid" in command[2:]:
                        remove_idea_by_uuid(command[command.index("--uuid")+1])
                    elif "--name" in command[2:]:
                        remove_idea_by_name(command[command.index("--name")+1])
        elif command[0] == "search":
            if command[1] == "idea":
                if "--name" in command[2:]:
                    search_idea(command[command.index("--name")+1])
        elif command[0] == "list":
            if command[1] == "idea":
                list_ideas()
        elif command[0] == "config":
            if command[1] == "reset":
                reset_settings()
            elif command[1] == "update":
                update()
            elif command[2] == "set": # WARN: если не будет значения после set то вернуть ошибку: E: Value Not Entered
                set_value(command[1], _parse_value(command[3], command[1]))
            elif command[2] == "get":
                get_value(command[1])
            elif command[2] == "reset":
                reset_value(command[1])
        elif command[0] == "test":
            test.test.main()



# TODO: добавить add, remove, rename, rewrite idea
# добавить поддержку версий и для идей

if __name__ == "__main__":
    main()
