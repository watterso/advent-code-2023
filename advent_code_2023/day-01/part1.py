import os.path
def get_left_most_digit(line: str) -> int:
    for char in line:
        if char.isdigit():
            return int(char)
    return -99999999

def get_right_most_digit(line: str) -> int:
    reversed = line[::-1]
    return get_left_most_digit(reversed)

path = '~/code/advent-code-2023/advent_code_2023/day-01/input.txt'

sum = 0
with open(os.path.expanduser(path), 'r') as input_file:
    for line in input_file:
        l = get_left_most_digit(line)
        r = get_right_most_digit(line)
        calibration_value = int(str(l) + str(r))
        sum += calibration_value

print("====================== ATTENTION =======================")
print(f'The Calibration values add up to: {sum}')