from collections import defaultdict
from dataclasses import dataclass
import typing

from advent_code_2023 import utils


@dataclass(frozen=True)
class CamelMapNode:
    name: str
    left_node_key: str
    right_node_key: str


def is_starting_node(node: CamelMapNode) -> bool:
    return node.name[-1] == "A"


def is_ending_node(node: CamelMapNode) -> bool:
    return node.name[-1] == "Z"


def yield_instruction_forever(
    base_instruction: str,
) -> typing.Generator[str, None, None]:
    current_index = 0
    instruction_length = len(base_instruction)
    # print(f"'{base_instruction}' | {instruction_length}")
    while True:
        if current_index == instruction_length:
            current_index = 0
        yield base_instruction[current_index]
        current_index = current_index + 1


def _parse_node_line(raw_line: str) -> CamelMapNode:
    name = raw_line.split("=")[0].strip()
    left, right = raw_line.split("=")[1].strip().strip("()").split(",")
    return CamelMapNode(name, left.strip(), right.strip())


def parse_input(path: str) -> tuple[str, dict[str, CamelMapNode]]:
    line_generator = utils.yield_lines_from_path(path)
    base_instruction = next(line_generator).strip()
    next(line_generator)  # skip blank line after instruction
    nodes: dict[str, CamelMapNode] = {}
    starting_nodes: list[CamelMapNode] = []
    for raw_line in line_generator:
        new_node = _parse_node_line(raw_line)
        nodes[new_node.name] = new_node
        if is_starting_node(new_node):
            starting_nodes.append(new_node)
    return (base_instruction, nodes, starting_nodes)


def get_deltas(step_counts: list[int]) -> list[int]:
    oot = [0]
    for i in range(1, len(step_counts)):
        oot.append(step_counts[i] - step_counts[i - 1])
    return oot


def get_prime_factors_for_number(number: int) -> list[int]:
    current_divisor = 2
    prime_factors = []

    while current_divisor * current_divisor <= number:
        if number % current_divisor:
            current_divisor += 1
        else:
            number = number / current_divisor
            prime_factors.append(current_divisor)
    if number > 1:
        prime_factors.append(number)
    return prime_factors


# INPUT_PATH = "advent_code_2023/day-08/test-input3.txt"
INPUT_PATH = "advent_code_2023/day-08/input.txt"
NUMBER_OF_DESTINATION_ITERS = 0

base_instruction, node_dict, starting_nodes = parse_input(INPUT_PATH)


step_count = 0
current_nodes = starting_nodes
node_hit_destination_count = defaultdict(int)
node_when_hit_destination_count = defaultdict(list)
for instruction in yield_instruction_forever(base_instruction):
    # print(f"{current_node} | {instruction}")
    # print(f"{current_node.name}", end="")
    if not current_nodes:
        # print()
        break
    # print(f" -> ", end="")
    indices_to_pop = []
    for index, node in enumerate(current_nodes):
        if is_ending_node(node):
            node_hit_destination_count[node] = node_hit_destination_count[node] + 1
            node_when_hit_destination_count[node].append(step_count)
            if node_hit_destination_count[node] > NUMBER_OF_DESTINATION_ITERS:
                indices_to_pop.append(index)
        current_nodes[index] = node_dict[
            node.left_node_key if instruction == "L" else node.right_node_key
        ]
    for i in sorted(indices_to_pop, reverse=True):
        current_nodes.pop(i)
    step_count = step_count + 1

unique_prime_factors = set()
for key, val in node_when_hit_destination_count.items():
    print(f"{key.name} | {val[0]} | {get_prime_factors_for_number(val[0])}")
    unique_prime_factors.update(get_prime_factors_for_number(val[0]))

number_of_steps = 1
for number in unique_prime_factors:
    number_of_steps *= number
print("====================== ATTENTION =======================")
print(f"The Total Number of Steps is: {number_of_steps}")
