from dataclasses import dataclass

from advent_code_2023 import utils

INPUT_PATH = "advent_code_2023/day-03/input.txt"


@dataclass(frozen=True)
class PotentialGear:
    x_index: int
    y_index: int


@dataclass(frozen=True)
class PotentialPartNumber:
    number: int
    x_index: int
    y_index: int


def is_valid_coordinate(coordinate: tuple[int, int], max_x: int, max_y: int) -> bool:
    if coordinate[0] < 0 or coordinate[1] < 0:
        return False
    if coordinate[0] >= max_x or coordinate[1] >= max_y:
        return False

    return True


potential_part_number_lookup_map: dict[int, dict[int, PotentialPartNumber]] = {}
potential_gears: list[PotentialGear] = []

y_index = 0
max_x = 0

for line in utils.yield_lines_from_path(INPUT_PATH):
    potential_part_number_lookup_map[y_index] = {}
    x_index = 0
    digits_so_far = []
    for char in line:
        if char.isdigit():
            digits_so_far.append(char)
        else:
            if digits_so_far:
                first_index = x_index - len(digits_so_far)
                potential_part_number = PotentialPartNumber(
                    int("".join(digits_so_far)), first_index, y_index
                )
                for i in range(first_index, x_index):
                    potential_part_number_lookup_map[y_index][i] = potential_part_number
                digits_so_far = []

            if char == "*":
                potential_gears.append(PotentialGear(x_index, y_index))
        x_index += 1
    max_x = max(max_x, x_index)
    y_index += 1
    # if y_index == 3:
    # break

gear_ratios: list[int] = []

for gear in potential_gears:
    valid_adjacent_coordinates = [
        coordinate
        for coordinate in [
            (gear.x_index - 1, gear.y_index - 1),  # up-left
            (gear.x_index, gear.y_index - 1),  # up-up
            (gear.x_index + 1, gear.y_index - 1),  # up-right
            (gear.x_index - 1, gear.y_index),  # left
            (gear.x_index + 1, gear.y_index),  # right
            (gear.x_index - 1, gear.y_index + 1),  # down-left
            (gear.x_index, gear.y_index + 1),  # down-down
            (gear.x_index + 1, gear.y_index + 1),  # down-right
        ]
        if is_valid_coordinate(coordinate, max_x, y_index)
    ]
    potential_part_numbers_for_gear = set(
        filter(
            None,
            [
                potential_part_number_lookup_map.get(coordinate[1], {}).get(
                    coordinate[0]
                )
                for coordinate in valid_adjacent_coordinates
            ],
        )
    )
    # print(f"{gear} | {potential_part_numbers_for_gear}")
    if len(potential_part_numbers_for_gear) == 2:
        gear_ratios.append(
            potential_part_numbers_for_gear.pop().number
            * potential_part_numbers_for_gear.pop().number
        )

print("====================== ATTENTION =======================")
print(f"The gear ratios add up to: {sum(gear_ratios)}")
