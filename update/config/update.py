from pathlib import Path
import json
import subprocess
import glob
import sys

def is_older_version(version1, version2):
    ver1 = [int(v) for v in version1.split(".")]
    ver2 = [int(v) for v in version2.split(".")]

    if ver1[0] > ver2[0]: # 1.0 > 0.12
        return True
    if ver1[0] == ver2[0]: # 3.4 ? 3.6
        if ver1[1] > ver2[1]: # 3.6 > 3.5
            return True
        return False # 3.4 < 3.6 & 3.4 = 3.4
    return False # 2.4 < 3.5

def update_from(old_version) -> (bool, str):
    try:
        subprocess.run(["python3", glob.glob(f"{Path(__file__).parent}/{old_version}_to_*.py")[0]])
    except IndexError:
        return (False, "")
    return (True, glob.glob(f"{Path(__file__).parent}/{old_version}_to_*.py")[0].split("_to_")[1].replace(".py", ""))

# WARN: кидать ошибку если нет data.config.version
with open((Path.home() / ".config" / "idead" / "config.json"), "r") as f:
    current_version = json.load(f)["config"]["version"]

with open((Path(__file__).parent.parent.parent / "default_config.json"), "r") as f:
    actual_version = json.load(f)["config"]["version"]

if is_older_version(actual_version, current_version): # если версия пользователя старше чем актуальная
    print(f"Update required: {current_version} -> {actual_version}")

    if input("Update? [yn] ") == "y":

        while is_older_version(actual_version, current_version):
            result = update_from(current_version)
            current_version = result[1]
            if not result[0]:
                print("E: Not Update File Found")
                sys.exit(0)

        print(f"Successful update! Current version: {current_version}")
else:
    print("Config version is up to date")
