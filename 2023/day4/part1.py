file = open("input.txt", "r")
lines = file.read().splitlines()

total_points = 0

for line in lines:
    number_sets = line.split(":")[1].split("|")
    winning_numbers = number_sets[0].strip().split(" ")
    my_numbers = number_sets[1].strip().split(" ")

    num_of_matches = 0
    for winning_number in winning_numbers:
        if winning_number == "":
            continue
        if winning_number in my_numbers:
            num_of_matches += 1

    card_points = 0
    if num_of_matches > 0:
        card_points = 2 ** (num_of_matches - 1)

    total_points += card_points

print(total_points)
