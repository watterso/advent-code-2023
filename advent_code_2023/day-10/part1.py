from collections import defaultdict

import typing

from advent_code_2023 import utils

STARTING_SYMBOL = "S"
JUST_PLAIN_GROUND = "."
COORD_DELTAS_TO_GET_CONNECTED_COORDS = {
    "|": ((0, -1), (0, 1)),
    "-": ((-1, 0), (1, 0)),
    "L": ((0, -1), (1, 0)),
    "J": ((0, -1), (-1, 0)),
    "7": ((-1, 0), (0, 1)),
    "F": ((1, 0), (0, 1)),
    "S": ((0, -1), (0, 1), (-1, 0), (1, 0)),
}
DELTA_COMPATIBLE_SYMBOL = {
    (0, -1): "|F7S",
    (0, 1): "|LJS",
    (-1, 0): "-LFS",
    (1, 0): "-J7S",
}


def get_delta_of_points(l: tuple[int, int], r: tuple[int, int]) -> tuple[int, int]:
    return (l[0] - r[0], l[1] - r[1])


def _pretty_print_map(parsed_map: dict[int, dict[int, str]]) -> None:
    for _, entry in parsed_map.items():
        print(" ".join(entry.values()))


def _pretty_print_path(path: list[tuple[int, int]]) -> None:
    if path:
        print(" -> ".join(map(str, path)))
    else:
        print(path)


def parse_map(path: str) -> tuple[tuple[int, int], dict[int, dict[int, str]]]:
    parsed_map: dict[int, dict[int, str]] = defaultdict(dict)
    starting_coordinates = (-1, -1)
    max_x = 0
    y_coordinate = 0
    for line in utils.yield_lines_from_path(path):
        x_coordinate = 0
        for char in line:
            if char == "\n":
                continue
            if char == STARTING_SYMBOL:
                starting_coordinates = (x_coordinate, y_coordinate)
            parsed_map[y_coordinate][x_coordinate] = char
            x_coordinate += 1
        y_coordinate += 1
        max_x = x_coordinate

    return (starting_coordinates, (max_x, y_coordinate), parsed_map)


def get_potential_next_points(
    target_point: tuple[int, int],
    target_symbol: str,
    previous_point: tuple[int, int],
    maxes: tuple[int, int],
) -> list[tuple[int, int]]:
    potential_points = [
        (target_point[0] + delta[0], target_point[1] + delta[1])
        for delta in COORD_DELTAS_TO_GET_CONNECTED_COORDS[target_symbol]
    ]
    potential_points_in_map_bounds = filter(
        lambda p: p[0] < maxes[0] and p[1] < maxes[1] and p[0] >= 0 and p[1] >= 0,
        potential_points,
    )
    potential_points_that_are_not_backwards = filter(
        lambda p: not (p[0] == previous_point[0] and p[1] == previous_point[1]),
        potential_points_in_map_bounds,
    )
    return list(potential_points_that_are_not_backwards)


def identify_loop(
    target_point: tuple[int, int],
    path_so_far: list[tuple[int, int]],
    parsed_map: dict[int, dict[int, str]],
    starting_point: tuple[int, int],
    maxes: tuple[int, int],
) -> list[tuple[int, int]] | None:
    # print(f"{len(path_so_far)} -> ", end="")
    target_symbol = parsed_map[target_point[1]][target_point[0]]
    if target_symbol == JUST_PLAIN_GROUND:
        return None
    if target_symbol == STARTING_SYMBOL:
        # print("S")
        return path_so_far
    # print(f"{target_symbol} -> ", end="")
    new_path_so_far = path_so_far.copy() + [target_point]
    potential_next_points = get_potential_next_points(
        target_point,
        target_symbol,
        path_so_far[-1],
        maxes,
    )
    compatible_next_points = filter(
        lambda p: parsed_map[p[1]][p[0]]
        in DELTA_COMPATIBLE_SYMBOL[get_delta_of_points(p, target_point)],
        potential_next_points,
    )
    potential_paths = [
        identify_loop(p, new_path_so_far, parsed_map, starting_point, maxes)
        for p in compatible_next_points
    ]
    return list(filter(None, potential_paths))[0]


# INPUT_PATH = "advent_code_2023/day-10/test-input.txt"
# INPUT_PATH = "advent_code_2023/day-10/test-input2.txt"
INPUT_PATH = "advent_code_2023/day-10/input.txt"


import sys

sys.setrecursionlimit(32000)

starting_coordinates, max_coordinates, parsed_map = parse_map(INPUT_PATH)
potential_paths = []
for p in get_potential_next_points(
    starting_coordinates, STARTING_SYMBOL, starting_coordinates, max_coordinates
):
    potential_path = identify_loop(
        p, [starting_coordinates], parsed_map, starting_coordinates, max_coordinates
    )
    if potential_path:
        # print(len(potential_path), end=" @ ")
        print(len(potential_path))
        # _pretty_print_path(potential_path)
        potential_paths.append(potential_path)

print("====================== ATTENTION =======================")
print(
    f"The point the furthest away is this many steps away: {max(*list(map(len, potential_paths)))/2}"
)
