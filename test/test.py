import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ideas import _get_list_of_files
from config import folder_cache
from datetime import datetime
import uuid

def main():
    # сначала получаем список файлов для теста
    modules = list(
        map(
            lambda x: x.replace(".py", ""),
            filter(
                lambda x: x not in ["__init__.py", "test.py"],
                _get_list_of_files(Path(__file__).resolve().parent)
            )
        )
    )
    # тестируем
    print("testing...", end="\r")

    uuid6 = uuid.uuid4().hex[:6]

    Path(folder_cache / "tests").mkdir(parents=True, exist_ok=True)

    completed = 0
    all = 0
    for module in modules:
        result = __import__(module).main()
        r = ""
        for i in result:
            r += f"{i}\n"

        with open((folder_cache / "tests" / f"{uuid6}.txt"), "a") as f: # создаем файл, если нет, добавляет в файл
            f.write(f"module: {module}\n")
            f.write(f"date: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n")
            f.write(f"{r}\n")
            f.write(f"{"-"*30}\n")

        # добавляем пройденные тесты и общее количество тестов
        completed += result[-1][0]
        all += result[-1][1]

    # пишем результат
    RED = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    num_of_progress_bar_segments = 30
    green_sells = int(num_of_progress_bar_segments / all * completed)

    print("[", end="")
    print(f"{GREEN}{"█"*green_sells}{RESET}", end="")
    print(f"{RED}{"█"*(num_of_progress_bar_segments - green_sells)}{RESET}", end="")
    print("]", end=" ")
    print(f"{completed}/{all} | {(completed/all*100):.0f}%")
    # записываем подробности в кэш
    # добавить флаг который показывает недавные тесты из кэша

if __name__ == "__main__":
    main()
