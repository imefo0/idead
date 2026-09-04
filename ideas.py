from pathlib import Path
from config import *
from datetime import datetime
import uuid
from utils import _warning

data = get()

# TODO: добавить город в метаданные идей и имя пользователя
# TODO: v0.7.0: разделить helper из config.json на config.json и helper.json а потом все равно перейти на toml (v0.8.0)
# TODO: v0.7.0: изменить прямые обращения к config на переменные вначале функции
# TODO: изменить пасхалку на нормальный хелпер в idead --help

class Idea:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

        self.uuid = uuid.uuid4().hex[:6]

        self.version = data["settings"]["ideas"]["version"]

        self.date = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M")

        self.date_mini = datetime.now().strftime("%Y%m%d")
        self.time_mini = datetime.now().strftime("%H%M")

    def save(self):
        content = f"---\nname: {self.name}\ndate: {self.date} {self.time}\nuuid: {self.uuid}\nversion: {self.version}\n---\n{self.desc}"
        (folder_ideas / f"i{self.date_mini}{self.time_mini}_{self.uuid}.md").write_text(content)

def _get_list_of_files(folder):
    files = []

    for item in folder.iterdir():
        if item.is_file():
            files.append(item.name)

    return files

def _clear_num(num_str):
    return ''.join(filter(str.isdigit, num_str))

def _get_value_from_metadata(metadata: list(str), data_search: str) -> (bool, str):
    prefix = f"{data_search}: "

    for item in metadata:
        if isinstance(item, str) and item.startswith(prefix):
            value = item[len(prefix):].strip()
            return True, value

    # Не найдено
    print("WARN: Name In Idea Not Found")
    return False, None

def _extract_metadata_as_list(lines):
    result = []
    started = False  # флаг: начали ли мы уже собирать метаданные

    for line in lines:
        stripped = line.strip()

        # Пропускаем пустые строки
        if not stripped:
            continue

        # Если встретили разделитель "---" после начала сбора — останавливаемся
        if stripped == "---":
            if started:
                break
            # Если ещё не начали, это может быть начальный разделитель — просто пропускаем
            continue

        started = True  # считаем, что метаданные начались

        # Проверяем формат key: value
        if ":" in stripped:
            result.append(stripped)
        # Всё остальное (включая *desc* и любые другие строки) просто пропускается
    return result

def _parse_filename_info(fname: str):
    # 1. Отрезаем .md, если есть
    base = fname.removesuffix(".md")
    
    # 2. Вырезаем данные по заранее известным позициям
    # Формат имени: iYYYYMMDDHHMMSS_uuid.md
    date_str = f"{base[1:5]}-{base[5:7]}-{base[7:9]}"       # YYYY-MM-DD
    time_str = f"{base[9:11]}:{base[11:13]}"               # HH:MM
    uuid_str = base[14:20]                                 # 6 символов UUID
    
    return {
        "date": date_str,
        "time": time_str,
        "uuid": uuid_str,
        "raw_date": base[1:9],   # Например, "20260804" - пригодится для сравнения
        "raw_time": base[9:13],  # Например, "1359"
        "filename": fname
    }

def init():
    folder_config.mkdir(parents=True, exist_ok=True)
    folder_data.mkdir(parents=True, exist_ok=True)
    folder_cache.mkdir(parents=True, exist_ok=True)

    folder_ideas.mkdir(parents=True, exist_ok=True)
    folder_posts.mkdir(parents=True, exist_ok=True)
    folder_tasks.mkdir(parents=True, exist_ok=True)
    folder_guides.mkdir(parents=True, exist_ok=True)

def new_idea(name, desc):
    format_date = "%Y-%m-%d"
    format_time = "%H:%M"

    time_now = datetime.now().strftime(f"{format_date} {format_time}")
    time_now_mini = datetime.now().strftime("%Y%m%d%H%M")

    uuid6 = uuid.uuid4().hex[:6]

    content_lines = [
        "---",
        f"name: {name}",
        f"date: {time_now}",
        f"uuid: {uuid6}",
        f"version: {data["settings"]["ideas"]["version"]}",
        "---",
        desc
    ]
    content = "\n".join(content_lines)

    (folder_ideas / f"i{time_now_mini}_{uuid6}.md").write_text(content)

    print(f"New idea: {name}; uuid: {uuid6}")

def test_new_idea(name, desc):
    format_date = "%Y-%m-%d"
    format_time = "%H:%M"

    time_now = datetime.now().strftime(f"{format_date} {format_time}")
    time_now_mini = datetime.now().strftime("%Y%m%d%H%M")

    uuid6 = uuid.uuid4().hex[:6]
    content = f"---\nname: {name}\ndate: {time_now}\nuuid: {uuid6}\nversion: {data["settings"]["ideas"]["version"]}\n---\n{desc}"

    (Path.home() / ".cache/idead/tests/ideas" / f"i{time_now_mini}_{uuid6}.md").write_text(content)

    return uuid6

def min_lens(*args: int):
    result = None
    if len(args) == 0:
        raise TypeError("min_lens expected at least 1 argument, got 0")
    for arg in args:
        if not isinstance(arg, int):
            raise TypeError(f"min_lens требует int а не {type(arg)}")
        if result is None or (arg < result and arg != -1):
            result = arg

    return result

