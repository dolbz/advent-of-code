decryption_key = 811589153


def read_input_file():
    file = open("input.txt", "r")
    lines = file.readlines()

    encrypted_message = list()
    for index, line in enumerate(lines):
        encrypted_message.append((int(line) * decryption_key, index))

    return encrypted_message


encrypted_message = read_input_file()

for _ in range(10):
    for iteration_index in range(len(encrypted_message)):
        for current_index, (current_number, original_index) in enumerate(
            encrypted_message
        ):
            if original_index == iteration_index:
                break

        new_index = current_index + current_number

        if new_index >= len(encrypted_message):
            new_index = new_index % (len(encrypted_message) - 1)
        elif new_index < 0:
            true_change = (abs(new_index) % (len(encrypted_message) - 1)) * -1
            new_index = len(encrypted_message) - 1 + true_change

        encrypted_message.pop(current_index)
        encrypted_message.insert(new_index, (current_number, original_index))

    message_numbers_only = [number for (number, _) in encrypted_message]
    # print(message_numbers_only)

while message_numbers_only[0] != 0:
    num = message_numbers_only.pop(0)
    message_numbers_only.append(num)

coord1 = message_numbers_only[1000 % len(message_numbers_only)]
coord2 = message_numbers_only[2000 % len(message_numbers_only)]
coord3 = message_numbers_only[3000 % len(message_numbers_only)]

print(f"{coord1}, {coord2}, {coord3}")
print(coord1 + coord2 + coord3)
