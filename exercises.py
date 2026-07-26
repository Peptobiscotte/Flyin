def find_path(graph, start, end) -> bool:
    visited = set()

    def explore(node) -> bool:
        visited.add(node)
        if node == end:
            return True
        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                if explore(neighbour):
                    return True
        return False

    return explore(start)


def is_connected(graph, start) -> bool:
    visited = set()

    def explore(node) -> bool:
        visited.add(node)

        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                explore(neighbour)
        return False

    explore(start)
    return len(visited) == len(graph)


def nb_components(graph) -> int:
    visited = set()
    n = 0

    def explore(node):
        visited.add(node)

        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                explore(neighbour)

    for node in graph:
        if node not in visited:
            n += 1
            explore(node)

    return n


if __name__ == "__main__":
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "E",],
        "D": ["B"],
        "E": ["C"],
        "F": ["G"],
        "G": ["F"]
    }
    start = "A"
    end = "E"
    print(nb_components(graph))
