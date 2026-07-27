def dfs(graph: dict[str, list[str]]) -> None:
    visited = []

    def explore(node: str) -> None:
        visited.append(node)

        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                explore(neighbour)

    for node in graph:
        if node not in visited:
            explore(node)
    print(visited)


def dfs_it(graph: dict[str, list[str]], start: str) -> None:
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbour in reversed(graph[node]):
            if neighbour not in visited:
                stack.append(neighbour)
    print(order)


def bfs(graph: dict[str, list[str]], start: str, end: str) -> list[str]:
    visited = {start}
    queue = [start]
    parent = {}
    
    while queue:
        node = queue.pop(0)
        if node == end:
            break

        for neighbours in graph[node]:
            if neighbours not in visited:
                visited.add(neighbours)
                queue.append(neighbours)
                parent[neighbours] = node
    
    if end not in visited:
        return []
    
    path = []
    current = end
    
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    print(path)
    return path
    

def dijkstra(graph, start, end) -> list[str]:
    if start not in graph or end not in graph:
        return []
    visited = set()
    parent = {}
    distances = {
    node: float("inf")
    for node in graph
    }
    distances[start] = 0
    
    def find_lowcost() -> str | None:
        
        min = float("inf")
        key_min = None
        for key, value in distances.items():
            if value < min and key not in visited:
                key_min = key
                min = value
        return key_min
            
    while True:
        node = find_lowcost()

        if node is None:
            break

        if node == end:
            break
        for neighbour, cost in graph.get(node, []):
            new_cost = distances[node] + cost
            if new_cost < distances[neighbour]:
                distances[neighbour] = new_cost
                parent[neighbour] = node

        visited.add(node)

    if distances[end] == float("inf"):
        return []    
    path = []
    current = end
        
    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()
    print(path)
    print(distances[end])
    return path


if __name__ == "__main__":
    graph_cost = {
        "A": [("B", 100), ("C", 1)],
        "B": [("A", 100), ("D", 1)],
        "C": [("A", 1), ("D", 1)],
        "D": [("B", 1), ("C", 1)],
    }    
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "E", "F"],
        "D": ["B", "G"],
        "E": ["C", "G"],
        "F": ["C"],
        "G": ["D", "E"],
    }
    start = "A"
    # dfs(graph)
    # dfs_it(graph, start)
    # bfs(graph, start, "E")
    dijkstra(graph_cost, start, "D")
    