def _identify_range(diapason: str, base: int = 0) -> list[int]:
    raw_nums = diapason.split("..")
    result = []
    #print("raw_nums:", raw_nums)
    if raw_nums[0].isdigit() and raw_nums[1].isdigit():
        #print("IS DIGIT")
        num_range = list(map(int, [(int(raw_nums[0]) + base - 1), (int(raw_nums[1]) + base - 1)]))
        #print("num_range:", num_range)
        if int(num_range[0]) <= int(num_range[1]):
            #print(f"{num_range[0]} <= {num_range[1]}")
            for num in range(num_range[0], num_range[1] + 1):
                result.append(num)
                #print("append:", num)
        else:
            for num in range(num_range[0], num_range[1] - 1, -1):
                result.append(num)
    return result

def _parse_select_answer(answer: str, *, all_len: int = -1) -> list[int]:
    # NOTE: можно написать 1 и будет [1]
    # если написать 1,2,3 или даже 1, 2, 3 то будет [1,2,3]
    # если написать 1..9, 12, 13, -9 то будет [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13]
    # если написать -7, -4, -3, abc, sdff то будет []
    # если написать 1, 2, 3, 7..5 то будет [1, 2, 3, 7, 6, 5]
    # NOTE:
    # если написать 1, 2, 4, 1..4 то будет [1, 2, 4, 3]
    # если написать 1 .. 4 или 1.. 4 или 1 ..4 то будет [1, 2, 3, 4]
    # NOTE:
    # v0.8.0+: добавить поддержку 1..4:2 где 2 это каждый второй или a..b:x что означает от a до b включая их но каждое x число
    # добавить поддержку -1 которая означает либо "все" либо "последний элемент" (настройка в конфиге)
    # добавить ЭТО: "n=*, a=1..4, b=3..6, a&b, 6..10?n>4+n<9". вот что означает:
    # сказать что n это все элементы, a это числа от 1 до 4, b это числа от 3 до 6
    # вывести числа которые являются объеденением a и b
    # и все числа от 6 до 10 но при условии что n>4 и n<9 либо сделать 6..10?n>4&n<9 
    # добавить флаг в функцию base который по умолчанию 0, то есть начинаем с нуля, но все примеры выше с base=1
    # ДОБАВИТЬ ЦИКЛЫ n>1..4: (n+3)..n?n<2
    # j=10, n>1..10: n+j, j--
    # даже n>1..10: n?n==3??n-1 и это будет работать так: for n in range(1, 11):
    #     if n == 3: lst.append(n)
    #     else: lst.append(n-1)
    # ЧТО ЭТО n>1..10: n?n<3??(n?n<7??n*2?n<5??n*3)
    # n>1..10: n?n==1??1?n==2??2?n==3??3?n==4??4?5
    # добавить while
    # а выход их цикла это ;
    # добавить функцию: $a#c#d: c+d; x=0, y=3, n>1..10: a#x#y, x=x+2, y--; (означает def a(c, d): return c+d)
    # $fib#n: n?n<2??fib#n-1+fib#n-2; n>1..10: fib#n
    # Enter number or DSL-request / query - сообщение
    commands = answer.replace(" ", "").split(";")
    commands = [(cmd if "," not in cmd and not cmd.isdigit() else cmd.split(",")) for cmd in commands]

    # TODO: добавить в конфиг
    base = 0
    list_len = all_len
    unique = True
    base_reset = True
    len_reset = True
    unique_reset = True

    result = []
    #print("commands:", commands)

    for cmd in commands:
        # TODO: в функции эти 3 условия
        if isinstance(cmd, list):
            #print("base:", base)
            #print("КОМАНДА ЯВЛЯЕТСЯ СПИСКОМ")
            #print(cmd)
            for sub_cmd in cmd:
                #print("s:", sub_cmd)
                if ".." in sub_cmd:
                    #print("ЕСТЬ ..!")
                    result += _identify_range(sub_cmd, base)
                    #print("ДОБАВЛЕННО:", result[-1])
                else:
                    if sub_cmd.isdigit(): result.append(int(sub_cmd) + base - 1)
        else:
            if ".." in cmd:
                #print("ЕСТЬ ..!")
                result += _identify_range(cmd, base)
                #print("ДОБАВЛЕННО:", result[-1])

            if cmd.startswith("base") and (raw_base := cmd.replace("base", "").replace(" ", "")).isdigit():
                base = int(raw_base)
                base_reset = False
            else:
                if base_reset:
                    base = 0 # default

            if cmd.startswith("len") and ((raw_len := cmd.replace("len", "").replace(" ", "")).isdigit() or raw_len == "*"):
                if raw_len == "*":
                    raw_len = -1
                else:
                    list_len = min_lens(int(raw_len), all_len) if raw_len.isdigit() else all_len
                len_reset = False
            else:
                if len_reset:
                    list_len = all_len # default

            if cmd.startswith("unique") and (raw_unique := cmd.replace("unique", "").replace(" ", "")) in ["true", "false"]:
                unique = True if raw_unique == "true" else False
                unique_reset = False
            else:
                if unique_reset:
                    unique = True # default
    #print(result)

    # NOTE: в конце обработать unique для result
    if unique:
        """
        Почему это работает
        Шаг	Что делает	Результат
        dict.fromkeys(lst)	Создаёт словарь, где ключи — элементы списка (порядок сохраняется)	{1: None, 2: None, 3: None}
        list(...)	Превращает ключи словаря обратно в список	[1, 2, 3]
        """
        result = list(dict.fromkeys(result))

        # len (*), unique (true)

    if list_len != -1: result = result[:list_len]

    #print("result:", result)
    #print(f"reset: {base_reset}, {len_reset}, {unique_reset}")
    #print(f"base: {base}, len: {list_len}, unique: {unique}")
    return result

