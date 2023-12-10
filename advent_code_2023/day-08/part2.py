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


# INPUT_PATH = "advent_code_2023/day-08/test-input3.txt"
INPUT_PATH = "advent_code_2023/day-08/input.txt"

base_instruction, node_dict, starting_nodes = parse_input(INPUT_PATH)


step_count = 0
current_nodes = starting_nodes
for instruction in yield_instruction_forever(base_instruction):
    # print(f"{current_node} | {instruction}")
    # print(f"{current_node.name}", end="")
    if all(map(is_ending_node, current_nodes)):
        # print()
        break
    # print(f" -> ", end="")
    for index, node in enumerate(current_nodes):
        current_nodes[index] = node_dict[
            current_nodes[index].left_node_key
            if instruction == "L"
            else current_nodes[index].right_node_key
        ]
    step_count = step_count + 1

print("====================== ATTENTION =======================")
print(f"The Total Number of Steps is: {step_count}")
