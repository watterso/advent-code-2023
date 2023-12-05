from dataclasses import dataclass

from advent_code_2023 import utils

INPUT_PATH = "advent_code_2023/day-04/input.txt"


@dataclass(frozen=True)
class ScratchCard:
    card_number: int
    winning_numbers: list[int]
    owned_numbers: list[int]

    def get_owned_winning_numbers(self) -> list[int]:
        # print(f"{self.winning_numbers} | {self.owned_numbers}")
        return list(filter(lambda x: x in self.winning_numbers, self.owned_numbers))


def _parse_number_list(number_list: str) -> list[int]:
    str_numbers = filter(None, number_list.strip().split(" "))
    return list(map(lambda x: int(x), str_numbers))


def parse_scratchcard_from_line(raw_line: str) -> ScratchCard:
    card_id_and_contents = raw_line.strip().split(":")
    winning_numbers_and_owned_numbers = card_id_and_contents[1].strip().split("|")
    # print(card_id_and_contents[0].split(" "))
    # print(_parse_number_list(winning_numbers_and_owned_numbers[0]))
    # print(_parse_number_list(winning_numbers_and_owned_numbers[1]))
    return ScratchCard(
        card_number=int(card_id_and_contents[0].split(" ")[-1]),
        winning_numbers=_parse_number_list(winning_numbers_and_owned_numbers[0]),
        owned_numbers=_parse_number_list(winning_numbers_and_owned_numbers[1]),
    )


card_values: list[int] = []

for line in utils.yield_lines_from_path(INPUT_PATH):
    card = parse_scratchcard_from_line(line)
    # print(card)
    owned_winning_numbers = card.get_owned_winning_numbers()
    # print(owned_winning_numbers)
    card_values.append(
        0 if len(owned_winning_numbers) == 0 else 2 ** (len(owned_winning_numbers) - 1)
    )

print("====================== ATTENTION =======================")
print(f"The card values add up to: {sum(card_values)}")