if __name__ == "__main__":
    _parse_select_answer(input())

# TODO: обновить ux всех remove и добавить флаг по триграммам
# TODO: обновить способ поиска в remove
# TODO: добавить поиск идеи по описанию в v0.7.0
# FIXME: исправить косметический баг когда выводится в found 1+ ideas for name, :
# TODO: v0.7.0: добавить удаление идей с помошью 1..5 и это будет работать как 1, 2, 3, 4, 5
def remove_idea(*, date=None, time=None, uuid6=None, name=None):
    remove_idea_match_mode = data["settings"]["ideas"]["remove"].get("search_mode", "soft") # hard/soft

    if date is None and time is None and uuid6 is None and name is None:
        print("E: No Data To Delete The Idea")
        return

    if date: date = _clear_num(date)
    if time: time = _clear_num(time)

    coincidences = []
    files = _get_list_of_files(folder_ideas)
    names = [_get_value_from_metadata(_extract_metadata_as_list((folder_ideas / x).read_text().splitlines()), "name") for x in files]
    weights = []

    """
    if not ideas:
        print("E: No Ideas Found")
        return

    table_columns = data["settings"]["ideas"]["list"]["table_columns"]

    description_list = []
    columns_data = { # NOTE: защита от дурака есть, потому что в классе Column предусмотренно что если есть недостающие строки
        "number": [],
        "date": [],
        "name": [],
        "description": description_list,
        "desc": description_list,
        "time": [],
        "uuid": [],
        "version": [],
        "score": []
    }
    description_list_candidate = []
    candidates_data = {
        "number": [],
        "date": [],
        "name": [],
        "description": description_list_candidate,
        "desc": description_list_candidate,
        "time": [],
        "uuid": [],
        "version": [],
        "score": []
    }
    default_cols = { # TODO: v0.7.0: добавить эти все настройки в конфиг
        # TODO: добавить type (i- - idea, g- guide и тд (префикс в файле))
        "number": "№",
        "date": "date",
        "name": "name",
        "description": "description", # TODO: v0.7.0: изменить в конфиге desc на description (ключ, не значение)
        "desc": "description",
        "time": "time",
        "uuid": "uuid",
        "version": "version",
        "score": "score"
    }

    remove_settings = data["settings"]["ideas"]["remove"]
    """
    num = 0
    """
    for idea in ideas: # i202608041359_dd0cd3.md -> i 2026-08-04 13:59 _ dd0cd3 .md
        finfo = _parse_filename_info(idea)

        if date is not None and finfo["date"] != date: continue
        if time4 is not None and finfo["time"] != time4: continue
        if uuid6 is not None and finfo["uuid"] != uuid6: continue
        if name is not None:
            if name is None or (name == candidate_name and remove_idea_match_mode == "hard"):
                coincidences.append(i)
                continue
            if remove_idea_match_mode != "hard":
                score = _jaccard_similarity(_to_trigram(name), _to_trigram(candidate_name))
                if score != 0.0:
                    coincidences.append(i)
                    weights.append((num, score))




        if any(x in ["date", "uuid", "time"] for x in table_columns):
            if "date" in table_columns: candidates_data["date"].append(finfo["date"])
            if "uuid" in table_columns: candidates_data["uuid"].append(finfo["uuid"])
            if "time" in table_columns: candidates_data["time"].append(finfo["time"])

        if any(x in ["name", "description", "desc", "version"] for x in table_columns):
            raw_content = (folder_ideas / idea).read_text().splitlines()
            fcontent = _extract_metadata_as_list(raw_content)

            if "name" in table_columns:
                if (name := _get_value_from_metadata(fcontent, "name"))[0]:
                    name = name[1]

                    candidates_data["name"].append(format_field(
                        name,
                        auto = remove_settings["max_symbols"]["auto"]["name"],
                        etc = remove_settings["etc"]["name"],
                        max_symbols_of_field = remove_settings["max_symbols"]["name"],
                        max_symbols_of_col = len(default_cols["name"])
                    ))
                else:
                    auto = remove_settings["max_symbols"]["auto"]["name"]
                    max_symbols_of_name = remove_settings["max_symbols"]["name"]
                    max_symbols_of_col = len(default_cols["name"])
                    name = "?" * (max_symbols_of_name if not auto else max_symbols_of_col)

                    candidates_data["name"].append(name)
            # INFO: ну нафиг эту поддержку - не актуально
            if "description" in table_columns or "desc" in table_columns: # WARN: поддерживаем старый вариант
                desc_lines = _extract_description(raw_content)

                # WARN: до v0.7.0: если значения не будет то тогда писать предупреждение что ее нет и ставить из default_config.json 
                candidates_data["description"].append(format_field(
                    desc_lines,
                    auto = remove_settings["max_symbols"]["auto"]["description"],
                    etc = remove_settings["etc"]["description"],
                    sep = remove_settings["separator_description"],
                    max_symbols_of_field = remove_settings["max_symbols"]["description"],
                    max_symbols_of_col = len(default_cols["description"])
                ))

            if "version" in table_columns: # TODO: добавить поддержку ver
                if (version := _get_value_from_metadata(fcontent, "version"))[0]: version = version[1]
                else: version = "?.?"

                candidates_data["version"].append(version)
        """
    for i in _get_list_of_files(folder_ideas):
        candidate_date = i[1:9]
        candidate_time = i[9:13]
        candidate_uuid = i[14:20]
        result = _get_value_from_metadata(_extract_metadata_as_list((folder_ideas / i).read_text().splitlines()), "name")
        if not result[0]:
            print(f"WARN: No Name In Idea (uuid: {candidate_uuid}) Found")
            continue
        candidate_name = result[1]

        if date is None or date == candidate_date:
            if time is None or time == candidate_time:
                if uuid6 is None or uuid6 == candidate_uuid:
                    if name is None or (name == candidate_name and remove_idea_match_mode == "hard"):
                        coincidences.append(i)
                        continue
                    if remove_idea_match_mode != "hard":
                        score = _jaccard_similarity(_to_trigram(name), _to_trigram(candidate_name))
                        if score != 0.0:
                            coincidences.append(i)
                            weights.append((num, score))
                            num += 1
    if name is not None and remove_idea_match_mode == "soft":
        weights.sort(key=lambda x: x[1], reverse=True)
        tmp_coincidences = coincidences.copy()
        coincidences = []
        for idx, score in weights:
            coincidences.append(tmp_coincidences[idx])

    """
    # INFO: логика лимита: если -1 то все показывать, иначе,
    # количество которое указано но если оно больше чем общее количество то только все которые есть
    limit = _determine_limit(
        max_results,
        ideas,
        default = data["settings"]["ideas"]["list"].get("max_results", -1)
    )

    # NOTE: новый код, и БЕЗ HACK

    table_columns = data["settings"]["ideas"]["list"]["table_columns"]

    description_list = []
    columns_data = { # NOTE: защита от дурака есть, потому что в классе Column предусмотренно что если есть недостающие строки
        "number": list(map(str, list(range(1, len(ideas[:limit])+1)))) if "number" in table_columns else [],
        "date": [],
        "name": [],
        "description": description_list,
        "desc": description_list,
        "time": [],
        "uuid": [],
        "version": []
    }
    default_cols = { # TODO: v0.7.0: добавить эти все настройки в конфиг
        # TODO: добавить type (i- - idea, g- guide и тд (префикс в файле))
        "number": "№",
        "date": "date",
        "name": "name",
        "description": "description", # TODO: v0.7.0: изменить в конфиге desc на description (ключ, не значение)
        "desc": "description",
        "time": "time",
        "uuid": "uuid",
        "version": "version"
    }
    # TODO: добавить настройку рядом table_columns которая убирает дубликаты

    # INFO: zip нужно когда надо пройти по 2 спискам одновременно
    # если надо до самого длинного то from itertools import zip_longest (недостающие значения заполняются None)
    # WARN: если будет 10k-50k+ идей то раздуется память - не актуально (хотя...)
    list_settings = data["settings"]["ideas"]["list"]

    for idea in ideas[:limit]:
        if any(x in ["date", "uuid", "time"] for x in table_columns):
            finfo = _parse_filename_info(idea)
            if "date" in table_columns: columns_data["date"].append(finfo["date"])
            if "uuid" in table_columns: columns_data["uuid"].append(finfo["uuid"])
            if "time" in table_columns: columns_data["time"].append(finfo["time"])

        if any(x in ["name", "description", "desc", "version"] for x in table_columns):
            raw_content = (folder_ideas / idea).read_text().splitlines()
            fcontent = _extract_metadata_as_list(raw_content)

            if "name" in table_columns:
                if (name := _get_value_from_metadata(fcontent, "name"))[0]:
                    name = name[1]

                    columns_data["name"].append(format_field(
                        name,
                        auto = list_settings["max_symbols"]["auto"]["name"],
                        etc = list_settings["etc"]["name"],
                        max_symbols_of_field = list_settings["max_symbols"]["name"],
                        max_symbols_of_col = len(default_cols["name"])
                    ))
                else:
                    auto = list_settings["max_symbols"]["auto"]["name"]
                    max_symbols_of_name = list_settings["max_symbols"]["name"]
                    max_symbols_of_col = len(default_cols["name"])
                    name = "?" * (max_symbols_of_name if not auto else max_symbols_of_col)

                    columns_data["name"].append(name)
            # INFO: ну нафиг эту поддержку - не актуально
            if "description" in table_columns or "desc" in table_columns: # WARN: поддерживаем старый вариант
                desc_lines = _extract_description(raw_content)

                # WARN: до v0.7.0: если значения не будет то тогда писать предупреждение что ее нет и ставить из default_config.json 
                columns_data["description"].append(format_field(
                    desc_lines,
                    auto = list_settings["max_symbols"]["auto"]["description"],
                    etc = list_settings["etc"]["description"],
                    sep = list_settings["separator_description"],
                    max_symbols_of_field = list_settings["max_symbols"]["description"],
                    max_symbols_of_col = len(default_cols["description"])
                ))

            if "version" in table_columns: # TODO: добавить поддержку ver
                if (version := _get_value_from_metadata(fcontent, "version"))[0]: version = version[1]
                else: version = "?.?"

                columns_data["version"].append(version)

    columns = []
    for column in filter(lambda x: x in default_cols, table_columns):
        columns.append(Column(default_cols[column], columns_data[column]))

    sep_settings = data["settings"]["ideas"]["list"]["separator"]
    table = TableRenderer(columns).config(
        line_separator = sep_settings["line"],
        column_separator = sep_settings["column_middle"],
        column_separator_end = sep_settings["column_end"],
        column_separator_start = sep_settings["column_start"],
        is_line_separator_start = sep_settings["line_start"],
        is_line_separator_middle = sep_settings["line_middle"],
        is_line_separator_end = sep_settings["line_end"]
    )
    print(table.render())
    """

    # TODO: добавить выравнивание у №, добавить настройку столбцов, добавить max_results
    if len(coincidences) == 0: # нет идей
        # TODO: добавить класс Error и добавить эту ошибку как Error.NoMatchesFound
        # TODO: добавить класс Error и добавить ошибку Error.IncorrectDate / IncorrectInput
        print("E: No Matches Found")

    elif len(coincidences) == 1:
        info = _parse_filename_info(coincidences[0])
        # TODO: добавить настройку чтобы выводились только определенные параметры или автоматически (в зависимости от введенных данных)
        print(f"Found 1 idea:\ndate: {info["date"]}, uuid: {info["uuid"]}")
        if _warning(data["warnings"]["ideas"]["delete"]["idea"]):
            print("Deleting idea...")
            (folder_ideas / info["filename"]).unlink()
        else:
            print("Abort")
    else: # много идей
        # TODO: добавить настройку столбцов таблицы
        print(f"Found {len(coincidences)} ideas for {f"{date}, " if date is not None else ""}{f"{time}, " if time is not None else ""}{f"{uuid6}, " if uuid6 is not None else ""}{f"{name}, " if name is not None else ""}:")
        print(data["settings"]["all"]["separator_symbol"] * data["settings"]["all"]["separator_length"])

        for i in range(len(coincidences)): # i202608041359_dd0cd3 -> i 20260804 1359 _dd0cd3
            info = _parse_filename_info(coincidences[i])
            print(f"  {i+1}. {info["date"]} {info["time"]} [{info["uuid"]}]")

        print(data["settings"]["all"]["separator_symbol"] * data["settings"]["all"]["separator_length"])

        # TODO: переместить в config
        # TODO: добавить настройку в конфиг чтобы эта звездочка не показывалась и справку
        print("* - Gexz code is DSL which is used to enter ranges")
        command = "base 1;" + input(f"Enter number to delete (1-{len(coincidences)}, 0 to cancel or Gexz* code (beta): ")
        answer = _parse_select_answer(command, all_len=len(coincidences))
        #print(answer)
        if answer == []:
            print("E: Answer is empty")
            print("Abort")
            return
        if 0 in answer:
            print("Abort")
            return

        if len(answer) == 1:
            answer = answer[0]
            info = _parse_filename_info(coincidences[answer-1])
            print(f"Selected idea:\ndate: {info["date"]}, uuid: {coincidences[answer-1][14:20]}")
            if _warning(data["warnings"]["ideas"]["delete"]["idea"]):
                print("Deleting idea...")
                (folder_ideas / coincidences[answer-1]).unlink()
            return
        if len(answer) > 1:
            print("Selected ideas:")
            for i in answer:
                info = _parse_filename_info(coincidences[int(i)-1])
                print(f"{i} | date: {info["date"]}, uuid: {info["uuid"]}")

            if _warning(data["warnings"]["ideas"]["delete"]["ideas"]):
                print("Deleting ideas...")
                for i in answer:
                    (folder_ideas / coincidences[int(i)-1]).unlink()
            return

