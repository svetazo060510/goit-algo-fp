import sys
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from config import *
from styles import *

def dijkstra_shortest_path(graph, start_node):
    """
    Реалізує алгоритм Дейкстри для знаходження найкоротшого шляху 
    від стартового вузла до всіх інших вузлів у зваженому графі.
    """
    # Ініціалізація відстаней: нескінченність для всіх, 0 для старту
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    
    # Словник для збереження шляхів
    paths = {node: [] for node in graph.nodes}
    paths[start_node] = [start_node]

    # Черга з пріоритетом (мінімальна купа)
    priority_queue = [(0, start_node)]

    while priority_queue:
        (current_distance, current_node) = heapq.heappop(priority_queue)

        # Якщо знайдена відстань уже більша за збережену — ігноруємо
        if current_distance > distances[current_node]:
            continue

        for neighbor, attributes in graph[current_node].items():
            weight = attributes.get('weight', 1) 
            distance = current_distance + weight

            # Релаксація ребра
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                paths[neighbor] = paths[current_node] + [neighbor]
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, paths

def run_transport_analysis():
    """
    Виконує аналіз транспортної мережі та візуалізує результат.
    Використовує стилі з styles.py для професійного виводу.
    """
    # 1. Побудова графа на основі TRANSPORT_NETWORK з конфігурації
    G = nx.Graph()
    G.add_weighted_edges_from(TRANSPORT_NETWORK)
    
    # 2. Обчислення найкоротших шляхів
    distances, shortest_paths = dijkstra_shortest_path(G, START_NODE)
    
    # 3. ВИВІД У ТЕРМІНАЛ
    # Використовуємо кольори та стилі з styles.py
    header = f"\n{STYLE_BRIGHT}--- Аналіз міських маршрутів (Старт: {START_NODE}) ---"
    print(COLOR_HEADER + header, flush=True)

    print(f"{COLOR_HEADER}{'Пункт призначення':<22} | {'Час (хв)':<10} | {'Найкоротший маршрут'}", flush=True)
    print(COLOR_DEFAULT + "-" * 75, flush=True)
    
    # Визначаємо межі для підсвічування
    valid_dists = [d for n, d in distances.items() if n != START_NODE and d != float('inf')]
    min_d = min(valid_dists) if valid_dists else 0
    max_d = max(valid_dists) if valid_dists else 0

    for node in sorted(G.nodes):
        if node == START_NODE:
            continue
            
        path_str = ' -> '.join(shortest_paths[node])
        dist = distances[node]
        
        line = f"{node:<22} | {dist:<10} | {path_str}"
        
        # Застосування колірної схеми на основі результатів
        if dist == min_d:
            print(COLOR_SHORTEST + line + LABEL_SHORTEST, flush=True)
        elif dist == max_d:
            print(COLOR_LONGEST + line + LABEL_LONGEST, flush=True)
        else:
            print(COLOR_DEFAULT + line, flush=True)

    print(COLOR_DEFAULT + "-" * 75, flush=True)
    print(f"\n{COLOR_INFO}ГРАФІК ВІДКРИВАЄТЬСЯ... (Закрийте вікно графіка, щоб завершити програму)", flush=True)
    sys.stdout.flush()

    # 4. ВІЗУАЛІЗАЦІЯ
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=LAYOUT_SEED)
    
    nx.draw(G, pos, 
            with_labels=True, 
            node_color=NODE_COLOR, 
            node_size=NODE_SIZE, 
            font_size=FONT_SIZE, 
            font_weight='bold')
            
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color=EDGE_LABEL_COLOR)
    
    plt.title(f"Схема маршрутів міста (Старт: {START_NODE})")
    
    # Відображення вікна (текст у терміналі вже доступний)
    plt.show()
    
    print(f"\n{COLOR_SHORTEST}Програму завершено успішно.")

if __name__ == "__main__":
    run_transport_analysis()