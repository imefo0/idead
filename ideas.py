from pathlib import Path
from config import *
from datetime import datetime
import uuid
from utils import _warning

data = get()

# TODO: добавить город в метаданные идей и имя пользователя
# TODO: v0.7.0: разделить helper из config.json на config.json и helper.json а потом все равно перейти на toml (v0.8.0)
# TODO: v0.7.0: изменить прямые обращения к config на переменные вначале функции

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

def _get_vale_from_metadata(metadata: list(str), data_search: str) -> (bool, str):
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

# TODO: обновить ux всех remove и добавить флаг по триграммам
# TODO: обновить способ поиска в remove
# TODO: добавить поиск идеи по описанию в v0.7.0
# FIXME: исправить косметический баг когда выводится в found 1+ ideas for name, :
def remove_idea(date=None, time=None, uuid6=None, name=None):
    remove_idea_match_mode = data["settings"]["ideas"]["remove"].get("search_mode", "soft") # hard/soft

    if date is None and time is None and uuid6 is None and name is None:
        print("E: No Data To Delete The Idea")
        return

    if date: date = _clear_num(date)
    if time: time = _clear_num(time)

    coincidences = []
    files = _get_list_of_files(folder_ideas)
    names = [_get_vale_from_metadata(_extract_metadata_as_list((folder_ideas / x).read_text().splitlines()), "name") for x in files]
    weights = []

    # проходимся по каждому файлу
    num = 0
    for i in _get_list_of_files(folder_ideas): # i202608041359_dd0cd3.md -> i 2026-08-04 13:59 _ dd0cd3 .md
        # сохраняем данные кандидата
        candidate_date = i[1:9]
        candidate_time = i[9:13]
        candidate_uuid = i[14:20]
        result = _get_vale_from_metadata(_extract_metadata_as_list((folder_ideas / i).read_text().splitlines()), "name")
        if not result[0]:
            print(f"WARN: No Name In Idea (uuid: {candidate_uuid}) Found")
            continue
        candidate_name = result[1]
        #print(f"date = {candidate_date}, time = {candidate_time}, uuid = {candidate_uuid}, name = {candidate_name}")

        # 1. если совпадают даты или если дата не введена то продолжить
        if date is None or date == candidate_date:
            # 2. если совпадает время или если время не введено то продолжить
            if time is None or time == candidate_time:
            # 3. если совпадает uuid или если uuid не введен то продолжить
                if uuid6 is None or uuid6 == candidate_uuid:
                    # 4. если совпадет имя и если спсоб hard то добавить в coincidences
                    if name is None or (name == candidate_name and remove_idea_match_mode == "hard"):
                        coincidences.append(i)
                        continue
                    if remove_idea_match_mode != "hard":
                    # если soft:
                    # (короче надо вывести весь список идей но в порядке убывания по уверенности, сопоставив каждый инедекс с списком имен файлов)
                    # надо получить список имен в том порядке в таком же как и в списке файлов (до for i in _get_list_of_files(folder_ideas))
                    # потом надо написать _trigram_search(candidate_name, name_variants)
                        score = _jaccard_similarity(_to_trigram(name), _to_trigram(candidate_name))
                        #print("score, num:", score, num)
                        if score != 0.0:
                            #print("APPEND:", score, num, i)
                            coincidences.append(i)
                            weights.append((num, score))
                            #print("--- AFTER APPENDING ---")
                            #print("coincidences:".upper(), coincidences)
                            #print("weights:".upper(), weights)
                            #print("-----------------------")
                            num += 1
                    # потом for i in _trigram_search():
                    #       coincidences.append(files[i[0]])
    if name is not None and remove_idea_match_mode == "soft":
        #print("started")
        #print("weights:", weights)
        weights.sort(key=lambda x: x[1], reverse=True)
        tmp_coincidences = coincidences.copy()
        coincidences = []
        for idx, score in weights:
            print(idx, score)
            print(tmp_coincidences[idx])
            coincidences.append(tmp_coincidences[idx])

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
        answer = input(f"Enter number to delete (1-{len(coincidences)}, 0 to cancel or enter ideas via ',' (1,2,3,4)): ")
        answer = answer.split(",")
        answer = answer[0] if len(answer) == 1 else answer
        if not isinstance(answer, list) and not answer.isdigit():
            print("E: Incorrect number")
            print("Abort")
            answer = 0
        if answer != 0 and answer != "0" and not isinstance(answer, list):
            info = _parse_filename_info(coincidences[answer-1])
            print(f"Selected idea:\ndate: {info["date"]}, uuid: {coincidences[answer-1][14:20]}")
            if _warning(data["warnings"]["ideas"]["delete"]["idea"]):
                print("Deleting idea...")
                (folder_ideas / coincidences[answer-1]).unlink()
        if isinstance(answer, list):
            for i in answer:
                if not i.isdigit():
                    print("E: Incorrect number")
                    print("Abort")
                    return
                if i == "0":
                    return
            print("Selected ideas:")
            for i in answer:
                info = _parse_filename_info(coincidences[int(i)-1])
                print(f"date: {info["date"]}, uuid: {info["uuid"]}")

            if _warning(data["warnings"]["ideas"]["delete"]["ideas"]):
                print("Deleting ideas...")
                for i in answer:
                    (folder_ideas / coincidences[int(i)-1]).unlink()

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