def remove_idea_by_custom_metadata(): pass

def _to_trigram(text):
    # hello -> hel ell llo -> 5 | 3
    # 1234567890 -> 123 234 345 456 567 678 789 890  -> 10 | 8
    # abcd -> abc bcd -> 4 | 2
    # abc -> abc -> 3 | 1
    # ab -> ab -> 2| 1
    # hello! how are you? -> hel ell llo lo! o!  ! h  ow how ow  w a ..
    # ab 0+2 = 2 == 2? true -> 
    new_text = []
    if len(text) - 2 <= 0:
        new_text.append(text)
    else:
        for i in range(len(text) - 2):
            new_text.append(text[i:i+3])
    return new_text

def _jaccard_similarity(text: list(str), variant: list(str)) -> float:
    #print("text (ожидается триграммы):", text)
    set_t = set(text)
    set_v = set(variant)

    if not set_t and not set_v:
        return 1.0

    intersection = len(set_t & set_v)

    union = len(set_t | set_v)

    return intersection / union if union != 0 else 0.0

# NOTE: конечная функция для search_idea()
def _trigram_search(text: str, variants: list(str)) -> tuple((int, float)): # возвращает (индекс, уверенность/оценка)
    # TODO: добавить настройку в config: отображение в процентах или в дробных числах 
    t = _to_trigram(text)
    v = []
    for i in variants:
        v.append(_to_trigram(i))

    ranked = []

    for idx, cand_trigrams in enumerate(v):
        score = _jaccard_similarity(t, cand_trigrams)
        ranked.append((idx, score))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked

