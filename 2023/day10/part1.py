class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return False

    def __str__(self):
        return f"({self.x}, {self.y})"


class Pipeline:
    def __init__(self, start_coordinate, next_coordinate):
        self.coordinates = [start_coordinate, next_coordinate]

    def addNode(self, coordinate):
        self.coordinates.append(coordinate)


def getAllAdjacentCoords(coord, max_x, max_y):
    coords = []

    coords.append(Coordinate(coord.x + 1, coord.y))
    coords.append(Coordinate(coord.x - 1, coord.y))
    coords.append(Coordinate(coord.x, coord.y - 1))
    coords.append(Coordinate(coord.x, coord.y + 1))

    return_coords = []

    for possible_coord in return_coords:
        if (
            possible_coord.x == -1
            or possible_coord.x > max_x
            or possible_coord.y == -1
            or possible_coord.y > max_y
        ):
            continue
        return_coords.append(coord)

    return coords


def getNextConnectionIfPossible(map, pipeline):
    connector_type = map[pipeline.coordinates[-1].y][pipeline.coordinates[-1].x]
    current_coord = pipeline.coordinates[-1]
    previous_coord = pipeline.coordinates[-2]

    previous_is_north = previous_coord.y < current_coord.y
    previous_is_south = previous_coord.y > current_coord.y
    previous_is_east = previous_coord.x > current_coord.x
    previous_is_west = previous_coord.x < current_coord.x

    southern_connectors = ["|", "F", "7"]
    northern_connectors = ["|", "J", "L"]
    eastern_connectors = ["F", "L", "-"]
    western_connectors = ["J", "7", "-"]

    north_coord = Coordinate(current_coord.x, current_coord.y - 1)
    east_coord = Coordinate(current_coord.x + 1, current_coord.y)
    south_coord = Coordinate(current_coord.x, current_coord.y + 1)
    west_coord = Coordinate(current_coord.x - 1, current_coord.y)

    if connector_type == "|":
        if previous_is_south:
            next_coord = north_coord
            compatible_connectors = southern_connectors
        elif previous_is_north:
            next_coord = south_coord
            compatible_connectors = northern_connectors
        else:
            return None
    elif connector_type == "-":
        if previous_is_east:
            next_coord = west_coord
            compatible_connectors = eastern_connectors
        elif previous_is_west:
            next_coord = east_coord
            compatible_connectors = western_connectors
        else:
            return None
    elif connector_type == "L":
        if previous_is_east:
            next_coord = north_coord
            compatible_connectors = southern_connectors
        elif previous_is_north:
            next_coord = east_coord
            compatible_connectors = western_connectors
        else:
            return None
    elif connector_type == "J":
        if previous_is_west:
            next_coord = north_coord
            compatible_connectors = southern_connectors
        elif previous_is_north:
            next_coord = west_coord
            compatible_connectors = eastern_connectors
        else:
            return None
    elif connector_type == "7":
        if previous_is_west:
            next_coord = south_coord
            compatible_connectors = northern_connectors
        elif previous_is_south:
            next_coord = west_coord
            compatible_connectors = eastern_connectors
        else:
            return None
    elif connector_type == "F":
        if previous_is_east:
            next_coord = south_coord
            compatible_connectors = northern_connectors
        elif previous_is_south:
            next_coord = east_coord
            compatible_connectors = western_connectors
        else:
            return None

    if (
        next_coord.x < 0
        or next_coord.y < 0
        or next_coord.y > len(map) - 1
        or next_coord.x > len(map[0]) - 1
    ):
        return None

    map_at_next_coord = map[next_coord.y][next_coord.x]

    if map_at_next_coord in compatible_connectors or map_at_next_coord == "S":
        return next_coord
    else:
        return None


file = open("input.txt", "r")
lines = file.read().splitlines()

start_coordinate = Coordinate(0, 0)

for x in range(len(lines[0]) - 1):
    for y in range(len(lines)):
        if lines[y][x] == "S":
            start_coordinate = Coordinate(x, y)
            break

initial_coords = getAllAdjacentCoords(
    start_coordinate, len(lines[0]) - 1, len(lines) - 1
)

candidate_pipelines = [Pipeline(start_coordinate, coord) for coord in initial_coords]

looped_pipeline = None

for candidate in candidate_pipelines:
    continue_exploring = True
    while continue_exploring:
        connecting_coord = getNextConnectionIfPossible(lines, candidate)

        if connecting_coord == None:
            continue_exploring = False

        if connecting_coord == candidate.coordinates[0]:
            looped_pipeline = candidate
            break

        candidate.addNode(connecting_coord)

    if looped_pipeline is not None:
        break

print(
    f"Found the loop, length {len(looped_pipeline.coordinates)}, max distance {len(looped_pipeline.coordinates)/2}"
)
