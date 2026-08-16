from pathlib import Path
import json
import copy

def load():
    with open((Path.home() / ".config" / "idead" / "config.json"), "r") as f:
        return json.load(f)

def save(data):
    with open((Path.home() / ".config" / "idead" / "config.json"), "w") as f:
        json.dump(data, f, indent=4)

def add(data: dict, path: str, default=None) -> dict:
    dataa = copy.deepcopy(data)

    keys = path.split(".")

    current = dataa

    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]

    last_key = keys[-1]
    if last_key not in current:
        current[last_key] = default if default is not None else {}

    return dataa

def ver(data, version):
    dataa = copy.deepcopy(data)

    if "config" not in dataa:
        dataa["config"] = {}
    dataa["config"]["version"] = version

    return dataa
