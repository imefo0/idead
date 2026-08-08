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

warning_choice = True

delete_idea_ask = "Are you sure you want to delete this idea?"

def init():
    folder_config.mkdir(parents=True, exist_ok=True)
    folder_data.mkdir(parents=True, exist_ok=True)
    folder_cache.mkdir(parents=True, exist_ok=True)

    folder_ideas.mkdir(parents=True, exist_ok=True)
    folder_posts.mkdir(parents=True, exist_ok=True)
    folder_tasks.mkdir(parents=True, exist_ok=True)
    folder_guides.mkdir(parents=True, exist_ok=True)

def new_idea(name, desc):
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

def warning(msg): # y, yes?, yn -> yes? [yn] y -> True
    if warning_choice:
        answer = input(f"{msg} [yn] ")
        if answer.lower() in ["y", "yes"]:
            return True
        else:
            return False
    return True

# TODO: добаввить функцию предупреждения чтобы можно было ее отключить через переменную auto_yes или choice_warning
# TODO: добавить город в метаданные идей

def remove_idea_by_date(date=False, time=False):
    
    coincidences = []
    for i in get_list_of_files(folder_ideas): # i202608041359_dd0cd3.md -> i 2026-08-04 13:59 _ dd0cd3 .md
        if not time:
            if i[1:9] == date:
                coincidences.append(i)
        else:
            if not date:
                if i[9:13] == time:
                    coincidences.append(i)
            else:
                if i[1:9] == date and i[9:13] == time:
                    coincidences.append(i)

    if len(coincidences) == 0: # нет идей
        # TODO: добавить класс Error и добавить эту ошибку как Error.NoMatchesFound
        # TODO: добавить класс Error и добавить ошибку Error.IncorrectDate / IncorrectInput
        print("E: No Matches Found")

    elif len(coincidences) == 1:
        # TODO: добавить так чтобы была понятна какая идея удаляется

        if warning(delete_idea_ask):
            print("Deleting idea...")
            (folder_ideas / coincidences[0]).unlink()
    else: # много идей
        # TODO: добавить удаление нескольких идей сразу

        print(f"Found {len(coincidences)} ideas for{f" {date[:4]}-{date[4:6]}-{date[6:8]}" if date else ""}{f" {time[:2]}:{time[2:]}" if time else ""}:")
        print("-"*30) # TODO: добавить переменную для этого числа (30)
        for i in range(len(coincidences)): # i202608041359_dd0cd3 -> i 20260804 1359 _dd0cd3
            date_coincidences = f"{coincidences[i][1:5]}-{coincidences[i][5:7]}-{coincidences[i][7:9]}"
            time_coincidences = f"{coincidences[i][9:11]}:{coincidences[i][11:13]}"
            print(f"  {i+1}. {date_coincidences} {time_coincidences} [{coincidences[i][14:-3]}]")

        print("-"*30)
        answer = int(input(f"Enter number to delete (1-{len(coincidences)}, or 0 to cancel): "))
        # WARN: добавить проверку на число
        if answer != 0:
            if warning(delete_idea_ask):
                print("Deleting idea...")
                (folder_ideas / coincidences[answer-1]).unlink()

def remove_idea_by_uuid(uuid_):

    coincidences = []
    for i in get_list_of_files(folder_ideas): # i202608041359_dd0cd3.md -> i 2026-08-04 13:59 _ dd0cd3 .md
        if i[14:20] == uuid_:
            coincidences.append(i)

    if len(coincidences) == 0: # нет идей
        # TODO: добавить класс Error и добавить эту ошибку как Error.NoMatchesFound
        # TODO: добавить класс Error и добавить ошибку Error.IncorrectDate / IncorrectInput
        print("E: No Matches Found")

    elif len(coincidences) == 1:
        # TODO: добавить так чтобы была понятна какая идея удаляется

        if warning(delete_idea_ask):
            print("Deleting idea...")
            (folder_ideas / coincidences[0]).unlink()

def remove_idea_by_name(name):
    pass

def remove_idea_by_custom_metadata(): pass


def main():
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

# TODO: добавить add, remove, rename, rewrite idea
# добавить название языка в waybar, nvim
# добавить поддержку версий и для идей

if __name__ == "__main__":
    main()
