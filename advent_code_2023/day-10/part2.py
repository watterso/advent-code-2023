# parse
# TileSpace class
#   contains all the coords in its bounded space,
#   has a flag for if it is an outside TileSpace or an Insides
#   given a coord, return true or false in the space
# iterate throught char by char
#   for each char check if in an existing TileSpace,
#       if yes, continue
#       if no, BFS out-of-bounds or non-squeezable pipe, define appropriately flagged TileSpace add to list of TileSpaces
# Get size of all inside Tilespaces and sum them

from collections import defaultdict

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
    potential_paths = [
        identify_loop(p, new_path_so_far, parsed_map, starting_point, maxes)
        for p in get_potential_next_points(
            target_point,
            target_symbol,
            path_so_far[-1],
            maxes,
        )
    ]
    return list(filter(None, potential_paths))[0]


def get_main_loop_lookup_map(
    main_loop: list[tuple[int, int]]
) -> defaultdict[int, defaultdict[int, bool]]:
    _default_dict_generator = lambda: defaultdict(lambda: False)
    lookup_map = defaultdict(_default_dict_generator)
    for point in main_loop:
        lookup_map[point[1]][point[0]] = True
    return lookup_map


def _pretty_print_path(path: list[tuple[int, int]]) -> None:
    if path:
        print(" -> ".join(map(str, path)))
    else:
        print(path)


class PointSpace:
    _presence_map: defaultdict[int, defaultdict[int, bool]]
    _member_points: list[tuple[int, int]]
    touches_edge_of_map: bool

    def __init__(self, initial_point: tuple[int, int]):
        self.touches_edge_of_map = False
        self._member_points = [initial_point]
        _default_dict_generator = lambda: defaultdict(lambda: False)
        self._presence_map = defaultdict(_default_dict_generator)
        self._presence_map[initial_point[1]][initial_point[0]] = True

    def append_to_space(self, new_point: tuple[int, int]):
        self._member_points.append(new_point)
        self._presence_map[new_point[1]][new_point[0]] = True

    def is_point_in_space(self, new_point: tuple[int, int]) -> bool:
        return self._presence_map[new_point[1]][new_point[0]]

    def __iter__(self):
        return iter(self._member_points)

    def __len__(self):
        return len(self._member_points)


class MapSpaces:
    _presence_map: defaultdict[int, defaultdict[int, PointSpace]]
    _member_spaces: list[PointSpace]

    def __init__(self):
        self._member_spaces = []
        self._calculate_presence_map()

    def _calculate_presence_map(self):
        _default_dict_generator = lambda: defaultdict(lambda: False)
        lookup_map = defaultdict(_default_dict_generator)
        for space in self._member_spaces:
            for point in space:
                lookup_map[point[1]][point[0]] = space
        self._presence_map = lookup_map

    def append_a_new_space(self, new_space: PointSpace):
        self._member_spaces.append(new_space)
        self._calculate_presence_map()

    def is_point_already_visited(self, point: tuple[int, int]) -> bool:
        return bool(self._presence_map[point[1]][point[0]])


# INPUT_PATH = "advent_code_2023/day-10/test-input3.txt"
INPUT_PATH = "advent_code_2023/day-10/test-input4.txt"
# INPUT_PATH = "advent_code_2023/day-10/test-input5.txt"
# INPUT_PATH = "advent_code_2023/day-10/test-input6.txt"
# INPUT_PATH = "advent_code_2023/day-10/input.txt"


starting_coordinates, max_coordinates, parsed_map = parse_map(INPUT_PATH)


main_loop = []
for p in get_potential_next_points(
    starting_coordinates, STARTING_SYMBOL, starting_coordinates, max_coordinates
):
    potential_path = identify_loop(
        p, [starting_coordinates], parsed_map, starting_coordinates, max_coordinates
    )
    if potential_path:
        main_loop = potential_path
        break

_main_loop_lookup_map = get_main_loop_lookup_map(main_loop)
is_in_main_loop = lambda p: _main_loop_lookup_map[p[1]][p[0]]
# print(len(main_loop), end=" @ ")
# _pretty_print_path(main_loop)


def is_point_out_of_bounds(point: tuple[int, int], maxes: tuple[int, int]) -> bool:
    return point[0] < 0 or point[1] < 0 or point[0] > maxes[0] or point[1] > maxes[1]


def get_points_to_consider(point: tuple[int, int]) -> list[tuple[int, int]]:
    return [
        (point[0] + delta[0], point[1] + delta[1])
        for delta in ((0, -1), (0, 1), (-1, 0), (1, 0))
    ]


spaces = MapSpaces()

for y in range(0, max_coordinates[1]):
    for x in range(0, max_coordinates[0]):
        if is_in_main_loop((x, y)):
            continue
        if spaces.is_point_already_visited((x, y)):
            continue
        new_space = PointSpace((x, y))
        points_to_consider = get_points_to_consider((x, y))
        while points_to_consider:
            to_consider = points_to_consider.pop(0)
            if is_point_out_of_bounds(to_consider, max_coordinates):
                new_space.touches_edge_of_map = True
                continue
            if is_in_main_loop(to_consider):
                continue
            if new_space.is_point_in_space(to_consider):
                continue
            points_to_consider.extend(get_points_to_consider(to_consider))
            new_space.append_to_space(to_consider)
        spaces.append_a_new_space(new_space)

for space in spaces._member_spaces:
    print(f"{len(space)} | {space.touches_edge_of_map}")


# TODO check the squeeeeze through
# TODO check orphan nodes are also count as contained (should already be done)
