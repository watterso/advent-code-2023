from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
import os.path


def HASH(input_str: str) -> int:
    current_value = 0
    for char in input_str.strip():
        ascii_code = ord(char)
        current_value += ascii_code
        current_value *= 17
        current_value = current_value % 256
    return current_value


@dataclass(frozen=True)
class LabeledLens:
    label: str
    focal_length: int


@dataclass(frozen=True)
class ReplaceOrAppend:
    raw_label: str
    focal_length: int
    hashed_label: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "hashed_label", HASH(self.raw_label))


@dataclass(frozen=True)
class FindAndPop:
    raw_label: str
    hashed_label: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "hashed_label", HASH(self.raw_label))


def parse_instruction(raw_str: str) -> ReplaceOrAppend | FindAndPop:
    if raw_str[-1] == "-":
        return FindAndPop(raw_str[:-1])
    elif raw_str[-2] == "=":
        return ReplaceOrAppend(raw_str[:-2], int(raw_str[-1]))


def parse_init_sequence(path: str) -> list[ReplaceOrAppend | FindAndPop]:
    with open(os.path.expanduser(path), "r") as input_file:
        return list(map(parse_instruction, input_file.readline().strip().split(",")))


def get_get_index_of_label(lens_box: list[LabeledLens], label: str) -> int:
    for i, lens in enumerate(lens_box):
        if lens.label == label:
            return i


def get_lens_box_with_lens_replaced(
    lens_box: list[LabeledLens], index: int, lens: LabeledLens
) -> list[LabeledLens]:
    if index + 1 < len(lens_box):
        return lens_box[:index] + [lens] + lens_box[index + 1 :]
    return lens_box[:index] + [lens]


def _print_boxes(lens_boxes: dict[list[LabeledLens]]):
    for key, val in lens_boxes.items():
        # print(f"{key} | {val}")
        if val:
            print(f"Box {key}: {list(map(lambda l: f"{l.label} {l.focal_length}", val))}")

def calculate_focusing_power(box_number: int, index_in_box:int, focal_length: int) ->int:
    return (1+box_number) * (index_in_box +1) * focal_length

# INPUT_PATH = "advent_code_2023/day-15/test-input.txt"
INPUT_PATH = "advent_code_2023/day-15/input.txt"

init_sequence = parse_init_sequence(INPUT_PATH)
lens_boxes = defaultdict(list)
for instruction in init_sequence:
    potential_index = get_get_index_of_label(
        lens_boxes[instruction.hashed_label], instruction.raw_label
    )
    if isinstance(instruction, ReplaceOrAppend):
        the_lens = LabeledLens(instruction.raw_label, instruction.focal_length)
        if potential_index is not None:
            lens_boxes[instruction.hashed_label] = get_lens_box_with_lens_replaced(
                lens_boxes[instruction.hashed_label],
                potential_index,
                the_lens,
            )
        else:
            lens_boxes[instruction.hashed_label] = lens_boxes[
                instruction.hashed_label
            ] + [the_lens]
    elif isinstance(instruction, FindAndPop) and potential_index is not None:
        lens_boxes[instruction.hashed_label].pop(potential_index)
    # print(f"After '{instruction}'")
    # _print_boxes(lens_boxes)
total_focus_power = 0
for box_number, lens_box in dict(lens_boxes).items():
    for lens_index, lens in enumerate(lens_box):
        total_focus_power += calculate_focusing_power(box_number, lens_index, lens.focal_length)

print("====================== ATTENTION =======================")
print(f"The summary number is: {total_focus_power}")
