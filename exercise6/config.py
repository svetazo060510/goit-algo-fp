"""
Конфігураційний файл для Завдання 6.
Містить вхідні дані про страви та налаштування бюджету.
"""

# Дані про їжу: Назва -> {вартість, калорійність}
ITEMS = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}

# Бюджет за замовчуванням для тестування
DEFAULT_BUDGET = 100