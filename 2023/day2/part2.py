file = open("input.txt", "r")
lines = file.read().splitlines()

power_sum = 0

for line in lines:
    (game, rounds_str) = tuple(line.split(":"))
    game_id = int(game.split(" ")[1])

    rounds_str_list = rounds_str.split(";")

    min_counts = {"red": 0, "green": 0, "blue": 0}

    rounds = []
    for round in rounds_str_list:
        colours_fetched = tuple(round.split(","))
        for colour_fetched in colours_fetched:
            (count, colour) = tuple(colour_fetched.strip().split(" "))
            count = int(count)

            current_min_count = min_counts[colour]

            if count > current_min_count:
                min_counts[colour] = count

    game_power = 1
    for colour, count in min_counts.items():
        game_power *= count

    power_sum += game_power

print(power_sum)
