file = open("input.txt", "r")
lines = file.read().splitlines()

num_of_cards = len(lines)
card_values = [1] * num_of_cards

for line_num in range(num_of_cards - 1, -1, -1):
    line = lines[line_num]
    number_sets = line.split(":")[1].split("|")
    winning_numbers = number_sets[0].strip().split(" ")
    my_numbers = number_sets[1].strip().split(" ")

    num_of_matches = 0
    for winning_number in winning_numbers:
        if winning_number == "":
            continue
        if winning_number in my_numbers:
            num_of_matches += 1

    if num_of_matches > 0:
        ulitmate_card_value = 1

        for i in range(num_of_matches):
            ulitmate_card_value += card_values[line_num + i + 1]

        card_values[line_num] = ulitmate_card_value

print(sum(card_values))
