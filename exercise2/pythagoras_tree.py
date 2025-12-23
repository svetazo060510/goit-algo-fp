import turtle
import math
from config import *

def get_color_intensity(level, max_level):
    """
    Обчислює колір для поточного рівня рекурсії на основі конфігурації.
    Перехід від коричневого (стовбур) до світло-зеленого (листя).
    """
    if level > max_level // 2:
        return TRUNK_COLOR
    
    # Розрахунок градієнта для листя
    intensity = (max_level // 2 - level) / (max_level // 2)
    green_val = int(100 + 155 * intensity)
    red_val = int(LEAF_COLOR_START[0] * (1 - intensity))
    return (red_val, green_val, 0)

def binary_tree_fractal(t, branch_length, level, max_level, angle):
    """
    Рекурсивна функція для малювання фрактального дерева.
    """
    if level == 0:
        return

    # 1. Налаштування стилю лінії згідно з конфігурацією
    t.pencolor(get_color_intensity(level, max_level))
    t.pensize(max(1, level * PEN_SIZE_FACTOR))
    
    # 2. Малювання поточної гілки
    t.forward(branch_length)
    
    # Зберігаємо позицію та кут після руху вперед
    pos_after_move = t.pos()
    heading_after_move = t.heading()

    # 3. Рекурсивний виклик для ПРАВОЇ гілки
    t.right(angle)
    binary_tree_fractal(t, branch_length * REDUCTION_FACTOR, level - 1, max_level, angle)
    
    # Повернення до точки розгалуження
    t.penup()
    t.goto(pos_after_move)
    t.setheading(heading_after_move)
    t.pendown()
    
    # 4. Рекурсивний виклик для ЛІВОЇ гілки
    t.left(angle)
    binary_tree_fractal(t, branch_length * REDUCTION_FACTOR, level - 1, max_level, angle)
    
    # 5. Повернення до основи поточної гілки
    t.penup()
    t.goto(pos_after_move)
    t.setheading(heading_after_move)
    t.backward(branch_length)
    t.pendown()

def draw_pythagoras_tree():
    """
    Основна функція для налаштування середовища та запуску фрактала.
    """
    screen = turtle.Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.bgcolor(BG_COLOR)
    screen.title(WINDOW_TITLE)
    
    turtle.colormode(255) 
    
    recursion_level = screen.numinput(
        "Рівень рекурсії", 
        f"Введіть глибину дерева (рекомендовано {DEFAULT_LEVEL}-{MAX_LEVEL - 3}):", 
        default=DEFAULT_LEVEL, minval=MIN_LEVEL, maxval=MAX_LEVEL
    )
    
    if recursion_level is None:
        return

    recursion_level = int(recursion_level)

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    
    # Вимикаємо анімацію для миттєвого малювання (режим "професійної візуалізації")
    screen.tracer(0) 
    
    t.penup()
    t.goto(START_POS) 
    t.setheading(START_HEADING)
    t.pendown()
    
    print(f"Малювання дерева з рівнем рекурсії: {recursion_level}...")
    
    binary_tree_fractal(t, INITIAL_LENGTH, recursion_level, recursion_level, BRANCH_ANGLE)
    
    screen.update()
    print("Малювання завершено успішно.")
    screen.mainloop()

if __name__ == "__main__":
    draw_pythagoras_tree()