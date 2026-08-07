import os
import subprocess
from pathlib import Path
import sys
from datetime import datetime # now = datetime.now().strftime("%Y-%m-%d %H:%M")
import uuid

home = Path.home()

# XDG folders
folder_config = home / ".config" / "idead"
folder_data = home / ".local" / "share" / "idead"
folder_cache = home / ".cache" / "idead"

# Other folders
folder_ideas = folder_data / "ideas"
folder_posts = folder_data / "posts"
folder_tasks = folder_data / "tasks"
folder_guides = folder_data / "guides"

command = sys.argv[1:]

ideas_format = "md"

def init():
    folder_config.mkdir(parents=True, exist_ok=True)
    folder_data.mkdir(parents=True, exist_ok=True)
    folder_cache.mkdir(parents=True, exist_ok=True)

    folder_ideas.mkdir(parents=True, exist_ok=True)
    folder_posts.mkdir(parents=True, exist_ok=True)
    folder_tasks.mkdir(parents=True, exist_ok=True)
    folder_guides.mkdir(parents=True, exist_ok=True)

def new_idea(name, desc): # FIX: исправить то что uuid нету
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    time_now_mini = now = datetime.now().strftime("%Y%m%d%H%M")

    uuid12 = uuid.uuid4().hex[:6]
    content = f"---\nname: {name}\ncreate_time: {time_now}\nuuid: {uuid12}\n---\n{desc}"

    (folder_ideas / f"i{time_now_mini}_{uuid12}.md").write_text(content)

def get_list_of_files(folder):
    files = []

    for item in folder.iterdir():
        if item.is_file():
            files.append(item.name)

    return files

def remove_idea_by_date(date, time=False):
    if time == False: # только по дате
        coincidences = []
        for i in get_list_of_files(folder_ideas): # i202608041359_dd0cd3.md -> i 2026-08-04 13:59 _ dd0cd3 .md
            if i[1:9] == date:
                coincidences.append(i)

        if len(coincidences) == 0: # нет идей
            # TODO: добавить класс Error и добавить эту ошибку как Error.NoMatchesFound
            # TODO: добавить класс Error и добавить ошибку Error.IncorrectDate / IncorrectInput
            print("E: No Matches Found")
        elif len(coincidences) == 1:
            # TODO: добавить так чтобы была понятна какая идея удаляется
            answer = input("Are you sure you want to delete this idea? [yn] ")
            if answer.lower() in ["y", "yes"]: # TODO: вынести список из y и yes в отдельную переменную для конфига
                print("Deleting idea...")
                (folder_ideas / coincidences[0]).unlink()
        else: # много идей
            print(f"Found {len(coincidences)} ideas for {date[0:4]}-{date[4:6]}-{date[6:]}:")
            print("-"*30) # TODO: добавить переменную для этого числа (30)
            for i in range(len(coincidences)):
                print(f"  {i+1}. {date[0:4]}-{date[4:6]}-{date[6:]} {coincidences[i][9:11]}:{coincidences[i][11:13]} [{coincidences[i][14:-3]}]")
            print("-"*30)
            # TODO: ПРОТЕСТИРОВАТЬ ЭТУ ДИЧЬ
            answer = int(input(f"Enter number to delete (1-{len(coincidences)}, or 0 to cancel): "))
            # TODO: добавить проверку на число
            if answer != 0:
                new_answer = input("Are you sure you want to delete this idea? [yn] ")
                if new_answer.lower() in ["y", "yes"]: # TODO: вынести список из y и yes в отдельную переменную для конфига
                    print("Deleting idea...")
                    (folder_ideas / coincidences[answer-1]).unlink()


    else: # по дате и времени
        if time[:1].isdigit() and time[2] == ":" and time[3:].isdigit():
            pass


def remove_idea_by_name(name):
    pass

def remove_idea_by_uuid(uuid):
    pass

def remove_idea_by_custom_metadata(): pass


def main():
    if len(command) > 0:
        if command[0] == "init":
            init()
        elif command[0] == "new":
            if command[1] == "idea":
                new_idea(command[2], command[3])
    remove_idea_by_date(input("enter date: "))

    remove_idea_by_name("Abc")
# TODO: добавить add, remove, rename, rewrite idea
# добавить название языка в waybar, nvim
# добавить поддержку версий и для идей

if __name__ == "__main__":
    main()
