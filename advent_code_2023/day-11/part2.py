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

    def get_min_coords_and_max_coords(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return (
            (
                min(self.alpha_galaxy[0], self.sigma_galaxy[0]),
                min(self.alpha_galaxy[1], self.sigma_galaxy[1]),
            ),
            (
                max(self.alpha_galaxy[0], self.sigma_galaxy[0]),
                max(self.alpha_galaxy[1], self.sigma_galaxy[1]),
            ),
        )


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


def compensate_galaxy_pairs(
    galaxy_pairs: list[GalaxyPair], empty_column_indices, empty_row_indices
) -> list[GalaxyPair]:
    compensated_pairs = []
    HOW_MANY_YOU_WANT_THERE_TO_BE = 1000000
    HOW_MANY_SPACES_TO_ADD = HOW_MANY_YOU_WANT_THERE_TO_BE - 1

    for g in galaxy_pairs:
        min_coords, max_coords = g.get_min_coords_and_max_coords()
        column_padding = HOW_MANY_SPACES_TO_ADD * len(
            list(
                filter(
                    None,
                    map(
                        lambda x: x > min_coords[0] and x < max_coords[0],
                        empty_column_indices,
                    ),
                )
            )
        )
        row_padding = HOW_MANY_SPACES_TO_ADD * len(
            list(
                filter(
                    None,
                    map(
                        lambda y: y > min_coords[1] and y < max_coords[1],
                        empty_row_indices,
                    ),
                )
            )
        )
        compensated_pairs.append(
            GalaxyPair(
                min_coords,
                (max_coords[0] + column_padding, max_coords[1] + row_padding),
            )
        )
    return compensated_pairs


# INPUT_PATH = "advent_code_2023/day-11/test-input.txt"
INPUT_PATH = "advent_code_2023/day-11/input.txt"

cosmic_image = parse_cosmic_image(INPUT_PATH)
empty_column_indices, empty_row_indices = get_empty_row_and_column_indices(cosmic_image)
galaxy_locations = get_locations_of_galaxies(cosmic_image)
galaxy_pairs = generate_galaxy_pairs_from_locations(galaxy_locations)
compensated_galaxy_pairs = compensate_galaxy_pairs(
    galaxy_pairs, empty_column_indices, empty_row_indices
)

print("====================== ATTENTION =======================")
print(
    f"The sum of galaxy lengths is: {sum(map(lambda g: g.path_length, compensated_galaxy_pairs))}"
)
