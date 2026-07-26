from parsing import MapParser


def main() -> None:
    parse_object = MapParser()
    graph = parse_object.parse("maps/easy/01_linear_path.txt")
    print(graph.start.name)


if __name__ == "__main__":
    main()
