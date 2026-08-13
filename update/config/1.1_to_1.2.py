import core
# добавляет settings.ideas.search.max_results и settings.ideas.search.table_columns
# table_columns: number, score, date, name, desc, time

data = core.load()

# INFO: проверяем отсутствует ли settings
if "settings" not in data:
    # INFO: создаем
    data["settings"] = {}

# INFO: проверяем отсутствует ли settings.ideas
if "ideas" not in data["settings"]:
    # INFO: создаем
    data["settings"]["ideas"] = {}

if "search" not in data["settings"]["ideas"]:
    # INFO: создаем settings.ideas.search.max_results и settings.ideas.search.table_columns
    data["settings"]["ideas"]["search"] = {"max_results": 5, "table_columns": ["number", "score", "date", "name"]}
# INFO: если есть settings.ideas.search
else:
    if "max_results" not in data["settings"]["ideas"]["search"]:
        data["settings"]["ideas"]["search"]["max_results"] = 5
    if "table_columns" not in data["settings"]["ideas"]["search"]:
        data["settings"]["ideas"]["search"]["table_columns"] = ["number", "score", "date", "name"]

# INFO: меняем версию
data["config"]["version"] = "1.2"

core.save(data)

print("1.1 -> 1.2:")
print("- new: settings.ideas.search.max_results")
print("- new: settings.ideas.search.table_columns")
