from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field

from advent_code_2023 import utils


def _print_cosmic_image(cosmic_image: list[list[str]], point_separator=""):
    for row in cosmic_image:
        print(point_separator.join(row))


@dataclass(frozen=True)
class GalaxyPair:
    alpha_galaxy: tuple[int, int]
    sigma_galaxy: tuple[int, int]
    path_length: int = field(init=False)

    def __post_init__(self):
        x_component = max(self.alpha_galaxy[0], self.sigma_galaxy[0]) - min(
            self.alpha_galaxy[0], self.sigma_galaxy[0]
        )
        y_component = max(self.alpha_galaxy[1], self.sigma_galaxy[1]) - min(
            self.alpha_galaxy[1], self.sigma_galaxy[1]
        )
        object.__setattr__(self, "path_length", x_component + y_component)

    def includes_this_galaxy(self, galaxy: tuple[int, int]) -> bool:
        return galaxy in [self.alpha_galaxy, self.sigma_galaxy]


def parse_cosmic_image(path: str) -> list[list[str]]:
    parsed_cosmic_image: list[list[str]] = []
    for line in utils.yield_lines_from_path(path):
        row = []
        for char in line:
            if char == "\n":
                continue
            row.append(char)
        parsed_cosmic_image.append(row)
    return parsed_cosmic_image


def get_empty_row_and_column_indices(
    cosmic_image: list[list[str]],
) -> tuple[list[int], list[int]]:
    empty_row_indices = []
    for i, row in enumerate(cosmic_image):
        if all(map(lambda c: c == ".", row)):
            empty_row_indices.append(i)

    empty_column_indices = []
    for column_index in range(len(cosmic_image[0])):
        column_values = []
        for row in cosmic_image:
            column_values.append(row[column_index])
        if all(map(lambda c: c == ".", column_values)):
            empty_column_indices.append(column_index)

    return (
        sorted(empty_column_indices, reverse=True),
        sorted(empty_row_indices, reverse=True),
    )


def _generate_empty_row_list(size: int) -> list[str]:
    row_list = []
    for i in range(size):
        row_list.append(".")
    return row_list


def compensate_for_gravity_expansion(cosmic_image: list[list[str]]) -> list[list[str]]:
    empty_column_indices, empty_row_indices = get_empty_row_and_column_indices(
        cosmic_image
    )
    cosmic_list = []
    for row in cosmic_image:
        new_row = row.copy()
        for i in empty_column_indices:
            new_row.insert(i, ".")
        cosmic_list.append(new_row)

    for i in empty_row_indices:
        cosmic_list.insert(i, _generate_empty_row_list(len(cosmic_list[0])))
    return cosmic_list


def get_locations_of_galaxies(cosmic_image: list[list[str]]) -> list[tuple[int, int]]:
    galaxy_locations: list[tuple[int, int]] = []
    for y, row in enumerate(cosmic_image):
        for x, char in enumerate(row):
            if char == "#":
                galaxy_locations.append((x, y))
    return galaxy_locations


def generate_galaxy_pairs_from_locations(
    galaxy_locations: list[tuple[int, int]]
) -> list[GalaxyPair]:
    galaxy_locations_for_processing = deepcopy(galaxy_locations)
    galaxy_pairs = []
    while galaxy_locations_for_processing:
        new_galaxy = galaxy_locations_for_processing.pop(0)
        for galaxy in galaxy_locations_for_processing:
            galaxy_pairs.append(GalaxyPair(new_galaxy, galaxy))
    return galaxy_pairs


INPUT_PATH = "advent_code_2023/day-11/test-input.txt"
# INPUT_PATH = "advent_code_2023/day-11/input.txt"

cosmic_image = parse_cosmic_image(INPUT_PATH)
compensated_image = compensate_for_gravity_expansion(cosmic_image)
galaxy_locations = get_locations_of_galaxies(compensated_image)
galaxy_pairs = generate_galaxy_pairs_from_locations(galaxy_locations)

print("====================== ATTENTION =======================")
print(
    f"The sum of galaxy lengths is: {sum(map(lambda g: g.path_length, galaxy_pairs))}"
)
