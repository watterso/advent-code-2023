from advent_code_2023 import utils


def parse_input(path: str) -> list[list[int]]:
    lists_of_ints = []
    for raw_line in utils.yield_lines_from_path(path):
        lists_of_ints.append(list(map(int, filter(None, raw_line.split(" ")))))
    return lists_of_ints


def get_deltas(input_list: list[int]) -> list[int]:
    oot = []
    for i in range(1, len(input_list)):
        oot.append(input_list[i] - input_list[i - 1])
    # print(input_list)
    return oot


def recurse_to_all_zeroes(input_list: list[int]) -> int:
    if all(map(lambda x: x == 0, input_list)):
        return 0
    return input_list[-1] + recurse_to_all_zeroes(get_deltas(input_list))


# INPUT_PATH = "advent_code_2023/day-09/test-input.txt"
INPUT_PATH = "advent_code_2023/day-09/input.txt"

inputs = parse_input(INPUT_PATH)

next_vals = []

for input_list in inputs:
    # print(input_list)
    next_val = recurse_to_all_zeroes(input_list)
    next_vals.append(next_val)
    # print(next_val)


print("====================== ATTENTION =======================")
print(f"The sum of the extrapolated numbers is: {sum(next_vals)}")
