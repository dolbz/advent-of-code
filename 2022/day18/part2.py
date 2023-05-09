import sys


class Point3d:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        if isinstance(other, Point3d):
            return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())


def read_input_file():
    file = open("input.txt", "r")
    lines = file.readlines()

    coords = dict()

    min_x = sys.maxsize
    min_y = sys.maxsize
    min_z = sys.maxsize

    # there are no negative points in the input
    max_x = 0
    max_y = 0
    max_z = 0

    points = list()

    for line in lines:
        parts = line.split(",")

        point = Point3d(int(parts[0]), int(parts[1]), int(parts[2]))
        points.append(point)

        if point.x < min_x:
            min_x = point.x
        if point.x > max_x:
            max_x = point.x

        if point.y < min_y:
            min_y = point.y
        if point.y > max_y:
            max_y = point.y

        if point.z < min_z:
            min_z = point.z
        if point.z > max_z:
            max_z = point.z

    # contains actual points from the scan including internal emtpy space
    point_presence_matrix = list()

    # starts fully populated as a solid cube. We will work from the outside inwards to subtract the external empty space until
    # we have a solid representation of the object _without_ internal empty space
    external_presence_matrix = list()

    for x in range(max_x + 2):
        point_presence_matrix.append(list())
        external_presence_matrix.append(list())
        for y in range(max_y + 2):
            point_presence_matrix[x].append(list())
            external_presence_matrix[x].append(list())
            for z in range(max_z + 2):
                point_presence_matrix[x][y].append(False)
                external_presence = True
                if (x == max_x + 1) or (y == max_y + 1) or (z == max_z + 1):
                    # This position is beyond where we _know_ there are points so we can mark it False
                    external_presence = False
                external_presence_matrix[x][y].append(external_presence)

    for point in points:
        point_presence_matrix[point.x][point.y][point.z] = True

    print(
        f"min_x {min_x}, min_y {min_y}, min_z {min_z},  max_x {max_x}, max_y {max_y}, max_z {max_z}"
    )

    # subtract external empty space
    # scan z axis for every x,y position
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            # start from min value until point is hit
            for z in range(max_z + 1):
                if point_presence_matrix[x][y][z]:
                    break
                external_presence_matrix[x][y][z] = False
            # then check from the opposite direction until point is hit
            for z in range(max_z, -1, -1):
                if point_presence_matrix[x][y][z]:
                    break
                external_presence_matrix[x][y][z] = False

    # scan y axis for every x,z position
    for x in range(max_x + 1):
        for z in range(max_z + 1):
            # start from min value until point is hit
            for y in range(max_y + 1):
                if point_presence_matrix[x][y][z]:
                    break
                external_presence_matrix[x][y][z] = False
            # then check from the opposite direction until point is hit
            for y in range(max_y, -1, -1):
                if point_presence_matrix[x][y][z]:
                    break
                external_presence_matrix[x][y][z] = False

    # scan x axis for every y,z position
    for y in range(max_y + 1):
        for z in range(max_z + 1):
            # start from min value until point is hit
            for x in range(max_x + 1):
                if point_presence_matrix[x][y][z]:
                    break
                external_presence_matrix[x][y][z] = False
            # then check from the opposite direction until point is hit
            for x in range(max_x, -1, -1):
                if point_presence_matrix[x][y][z]:
                    break
                external_presence_matrix[x][y][z] = False

    return (points, external_presence_matrix)


def number_of_neighbours(point, point_presence_matrix):
    neighbours = 0

    if point_presence_matrix[point.x][point.y][point.z + 1]:
        neighbours += 1
    if point.z > 0 and point_presence_matrix[point.x][point.y][point.z - 1]:
        neighbours += 1

    if point_presence_matrix[point.x][point.y + 1][point.z]:
        neighbours += 1
    if point.y > 0 and point_presence_matrix[point.x][point.y - 1][point.z]:
        neighbours += 1

    if point_presence_matrix[point.x + 1][point.y][point.z]:
        neighbours += 1
    if point.x > 0 and point_presence_matrix[point.x - 1][point.y][point.z]:
        neighbours += 1

    return neighbours


(points, external_presence_matrix) = read_input_file()

exposed_edges = 0

for point in points:
    neighbours_count = number_of_neighbours(point, external_presence_matrix)

    exposed_edges += 6 - neighbours_count

print(exposed_edges)
