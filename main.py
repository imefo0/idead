#!/usr/bin/env python3

import sys
import os

project_dir = os.path.dirname(os.path.realpath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

import ideas

command = sys.argv[1:]
print(command)
def main():
    # TODO: вынести в parser.py потом

    # команды:
    # idead new idea <name> <idea>

    if command[0] == "new":
        if command[1] == "idea":
            ideas.new(command[2].replace(" ", "\\ "), command[3].replace(" ", "\\ "), command[4].replace(" ", "\\ "))

if __name__ == "__main__":
    main()