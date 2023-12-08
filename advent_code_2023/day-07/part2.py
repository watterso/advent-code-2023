from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
import typing

from advent_code_2023 import utils


@total_ordering
class CamelCard(Enum):
    A = 14
    K = 13
    Q = 12
    T = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    J = 1

    def __lt__(self, other: typing.Self) -> bool:
        return self.value < other.value

    def __eq__(self, other: typing.Self) -> bool:
        return self.value == other.value

    def __hash__(self) -> int:
        return super().__hash__()


CAMEL_CARD_PARSING_MAP = {
    "A": CamelCard.A,
    "K": CamelCard.K,
    "Q": CamelCard.Q,
    "J": CamelCard.J,
    "T": CamelCard.T,
    "9": CamelCard.NINE,
    "8": CamelCard.EIGHT,
    "7": CamelCard.SEVEN,
    "6": CamelCard.SIX,
    "5": CamelCard.FIVE,
    "4": CamelCard.FOUR,
    "3": CamelCard.THREE,
    "2": CamelCard.TWO,
}


@total_ordering
class CamelCardHandStrength(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __lt__(self, other: typing.Self) -> bool:
        return self.value < other.value

    def __eq__(self, other: typing.Self) -> bool:
        return self.value == other.value


@dataclass(frozen=True)
@total_ordering
class CamelCardHand:
    strength: CamelCardHandStrength
    cards: tuple[CamelCard, CamelCard, CamelCard, CamelCard, CamelCard]
    bid: int

    def __lt__(self, other: typing.Self) -> bool:
        if self.strength > other.strength:
            return False
        elif self.strength < other.strength:
            return True
        # print(f"{self.cards} vs {other.cards}")
        for my_card, their_card in zip(self.cards, other.cards):
            # print(f"{my_card} ? {their_card}:", end=" ")
            if my_card == their_card:
                # print(f"Equal")
                continue
            if my_card < their_card:
                # print(f"Less")
                return True
            elif my_card > their_card:
                # print(f"Greater")
                return False

        # print(f"Greater")
        return False

    def __eq__(self, other: typing.Self) -> bool:
        return self.strength == other.strength and self.cards == other.cards


def _parse_hand_card_str(
    hand_str: str,
) -> tuple[CamelCard, CamelCard, CamelCard, CamelCard, CamelCard]:
    cards = []
    for char in hand_str:
        cards.append(CAMEL_CARD_PARSING_MAP[char])
    return tuple(cards)


def calculate_hand_strength(
    cards: tuple[CamelCard, CamelCard, CamelCard, CamelCard, CamelCard]
) -> CamelCardHandStrength:
    card_to_count = defaultdict(int)
    for card in cards:
        card_to_count[card] = card_to_count[card] + 1

    card_counts = sorted(card_to_count.items(), key=lambda x: x[1], reverse=True)
    unique_cards = len(card_counts)
    number_of_wild_cards = card_to_count[CamelCard.J]
    if unique_cards == 1:
        return CamelCardHandStrength.FIVE_OF_A_KIND
    if unique_cards == 2:
        if card_counts[1][1] == 1:
            # If there is only one card of the second most frequent card
            # when there are 2 unique cards, that implies 4 of a kind.
            if number_of_wild_cards == 4:
                return CamelCardHandStrength.FIVE_OF_A_KIND
            if number_of_wild_cards == 1:
                return CamelCardHandStrength.FIVE_OF_A_KIND
            return CamelCardHandStrength.FOUR_OF_A_KIND
        if card_counts[1][1] == 2:
            # If there are two cards of the second most frequent card
            # when there are 2 unique cards, that implies full house.
            if number_of_wild_cards == 3:
                return CamelCardHandStrength.FIVE_OF_A_KIND
            if number_of_wild_cards == 2:
                return CamelCardHandStrength.FIVE_OF_A_KIND
            return CamelCardHandStrength.FULL_HOUSE
    if unique_cards == 3:
        if card_counts[1][1] == 1:
            # If there is only one card of the second most frequent card
            # when there are 3 unique cards, that implies 3 of a kind and two different cards.
            if number_of_wild_cards == 3:
                return CamelCardHandStrength.FOUR_OF_A_KIND
            if number_of_wild_cards == 1:
                return CamelCardHandStrength.FOUR_OF_A_KIND
            return CamelCardHandStrength.THREE_OF_A_KIND
        if card_counts[1][1] == 2:
            # If there are two cards of the second most frequent card
            # when there are 3 unique cards, then there is another pair and a single card.
            if number_of_wild_cards == 2:
                return CamelCardHandStrength.FOUR_OF_A_KIND
            if number_of_wild_cards == 1:
                return CamelCardHandStrength.FULL_HOUSE
            return CamelCardHandStrength.TWO_PAIR
    if unique_cards == 4:
        if card_counts[0][1] == 2:
            # If the most frequent card has 2 cards, thats one pair!
            if number_of_wild_cards == 1:
                return CamelCardHandStrength.THREE_OF_A_KIND
            if number_of_wild_cards == 2:
                return CamelCardHandStrength.THREE_OF_A_KIND
            return CamelCardHandStrength.ONE_PAIR

    if number_of_wild_cards == 1:
        return CamelCardHandStrength.ONE_PAIR
    return CamelCardHandStrength.HIGH_CARD


def parse_hands(path: str) -> list[CamelCardHand]:
    hands = []
    for raw_line in utils.yield_lines_from_path(path):
        cards = _parse_hand_card_str(raw_line.strip().split(" ")[0])
        bid = int(raw_line.strip().split(" ")[1])
        strength = calculate_hand_strength(cards)
        if False:  # CamelCard.J in cards:
            print(", ".join(map(lambda x: x.name, cards)) + f" - {strength.name}")
            input()
        hands.append(CamelCardHand(strength, cards, bid))
    return hands


# INPUT_PATH = "advent_code_2023/day-07/test-input.txt"
INPUT_PATH = "advent_code_2023/day-07/input.txt"

hands = parse_hands(INPUT_PATH)
hands = sorted(hands)

rank_counter = 1
total_winnings_accumulator = 0
for h in hands:
    # print(
    #     f"{h.strength} w/ {h.cards}: {rank_counter} * {h.bid} = {rank_counter * h.bid}"
    # )
    total_winnings_accumulator = total_winnings_accumulator + (rank_counter * h.bid)
    rank_counter = rank_counter + 1

print("====================== ATTENTION =======================")
print(f"The Total Winnings are: {total_winnings_accumulator}")
