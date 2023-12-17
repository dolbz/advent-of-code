def calculateHash(input):
    current_value = 0
    for character in input:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256

    return current_value


file = open("input.txt", "r")
line = file.read()

strings = line.split(",")

hash_sum = 0

for steps in strings:
    hash_value = calculateHash(steps)
    hash_sum += hash_value

print(hash_sum)
