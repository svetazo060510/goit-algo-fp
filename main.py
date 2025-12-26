import os
import subprocess
import sys
from pathlib import Path

# Спроба імпорту colorama для запобігання падінню програми
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_INSTALLED = True
except ImportError:
    COLORAMA_INSTALLED = False

def clear_screen():
    """Очищення екрана термінала."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color_code=""):
    """Друкує текст кольором, якщо colorama доступна."""
    if COLORAMA_INSTALLED:
        print(f"{color_code}{text}")
    else:
        print(text)

def run_script(script_path):
    """
    Запуск скрипту через окремий процес Python.
    Змінює робочий каталог (cwd) на папку скрипту для коректних імпортів.
    """
    path = Path(script_path)
    if not path.exists():
        print_colored(f"\nПомилка: Файл {script_path} не знайдено.", Fore.RED if COLORAMA_INSTALLED else "")
        input("\nНатисніть Enter для продовження...")
        return

    try:
        header_color = Fore.CYAN if COLORAMA_INSTALLED else ""
        print_colored(f"\nЗапуск {script_path}...\n" + "-"*30, header_color)
        
        # ВАЖЛИВО: Встановлюємо cwd (Current Working Directory) на папку, де лежить скрипт.
        # Це дозволяє скриптам у підпапках імпортувати свої конфігураційні файли.
        subprocess.run(
            [sys.executable, path.name], 
            cwd=path.parent, 
            check=True
        )
        
        success_color = Fore.GREEN if COLORAMA_INSTALLED else ""
        print_colored("-"*30 + f"\nВиконання завершено.", success_color)
    except subprocess.CalledProcessError:
        print_colored(f"\nПроцес завершився з помилкою.", Fore.RED if COLORAMA_INSTALLED else "")
    except Exception as e:
        print_colored(f"\nНепередбачена помилка: {e}", Fore.RED if COLORAMA_INSTALLED else "")
    
    yellow_color = Fore.YELLOW if COLORAMA_INSTALLED else ""
    input(f"\nНатисніть Enter, щоб повернутися до меню...")

def main_menu():
    """Головне меню проєкту."""
    if not COLORAMA_INSTALLED:
        print("ПОПЕРЕДЖЕННЯ: Бібліотека 'colorama' не знайдена. Кольори вимкнено.")
        print("Виконайте 'pip install colorama' для кращого вигляду.\n")

    tasks = {
        "1": ("Алгоритми однозв'язного списку", "exercise1/linked_list_algorithms.py"),
        "2": ("Фрактал 'Дерево Піфагора'", "exercise2/pythagoras_tree.py"),
        "3": ("Алгоритм Дейкстри (Транспортна мережа)", "exercise3/dijkstra_algorithm.py"),
        "4": ("Візуалізація бінарної купи", "exercise4/heap_visualization.py"),
        "5": ("Візуалізація обходів дерева (DFS/BFS)", "exercise5/traversal_visualization.py"),
        "6": ("Оптимізація вибору страв (Greedy/DP)", "exercise6/food_optimization.py"),
        "7": ("Метод Монте-Карло (Кидання кубиків)", "exercise7/dice_simulation.py")
    }

    while True:
        clear_screen()
        mag_color = Fore.MAGENTA + Style.BRIGHT if COLORAMA_INSTALLED else ""
        cyan_color = Fore.CYAN if COLORAMA_INSTALLED else ""
        red_color = Fore.RED if COLORAMA_INSTALLED else ""
        
        print(f"{mag_color}==========================================")
        print(f"{mag_color}   ФІНАЛЬНИЙ ПРОЄКТ: АЛГОРИТМИ ТА СТРУКТУРИ")
        print(f"{mag_color}==========================================")
        
        for key, (name, _) in tasks.items():
            print(f"{cyan_color}{key}. {Fore.WHITE if COLORAMA_INSTALLED else ''}{name}")
            
        print(f"{mag_color}------------------------------------------")
        print(f"{red_color}0. Вихід")
        print(f"{mag_color}==========================================")
        
        yellow_color = Fore.YELLOW if COLORAMA_INSTALLED else ""
        choice = input(f"{yellow_color}Оберіть номер завдання для запуску: ").strip()
        
        if choice == "0":
            print_colored("Дякуємо за використання! До зустрічі.", Fore.GREEN if COLORAMA_INSTALLED else "")
            break
        elif choice in tasks:
            _, path = tasks[choice]
            run_script(path)
        else:
            print_colored("Неправильний вибір. Спробуйте ще раз.", Fore.RED if COLORAMA_INSTALLED else "")
            input("\nНатисніть Enter для продовження...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print_colored("\n\nПрограму перервано користувачем.", Fore.YELLOW if COLORAMA_INSTALLED else "")
        sys.exit(0)