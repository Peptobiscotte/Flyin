from models import Hub, Graph, Connection


class MapParser:
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.hubs: dict[str, Hub] = {}
        self.start: Hub | None = None
        self.end: Hub | None = None
        self.connections: list[Connection] = []

    def parse(self, filename: str) -> Graph:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue

                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if key == "nb_drones" and value.isdigit():
                    self.nb_drones = int(value)

                if key in ("start_hub", "end_hub", "hub"):
                    hub = self._parse_hub(value, key)
                    self.hubs[hub.name] = hub

                    if key == "start_hub":
                        if self.start is not None:
                            raise ValueError("Multiple start hubs")
                        self.start = hub
                    elif key == "end_hub":
                        if self.end is not None:
                            raise ValueError("Multiple end hubs")
                        self.end = hub

                if key == "connection":
                    self.connections.append(self._parse_connect(value))

                if key not in (
                    "start_hub",
                    "end_hub",
                    "hub",
                    "connection",
                    "nb_drones"
                ):
                    raise ValueError("Unknown key in config")

            if self.start is None:
                raise ValueError("Missing start hub")

            if self.end is None:
                raise ValueError("Missing end hub")

            graph = Graph(
                self.nb_drones,
                self.hubs,
                self.connections,
                self.start,
                self.end
                )
            self._validate_parsing(graph)

        return graph

    def _parse_hub(self, value: str, key: str) -> Hub:
        value_start: list[str] = value.split(" ")
        max_drones_defined = False
        color_defined = False
        zone_defined = False
        if len(value_start) < 3:
            raise ValueError("Not enough values in hub config")

        name = value_start[0]
        if name.isdigit():
            raise ValueError("Hub name cannot be a number")
        if not value_start[1].isdigit() or not value_start[2].isdigit():
            raise ValueError("X and Y values must be integers")
        x = int(value_start[1])
        y = int(value_start[2])
        color_start: str | None = None
        hub_type: str = "normal"
        max_drones: int = 1
        if len(value_start) > 3:
            for i in range(3, len(value_start)):
                bracket_rem = value_start[i].strip("[]")
                option_list = bracket_rem.split(" ")
                for option in option_list:
                    option_split = option.split("=", 1)
                    if len(option_split) != 2 or not option_split[1]:
                        raise ValueError(
                            "Incorrect syntax in optional argument"
                            )
                    if option_split[0] not in ("color", "zone", "max_drones"):
                        raise ValueError("Unknown metadata")
                    if option_split[0] == "color":
                        if color_defined:
                            raise ValueError("Optional parameter duplication")
                        color_defined = True
                        color_start = option_split[1]
                    if option_split[0] == "zone":
                        if zone_defined:
                            raise ValueError("Optional parameter duplication")
                        zone_defined = True
                        hub_type = option_split[1]
                    if option_split[0] == "max_drones":
                        if max_drones_defined:
                            raise ValueError("Optional parameter duplication")
                        max_drones_defined = True
                        if not option_split[1].isdigit():
                            raise ValueError("max_drones must be a number")
                        max_drones = int(option_split[1])
                    if key in (
                            "start_hub", "end_hub"
                            ) and not max_drones_defined:
                        max_drones = self.nb_drones
            hub = Hub(
                name,
                x,
                y,
                hub_type,
                color_start,
                max_drones)
        self._validate_hub(hub, key)
        return hub

    def _validate_hub(self, hub: Hub, key: str) -> None:

        for sethub in self.hubs:
            if hub.name == sethub:
                raise ValueError("Hub name duplications")

        if hub.hub_type not in ("normal", "blocked", "restricted", "priority"):
            raise ValueError("Unknown zone value")

        if key == "start_hub":
            if hub.hub_type == "blocked":
                raise ValueError("Start hub cannot be blocked")
            if hub.max_drones < self.nb_drones:
                raise ValueError("Start hub must hold every drone")

        if key == "end_hub":
            if hub.hub_type == "blocked":
                raise ValueError("End hub cannot be blocked")
            if hub.max_drones < self.nb_drones:
                raise ValueError("End hub must hold every drone")

        if key == "hub":
            if hub.max_drones < 0:
                raise ValueError("Drone occupancy can't be negative")

    def _parse_connect(self, value: str) -> Connection:
        value_start: list[str] = value.split(" ")
        max_link: int = 1

        if not value_start:
            raise ValueError("Missing edge definition")
        if len(value_start) > 2:
            raise ValueError("Too many parameters to connection")
        edge = value_start[0].split("-", 1)
        if len(edge) != 2 or not edge[0] or not edge[1]:
            raise ValueError("Connection must use hub1-hub2 syntax")
        hub1_name = edge[0]
        hub2_name = edge[1]
        if len(value_start) == 2:
            rem_bracket = value_start[1].strip("[]")
            option = rem_bracket.split("=", 1)
            if len(option) != 2 or not option[1]:
                raise ValueError("Incorrect connection option syntax")
            if option[0] != "max_link_capacity":
                raise ValueError(f"Unknown connection option: {option[0]}")
            if not option[1].isdigit():
                raise ValueError("Max capacity must be positive integer")
            if option[1].isdigit():
                max_link = int(option[1])
        hub1 = self.hubs.get(hub1_name)
        hub2 = self.hubs.get(hub2_name)

        if hub1 is None or hub2 is None:
            raise ValueError("Incorrect hub name in connection")

        connection = Connection(hub1, hub2, max_link)
        self._validate_connect(connection)
        return connection

    def _validate_connect(self, connection: Connection) -> None:
        if connection.max_capacity <= 0:
            raise ValueError("Capacity must be positive integer")
        if connection.hub1 is connection.hub2:
            raise ValueError("A hub cannot connect to itself")

    def _validate_parsing(self, graph: Graph) -> None:
        if graph.nb_drones <= 0:
            raise ValueError("Number of drones must be a positive integer")

        if not graph.hubs:
            raise ValueError("Graph must contain at least one hub")

        if graph.start.name not in graph.hubs:
            raise ValueError("Start hub is missing from graph hubs")

        if graph.end.name not in graph.hubs:
            raise ValueError("End hub is missing from graph hubs")

        if not graph.connections:
            raise ValueError("Graph must contain at least one connection")

        seen_connections: set[frozenset[str]] = set()

        for connection in graph.connections:
            edge = frozenset((
                connection.hub1.name,
                connection.hub2.name,
            ))

            if edge in seen_connections:
                raise ValueError(
                    "Duplicate connection: "
                    f"{connection.hub1.name}-{connection.hub2.name}"
                )
            seen_connections.add(edge)
