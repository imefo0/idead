import os
import subprocess
from pathlib import Path
import sys
from datetime import datetime # now = datetime.now().strftime("%Y-%m-%d %H:%M")

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

def new_idea(name, desc):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    time_now_mini = now = datetime.now().strftime("%Y%m%d%H%M")

    content = f"---\nname: {name}\ncreate_time: {time_now}\n---\n{desc}"

    (folder_ideas / f"i{time_now_mini}.md").write_text(content)

def remove_idea_by_date(date):
    pass
def get_list_of_files(folder):
    files = []

    for item in folder.iterdir():
        if item.is_file():
            files.append(item.name)

    return files


def remove_idea_by_name(name):
    pass

def remove_idea_by_uuid(uuid):
    pass

def remove_idea_by_custom_metadata(): pass


def main():
    if command[0] == "init":
        init()
    elif command[0] == "new":
        if command[1] == "idea":
            new_idea(command[2], command[3])

# TODO: добавить add, remove, rename, rewrite idea
# добавить название языка в waybar, nvim
# добавить поддержку версий и для идей

if __name__ == "__main__":
    main()