# WARN: тестовое

def _extract_description(raw_content: list[str]) -> list[str]:
    sep = [i for i, line in enumerate(raw_content) if line.strip() == "---"]

    if len(sep) >= 2:
        return raw_content[sep[1] + 1:]
    elif len(sep) == 1:
        return raw_content[sep[0] + 1:]
    else:
        return raw_content

def format_field(field_lines: list[str] | str, *, auto: bool, sep: str = "", etc: str, max_symbols_of_field: int, max_symbols_of_col: int) -> str:
    field = sep.join(field_lines if isinstance(field_lines, list) else [field_lines]) # TODO: добавить разделитель в конфиг - добавлено

    if not auto:
        if len(field) > max_symbols_of_field:
            field = f"{field[:max_symbols_of_field - len(etc)]}{etc}"
    else:
        if len(field) > max_symbols_of_col:
            field = f"{field[:max_symbols_of_col - len(etc)]}{etc}"

    return field

def _determine_limit(limit: int, lst: list, *, default=-1) -> int:
    if limit is None:
        if default <= -1:
            return len(lst)
        return default
    return min((len(lst) if limit <= -1 else limit), len(lst))

class Column:
    def __init__(self, name: str, lines: list[str] = None):
        self.name = name
        self.lines = [str(x) for x in lines] if lines is not None else []
        self._width = None
        self.no_column_found_symbol = "-"

        # WARN: убрать
        #for line in [self.name, *self.lines]:
            #if (len_of_line := len(str(line))) > self.width: self.width = len_of_line

    @property
    def width(self) -> int:
        # TODO: изменить
        max_val_len = max((len(v) for v in self.lines), default=0)
        self._width = max(len(self.name), max_val_len)
        return self._width

    def __str__(self):
        return f"Class Column:\nName: {self.name}\nWidth: {self.width}\nLines: {self.lines}"

    def __repr__(self):
        return f"{self.name}({self.width}): {self.lines}"

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, key):
        try:
            return self.lines[key]
        except IndexError:
            return self.no_column_found_symbol

