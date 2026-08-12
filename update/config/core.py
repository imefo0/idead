from pathlib import Path
import json

def load():
    with open((Path.home() / ".config" / "idead" / "config.json"), "r") as f:
        return json.load(f)

def save(data):
    with open((Path.home() / ".config" / "idead" / "config.json"), "w") as f:
        json.dump(data, f, indent=4)

