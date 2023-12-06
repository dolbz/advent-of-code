def is_adjacent_to_part(diagram_lines, line_number, number_start_pos, number_end_pos):
    line_length = len(lines[0])

    for current_line_num in range(line_number - 1, line_number + 2):
        if current_line_num < 0 or current_line_num > len(diagram_lines) - 1:
            continue

        for pos_to_check in range(number_start_pos - 1, number_end_pos + 2):
            if pos_to_check < 0 or pos_to_check > line_length - 1:
                continue

            # print(f"check {current_line_num},{pos_to_check}")
            char_at_pos = diagram_lines[current_line_num][pos_to_check]

            if char_at_pos != "." and not char_at_pos.isdigit():
                # print(" is part!")
                return True

    return False


file = open("input.txt", "r")
lines = file.read().splitlines()

num_of_lines = len(lines)
line_length = len(lines[0])

part_numbers_sum = 0

for i in range(num_of_lines):
    digit_buffer = []

    for j in range(line_length):
        if lines[i][j].isdigit():
            digit_buffer.append(lines[i][j])

        if len(digit_buffer) > 0 and (
            j == line_length - 1 or not lines[i][j].isdigit()
        ):
            pos_to_check = j
            if j == line_length - 1 and lines[i][j].isdigit():
                pos_to_check = j + 1
            number = int("".join(digit_buffer))
            number_of_digits = len(digit_buffer)

            if is_adjacent_to_part(
                lines, i, pos_to_check - number_of_digits, pos_to_check - 1
            ):
                part_numbers_sum += number

            digit_buffer = []

print(part_numbers_sum)
