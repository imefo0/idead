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