class Column:
    def __init__(self, name: str, lines: list[str] = None):
        self.name = name
        self.lines = lines if lines is not None else []
        self.width = 0
        self.no_column_found_symbol = "-"

        for line in [self.name, *self.lines]:
            if (len_of_line := len(str(line))) > self.width: self.width = len_of_line

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
    def __init__(self, columns: list[Column] = []):
        self.columns = columns
        self.column_separator = " | "
        self.column_separator_start = ""
        self.column_separator_end = ""
        self.line_separator = "-"
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

        result += text + "\n"
        result += (len(text) * self.line_separator) + "\n"

        max_index = max([len(column) for column in self.columns])
        #print(max_index)

        for x in range(max_index):
            result += self.column_separator_start
            for index, column in enumerate(self.columns):
                result += f"{column[x]:^{column.width}}" + (self.column_separator_end + "\n" if index+1 == len(self.columns) else self.column_separator)

        return result
if __name__ == "__main__":
    table = TableRenderer([Column(x, ["1", "2", "34", "123456"]) for x in ["name", "test", "desc", "testing", "a"]] + [Column("abc", "a")])
    print(table)
    #print(len(table.columns))
    print(table.render())

# NOTE: тут только по названию
# WARN: refactor (срезы)
# FIXME: n не используется
def search_idea(text): # TODO: добавить поиск только по имени или только по описанию
    # TODO: добавить так чтобы можно было считать не по триграммам а можно по 2 буквам или по 3 буквам
    # TODO: добавить ограничение текста в config у name
    # получить список текстов
    ideas = _get_list_of_files(folder_ideas)
    variants = []
    descs = []
    uuids = []
    for i in ideas:
        info = (folder_ideas / i).read_text().splitlines()[1][6:]
        variants.append(info)
        descs.append((folder_ideas / i).read_text().splitlines()[6])
        uuids.append((folder_ideas / i).read_text().splitlines()[3])

    max_number = data["settings"]["ideas"]["search"]["max_results"]

    # сделать поиск
    search_status = _trigram_search(text, variants)
    # вывести результаты
    number = 1

    for i in data["settings"]["ideas"]["search"]["table_columns"]:
        if i == "number": print(f"{" "*(len(str(min(max_number, len(search_status))))-1)}№", end=" ")
        elif i == "score": print("scr.", end=" ")
        elif i == "date": print("   date   ", end=" ") 
        elif i == "name": print("    name     ", end=" ")
        elif i == "desc": print(" description ", end=" ")
        elif i == "time": print("time ", end=" ")
        elif i == "uuid": print(" uuid ", end=" ")
    print()

    print(data["settings"]["all"]["separator_symbol"] * data["settings"]["all"]["separator_length"])

    for index, status in search_status[:min(max_number, len(search_status))]:
        # TODO: добавить настройку точки после № например если стоит true то будет "1." а если false то "1" в config
        # WARN: добавить оптимизацию чтобы считались только те данные которые нужны

        n = f"{number:>{len(str(min(max_number, len(search_status))))}}"
        score_style = data["settings"]["ideas"]["search"]["score_style"] # percent или "decimal"
        # TODO: добавить вывод в процентах
        if score_style == "percent":
            score = f"{round(status * 100):>3}%"
        else:
            score = f"{status:.2f}"

        date = ideas[index][1:9]
        date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
        name = f"{variants[index][:10]}{"..." if len(variants[index]) >= 10 else " "*(13 - len(variants[index]))}"
        desc = f"{descs[index][:10]}{"..." if len(descs[index]) >= 10 else " "*(13 - len(descs[index]))}"
        time_t = ideas[index][9:13]
        time_t = f"{time_t[0:2]}:{time_t[2:4]}"
        uuid_t = f"{uuids[index][6:]}"
        #       1. 0.31 2026-08-08 this is a ...
        # status:.1% -> 75.9% 
        for i in data["settings"]["ideas"]["search"]["table_columns"]:
            if i == "number": print(number, end=" ")
            elif i == "score": print(score, end=" ")
            elif i == "date": print(date, end=" ")
            elif i == "name": print(name, end=" ")
            elif i == "desc": print(desc, end=" ")
            elif i == "time": print(time_t, end=" ")
            elif i == "uuid": print(uuid_t, end=" ")
        print()
        number += 1

