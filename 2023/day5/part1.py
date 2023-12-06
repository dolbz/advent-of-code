import sys


class IndividualMapping:
    def __init__(self, source_start, target_start, range):
        self.source_start = source_start
        self.target_start = target_start
        self.range = range

    def __str__(self):
        return f"source_start: {self.source_start}, target_start: {self.target_start}, range: {self.range}"

    def value_is_covered(self, value):
        return value >= self.source_start and value < self.source_start + self.range

    def map_source_to_target(self, source_value):
        if not self.value_is_covered(source_value):
            raise Exception(
                "Sanity check failed. Tried to map value that isn't covered by the mapping"
            )

        offset = source_value - self.source_start
        return self.target_start + offset


class BigMap:
    def __init__(self, map_lines, target_map):
        self.mappings = []

        self.map_desc = map_lines[0]
        for line in map_lines[1:]:
            mapping_parts = line.split(" ")
            self.mappings.append(
                IndividualMapping(
                    int(mapping_parts[1]), int(mapping_parts[0]), int(mapping_parts[2])
                )
            )

        self.target_map = target_map

    def __str__(self):
        return f"{self.map_desc}\n{[str(mapping) for mapping in self.mappings]}\ntarget_map: {self.target_map}"

    def map_value(self, value):
        mapped_value = value

        for mapping in self.mappings:
            if mapping.value_is_covered(value):
                mapped_value = mapping.map_source_to_target(value)
                break

        if self.target_map is not None:
            return self.target_map.map_value(mapped_value)
        else:
            return mapped_value


file = open("input.txt", "r")
lines = file.read().splitlines()

start_seeds = []
seed_strings = lines[0].split(":")[1].strip().split(" ")
for seed_string in seed_strings:
    start_seeds.append(int(seed_string))

lines = lines[2:]

end_of_map_range = len(lines)
previous_map = None
for line_num in range(len(lines) - 1, -1, -1):
    if lines[line_num].endswith(":"):
        previous_map = BigMap(lines[line_num:end_of_map_range], previous_map)
        end_of_map_range = line_num - 1  # -1 to remove the blank line between maps

root_map = previous_map
lowest_location = sys.maxsize

for seed in start_seeds:
    location = root_map.map_value(seed)
    if location < lowest_location:
        lowest_location = location

print(lowest_location)
