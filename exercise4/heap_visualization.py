import uuid
import networkx as nx
import matplotlib.pyplot as plt
from config import *

class Node:
    """
    Клас вузла для побудови ієрархічної структури дерева.
    """
    def __init__(self, key, color=NODE_COLOR_DEFAULT):
        self.left = None
        self.right = None
        self.val = key
        self.color = color # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4()) # Унікальний ідентифікатор для кожного вузла

def build_tree_from_heap(heap, index=0):
    """
    Рекурсивно перетворює масив (купу) у зв'язну структуру об'єктів Node.
    Використовує формули: лівий син = 2i + 1, правий син = 2i + 2.
    """
    if index >= len(heap):
        return None

    # Створюємо поточний вузол
    node = Node(heap[index])
    
    # Рекурсивно будуємо ліве та праве піддерева
    node.left = build_tree_from_heap(heap, 2 * index + 1)
    node.right = build_tree_from_heap(heap, 2 * index + 2)
    
    return node

# Початкову функцію з завдання було оптимізовано з наступних причин:
# 1. Уніфіковане позиціонування: присвоєння координат pos[node.id] перенесено на початок 
#    функції для однаковій обробки всіх вузлів (включаючи корінь).
# 2. Видалення зайвих присвоєнь: оскільки об'єкти graph та pos є мутабельними і 
#    змінюються "на місці", збереження результату рекурсивного виклику у змінні (l, r) 
#    було видалено для спрощення коду.
# 3. Читабельність: код став більш "Pythonic" та легшим для підтримки.
def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """
    Рекурсивно додає вузли та ребра до графа NetworkX та визначає координати вузлів.
    """
    if node is not None:
        # Додаємо вузол до графа
        graph.add_node(node.id, color=node.color, label=node.val)
        pos[node.id] = (x, y)
        
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
            
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
            
    return graph

def draw_heap(heap_list):
    """
    Головна функція для перетворення масиву в дерево та його візуалізації.
    """
    # 1. Побудова дерева з купи
    root = build_tree_from_heap(heap_list)
    if not root:
        print("Помилка: Купа порожня.")
        return

    # 2. Створення графа NetworkX
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    tree = add_edges(tree, root, pos)

    # 3. Підготовка даних для відображення
    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    # 4. Візуалізація через Matplotlib
    plt.figure(figsize=FIGURE_SIZE)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, 
            node_size=NODE_SIZE, node_color=colors, 
            font_size=FONT_SIZE, font_color=FONT_COLOR, 
            edge_color=EDGE_COLOR)
    
    plt.title("Візуалізація структури Бінарної Купи")
    plt.show()

if __name__ == "__main__":
    print(f"Побудова візуалізації для купи: {TEST_HEAP_DATA}")
    draw_heap(TEST_HEAP_DATA)