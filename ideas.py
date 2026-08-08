from pathlib import Path
from config import *
from datetime import datetime

# TODO: добавить город в метаданные идей и имя пользователя
# TODO: добавить триграммы в search & remove

def _get_list_of_files(folder):
    files = []

    for item in folder.iterdir():
        if item.is_file():
            files.append(item.name)

    return files

def _warning(msg): # y, yes?, yn -> yes? [yn] y -> True
    if warning_choice:
        answer = input(f"{msg} [yn] ")
        if answer.lower() in ["y", "yes"]:
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
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    time_now_mini = now = datetime.now().strftime("%Y%m%d%H%M")

    uuid12 = uuid.uuid4().hex[:6]
    content = f"---\nname: {name}\ncreate_time: {time_now}\nuuid: {uuid12}\nversion: {idea_version}\n---\n{desc}"

    (folder_ideas / f"i{time_now_mini}_{uuid12}.md").write_text(content)

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

        if _warning(delete_idea_ask):
            print("Deleting idea...")
            (folder_ideas / coincidences[0]).unlink()
    else: # много идей
        # TODO: добавить удаление нескольких идей сразу

        print(f"Found {len(coincidences)} ideas for{f" {date[:4]}-{date[4:6]}-{date[6:8]}" if date else ""}{f" {time[:2]}:{time[2:]}" if time else ""}:")
        print(separator_symbol * separator_length)
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
            if _warning(delete_idea_ask):
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

        if _warning(delete_idea_ask):
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

        if _warning(delete_idea_ask):
            print("Deleting idea...")
            (folder_ideas / coincidences[0]).unlink()

    else: # много идей
        # TODO: добавить удаление нескольких идей сразу

        print(f"Found {len(coincidences)} ideas for {name}:")
        print(separator_symbol * separator_length)
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
            if _warning(delete_idea_ask):
                print("Deleting idea...")
                (folder_ideas / coincidences[answer-1]).unlink()

def remove_idea_by_custom_metadata(): pass

