from dataclasses import dataclass

from advent_code_2023 import utils

INPUT_PATH = "advent_code_2023/day-03/input.txt"


@dataclass(frozen=True)
class PartSymbol:
    symbol: str
    x_index: int
    y_index: int


@dataclass(frozen=True)
class PotentialPartNumber:
    number: int
    x_index: int
    y_index: int


def _is_valid_coordinate(coordinate: tuple[int, int], max_x: int, max_y: int) -> bool:
    if coordinate[0] < 0 or coordinate[1] < 0:
        return False
    if coordinate[0] >= max_x or coordinate[1] >= max_y:
        return False

    return True


def generate_valid_adjacent_coordinates(symbol: PartSymbol, max_x: int, max_y: int):
    return [
        coordinate
        for coordinate in [
            (symbol.x_index - 1, symbol.y_index - 1),  # up-left
            (symbol.x_index, symbol.y_index - 1),  # up-up
            (symbol.x_index + 1, symbol.y_index - 1),  # up-right
            (symbol.x_index - 1, symbol.y_index),  # left
            (symbol.x_index + 1, symbol.y_index),  # right
            (symbol.x_index - 1, symbol.y_index + 1),  # down-left
            (symbol.x_index, symbol.y_index + 1),  # down-down
            (symbol.x_index + 1, symbol.y_index + 1),  # down-right
        ]
        if _is_valid_coordinate(coordinate, max_x, max_y)
    ]


potential_part_number_lookup_map: dict[int, dict[int, PotentialPartNumber]] = {}
part_symbols: list[PartSymbol] = []

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

            if char not in [".", "\n"]:
                part_symbols.append(PartSymbol(char, x_index, y_index))
        x_index += 1
    max_x = max(max_x, x_index)
    y_index += 1
    # if y_index == 3:
    # break

confirmed_part_numbers: set[int] = []


for symbol in part_symbols:
    valid_adjacent_coordinates = generate_valid_adjacent_coordinates(
        symbol, max_x, y_index
    )
    potential_part_numbers_for_symbol = [
        potential_part_number_lookup_map.get(coordinate[1], {}).get(coordinate[0])
        for coordinate in valid_adjacent_coordinates
    ]
    # print(f"{symbol} | {set(filter(None, potential_part_numbers_for_symbol))}")
    confirmed_part_numbers.extend(set(filter(None, potential_part_numbers_for_symbol)))

# print(part_symbols)
# print(potential_part_number_lookup_map)
print("====================== ATTENTION =======================")
print(
    f"The part numbers add up to: {sum(map(lambda x: x.number, confirmed_part_numbers))}"
)
