file = open("input.txt", "r")
lines = file.read().splitlines()

running_total = 0

for line in lines:
    first_digit = None
    last_digit = None

    for character in line:
        if character.isdigit():
            if first_digit is None:
                first_digit = int(character)

            last_digit = int(character)

    calibration_value = (first_digit * 10) + last_digit
    running_total += calibration_value

print(running_total)