class TableRenderer:
    # WARN: НИКОГДА НЕ ПЕРЕДАВАТЬ СПИСОК КАК ОБЫЧНЕ ЗНАЧЕНИЕ В ПАРАМЕТРАХ
    def __init__(self, columns: list[Column] = None):
        self.columns = columns if columns is not None else []
        self.column_separator = " | "
        self.column_separator_start = ""
        self.column_separator_end = ""
        self.line_separator = "-"
        self.is_line_separator_end = False
        self.is_line_separator_start = True
        self.is_line_separator_middle = False
        # TODO: добавить переменную пересечения,
        # типа если полоса строки пересечется с полосой колонки то написать вместо l_sep наод "+" или другую строку

    def __str__(self):
        columns = "\n\t".join([repr(x) for x in self.columns])
        return f"Class TableRenderer\nColumns:\n\t{columns}"

    def config(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"TableRenderer has no attribute '{key}'")
        return self

    def render(self):
        result = ""

        cells = [f"{column.name:^{column.width}}" for column in self.columns]
        text = self.column_separator_start + (self.column_separator).join(cells) + self.column_separator_end

        if self.is_line_separator_start: result += (len(text) * self.line_separator) + "\n"
        result += text + "\n"
        if self.is_line_separator_middle: result += (len(text) * self.line_separator) + "\n"

        max_index = max([len(column) for column in self.columns])
        #print(max_index)

        for x in range(max_index):
            result += self.column_separator_start
            for index, column in enumerate(self.columns):
                result += f"{column[x]:^{column.width}}" + (self.column_separator_end + "\n" if index+1 == len(self.columns) else self.column_separator)

        if self.is_line_separator_end: result += (len(text) * self.line_separator) + "\n"

        return result

#if __name__ == "__main__":
    #col1 = Column("name")     # lines = []
    #col2 = Column("test")     # lines = [] (этот же список!)
    #col1.lines.append("hello")
    #print(col2.lines)  # ['hello']  # БАГ!

    #table = TableRenderer([Column(x, ["1", "2", "34", "123456"]) for x in ["name", "test", "desc", "testing", "a"]] + [Column("abc", "a")])
    #print(table)
    #print(len(table.columns))
    #print(table.render())

