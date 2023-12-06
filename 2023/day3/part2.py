class PartNum:
    def __init__(self, line, start_pos, value):
        self.line = line
        self.start_pos = start_pos
        self.value = value

    def __repr__(self):
        return f"({self.start_pos}, {self.line})"

    def __eq__(self, other):
        if isinstance(other, PartNum):
            return (self.start_pos == other.start_pos) and (self.line == other.line)
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())


def expand_part_number(diagram_lines, line_number, line_pos):
    while line_pos >= 0 and diagram_lines[line_number][line_pos].isdigit():
        line_pos -= 1

    line_pos += 1
    start_pos = line_pos

    digit_buffer = []
    while line_pos < len(diagram_lines[0]):
        current_char = diagram_lines[line_number][line_pos]

        line_pos += 1

        if current_char.isdigit():
            digit_buffer.append(current_char)
        else:
            break

    return PartNum(line_number, start_pos, int("".join(digit_buffer)))


def get_gear_ratio(diagram_lines, line_number, line_pos):
    line_length = len(lines[0])

    adjacent_part_numbers = {}

    for current_line_num in range(line_number - 1, line_number + 2):
        if current_line_num < 0 or current_line_num > len(diagram_lines) - 1:
            continue

        for pos_to_check in range(line_pos - 1, line_pos + 2):
            if pos_to_check < 0 or pos_to_check > line_length - 1:
                continue

            char_at_pos = diagram_lines[current_line_num][pos_to_check]

            if char_at_pos.isdigit():
                part_num = expand_part_number(
                    diagram_lines, current_line_num, pos_to_check
                )
                adjacent_part_numbers[part_num] = part_num.value

    if len(adjacent_part_numbers.items()) == 2:
        gear_ratio = 1
        for value in adjacent_part_numbers.values():
            gear_ratio *= value

        return gear_ratio
    else:
        return -1


file = open("input.txt", "r")
lines = file.read().splitlines()

num_of_lines = len(lines)
line_length = len(lines[0])

gear_ratios_sum = 0

for i in range(num_of_lines):
    for j in range(line_length):
        if lines[i][j] == "*":
            gear_ratio = get_gear_ratio(lines, i, j)
            if gear_ratio > -1:
                gear_ratios_sum += gear_ratio

print(gear_ratios_sum)
