wordy_digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

file = open("input.txt", "r")
lines = file.read().splitlines()

running_total = 0

for line in lines:
    first_digit = None
    last_digit = None
    candidate_wordy_digits = []

    for character in line:
        candidate_wordy_digits.append("")

        updated_candidates = []

        unreplaced_character = character
        for candidate in candidate_wordy_digits:
            new_candidate = candidate + unreplaced_character
            for wordy_digit, replacement in wordy_digits.items():
                if new_candidate == wordy_digit:
                    character = replacement
                elif wordy_digit.startswith(new_candidate):
                    updated_candidates.append(new_candidate)

        candidate_wordy_digits = updated_candidates

        if character.isdigit():
            if first_digit is None:
                first_digit = int(character)

            last_digit = int(character)

    calibration_value = (first_digit * 10) + last_digit
    running_total += calibration_value

print(running_total)