def list_ideas(max_results=None):
    # TODO: добавить выравнивание - уже будет готово благодаря TR
    # TODO: добавить проверку даты и uuid в названии файла а не только в метаданных
    # WARN: refactor - уже идет (v0.6.0 -> v0.7.0)
    # TODO: добавить настройку которая означает "показывать ли столбцы в таблице" - уже есть: v0.7.0-dev (#42625e)
    # теперь я буду помечать выполненые todo через #hesh_of_commit и версию когда добавленна но если приставка -dev, то
    # добавленно именно во время разработки версии и она еще не вышла

    # NOTE: это старый код который не требуется в рефакторинге
    ideas = _get_list_of_files(folder_ideas)

    if not ideas:
        print("E: No Ideas Found")
        return

    number = 1

    # INFO: логика лимита: если -1 то все показывать, иначе,
    # количество которое указано но если оно больше чем общее количество то только все которые есть
    if max_results is not None: limit = max_results
    else:
        max_results_config = data["settings"]["ideas"]["list"].get("max_results", -1)
        limit = len(ideas) if max_results_config == -1 else max_results_config
    limit = min(limit, len(ideas))

    """
    # INFO: вывод шапки таблицы
    print(f"{"№":<{len(str(limit))+1}}    date    time   uuid  ver    name")
    print(data["settings"]["all"]["separator_symbol"] * data["settings"]["all"]["separator_length"])
    """

    # FIXME: длина разделяющая шапки меньше чем сами данные (надо сделать динамическую длину)
    #"""
    
    # NOTE: вывод шапки таблицы
    #for i in data["settings"]["ideas"]["list"]["table_columns"]:
        #if i == "number": print(f"{"№":<{len(str(limit))}}", end=" | ")
        #elif i == "date": print("   date   ", end=" | ")
        #elif i == "name": print("    name     ", end=" | ")
        #elif i == "desc": print(" description ", end=" | ")
        #elif i == "time": print("time ", end=" | ")
        #elif i == "uuid": print(" uuid ", end=" | ")
        #elif i == "version": print("ver", end=" | ") # FIXME: если версия будет больше 10, например 1.13 или 23.4, то будет неверный вывод
        ## WARN: добавить версию
    #print()

    # NOTE: новый код, но с HACK

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
                if (name := _get_vale_from_metadata(fcontent, "name"))[0]:
                    name = name[1]

                    if len(name) > 13:
                        name = f"{name[:10]}..."
                    else:
                        name = f"{name[:13]:<13}"
                else: name = "?????????????"

                columns_data["name"].append(name)
            # INFO: ну нафиг эту поддержку - не актуально
            if "description" in table_columns or "desc" in table_columns: # WARN: поддерживаем старый вариант
                sep = [i for i, line in enumerate(raw_content) if line.strip() == "---"]

                if len(sep) >= 2:
                    desc_lines = raw_content[sep[1] + 1:]
                elif len(sep) == 1:
                    desc_lines = raw_content[sep[0] + 1:]
                else:
                    desc_lines = raw_content

                desc = "; ".join(desc_lines) # TODO: добавить разделитель в конфиг

                columns_data["description"].append(desc)

            if "version" in table_columns: # TODO: добавить поддержку ver
                if (version := _get_vale_from_metadata(fcontent, "version"))[0]: version = version[1]
                else: version = "?.?"

                columns_data["version"].append(version)

    columns = []
    for column in filter(lambda x: x in default_cols, table_columns):
        columns.append(Column(default_cols[column], columns_data[column]))

    table = TableRenderer(columns)
    print(table.render())

    # TODO: удалить separator_length

    # NOTE: старый код который надо потом удалить, причина почему не могу сейчас, потому что он считает все данные по номерам
    # то есть по строкам, а надо по столбцам, потому что логика таблицы изменилась и ее надо кормить столбиками,
    # а не строками как раньше без ооп
    """
    print(data["settings"]["all"]["separator_symbol"] * data["settings"]["all"]["separator_length"])

    for i in ideas[:limit]:
        # TODO: добавить настройку точки после № например если стоит true то будет "1." а если false то "1" в config
        # WARN: добавить оптимизацию чтобы считались только те данные которые нужны
        # WARN: dry

        n = f"{number:>{len(str(limit))}}"
        finfo = _parse_filename_info(i)
        raw_content = (folder_ideas / i).read_text().splitlines()
        fcontent = _extract_metadata_as_list(raw_content)

        date = finfo["date"] #ideas[index][1:9]
        # FIXME: если имя будет в 13 символов то нет смысла выводить name[:10] + "..."
        # WARN: если имя будет тоже многострочное то будет ошибка (наверное)
        if (name := _get_vale_from_metadata(fcontent, "name"))[0]: name = name[1]
        else: name = "?????????????"

        name = f"{name[:10]:<10}" + ("..." if len(name) > 10 else "   ")

        sep_indices = [i for i, line in enumerate(raw_content) if line.strip() == "---"]

        if len(sep_indices) >= 2:
            desc_lines = raw_content[sep_indices[1] + 1:]
        elif len(sep_indices) == 1:
            desc_lines = raw_content[sep_indices[0] + 1:]
        else:
            desc_lines = raw_content

        # TODO: добавить настройку этого разделителя: "; "
        desc = "; ".join(desc_lines)
        desc = f"{desc[:10]:<10}" + ("..." if len(desc) > 10 else "   ")

        if (version := _get_vale_from_metadata(fcontent, "version"))[0]: version = version[1]
        else: version = "?.?"
        #version = "1.0" # HACK заглушка
        time_t = finfo["time"]
        uuid_t = finfo["uuid"]
        #       1. 0.31 2026-08-08 this is a ...
        # status:.1% -> 75.9% 
        for i in data["settings"]["ideas"]["list"]["table_columns"]:
            if i == "number": print(n, end=" | ")
            elif i == "date": print(date, end=" | ")
            elif i == "name": print(name, end=" | ")
            elif i == "desc": print(desc, end=" | ")
            elif i == "time": print(time_t, end=" | ")
            elif i == "uuid": print(uuid_t, end=" | ")
            elif i == "version": print(version, end=" | ")
        print()
        number += 1

    """

    """
    for i in ideas[:limit]:
        info = (folder_ideas / i).read_text().splitlines()
        #print(data)
        #      1. 2026-08-08 11:44 20d2aa 1.0 text
        print(f"{f"{number:>{len(str(limit))}}"}. ", end="")
        print(f"{info[2][6:] if any("date" in line for line in info) else "????-??-?? ??:??"}", end=" ")
        print(f"{f"{info[3][6:]}" if any("uuid" in line for line in info) else "??????"}", end=" ")
        print(f"{f"{info[4][9:12]}" if any("version" in line for line in info) else "?.?"}", end=" ")
        print(f"{f"{info[1][6:16]}" if any("name" in line for line in info) else "??????????"}{"..." if len(info[1][6:]) >= 10 else ""}")

        number += 1

    print(data["settings"]["all"]["separator_symbol"] * data["settings"]["all"]["separator_length"])
    """
    # TODO: добавить настройку которая будет показывать или не будет эту линию и также будет ли она внизу или нет

#if __name__ == "__main__":
#    print(_parse_filename_info(input()))
