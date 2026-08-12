from pathlib import Path
import json
import re

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

# TODO: убрать это
ideas_format = "md"

warning_choice = True

separator_length = 30
separator_symbol = "-"

delete_idea_ask = "Are you sure you want to delete this idea?"

ideas_version = "1.0"

# TODO: переместить data в файл внутри проекта
data = {
    # "paths": {
        # "unnamed": "unnamed",
        # "home": f"/home/unnamed"
        # "config": "{paths.home}/.config/idead",
        # "data": "{paths.home}/.local/share/idead",
        # "cache": "{paths.home}/.cache/idead/",
        # "ideas": "{paths.data}/idead/ideas",
        # "posts": "{paths.data}/idead/posts",
        # "tasks": "{paths.data}/idead/tasks",
        # "guides": "{paths.data}/idead/guides"
    # },
    "settings": {
        "all": {
            "warning_choice": True,
            "separator_length": 30,
            "separator_symbol": "-"
        },
        "ideas": {
            "version": "1.0",
            "format": "md"
        },
    },
    "warnings": {
        "ideas": {
            "delete": "Are you sure you want to delete this idea?"
        }
    },
    "config": {
        "version": "1.1",
        # "name": "config.json"
    }
}

def resolve_templates(obj, context=None):
    if context is None:
        context = obj
    
    # INFO: если встречаем словарь то вызываем эту же функцию в рекурсии
    if isinstance(obj, dict):
        return {k: resolve_templates(v, context) for k, v in obj.items()}

    # INFO: если встречаем список то вызываем эту же функцию в рекурсии
    elif isinstance(obj, list):
        return [resolve_templates(item, context) for item in obj]

    # INFO: если втсречаем строку то ищем шаблоны
    elif isinstance(obj, str):
        # INFO: находит все куски строки, которые содержат {a.b.c.d}
        pattern = r'\{([^{}]+)\}'
        matches = re.findall(pattern, obj)

        for match in matches:

            # INFO: разбираем {a.b.c.d} на ["a", "b", "c", "d"]
            parts = match.split('.')

            # INFO: проходит в словаре по пути a -> b -> c -> d и получает значение abcd
            value = context
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    value = None
                    break

            # INFO: замена шаблона на значение
            if value is not None:
                obj = obj.replace(f'{{{match}}}', str(value))
        return obj

    # INFO: если не строка то возвращаем как есть
    else:
        return obj

def get():
    with open (folder_config / "config.json") as f:
        return json.load(f)

def reset_settings():
    # INFO: функция проходит по data и меняет {a.b.c.d} на настоящие имена
    resolved = resolve_templates(data)

    # INFO: берем путь из resolved:paths.config (написал в кратком виде) и файл resolved.config.name
    config_path = folder_config / "config.json"

    # INFO: создает папки если их нет
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("ok")

def load_config():
    pass
