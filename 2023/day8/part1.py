file = open("input.txt", "r")
lines = file.read().splitlines()

directions = lines[0]

network_nodes = {}

network_lines = lines[2:]

for network_line in network_lines:
    node = network_line.split(" = ")
    node_directions = node[1][1:-1].split(", ")

    network_nodes[node[0]] = node_directions

steps = 0
current_node = "AAA"

while True:
    direction_index = 0
    if directions[steps % len(directions)] == "R":
        direction_index = 1

    current_node = network_nodes[current_node][direction_index]
    steps += 1

    if current_node == "ZZZ":
        break

print(steps)
