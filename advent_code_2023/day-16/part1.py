from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Optional
from typing import Self

from advent_code_2023 import utils


@dataclass(frozen=True, order=True)
class Moment:
    position: tuple[int, int]
    velocity: tuple[int, int]

    def __next__(self) -> Self:
        return Moment(
            (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1]),
            self.velocity,
        )

    def with_new_velocity(self, new_velocity: tuple[int, int]) -> Self:
        return Moment(self.position, new_velocity)


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


@dataclass
class MirrorContraptionMap:
    _the_map: list[str]
    _experienced_moments: set[Moment] = field(default_factory=set)

    def __str__(self) -> str:
        return "\n".join(self._the_map)

    def get_char_at_point(self, point: tuple[int, int]) -> Optional[str]:
        if not self.is_point_in_bounds(point):
            return None
        return self._the_map[point[1]][point[0]]

    def is_point_in_bounds(self, point: tuple[int, int]) -> bool:
        if point[0] < 0 or point[1] < 0:
            return False
        if point[0] >= len(self._the_map[0]) or point[1] >= len(self._the_map):
            return False
        return True

    def print_with_path_so_far(self, latest: Moment):
        for y, row in enumerate(self._the_map):
            something = defaultdict(int)
            for mo in self._experienced_moments:
                if mo.position[1] == y:
                    something[mo.position[0]] += 1
            for x, char in enumerate(row):
                if (x, y) == latest.position:
                    if something[x]:
                        print(
                            f"{color.BOLD}{color.YELLOW}{something[x]}{color.END}",
                            end="",
                        )
                    else:
                        print(f"{color.BOLD}{color.YELLOW}{char}{color.END}", end="")
                elif something[x] > 0:
                    print(f"{color.RED}{something[x]}{color.END}", end="")
                else:
                    print(char, end="")
            print()
        print(
            "============================================================================"
        )

    def mark_moment_visited(self, mo: Moment):
        self._experienced_moments.add(mo)

    def is_moment_visited(self, mo: Moment) -> bool:
        return mo in self._experienced_moments


class VelocityConstant(Enum):
    FROM_LEFT_TO_RIGHT = (1, 0)
    FROM_RIGHT_TO_LEFT = (-1, 0)
    FROM_TOP_TO_BOTTOM = (0, 1)
    FROM_BOTTOM_TO_TOP = (0, -1)


def calculate_new_velocity_for_mirror(
    velocity: tuple[int, int], mirror: str
) -> tuple[int, int]:
    if (velocity, mirror) in (
        (VelocityConstant.FROM_LEFT_TO_RIGHT.value, "/"),
        (VelocityConstant.FROM_RIGHT_TO_LEFT.value, "\\"),
    ):
        # -> / or \ <- ? Go up
        return (0, -1)
    if (velocity, mirror) in (
        (VelocityConstant.FROM_RIGHT_TO_LEFT.value, "/"),
        (VelocityConstant.FROM_LEFT_TO_RIGHT.value, "\\"),
    ):
        # -> \ or / <- ? Go down
        return (0, 1)
    if (velocity, mirror) in (
        (VelocityConstant.FROM_BOTTOM_TO_TOP.value, "/"),
        (VelocityConstant.FROM_TOP_TO_BOTTOM.value, "\\"),
    ):
        # /    |
        # ^    v
        # | or \ ? Go right
        return (1, 0)
    if (velocity, mirror) in (
        (VelocityConstant.FROM_TOP_TO_BOTTOM.value, "/"),
        (VelocityConstant.FROM_BOTTOM_TO_TOP.value, "\\"),
    ):
        # \    |
        # ^    v
        # | or / ? Go left
        return (-1, 0)
    print(f"{velocity} int '{mirror}'")
    exit(-1)


def get_new_moment_for_mirror(mo: Moment, mirror: str) -> Moment:
    return next(
        mo.with_new_velocity(calculate_new_velocity_for_mirror(mo.velocity, mirror))
    )


