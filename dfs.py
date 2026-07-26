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


if __name__ == "__main__":
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
    dfs(graph)
    dfs_it(graph, start)
