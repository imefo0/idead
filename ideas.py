from pathlib import Path
from config import *
from datetime import datetime
import uuid

data = get()

# TODO: добавить город в метаданные идей и имя пользователя
# TODO: добавить триграммы в search & remove

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

if __name__ == "__main__":
    idea = Idea(input(), input())
    idea.save()

def _get_list_of_files(folder):
    files = []

    for item in folder.iterdir():
        if item.is_file():
            files.append(item.name)

    return files

def _warning(msg): # y, yes?, yn -> yes? [yn] y -> True
    if data["settings"]["all"]["warning_choice"]:
        answer = input(f"{msg} [yn] ")
        if answer.lower().replace(" ", "").replace("\t", "").replace("\n", "") in ["y", "yes"]:
            return True
        else:
            return False
    return True

def _clear_num(num_str): # WARN: FFP
    return ''.join(filter(str.isdigit, num_str))


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
    # TODO: добавить в config формат даты
    # TODO: доавить сообщение о том что идея добавилась и показать uuid
    time_now = datetime.now().strftime(format_date + format_time)
    time_now_mini = datetime.now().strftime("%Y%m%d%H%M")

    uuid6 = uuid.uuid4().hex[:6]
    content = f"---\nname: {name}\ndate: {time_now}\nuuid: {uuid6}\nversion: {data["settings"]["ideas"]["version"]}\n---\n{desc}"

    (folder_ideas / f"i{time_now_mini}_{uuid12}.md").write_text(content)

def test_new_idea(name, desc):
    # TODO: добавит в config формат даты
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    time_now_mini = datetime.now().strftime("%Y%m%d%H%M")

    uuid6 = uuid.uuid4().hex[:6]
    content = f"---\nname: {name}\ndate: {time_now}\nuuid: {uuid6}\nversion: {data["settings"]["ideas"]["version"]}\n---\n{desc}"

    (Path.home() / ".cache/idead/tests/ideas" / f"i{time_now_mini}_{uuid6}.md").write_text(content)

    return uuid6

# TODO: обновить ux всех remove и добавить флаг по триграммам
# TODO: обновить способ поиска в remove
def remove_idea_by_date(date=False, time=False):

    if date: date = _clear_num(date)
    if time: time = _clear_num(time)

    coincidences = []
    for i in _get_list_of_files(folder_ideas): # i202608041359_dd0cd3.md -> i 2026-08-04 13:59 _ dd0cd3 .md
        if not time:
            if i[1:9] == date:
                coincidences.append(i)
        else:
            if not date:
                if i[9:13] == time:
                    coincidences.append(i)
            else:
                if i[1:9] == date and i[9:13] == time:
                    coincidences.append(i)

    if len(coincidences) == 0: # нет идей
        # TODO: добавить класс Error и добавить эту ошибку как Error.NoMatchesFound
        # TODO: добавить класс Error и добавить ошибку Error.IncorrectDate / IncorrectInput
        print("E: No Matches Found")

    elif len(coincidences) == 1:
        # TODO: добавить так чтобы была понятна какая идея удаляется
        
        # TODO: переместить data["warnings"]["ideas"]["delete"] в config
        if _warning(data["warnings"]["ideas"]["delete"]):
            print("Deleting idea...")
            (folder_ideas / coincidences[0]).unlink()
    else: # много идей
        # TODO: добавить удаление нескольких идей сразу

        print(f"Found {len(coincidences)} ideas for{f" {date[:4]}-{date[4:6]}-{date[6:8]}" if date else ""}{f" {time[:2]}:{time[2:]}" if time else ""}:")
        print(data["settings"]["all"]["separator_symbol"] * data["settings"]["all"]["separator_length"])
        for i in range(len(coincidences)): # i202608041359_dd0cd3 -> i 20260804 1359 _dd0cd3
            date_coincidences = f"{coincidences[i][1:5]}-{coincidences[i][5:7]}-{coincidences[i][7:9]}"
            time_coincidences = f"{coincidences[i][9:11]}:{coincidences[i][11:13]}"
            print(f"  {i+1}. {date_coincidences} {time_coincidences} [{coincidences[i][14:-3]}]")

        print(data["settings"]["all"]["separator_symbol"] * data["settings"]["all"]["separator_length"])
        try:
            # TODO: переместить в config
            answer = int(input(f"Enter number to delete (1-{len(coincidences)}, or 0 to cancel): "))
        except ValueError:
            print("E: Incorrect number")
            print("Cancellation...")
            answer = 0
        if answer != 0:
            if _warning(data["warnings"]["ideas"]["delete"]):
                print("Deleting idea...")
                (folder_ideas / coincidences[answer-1]).unlink()

