from pathlib import Path
import json
import core
# удаляет paths.* и config.name

data = core.load()

# INFO: проверяем есть ли paths:
if "paths" in data:
    del data["paths"]

# INFO: проверяем есть ли config.name
if "config" in data and "name" in data["config"]:
    del data["config"]["name"]

# INFO: меняем версию
data["config"]["version"] = "1.1"

core.save(data)

print("1.0 -> 1.1:")
print("- rm: paths.*")
print("- rm: config.name")
