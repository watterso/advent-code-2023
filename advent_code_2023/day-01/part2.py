import os.path

WORD_TO_DIGIT_LOOKUP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
WORD_DIGIT_REVERSED_TO_DIGIT_LOOKUP = {
    key[::-1]: value for key, value in WORD_TO_DIGIT_LOOKUP.items()
}


def get_left_most_digit(
    line: str, word_digit_to_value: dict[str, int] = WORD_TO_DIGIT_LOOKUP
) -> int:
    chars_so_far = []
    for char in line:
        if char.isdigit():
            return int(char)
        else:
            chars_so_far.append(char)
            chars_so_far_str = "".join(chars_so_far)
            for word_digit in word_digit_to_value.keys():
                if word_digit in chars_so_far_str:
                    return word_digit_to_value[word_digit]
    return -99999999


def get_right_most_digit(line: str) -> int:
    reversed = line[::-1]
    return get_left_most_digit(reversed, WORD_DIGIT_REVERSED_TO_DIGIT_LOOKUP)


path = "~/code/advent-code-2023/advent_code_2023/day-01/input.txt"

sum = 0
with open(os.path.expanduser(path), "r") as input_file:
    count = 1
    for line in input_file:
        l = get_left_most_digit(line)
        r = get_right_most_digit(line)
        # print(f'{count}: {l}{r} | {line}')
        count += 1
        calibration_value = int(str(l) + str(r))
        sum += calibration_value

print("====================== ATTENTION =======================")
print(f"The Calibration values add up to: {sum}")
