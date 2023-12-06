import importlib

helpers = importlib.import_module("advent_code_2023.day-05.helpers")

# INPUT_PATH = "advent_code_2023/day-05/test-input.txt"
INPUT_PATH = "advent_code_2023/day-05/input.txt"

almanac = helpers.parse_file(INPUT_PATH)
locations = []
for seed in almanac.seeds:
    locations.append(almanac.get_location_for_seed(seed))

print("====================== ATTENTION =======================")
print(f"The lowest location is: {sorted(locations)[0]}")
