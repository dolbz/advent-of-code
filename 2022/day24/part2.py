import sys


class CheckedPoint:
    def __init__(self, point, step_count):
        self.point = point
        self.step_count = step_count

    def __repr__(self):
        return f"({self.point}, {self.step_count})"

    def __eq__(self, other):
        if isinstance(other, CheckedPoint):
            return (self.point == other.point) and (self.step_count == other.step_count)
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())


def read_input_file():
    file = open("input.txt", "r")
    lines = file.read().splitlines()
    lines = lines[1:-1]

    grid = [None] * len(lines[0][1:-1])
    for i in range(len(grid)):
        grid[i] = [None] * len(lines)

    for row_index, line in enumerate(lines):
        line = line[1:-1]
        for column_index, content in enumerate(line):
            grid[column_index][row_index] = list()
            if content != ".":
                grid[column_index][row_index].append(content)
        # print(line)

    return grid


def run_avalanche_step(grid):
    x_length = len(grid)
    y_length = len(grid[0])

    next_grid = [None] * x_length
    for i in range(len(grid)):
        next_grid[i] = [None] * y_length

    for y in range(y_length):
        for x in range(x_length):
            next_grid[x][y] = list()

    for y in range(y_length):
        for x in range(x_length):
            contents = grid[x][y]
            for item in contents:
                new_x = x
                new_y = y
                if item == "^":
                    new_y -= 1
                    if new_y == -1:
                        new_y = y_length - 1
                elif item == "<":
                    new_x -= 1
                    if new_x == -1:
                        new_x = x_length - 1
                elif item == ">":
                    new_x += 1
                    if new_x == x_length:
                        new_x = 0
                else:
                    new_y += 1
                    if new_y == y_length:
                        new_y = 0

                next_grid[new_x][new_y].append(item)

    return next_grid


def print_grid(grid):
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            content = grid[x][y]
            if len(content) == 0:
                print(".", end="")
            elif len(content) == 1:
                print(content[0], end="")
            else:
                print(len(content), end="")
        print()
    print()


def find_possible_next_positions(current_pos, target_pos, grid, step_number):
    end_pos = Point(len(grid) - 1, len(grid[0]))
    start_pos = Point(0, -1)
    possible_positions = list()

    # special case for first move
    if current_pos == start_pos:
        possible_positions.append((Point(0, 0), step_number))
        possible_positions.append((start_pos, step_number))
        return possible_positions
    elif current_pos == end_pos:
        possible_positions.append((end_pos, step_number))
        possible_positions.append((Point(end_pos.x, end_pos.y - 1), step_number))
        return possible_positions

    # special case for move from position just before the end
    if (
        target_pos == end_pos
        and current_pos.x == target_pos.x
        and current_pos.y == target_pos.y - 1
    ):
        possible_positions.append((end_pos, step_number))
        return possible_positions
    elif target_pos == start_pos and current_pos == Point(0, 0):
        possible_positions.append((start_pos, step_number))
        return possible_positions

    for x_offset, y_offset in [(-1, 0), (0, 0), (1, 0), (0, -1), (0, 1)]:
        test_pos = Point(current_pos.x + x_offset, current_pos.y + y_offset)

        if (
            test_pos.x < 0
            or test_pos.y < 0
            or test_pos.x > len(grid) - 1
            or test_pos.y > len(grid[0]) - 1
        ):
            # out of bounds
            continue

        if len(grid[test_pos.x][test_pos.y]) == 0:
            possible_positions.append((test_pos, step_number))

    return possible_positions


def find_minimum_step_route(start_grid, start_pos, target_pos):
    grids = list()
    grids.append(start_grid)
    min_step_count = sys.maxsize
    positions_to_test = list()
    positions_to_test.append((start_pos, 0))
    checked_points = dict()

    while True:
        (position, step_count) = positions_to_test.pop(0)
        print(
            f"checking {position} on step count {step_count}, min count {min_step_count}"
        )

        if len(grids) == step_count + 1:
            grids.append(run_avalanche_step(grids[step_count]))

        next_positions = find_possible_next_positions(
            position, target_pos, grids[step_count + 1], step_count + 1
        )

        for next_position, next_step_count in next_positions:
            checked_point = CheckedPoint(next_position, next_step_count)
            if checked_point in checked_points:
                continue
            checked_points[checked_point] = True
            if next_position == target_pos and next_step_count < min_step_count:
                print(f"Found a solution in {next_step_count} steps")
                min_step_count = next_step_count
            elif next_step_count < min_step_count:
                positions_to_test.append((next_position, next_step_count))

        if len(positions_to_test) == 0:
            break
    return (min_step_count, grids[min_step_count])


grid = read_input_file()

end_pos = Point(len(grid) - 1, len(grid[0]))
start_pos = Point(0, -1)

(step_count_1, final_grid) = find_minimum_step_route(grid, start_pos, end_pos)
(step_count_2, final_grid) = find_minimum_step_route(final_grid, end_pos, start_pos)
(step_count_3, final_grid) = find_minimum_step_route(final_grid, start_pos, end_pos)

print(f"Steps {step_count_1}, {step_count_2}, {step_count_3}")
print(f"Total {step_count_1 + step_count_2 + step_count_3}")
