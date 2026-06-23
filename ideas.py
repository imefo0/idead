#!/usr/bin/env python3
import os

# управление идеями

local_path = "~/.local/share/idead"
# создание всех каталогов
os.system(f"mkdir -p {local_path}/ideas/all")

def new(name, about, date):
    os.system(f"echo \"{about}\" > {local_path}/ideas/all/{name}_{date}.md")