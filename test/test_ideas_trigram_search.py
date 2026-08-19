import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ideas import _trigram_search

def main():
    test = [
        # 1. Точное совпадение (должен быть на первом месте с 1.0)
        [
            ["привет", ["привет", "мир", "пока"]],
            [(0, 1.0), (1, 0.0), (2, 0.0)]
        ],
        
        # 2. Похожие слова (проверяем ранжирование)
        [
            ["привет", ["приветствие", "прив", "мир"]],
            [(1, 0.5), (0, 0.4444444444444444), (2, 0.0)]
        ],
        
        # 3. Пустой запрос (должен вернуть пустой список или все с 0.0)
        [
            ["", ["привет", "мир", "пока"]],
            [(0, 0.0), (1, 0.0), (2, 0.0)]
        ],
        
        # 4. Один вариант (всегда индекс 0, оценка = сходство)
        [
            ["привет", ["привет"]],
            [(0, 1.0)]
        ],
        
        # 5. Много вариантов с разной похожестью
        [
            ["программирование", ["программист", "прога", "компилятор", "код"]],
            [(0, 0.4375), (1, 0.13333333333333333), (2, 0.0), (3, 0.0)]
        ]
    ]
    results = []

    completed = 0
    all = len(test)
    for i, answer in test:
        result = _trigram_search(*i)
        #print(result)
        results.append([result == answer, result, answer])
        if result == answer:
            completed += 1
        #print(f"{"ok:" if result == answer else " e:"} {result} {answer}")

    results.append((completed, all))

    return results

if __name__ == "__main__":
    main()
