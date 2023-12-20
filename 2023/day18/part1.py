import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


# Line dfined by two coordinate points
class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def __repr__(self) -> str:
        return f"[{self.point1}, {self.point2}]"

    def intersects(self, otherLine):
        # From https://stackoverflow.com/a/62625458
        # But it doesn't work well with the edges like this that are exactly
        # 'pixel' aligned and pixel width

        dx0 = self.point2.x - self.point1.x
        dx1 = otherLine.point2.x - otherLine.point1.x
        dy0 = self.point2.y - self.point1.y
        dy1 = otherLine.point2.y - otherLine.point1.y
        p0 = dy1 * (otherLine.point2.x - self.point1.x) - dx1 * (
            otherLine.point2.y - self.point1.y
        )
        p1 = dy1 * (otherLine.point2.x - self.point2.x) - dx1 * (
            otherLine.point2.y - self.point2.y
        )
        p2 = dy0 * (self.point2.x - otherLine.point1.x) - dx0 * (
            self.point2.y - otherLine.point1.y
        )
        p3 = dy0 * (self.point2.x - otherLine.point2.x) - dx0 * (
            self.point2.y - otherLine.point2.y
        )
        return (p0 * p1 < 0) & (p2 * p3 < 0)


def getPointsOnPath(current_pos, direction, distance):
    x_change = 0
    y_change = 0

    if direction == "R":
        x_change = distance
    elif direction == "L":
        x_change = -distance
    elif direction == "U":
        y_change = -distance
    elif direction == "D":
        y_change = distance

    pathPoints = []

    x_step = 1 if x_change > 0 else -1
    y_step = 1 if y_change > 0 else -1

    for x in range(current_pos.x + x_step, current_pos.x + x_change + x_step, x_step):
        pathPoints.append(Point(x, current_pos.y))

    for y in range(current_pos.y + y_step, current_pos.y + y_change + y_step, y_step):
        pathPoints.append(Point(current_pos.x, y))

    return pathPoints


def digOutTrench(lines, layout):
    current_pos = Point(0, 0)

    trench_count = 0

    for line in lines:
        line_parts = line.split(" ")
        direction = line_parts[0]
        distance = int(line_parts[1])
        colour = line_parts[2]  # why?

        points_on_path = getPointsOnPath(current_pos, direction, distance)

        for point in points_on_path:
            # print(point)
            current_pos = point
            layout[point.x - min_x][point.y - min_y] = "#"
            trench_count += 1

    return trench_count


def countEdgesIntersected(point, edges):
    # cast a ray from (point.x, 0) to the point of interest
    # count the edges intersected. This allows us to say if a point is
    # inside or outside of the shape

    cast_line = Line(Point(point.x, -1), point)

    intersections = 0
    for edge in edges:
        if cast_line.intersects(edge):
            intersections += 1
    return intersections


def digOutInterior(layout, edges):
    inside_point = None
    for x, column in enumerate(layout):
        for y, content in enumerate(column):
            if content == ".":
                current_pos = Point(x, y)
                intersectionCount = countEdgesIntersected(current_pos, edges)

                # originally I checked the intersected edges count for every space
                # to work out which spaces lay inside the shape. This was slow and
                # didn't work as expected in all cases. See comment in the intersection
                # implementation. So now we find one point inside and flood fill.
                if intersectionCount == 1:
                    # We have a point inside!
                    inside_point = current_pos
                    break

        if inside_point is not None:
            break

    # flood fill from found point
    fill_queue = []
    fill_queue.append(current_pos)

    excavated_count = 0

    while len(fill_queue) != 0:
        current_pos = fill_queue.pop(0)
        if layout[current_pos.x][current_pos.y] != "#":
            excavated_count += 1
            layout[current_pos.x][current_pos.y] = "#"

            if current_pos.x + 1 < len(layout):
                fill_queue.append(Point(current_pos.x + 1, current_pos.y))
            if current_pos.x > 0:
                fill_queue.append(Point(current_pos.x - 1, current_pos.y))

            if current_pos.y + 1 < len(layout[0]):
                fill_queue.append(Point(current_pos.x, current_pos.y + 1))
            if current_pos.y > 0:
                fill_queue.append(Point(current_pos.x, current_pos.y - 1))

    return excavated_count


file = open("input.txt", "r")
lines = file.read().splitlines()

max_x = 0
max_y = 0

min_x = 0
min_y = 0

current_pos = Point(0, 0)
edges = []

for line in lines:
    line_parts = line.split(" ")
    direction = line_parts[0]
    distance = int(line_parts[1])
    colour = line_parts[2]  # why?

    points_on_path = getPointsOnPath(current_pos, direction, distance)

    edges.append(Line(current_pos, points_on_path[-1]))

    current_pos = points_on_path[-1]

    if current_pos.x > max_x:
        max_x = current_pos.x
    if current_pos.y > max_y:
        max_y = current_pos.y
    if current_pos.x < min_x:
        min_x = current_pos.x
    if current_pos.y < min_y:
        min_y = current_pos.y

# renormalize points to be > 0
normalized_edges = []
for edge in edges:
    normalized_point1 = Point(edge.point1.x - min_x, edge.point1.y - min_y)
    normalized_point2 = Point(edge.point2.x - min_x, edge.point2.y - min_y)

    normalized_edges.append(Line(normalized_point1, normalized_point2))
edges = normalized_edges

layout = []
for i in range((max_x - min_x) + 1):
    layout.append(["."] * ((max_y - min_y) + 1))


trench_count = digOutTrench(lines, layout)

for y in range(len(layout[0])):
    for x in range(len(layout)):
        print(layout[x][y], end="")
    print()

print()

excavation_count = digOutInterior(layout, edges)

for y in range(len(layout[0])):
    for x in range(len(layout)):
        print(layout[x][y], end="")
    print()

print()

print(trench_count + excavation_count)