# NOTE: тут только по названию
# WARN: refactor (срезы)
# FIXME: n не используется
def search_idea(text): # TODO: добавить поиск только по имени или только по описанию
    # TODO: v0.7.0: добаивть --sort и --reverse
    # TODO: добавить так чтобы можно было считать не по триграммам а можно по 2 буквам или по 3 буквам
    # TODO: добавить ограничение текста в config у name
    # TODO: сделать безопасное обращение к config и еще объединить в одну переменную чтобы легко было менять
    # например вместо data["settings"]["ideas"]["search"]["max_results"] сделать search["max_results"] чтобы было легко менять только одно
    # NOTE: вся логика поиска тут
    ideas = _get_list_of_files(folder_ideas)
    variants = []
    #descs = []
    #uuids = []
    for i in ideas:
        info = (folder_ideas / i).read_text().splitlines()[1][6:]
        variants.append(info)
    #descs.append((folder_ideas / i).read_text().splitlines()[6])
    #uuids.append((folder_ideas / i).read_text().splitlines()[3])
    #
    #max_number = data["settings"]["ideas"]["search"]["max_results"]

    # сделать поиск
    ideas_scores = _trigram_search(text, variants)
    # ideas
    # вывести результаты
    #number = 1

    # INFO: надо полчить на вход список (уверенности и оценки) и тот же список но уже с названиями файлов


    limit = _determine_limit(
        data["settings"]["ideas"]["search"]["max_results"],
        ideas_scores,
        default = data["settings"]["ideas"]["search"].get("max_results", -1)
    )

    table_columns = data["settings"]["ideas"]["search"]["table_columns"]

    description_list = []
    columns_data = { # NOTE: защита от дурака есть, потому что в классе Column предусмотренно что если есть недостающие строки
        "number": list(map(str, list(range(1, len(ideas[:limit])+1)))) if "number" in table_columns else [],
        "score": [],
        "date": [],
        "name": [],
        "description": description_list,
        "desc": description_list,
        "time": [],
        "uuid": [],
        "version": []
    }
    default_cols = { # TODO: v0.7.0: добавить эти все настройки в конфиг
        # TODO: добавить type (i- - idea, g- guide и тд (префикс в файле))
        "number": "№",
        "date": "date",
        "name": "name",
        "description": "description", # TODO: v0.7.0: изменить в конфиге desc на description (ключ, не значение)
        "desc": "description",
        "time": "time",
        "uuid": "uuid",
        "version": "version",
        "score": "score"
    }
    # TODO: v0.7.0; добавить настройку рядом table_columns которая убирает дубликаты

    # INFO: zip нужно когда надо пройти по 2 спискам одновременно
    # если надо до самого длинного то from itertools import zip_longest (недостающие значения заполняются None)
    # WARN: если будет 10k-50k+ идей то раздуется память - не актуально (хотя...)
    search_settings = data["settings"]["ideas"]["search"]

    for index, score in ideas_scores[:limit]:
        if any(x in ["date", "uuid", "time"] for x in table_columns):
            finfo = _parse_filename_info(ideas[index])
            if "date" in table_columns: columns_data["date"].append(finfo["date"])
            if "uuid" in table_columns: columns_data["uuid"].append(finfo["uuid"])
            if "time" in table_columns: columns_data["time"].append(finfo["time"])

        if "score" in table_columns:
            if search_settings["score_style"] == "percent":
                columns_data["score"].append(f"{score * 100:>3.0f}%")
            else: columns_data["score"].append(score)

        if any(x in ["name", "description", "desc", "version"] for x in table_columns):
            raw_content = (folder_ideas / ideas[index]).read_text().splitlines()
            fcontent = _extract_metadata_as_list(raw_content)

            if "name" in table_columns:
                if (name := _get_value_from_metadata(fcontent, "name"))[0]:
                    name = name[1]

                    columns_data["name"].append(format_field(
                        name,
                        auto = search_settings["max_symbols"]["auto"]["name"],
                        etc = search_settings["etc"]["name"],
                        max_symbols_of_field = search_settings["max_symbols"]["name"],
                        max_symbols_of_col = len(default_cols["name"])
                    ))
                else:
                    auto = search_settings["max_symbols"]["auto"]["name"]
                    max_symbols_of_name = search_settings["max_symbols"]["name"]
                    max_symbols_of_col = len(default_cols["name"])
                    name = "?" * (max_symbols_of_name if not auto else max_symbols_of_col)

                    columns_data["name"].append(name)
            if "description" in table_columns or "desc" in table_columns: # WARN: поддерживаем старый вариант
                desc_lines = _extract_description(raw_content)

                # WARN: до v0.7.0: если значения не будет то тогда писать предупреждение что ее нет и ставить из default_config.json 
                columns_data["description"].append(format_field(
                    desc_lines,
                    auto = search_settings["max_symbols"]["auto"]["description"],
                    etc = search_settings["etc"]["description"],
                    sep = search_settings["separator_description"],
                    max_symbols_of_field = search_settings["max_symbols"]["description"],
                    max_symbols_of_col = len(default_cols["description"])
                ))

            if "version" in table_columns: # TODO: добавить поддержку ver
                if (version := _get_value_from_metadata(fcontent, "version"))[0]: version = version[1]
                else: version = "?.?"

                columns_data["version"].append(version)

    columns = []
    for column in filter(lambda x: x in default_cols, table_columns):
        columns.append(Column(default_cols[column], columns_data[column]))

    sep_settings = data["settings"]["ideas"]["search"]["separator"]
    #print(sep_settings)
    table = TableRenderer(columns).config(
        line_separator = sep_settings["line"],
        column_separator = sep_settings["column_middle"],
        column_separator_end = sep_settings["column_end"],
        column_separator_start = sep_settings["column_start"],
        is_line_separator_start = sep_settings["line_start"],
        is_line_separator_middle = sep_settings["line_middle"],
        is_line_separator_end = sep_settings["line_end"]
    )
    print(table.render())