def get_new_moments_for_splitter(mo: Moment, splitter: str) -> list[Moment]:
    if (mo.velocity, splitter) in (
        (VelocityConstant.FROM_BOTTOM_TO_TOP.value, "|"),
        (VelocityConstant.FROM_TOP_TO_BOTTOM.value, "|"),
        (VelocityConstant.FROM_LEFT_TO_RIGHT.value, "-"),
        (VelocityConstant.FROM_RIGHT_TO_LEFT.value, "-"),
    ):
        # Pass through as if its not there
        return [next(mo)]
    if (mo.velocity, splitter) in (
        (VelocityConstant.FROM_LEFT_TO_RIGHT.value, "|"),
        (VelocityConstant.FROM_RIGHT_TO_LEFT.value, "|"),
    ):
        return [
            next(mo.with_new_velocity(VelocityConstant.FROM_BOTTOM_TO_TOP.value)),
            next(mo.with_new_velocity(VelocityConstant.FROM_TOP_TO_BOTTOM.value)),
        ]
    if (mo.velocity, splitter) in (
        (VelocityConstant.FROM_BOTTOM_TO_TOP.value, "-"),
        (VelocityConstant.FROM_TOP_TO_BOTTOM.value, "-"),
    ):
        return [
            next(mo.with_new_velocity(VelocityConstant.FROM_LEFT_TO_RIGHT.value)),
            next(mo.with_new_velocity(VelocityConstant.FROM_RIGHT_TO_LEFT.value)),
        ]
    print(f"{mo.velocity} int '{splitter}'")
    exit(-1)


import time


def _get_paths_from_moment(
    mo: Moment, path_so_far: list[Moment], contraption: MirrorContraptionMap
) -> list[list[Moment]]:
    if contraption.is_moment_visited(mo):
        # We've come to this point with the same velocity before
        return [path_so_far]
    char_at_point = contraption.get_char_at_point(mo.position)
    if not char_at_point:
        # We've hit the edge
        return [path_so_far]
    new_path_so_far = deepcopy(path_so_far)
    new_path_so_far.append(mo)
    contraption.mark_moment_visited(mo)
    if len(contraption._experienced_moments) % 1000 == 0:
        print(f"{len(contraption._experienced_moments)} moments experienced!!")
    # contraption.print_with_path_so_far(mo)
    # input()
    if char_at_point == ".":
        return _get_paths_from_moment(next(mo), new_path_so_far, contraption)
    if char_at_point in ("/", "\\"):
        return _get_paths_from_moment(
            get_new_moment_for_mirror(mo, char_at_point), new_path_so_far, contraption
        )
    if char_at_point in ("-", "|"):
        new_moments = get_new_moments_for_splitter(mo, char_at_point)
        if len(new_moments) > 1:
            paths = []
            for new_mo in new_moments:
                new_paths = _get_paths_from_moment(new_mo, new_path_so_far, contraption)
                for potentially_multiple_paths in new_paths:
                    if isinstance(potentially_multiple_paths[0], list):
                        for path in potentially_multiple_paths:
                            paths.append(path)
                    else:
                        paths.append(potentially_multiple_paths)
            return paths
        else:
            return _get_paths_from_moment(new_moments[0], new_path_so_far, contraption)


def get_energized_points_starting_at_point(
    contraption: MirrorContraptionMap,
    point: tuple[int, int],
    velocity: tuple[int, int] = (1, 0),
) -> set[tuple[int, int]]:
    paths = _get_paths_from_moment(Moment(point, velocity), [], contraption)
    unique_points = set()
    for path in paths:
        for mo in path:
            unique_points.add(mo.position)
    return unique_points


def parse_contraption_map(path: str) -> MirrorContraptionMap:
    raw_contraption_map: list[str] = []
    for line in utils.yield_lines_from_path(path):
        raw_contraption_map.append(line.strip())
    return MirrorContraptionMap(raw_contraption_map)


# INPUT_PATH = "advent_code_2023/day-16/test-input.txt"
INPUT_PATH = "advent_code_2023/day-16/input.txt"

import sys

sys.setrecursionlimit(32000)

contraption = parse_contraption_map(INPUT_PATH)
energized_points = get_energized_points_starting_at_point(contraption, (0, 0))

print("====================== ATTENTION =======================")
print(f"The number of energized tiles is: {len(energized_points)}")
