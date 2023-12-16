import os.path


def HASH(input_str: str) -> int:
    current_value = 0
    for char in input_str.strip():
        ascii_code = ord(char)
        current_value += ascii_code
        current_value *= 17
        current_value = current_value % 256
    return current_value


def parse_init_sequence(path: str) -> list[str]:
    with open(os.path.expanduser(path), "r") as input_file:
        return input_file.readline().strip().split(",")


# INPUT_PATH = "advent_code_2023/day-15/test-input.txt"
INPUT_PATH = "advent_code_2023/day-15/input.txt"

init_sequence = parse_init_sequence(INPUT_PATH)
print("====================== ATTENTION =======================")
print(f"The summary number is: {sum(map(HASH, init_sequence))}")
