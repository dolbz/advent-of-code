import re
import math

file = open("input.txt", "r")
lines = file.read().splitlines()

times = [int(time) for time in re.split("\s+", lines[0])[1:]]
distances = [int(distance) for distance in re.split("\s+", lines[1])[1:]]

ways_to_win_multiple = 1

for race in range(len(times)):
    race_time = times[race]
    record_distance = distances[race]

    a = -1
    b = race_time
    c = -record_distance

    x1 = (-b + math.sqrt((b * b) - (4 * a * c))) / (2 * a)
    x2 = (-b - math.sqrt((b * b) - (4 * a * c))) / (2 * a)

    if x1.is_integer():
        x1 += 1
    x1 = math.ceil(x1)
    x2 = math.ceil(x2)

    ways_to_win = x2 - x1
    ways_to_win_multiple *= ways_to_win

print(ways_to_win_multiple)
