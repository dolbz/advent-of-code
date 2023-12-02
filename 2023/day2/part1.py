file = open("input.txt", "r")
lines = file.read().splitlines()

red_count = 12
green_count = 13
blue_count = 14

possible_games_sum = 0

for line in lines:
    (game, rounds_str) = tuple(line.split(":"))
    game_id = int(game.split(" ")[1])

    rounds_str_list = rounds_str.split(";")

    game_possible = True
    rounds = []
    for round in rounds_str_list:
        colours_fetched = tuple(round.split(","))
        for colour_fetched in colours_fetched:
            (count, colour) = tuple(colour_fetched.strip().split(" "))
            count = int(count)

            match colour:
                case "red":
                    current_max_count = red_count
                case "green":
                    current_max_count = green_count
                case "blue":
                    current_max_count = blue_count

            if count > current_max_count:
                game_possible = False
                break
        if not game_possible:
            break

    if game_possible:
        possible_games_sum += game_id

print(possible_games_sum)
