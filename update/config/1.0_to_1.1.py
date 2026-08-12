import config
# удаляет paths.* и config.name

with open(folder_config / "config.json") as f:
    data = json.load(f)

# INFO: проверяем есть ли paths:
if "paths" in data:
    del data["paths"]

# INFO: проверяем есть ли config.name
if "config" in data and "name" in data["config"]:
    del data["config"]["name"]

# INFO: меняем версию
data.setdefault("config", {})["version"] = "1.1"

print("1.0 -> 1.1:")
print("- rm: paths.*")
print("- rm: config.name")
