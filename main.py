#!/usr/bin/env python3

from pathlib import Path
import sys
from datetime import datetime # now = datetime.now().strftime("%Y-%m-%d %H:%M")
import uuid
from config import *
from ideas import *

command = sys.argv[1:]

# TODO: добавить --help
# TODO: добавить use: ... в каждую команду
# TODO: добавить update.idea.update
# TODO: добавить тесты
# TODO: добавить плагины и их поддержку
# TODO: добавить описание ошибки и решение

def main():
    # TODO: добавить переменные для обозначения флагов
    # TODO: добавить поддержку удаления идеи сразу с несколькими флагами
    if len(command) > 0:
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
                set_value(command[1], command[3])
            elif command[2] == "get":
                get_value(command[1])
            elif command[2] == "reset":
                reset_value(command[1])


# TODO: добавить add, remove, rename, rewrite idea
# добавить поддержку версий и для идей

if __name__ == "__main__":
    main()
