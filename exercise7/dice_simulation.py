import random
import matplotlib.pyplot as plt
from collections import Counter
from config import NUM_ROLLS, ANALYTICAL_PROBS
from styles import *

def simulate_dice_rolls(num_rolls):
    """
    Імітує кидання двох кубиків задану кількість разів.
    Повертає словник з ймовірностями для кожної суми.
    """
    sums_counts = Counter()

    for _ in range(num_rolls):
        # Кидаємо два кубики (значення від 1 до 6 кожен)
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        sums_counts[die1 + die2] += 1

    # Обчислюємо ймовірність у відсотках
    probabilities = {s: (count / num_rolls) * 100 for s, count in sums_counts.items()}
    return probabilities

def plot_comparison(mc_probs, analytical_probs):
    """
    Будує графік порівняння результатів Монте-Карло та аналітичних даних.
    """
    sums = sorted(analytical_probs.keys())
    mc_values = [mc_probs.get(s, 0) for s in sums]
    analytical_values = [analytical_probs[s] for s in sums]

    plt.figure(figsize=(12, 6))
    
    # Побудова стовпчиків
    bar_width = 0.35
    index = range(len(sums))

    plt.bar(index, mc_values, bar_width, label='Монте-Карло', color='skyblue', alpha=0.8)
    plt.bar([i + bar_width for i in index], analytical_values, bar_width, 
            label='Аналітичні', color='orange', alpha=0.6)

    plt.xlabel('Сума чисел на кубиках')
    plt.ylabel('Ймовірність (%)')
    plt.title(f'Порівняння ймовірностей сум (N={NUM_ROLLS})')
    plt.xticks([i + bar_width / 2 for i in index], sums)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

def print_results_table(mc_probs, analytical_probs):
    """Виводить порівняльну кольорову таблицю в консоль."""
    header_text = f"\n{STYLE_BRIGHT}--- Результати симуляції (Кидків: {NUM_ROLLS}) ---"
    print(COLOR_HEADER + header_text)
    
    table_header = f"{'Сума':<6} | {'Монте-Карло (%)':<18} | {'Аналітична (%)':<18} | {'Різниця'}"
    print(COLOR_HEADER + table_header)
    print(COLOR_DEFAULT + "-" * 65)
    
    for s in sorted(analytical_probs.keys()):
        mc = mc_probs.get(s, 0)
        an = analytical_probs[s]
        diff = abs(mc - an)
        
        # Format the row with specific colors for each column
        row = (f"{COLOR_DEFAULT}{s:<6} | "
               f"{COLOR_MC}{mc:<18.2f} | "
               f"{COLOR_ANALYTICAL}{an:<18.2f} | "
               f"{COLOR_DIFF}{diff:.4f}")
        print(row)

    print(COLOR_DEFAULT + "-" * 65)
    print(f"{COLOR_SUCCESS}Симуляція завершена успішно.\n")

if __name__ == "__main__":
    print(f"{COLOR_HEADER}Запуск симуляції Монте-Карло для {NUM_ROLLS} кидків...")
    
    # 1. Запуск симуляції
    mc_results = simulate_dice_rolls(NUM_ROLLS)
    
    # 2. Вивід таблиці зі стилями
    print_results_table(mc_results, ANALYTICAL_PROBS)
    
    # 3. Візуалізація (Matplotlib)
    plot_comparison(mc_results, ANALYTICAL_PROBS)