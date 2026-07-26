class Hub:
    """Represent a zone in the graph."""

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        hub_type: str = "normal",
        color: str | None = None,
        max_drones: int = 1,
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.hub_type = hub_type
        self.color = color
        self.max_drones = max_drones


class Connection:
    """Represent a bidirectional connection between two hubs."""

    def __init__(
        self,
        hub1: Hub,
        hub2: Hub,
        max_capacity: int = 1,
    ) -> None:
        self.hub1 = hub1
        self.hub2 = hub2
        self.max_capacity = max_capacity


class Graph:
    """Represent the complete drone network."""

    def __init__(
        self,
        nb_drones: int,
        hubs: dict[str, Hub],
        connections: list[Connection],
        start: Hub,
        end: Hub
    ) -> None:
        self.nb_drones = nb_drones
        self.hubs = hubs
        self.connections = connections
        self.start = start
        self.end = end
