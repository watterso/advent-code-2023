import os.path
import typing
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class SymmetryDetails:
    index_of_char_before_reflection: int
    length_of_reflection: int


@dataclass(frozen=True)
class AshRockMap:
    by_columns: list[list[str]]
    by_rows: list[list[str]]

    def _get_symmetry(
        self, specific_list: list[list[str]]
    ) -> typing.Optional[SymmetryDetails]:
        symmmetry_counter = defaultdict(int)
        for row in specific_list:
            wa = find_symmetry_point_if_any(row)
            # print(wa)
            for s in wa:
                symmmetry_counter[s] += 1
        for key, value in symmmetry_counter.items():
            if value == len(specific_list):
                return key

    def get_hot_dog_symmetry(self) -> typing.Optional[SymmetryDetails]:
        return self._get_symmetry(self.by_rows)

    def get_hamburger_symmetry(self) -> typing.Optional[SymmetryDetails]:
        return self._get_symmetry(self.by_columns)


def parse_ash_rock_maps(path: str) -> list[AshRockMap]:
    ash_rock_maps: list[AshRockMap] = []
    with open(os.path.expanduser(path), "r") as input_file:
        list_of_rows: list[list[str]] = []
        list_of_columns: list[list[str]] = []
        line = input_file.readline()
        while line != "":
            while line not in ["\n", ""]:
                row_as_list = [char for char in line.strip()]
                if not list_of_columns:
                    list_of_columns = [[] for char in row_as_list]
                list_of_rows.append(row_as_list)
                for i, char in enumerate(row_as_list):
                    list_of_columns[i].append(char)
                line = input_file.readline()
            ash_rock_maps.append(AshRockMap(list_of_columns, list_of_rows))
            list_of_rows = []
            list_of_columns = []
            line = input_file.readline()

    return ash_rock_maps


def find_symmetry_point_if_any(string: list[str]) -> typing.Optional[SymmetryDetails]:
    symmetry_point = -1
    something = []
    for i in range(len(string) - 1):
        if string[i] == string[i + 1]:
            potential_length = min(i + 1, len(string) - (i + 1))
            left = string[max(i + 1 - potential_length, 0) : i + 1]
            right = string[i + 1 : i + 1 + potential_length]
            if False:
                print(f"[{i}] '{string[i]}' == [{i+1}] '{string[i+1]}' !")
                print(f"{i+1} >< {len(string)-(i+1)}")
                print(f"{potential_length}")
                print(
                    f"{left} ? {list(reversed(right))} | {left == list(reversed(right))}"
                )
            if left == list(reversed(right)):
                something.append(
                    SymmetryDetails(
                        i,
                        min(i, len(string) - i),
                    )
                )

    return something


# INPUT_PATH = "advent_code_2023/day-13/test-input.txt"
INPUT_PATH = "advent_code_2023/day-13/input.txt"

maps = parse_ash_rock_maps(INPUT_PATH)
summary_number = 0
for map in maps:
    # print("========= new map =========")
    # print(map.get_hot_dog_symmetry())
    # print(map.get_hamburger_symmetry())
    hot_dog = map.get_hot_dog_symmetry()
    if hot_dog:
        summary_number += hot_dog.index_of_char_before_reflection + 1
    hamburger = map.get_hamburger_symmetry()
    if hamburger:
        summary_number += 100 * (hamburger.index_of_char_before_reflection + 1)


print("====================== ATTENTION =======================")
print(f"The summary number is: {summary_number}")
