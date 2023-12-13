def extractPatternsFromInput():
    file = open("input.txt", "r")
    lines = file.read().splitlines()

    lines.append("")

    current_pattern_lines = []

    pattern_index = 0

    patterns = []

    for line in lines:
        if line == "":
            # Whole pattern found. Process it!
            vertical_pattern_lines = []

            for x in range(len(current_pattern_lines[0])):
                vertical_characters = []
                for y in range(len(current_pattern_lines)):
                    vertical_characters.append(current_pattern_lines[y][x])

                vertical_pattern_lines.append("".join(vertical_characters))

            patterns.append(
                {
                    "horizontal": current_pattern_lines,
                    "vertical": vertical_pattern_lines,
                }
            )

            # Clean up for next pattern
            current_pattern_lines = []
            pattern_index += 1
            continue
        current_pattern_lines.append(line)

    return patterns


def verifyReflectionForPattern(pattern, reflection_start):
    i = 0
    while reflection_start - (i + 1) >= 0 and reflection_start + i < len(pattern):
        if pattern[reflection_start - (i + 1)] != pattern[reflection_start + i]:
            return False
        i += 1
    return True


def findReflectionIn(pattern):
    previous_line = None
    for i in range(len(pattern)):
        line = pattern[i]
        if line == previous_line:
            if verifyReflectionForPattern(pattern, i):
                return i
        previous_line = line
    return None


patterns = extractPatternsFromInput()

reflection_total = 0

for pattern in patterns:
    verticalReflectionIndex = findReflectionIn(pattern["vertical"])
    if verticalReflectionIndex is None:
        horizontalReflectionIndex = findReflectionIn(pattern["horizontal"])
        reflection_total += 100 * horizontalReflectionIndex
    else:
        reflection_total += verticalReflectionIndex

print(f"Reflection total: {reflection_total}")
