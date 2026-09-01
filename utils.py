from pathlib import Path
import json

folder_config = Path.home() / ".config" / "idead"

# HACK: надо как-то добавить куда-то это потому что надо dry
def get_config_data():
    with open(folder_config / "config.json", "r") as f:
        return json.load(f)

data = get_config_data()

def _warning(msg): # y, yes?, yn -> yes? [yn] y -> True
    if data["settings"]["all"]["warning_choice"]:
        answer = input(f"{msg} [yn] ")
        if answer.lower().replace(" ", "").replace("\t", "").replace("\n", "") in ["y", "yes"]:
            return True
        else:
            return False
    return True
