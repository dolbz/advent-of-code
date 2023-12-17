def calculateHash(input):
    current_value = 0
    for character in input:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256

    return current_value


file = open("input.txt", "r")
line = file.read()

steps = line.split(",")

boxes = [list() for x in range(256)]

for step in steps:
    label_index = -2  # For the = steps
    strength = None

    if step[-1] == "-":
        label_index = -1
    else:
        strength = int(step[-1])

    label = step[:label_index]
    label_hash = calculateHash(label)

    box_contents = boxes[label_hash]

    boxed_index = None
    for i in range(len(box_contents)):
        (boxed_label, boxed_lens_strength) = box_contents[i]
        if label == boxed_label:
            boxed_index = i

    if strength == None:  # strength of none means we should remove the lens
        if boxed_index != None:
            del box_contents[boxed_index]
    elif boxed_index == None:  # this lens isn't already in the box so add it
        box_contents.append((label, strength))
    else:  # replace the existing lens in the box
        box_contents[boxed_index] = (label, strength)

total_focusing_power = 0

for box_num in range(256):
    for slot_num in range(len(boxes[box_num])):
        focusing_power = (box_num + 1) * (slot_num + 1) * boxes[box_num][slot_num][1]
        total_focusing_power += focusing_power

print(total_focusing_power)
