from config import ITEMS, DEFAULT_BUDGET
from styles import *

def greedy_algorithm(items, budget):
    """
    Жадібний алгоритм: вибирає страви, максимізуючи співвідношення калорій до вартості.
    """
    # Розраховуємо питому калорійність та сортуємо
    sorted_items = sorted(
        items.items(), 
        key=lambda x: x[1]['calories'] / x[1]['cost'], 
        reverse=True
    )

    chosen_items = []
    total_cost = 0
    total_calories = 0
    remaining_budget = budget

    for name, data in sorted_items:
        cost = data['cost']
        if remaining_budget >= cost:
            remaining_budget -= cost
            total_cost += cost
            total_calories += data['calories']
            chosen_items.append(name)

    return chosen_items, total_calories, total_cost

def dynamic_programming(items, budget):
    """
    Алгоритм динамічного програмування: знаходить оптимальний набір страв 
    для максимальної калорійності при заданому бюджеті.
    """
    names = list(items.keys())
    costs = [items[name]['cost'] for name in names]
    calories = [items[name]['calories'] for name in names]
    n = len(items)

    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(budget + 1):
            if costs[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - costs[i-1]] + calories[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    result_items = []
    w = budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            result_items.append(names[i-1])
            w -= costs[i-1]

    return result_items, dp[n][budget], budget - w

def print_result(title, items, calories, cost, color):
    """Допоміжна функція для кольорового виводу результатів."""
    print(f"\n{color}{STYLE_BRIGHT}[{title}]:")
    print(f"{color}  Набір: {items}")
    print(f"{color}  Калорії: {calories}")
    print(f"{color}  Вартість: {cost}")

if __name__ == "__main__":
    budget = DEFAULT_BUDGET
    
    print(f"{COLOR_HEADER}--- Аналіз вибору страв для бюджету: {budget} ---")
    
    # Виконання алгоритмів
    g_items, g_cal, g_cost = greedy_algorithm(ITEMS, budget)
    dp_items, dp_cal, dp_cost = dynamic_programming(ITEMS, budget)

    # Вивід результатів
    print_result("Жадібний алгоритм", g_items, g_cal, g_cost, COLOR_GREEDY)
    print_result("Динамічне програмування", dp_items, dp_cal, dp_cost, COLOR_DP)
    
    # Порівняння та фінальний висновок
    print(f"\n{COLOR_DEFAULT}" + "="*50)
    if dp_cal > g_cal:
        print(f"{COLOR_WINNER}ПЕРЕМОЖЕЦЬ: Динамічне програмування")
        print(f"{COLOR_INFO}Різниця: +{dp_cal - g_cal} калорій на користь оптимального рішення.")
    elif g_cal > dp_cal:
        # У цій задачі DP завжди >= Greedy
        print(f"{COLOR_WINNER}ПЕРЕМОЖЕЦЬ: Жадібний алгоритм")
    else:
        print(f"{COLOR_WINNER}РЕЗУЛЬТАТ: Обидва алгоритми знайшли однаково ефективний набір.")
    print(f"{COLOR_DEFAULT}" + "="*50)