from collections import defaultdict
from dataclasses import dataclass
import typing

from advent_code_2023 import utils

# INPUT_PATH = "advent_code_2023/day-04/test-input.txt"
INPUT_PATH = "advent_code_2023/day-04/input.txt"


@dataclass(frozen=True)
class CardToSpawn:
    target_card_number: int
    originating_card_number: int


@dataclass(frozen=True)
class ScratchCard:
    card_number: int
    originating_card_number: int
    winning_numbers: list[int]
    owned_numbers: list[int]

    def get_owned_winning_numbers(self) -> list[int]:
        # print(f"{self.winning_numbers} | {self.owned_numbers}")
        return list(filter(lambda x: x in self.winning_numbers, self.owned_numbers))

    def get_cards_to_spawn(self) -> list[CardToSpawn]:
        owned_winning_numbers = card.get_owned_winning_numbers()
        cards_to_spawn = []
        if owned_winning_numbers:
            for i in range(1, len(owned_winning_numbers) + 1):
                cards_to_spawn.append(
                    CardToSpawn(self.card_number + i, self.card_number)
                )
        return cards_to_spawn

    def spawn_card(self, spawn_details: CardToSpawn) -> typing.Self:
        return ScratchCard(
            self.card_number,
            spawn_details.originating_card_number,
            self.winning_numbers,
            self.owned_numbers,
        )


def _generate_score_breakdown(cards: list[ScratchCard]) -> dict[int, int]:
    out = defaultdict(int)
    for c in cards:
        out[c.card_number] += 1
    return out


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
        originating_card_number=-1,
        winning_numbers=_parse_number_list(winning_numbers_and_owned_numbers[0]),
        owned_numbers=_parse_number_list(winning_numbers_and_owned_numbers[1]),
    )


cards: list[ScratchCard] = []
cards_to_spawn_map: dict[int, list[CardToSpawn]] = defaultdict(list)

for line in utils.yield_lines_from_path(INPUT_PATH):
    originating_card = parse_scratchcard_from_line(line)
    cards_to_spawn = (
        cards_to_spawn_map.pop(originating_card.card_number)
        if originating_card.card_number in cards_to_spawn_map
        else []
    )
    cards_to_process = [originating_card] + [
        originating_card.spawn_card(c) for c in cards_to_spawn
    ]
    # print(f"{originating_card.card_number} | {len(cards_to_process)}")
    cards_to_add_to_spawn_list: list[CardToSpawn] = []
    for card in cards_to_process:
        cards_to_add_to_spawn_list.extend(card.get_cards_to_spawn())
        cards.append(card)

    for spawn_card in cards_to_add_to_spawn_list:
        # print(spawn_card, end="")
        cards_to_spawn_map[spawn_card.target_card_number].append(spawn_card)
    # print()

# print(f"{_generate_score_breakdown(cards)}")
print("====================== ATTENTION =======================")
print(f"The number of cards after scoring is: {len(cards)}")
