import re
import math

file = open("input.txt", "r")
lines = file.read().splitlines()

race_time = int("".join(lines[0].split(":")[1].strip().split(" ")))
record_distance = int("".join(lines[1].split(":")[1].strip().split(" ")))

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

print(ways_to_win)
