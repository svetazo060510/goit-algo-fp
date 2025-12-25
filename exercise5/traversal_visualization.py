import uuid
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from config import *

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.color = "#EEEEEE" # Світло-сірий колір за замовчуванням для видимості
        self.id = str(uuid.uuid4())

def generate_colors(count, base_rgb):
    """
    Генерує список кольорів у форматі HEX від темного до світлого.
    """
    colors = []
    r_base, g_base, b_base = base_rgb
    
    for i in range(count):
        # Розрахунок освітлення: обмежимо максимум до 240, щоб колір не ставав чисто білим
        factor = i / max(1, count - 1)
        r = int(r_base + (240 - r_base) * factor)
        g = int(g_base + (240 - g_base) * factor)
        b = int(b_base + (240 - b_base) * factor)
        
        # Перетворення в 16-ву систему (HEX)
        hex_color = f"#{r:02X}{g:02X}{b:02X}"
        colors.append(hex_color)
    
    return colors

def build_tree(data, index=0):
    """Побудова дерева з масиву (аналогічно Завданню 4)."""
    if index >= len(data):
        return None
    node = Node(data[index])
    node.left = build_tree(data, 2 * index + 1)
    node.right = build_tree(data, 2 * index + 2)
    return node

def get_bfs_order(root):
    """Обхід у ширину (BFS) з використанням ЧЕРГИ."""
    if not root:
        return []
    
    order = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
            
    return order

def get_dfs_order(root):
    """Обхід у глибину (DFS) з використанням СТЕКА."""
    if not root:
        return []
    
    order = []
    stack = [root]
    visited = set()
    
    while stack:
        node = stack.pop()
        if node.id not in visited:
            visited.add(node.id)
            order.append(node)
            
            # Додаємо спочатку правий, потім лівий, щоб лівий обробився першим (LIFO)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
                
    return order

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """Додавання ребер та позицій (як у Завданні 4)."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        pos[node.id] = (x, y)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            add_edges(graph, node.left, pos, x=x - 1/2**layer, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            add_edges(graph, node.right, pos, x=x + 1/2**layer, y=y - 1, layer=layer + 1)
    return graph

def draw_traversal(root, order, base_rgb, title):
    """Візуалізація дерева з розфарбованими вузлами згідно з черговістю."""
    # Призначаємо кольори згідно з порядком обходу
    colors_hex = generate_colors(len(order), base_rgb)
    for i, node in enumerate(order):
        node.color = colors_hex[i]
        
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(tree, root, pos)
    
    # Отримуємо кольори та мітки для малювання
    node_colors = [tree.nodes[n]['color'] for n in tree.nodes]
    node_labels = {n: tree.nodes[n]['label'] for n in tree.nodes}
    
    plt.figure(figsize=(10, 7))
    # Додано edgecolors='black' та linewidths=1 для чіткого відображення меж вузлів
    nx.draw(tree, pos=pos, labels=node_labels, arrows=False, 
            node_size=NODE_SIZE, node_color=node_colors, font_weight='bold',
            edgecolors='black', linewidths=1)
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    # 1. Створення дерева
    tree_root = build_tree(TREE_DATA)
    
    # 2. Візуалізація DFS (Глибина)
    print("Виконання обходу в глибину (DFS)...")
    dfs_order = get_dfs_order(tree_root)
    draw_traversal(tree_root, dfs_order, DFS_BASE_RGB, "Візуалізація DFS (від темного до світлого)")
    
    # 3. Візуалізація BFS (Ширина)
    print("Виконання обходу в ширину (BFS)...")
    bfs_order = get_bfs_order(tree_root)
    draw_traversal(tree_root, bfs_order, BFS_BASE_RGB, "Візуалізація BFS (від темного до світлого)")