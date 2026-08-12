from pathlib import Path
import json
# удаляет paths.* и config.name

with open((Path.home() / ".config" / "idead" / "config.json"), "r") as f:
    data = json.load(f)

# INFO: проверяем есть ли paths:
if "paths" in data:
    del data["paths"]

# INFO: проверяем есть ли config.name
if "config" in data and "name" in data["config"]:
    del data["config"]["name"]

# INFO: меняем версию
data["config"]["version"] = "1.1"

with open((Path.home() / ".config" / "idead" / "config.json"), "w") as f:
    json.dump(data, f, indent=4)

print("1.0 -> 1.1:")
print("- rm: paths.*")
print("- rm: config.name")
