import uuid
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from config import *

class Node:
    """
    Клас вузла для побудови структури дерева.
    """
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.color = "#EEEEEE"  # Світло-сірий за замовчуванням
        self.id = str(uuid.uuid4())

def build_tree(data, index=0):
    """
    Будує зв'язне дерево з масиву (купи).
    """
    if index >= len(data):
        return None
    node = Node(data[index])
    node.left = build_tree(data, 2 * index + 1)
    node.right = build_tree(data, 2 * index + 2)
    return node

def generate_hex_gradient(count, base_rgb):
    """
    Генерує HEX-кольори від темного до світлого.
    """
    colors = []
    r_base, g_base, b_base = base_rgb
    for i in range(count):
        factor = i / max(1, count - 1)
        r = int(r_base + (235 - r_base) * factor)
        g = int(g_base + (235 - g_base) * factor)
        b = int(b_base + (235 - b_base) * factor)
        colors.append(f"#{r:02X}{g:02X}{b:02X}")
    return colors

def get_bfs_order(root):
    """Обхід у ширину (BFS) через чергу."""
    if not root: return []
    order, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left: queue.append(node.left)
        if node.right: queue.append(node.right)
    return order

def get_dfs_order(root):
    """Обхід у глибину (DFS) через стек."""
    if not root: return []
    order, stack, visited = [], [root], set()
    while stack:
        node = stack.pop()
        if node.id not in visited:
            visited.add(node.id)
            order.append(node)
            if node.right: stack.append(node.right)
            if node.left: stack.append(node.left)
    return order

def populate_graph(graph, node, pos, x=0, y=0, layer=1):
    """Заповнює граф та розраховує позиції для візуалізації."""
    if node is not None:
        graph.add_node(node.id, label=node.val)
        pos[node.id] = (x, y)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            populate_graph(graph, node.left, pos, x=x - 1/2**layer, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            populate_graph(graph, node.right, pos, x=x + 1/2**layer, y=y - 1, layer=layer + 1)

def animate_traversal(root, traversal_type="DFS"):
    """
    Створює анімовану візуалізацію обходу дерева.
    """
    if traversal_type == "DFS":
        order = get_dfs_order(root)
        base_rgb = DFS_BASE_RGB
        title = "Анімація обходу в глибину (DFS)"
    else:
        order = get_bfs_order(root)
        base_rgb = BFS_BASE_RGB
        title = "Анімація обходу в ширину (BFS)"

    gradient = generate_hex_gradient(len(order), base_rgb)
    
    # Створюємо статичний граф для структури
    G = nx.DiGraph()
    pos = {root.id: (0, 0)}
    populate_graph(G, root, pos)
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    node_labels = {node_id: G.nodes[node_id]['label'] for node_id in G.nodes}
    
    # Початковий стан: всі вузли сірі
    current_colors = {node.id: "#EEEEEE" for node in order}

    def update(frame):
        ax.clear()
        ax.set_title(f"{title} | Крок {frame + 1}")
        
        # Оновлюємо колір поточного вузла в анімації
        node_to_color = order[frame]
        current_colors[node_to_color.id] = gradient[frame]
        
        colors_list = [current_colors[node_id] for node_id in G.nodes]
        
        nx.draw(G, pos=pos, ax=ax, labels=node_labels, arrows=False, 
                node_size=NODE_SIZE, node_color=colors_list, 
                font_weight='bold', edgecolors='black', linewidths=1.5)

    ani = animation.FuncAnimation(fig, update, frames=len(order), repeat=False, interval=800)
    plt.show()

if __name__ == "__main__":
    # Будуємо дерево один раз
    root_node = build_tree(TREE_DATA)
    
    print("Запуск анімації DFS...")
    animate_traversal(root_node, "DFS")
    
    # Скидаємо кольори для наступної анімації
    root_node = build_tree(TREE_DATA)
    print("Запуск анімації BFS...")
    animate_traversal(root_node, "BFS")