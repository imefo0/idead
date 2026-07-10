#!/usr/bin/env python3
# пусть эта строка доживет до релиза

import sys
import os

project_dir = os.path.dirname(os.path.realpath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

import ideas

command = sys.argv[1:]

#print(command)

def main():
    # TODO: вынести в parser.py потом
    # TODO: изменить условия на словари

    # команды:
    # idead new idea <name> <idea>

    if len(command) == 0:
        print("Using: idead <new>...")
        return

    # TODO: все help-еры (команды-помощники) убрать в другое место (в конфиг)
    if command[0] == "new":
        if command[1] == "idea":
            # TODO: изменить так чтобы можно было не ставить дату или описание
            # TODO: изменить синтаксис
            try:
                ideas.new(command[2].replace(" ", "\\ "), command[3].replace(" ", "\\ "), command[4].replace(" ", "\\ "))
            except:
                print("Using: idead new idea <name> <about> <date>")
    elif command[0] == "list":
        if command[1] == "idea":
            try: ideas.list_()
            except: print("Using: idead list idea")

if __name__ == "__main__":
    main()