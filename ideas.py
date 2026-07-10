#!/usr/bin/env python3
import os
import subprocess

# управление идеями

user = os.getenv("USER")
local_path = f"/home/{user}/.local/share/idead"
# создание всех каталогов
os.system(f"mkdir -p {local_path}/ideas/all")

def new(name, about, date):
    os.system(f"echo \"{about}\" > {local_path}/ideas/all/{name}_{date}.md")

def list_():
    # TODO: добавить количество слов и размер идеи
    # TODO: а если вывод ls будет без кавычек?
    # TODO: а что если local path вначале не будет иметь ~?
    #print(f"Реальный путь к папке: {local_path}/ideas/all")

    list_of_ideas = subprocess.run(["ls", f"{local_path}/ideas/all"],
    capture_output=True,
    text=True).stdout.split("\n")[:-1]

    print(f"name{"\t"*3}date")
    print("-"*40) # TODO: а что если текст выйдет за границы терминала или за границы "-----"?

    for bar in list_of_ideas:
        text = bar[:-3].split("_") # TODO: а что если в имени или в дате будет _?
        print(f"{text[0]}{"\t"*2}{text[1]}")