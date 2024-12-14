from collections import deque

def dinic_algorithm(graph, source, sink):
    """
    Реализация алгоритма Диница для вычисления максимального потока.
    graph: Граф в виде словаря, где ключи - узлы, значения - словари соседей и их пропускной способности.
    source: Исток (начальная вершина потока).
    sink: Сток (конечная вершина потока).
    """
    def bfs_level_graph():
        """
        Построение уровневого графа с использованием BFS.
        Возвращает уровни вершин или -1, если сток недостижим.
        """
        levels = {node: -1 for node in graph}
        levels[source] = 0
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            for neighbor, capacity in graph[current].items():
                if levels[neighbor] == -1 and capacity > 0:  # Не посещен и имеет остаточную пропускную способность
                    levels[neighbor] = levels[current] + 1
                    queue.append(neighbor)
        return levels

    def dfs_blocking_flow(current, flow):
        """
        Поиск блокирующего потока с использованием DFS.
        current: Текущая вершина.
        flow: Остаточный поток.
        """
        if current == sink:
            return flow
        for neighbor in list(graph[current].keys()):
            if levels[neighbor] == levels[current] + 1 and graph[current][neighbor] > 0:
                min_flow = min(flow, graph[current][neighbor])
                result = dfs_blocking_flow(neighbor, min_flow)
                if result > 0:
                    graph[current][neighbor] -= result
                    graph[neighbor][current] += result
                    return result
        return 0

    max_flow = 0
    while True:
        # Шаг 1: Построение уровневого графа
        levels = bfs_level_graph()
        if levels[sink] == -1:  # Если сток недостижим, то завершить
            break
        while True:
            # Шаг 2: Поиск блокирующего потока
            flow = dfs_blocking_flow(source, float('inf'))
            if flow == 0:
                break
            max_flow += flow
    return max_flow

# Функция для добавления ребра в граф
def add_edge(graph, u, v, capacity):
    """Добавить ребро с пропускной способностью в граф."""
    if u not in graph:
        graph[u] = {}
    if v not in graph:
        graph[v] = {}
    graph[u][v] = capacity
    graph[v][u] = 0  # обратное ребро с начальной пропускной способностью 0

# Пример графа
graph = {}
add_edge(graph, 'A', 'B', 10)
add_edge(graph, 'A', 'C', 5)
add_edge(graph, 'B', 'D', 15)
add_edge(graph, 'C', 'D', 10)

# Вычисление максимального потока
source = 'A'
sink = 'D'
max_flow = dinic_algorithm(graph, source, sink)
print(f"Максимальный поток: {max_flow}")
