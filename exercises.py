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


def number_of_islands(grid: list[list[str]]) -> int:
    visited = set()
    isles = 0
    h = len(grid)
    w = len(grid[0])
    
    
    def explore(row, col):
        visited.add((row, col))
        print(visited)
        if row + 1 < h and grid[row +1][col] == "1" and (row + 1, col) not in visited:
            explore(row + 1, col)
        if row - 1 >= 0 and grid[row -1][col] == "1" and (row - 1, col) not in visited:
            explore(row - 1, col)
        if col + 1 < w and grid[row][col + 1] == "1" and (row, col +1) not in visited:
            explore(row, col + 1)
        if col - 1 >= 0 and grid[row][col - 1] == "1" and (row, col - 1) not in visited:
            explore(row, col - 1)
            
    
    for row in range(h):
        for col in range(w):
            if (row, col) not in visited and grid[row][col] == "1":
                isles += 1
                explore(row, col)
    
    return isles


def flood_fill(
    image: list[list[int]],
    sr: int,
    sc: int,
    new_color: int
) -> list[list[int]]:
    visited = set()
    h = len(image)
    w = len(image[0])
    start_color = image[sr][sc]
    if not image or not sr or not sc or not start_color:
        return []
    if new_color == image[sr][sc]:
        return image
    
    def explore(row, col):
        visited.add((row, col))
        image[row][col] = new_color
        if row + 1 < h and image[row +1][col] == start_color and (row + 1, col) not in visited:
            explore(row + 1, col)
        if row - 1 >= 0 and image[row -1][col] == start_color and (row - 1, col) not in visited:
            explore(row - 1, col)
        if col + 1 < w and image[row][col + 1] == start_color and (row, col +1) not in visited:
            explore(row, col + 1)
        if col - 1 >= 0 and image[row][col - 1] == start_color and (row, col - 1) not in visited:
            explore(row, col - 1)
            
    explore(sr, sc)
    
    return image
    
def cycle(graph):
    visited = set()
    
    def has_cycle(node, parent):
        visited.add(node)
        
        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                if has_cycle(neighbour, node):
                    return True
            elif neighbour != parent:
                return True
        
        
        return False
        
    for node in graph:
        if node not in visited:
            if has_cycle(node, None):
                return True
    return False
    


if __name__ == "__main__":
    isles = [
            ["1","1","0","0"],
            ["1","0","0","1"],
            ["0","0","1","1"],
            ["0","0","0","0"]
        ]
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "E",],
        "D": ["B"],
        "E": ["C"],
        "F": ["G"],
        "G": ["F"]
    }
    graph_cycle = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"]
    }
    image = [
        [1,1,1],
        [1,1,0],
        [1,0,1]
    ]

    sr = 1
    sc = 1

    new_color = 2
    start = "A"
    end = "E"
    print(cycle(graph_cycle))