def remove_idea_by_uuid(uuid_):

    coincidences = []
    for i in _get_list_of_files(folder_ideas): # i202608041359_dd0cd3.md -> i 2026-08-04 13:59 _ dd0cd3 .md
        if i[14:20] == uuid_:
            coincidences.append(i)

    if len(coincidences) == 0: # нет идей
        # TODO: добавить класс Error и добавить эту ошибку как Error.NoMatchesFound
        # TODO: добавить класс Error и добавить ошибку Error.IncorrectDate / IncorrectInput
        print("E: No Matches Found")

    elif len(coincidences) == 1:
        # TODO: добавить так чтобы была понятна какая идея удаляется

        if _warning(data["warnings"]["ideas"]["delete"]):
            print("Deleting idea...")
            (folder_ideas / coincidences[0]).unlink()

def remove_idea_by_name(name):

    coincidences = []
    for i in _get_list_of_files(folder_ideas): # i202608041359_dd0cd3.md -> i 2026-08-04 13:59 _ dd0cd3 .md
        # print((folder_ideas / i).read_text().splitlines()[1])
        if (folder_ideas / i).read_text().splitlines()[1][6:] == name:
            coincidences.append(i)

    if len(coincidences) == 0: # нет идей
        # TODO: добавить класс Error и добавить эту ошибку как Error.NoMatchesFound
        # TODO: добавить класс Error и добавить ошибку Error.IncorrectDate / IncorrectInput
        print("E: No Matches Found")

    elif len(coincidences) == 1:
        # TODO: добавить так чтобы была понятна какая идея удаляется

        if _warning(data["warnings"]["ideas"]["delete"]):
            print("Deleting idea...")
            (folder_ideas / coincidences[0]).unlink()

    else: # много идей
        # TODO: добавить удаление нескольких идей сразу

        print(f"Found {len(coincidences)} ideas for {name}:")
        print(data["settings"]["all"]["separator_symbol"] * data["settings"]["all"]["separator_length"])
        for i in range(len(coincidences)): # i202608041359_dd0cd3 -> i 20260804 1359 _dd0cd3
            date_coincidences = f"{coincidences[i][1:5]}-{coincidences[i][5:7]}-{coincidences[i][7:9]}"
            time_coincidences = f"{coincidences[i][9:11]}:{coincidences[i][11:13]}"
            print(f"  {i+1}. {date_coincidences} {time_coincidences} [{coincidences[i][14:-3]}]")

        print("-"*30)
        try:
            answer = int(input(f"Enter number to delete (1-{len(coincidences)}, or 0 to cancel): "))
        except ValueError:
            print("E: Incorrect number")
            print("Cancellation...")
            answer = 0

        if answer != 0:
            if _warning(data["warnings"]["ideas"]["delete"]):
                print("Deleting idea...")
                (folder_ideas / coincidences[answer-1]).unlink()

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

# NOTE: тут только по названию
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
        score = f"{status:.2f}" # TODO: добавить вывод в процентах
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

def list_ideas():
    # TODO: добавить выравнивание
    # TODO: добавить проверку даты и uuid в названии файла а не только в метаданных
    # WARN: refactor
    ideas = _get_list_of_files(folder_ideas)

    if not ideas:
        print("E: No Ideas Found")
        return

    print(" №     date    time   uuid  ver    name")
    print(data["settings"]["all"]["separator_symbol"] * data["settings"]["all"]["separator_length"])
    num = 1
    for i in ideas:
        info = (folder_ideas / i).read_text().splitlines()
        #print(data)
        #      1. 2026-08-08 11:44 20d2aa 1.0 text
        print(f"{num if num >= 10 else f" {num}"}. ", end="")
        print(f"{info[2][6:] if any("date" in line for line in info) else "????-??-?? ??:??"}", end=" ")
        print(f"{f"{info[3][6:]}" if any("uuid" in line for line in info) else "??????"}", end=" ")
        print(f"{f"{info[4][9:12]}" if any("version" in line for line in info) else "?.?"}", end=" ")
        print(f"{f"{info[1][6:16]}" if any("name" in line for line in info) else "??????????"}{"..." if len(info[1][6:]) >= 10 else ""}")

        num += 1

    print(data["settings"]["all"]["separator_symbol"] * data["settings"]["all"]["separator_length"])