def list_ideas(max_results=None):
    # TODO: добавить проверку даты и uuid в названии файла а не только в метаданных
    # теперь я буду помечать выполненые todo через #hesh_of_commit и версию когда добавленна но если приставка -dev, то
    # добавленно именно во время разработки версии и она еще не вышла

    # NOTE: это старый код который не требуется в рефакторинге
    ideas = _get_list_of_files(folder_ideas)

    if not ideas:
        print("E: No Ideas Found")
        return

    # INFO: логика лимита: если -1 то все показывать, иначе,
    # количество которое указано но если оно больше чем общее количество то только все которые есть
    limit = _determine_limit(
        max_results,
        ideas,
        default = data["settings"]["ideas"]["list"].get("max_results", -1)
    )

    # NOTE: новый код, и БЕЗ HACK

    table_columns = data["settings"]["ideas"]["list"]["table_columns"]

    description_list = []
    columns_data = { # NOTE: защита от дурака есть, потому что в классе Column предусмотренно что если есть недостающие строки
        "number": list(map(str, list(range(1, len(ideas[:limit])+1)))) if "number" in table_columns else [],
        "date": [],
        "name": [],
        "description": description_list,
        "desc": description_list,
        "time": [],
        "uuid": [],
        "version": []
    }
    default_cols = { # TODO: v0.7.0: добавить эти все настройки в конфиг
        # TODO: добавить type (i- - idea, g- guide и тд (префикс в файле))
        "number": "№",
        "date": "date",
        "name": "name",
        "description": "description", # TODO: v0.7.0: изменить в конфиге desc на description (ключ, не значение)
        "desc": "description",
        "time": "time",
        "uuid": "uuid",
        "version": "version"
    }
    # TODO: добавить настройку рядом table_columns которая убирает дубликаты

    # INFO: zip нужно когда надо пройти по 2 спискам одновременно
    # если надо до самого длинного то from itertools import zip_longest (недостающие значения заполняются None)
    # WARN: если будет 10k-50k+ идей то раздуется память - не актуально (хотя...)
    list_settings = data["settings"]["ideas"]["list"]

    for idea in ideas[:limit]:
        if any(x in ["date", "uuid", "time"] for x in table_columns):
            finfo = _parse_filename_info(idea)
            if "date" in table_columns: columns_data["date"].append(finfo["date"])
            if "uuid" in table_columns: columns_data["uuid"].append(finfo["uuid"])
            if "time" in table_columns: columns_data["time"].append(finfo["time"])

        if any(x in ["name", "description", "desc", "version"] for x in table_columns):
            raw_content = (folder_ideas / idea).read_text().splitlines()
            fcontent = _extract_metadata_as_list(raw_content)

            if "name" in table_columns:
                if (name := _get_value_from_metadata(fcontent, "name"))[0]:
                    name = name[1]

                    columns_data["name"].append(format_field(
                        name,
                        auto = list_settings["max_symbols"]["auto"]["name"],
                        etc = list_settings["etc"]["name"],
                        max_symbols_of_field = list_settings["max_symbols"]["name"],
                        max_symbols_of_col = len(default_cols["name"])
                    ))
                else:
                    auto = list_settings["max_symbols"]["auto"]["name"]
                    max_symbols_of_name = list_settings["max_symbols"]["name"]
                    max_symbols_of_col = len(default_cols["name"])
                    name = "?" * (max_symbols_of_name if not auto else max_symbols_of_col)

                    columns_data["name"].append(name)
            # INFO: ну нафиг эту поддержку - не актуально
            if "description" in table_columns or "desc" in table_columns: # WARN: поддерживаем старый вариант
                desc_lines = _extract_description(raw_content)

                # WARN: до v0.7.0: если значения не будет то тогда писать предупреждение что ее нет и ставить из default_config.json 
                columns_data["description"].append(format_field(
                    desc_lines,
                    auto = list_settings["max_symbols"]["auto"]["description"],
                    etc = list_settings["etc"]["description"],
                    sep = list_settings["separator_description"],
                    max_symbols_of_field = list_settings["max_symbols"]["description"],
                    max_symbols_of_col = len(default_cols["description"])
                ))

            if "version" in table_columns: # TODO: добавить поддержку ver
                if (version := _get_value_from_metadata(fcontent, "version"))[0]: version = version[1]
                else: version = "?.?"

                columns_data["version"].append(version)

    columns = []
    for column in filter(lambda x: x in default_cols, table_columns):
        columns.append(Column(default_cols[column], columns_data[column]))

    sep_settings = data["settings"]["ideas"]["list"]["separator"]
    table = TableRenderer(columns).config(
        line_separator = sep_settings["line"],
        column_separator = sep_settings["column_middle"],
        column_separator_end = sep_settings["column_end"],
        column_separator_start = sep_settings["column_start"],
        is_line_separator_start = sep_settings["line_start"],
        is_line_separator_middle = sep_settings["line_middle"],
        is_line_separator_end = sep_settings["line_end"]
    )
    print(table.render())

    # TODO: удалить separator_length
    # TODO: добавить настройку которая будет показывать или не будет эту линию и также будет ли она внизу или нет - есть!

#if __name__ == "__main__":
#    print(_parse_filename_info(input()))
