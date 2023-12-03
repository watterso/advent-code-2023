from advent_code_2023 import utils

INPUT_PATH = "advent_code_2023/day-02/input.txt"

RED_MAX = 12
GREEN_MAX = 13
BLUE_MAX = 14


def is_clue_sample_possible(red_count: int, green_count: int, blue_count: int) -> bool:
    # print(f'{red_count}, {green_count}, {blue_count} is ', end='')
    return red_count <= RED_MAX and green_count <= GREEN_MAX and blue_count <= BLUE_MAX


def parse_clue_sample(raw_clue: str) -> (int, int, int):
    unparsed_color_counts = raw_clue.split(",")
    red_count, green_count, blue_count = (0, 0, 0)
    for color_count in unparsed_color_counts:
        number_and_color = color_count.strip().split(" ")
        # print(number_and_color)
        if number_and_color[1] == "red":
            red_count = int(number_and_color[0])
        if number_and_color[1] == "green":
            green_count = int(number_and_color[0])
        if number_and_color[1] == "blue":
            blue_count = int(number_and_color[0])
    return (red_count, green_count, blue_count)


possible_games: list[int] = []

for game_line in utils.yield_lines_from_path(INPUT_PATH):
    game_id_and_clue_samples = game_line.split(":")
    game_id = int(game_id_and_clue_samples[0].split(" ")[1])

    clue_samples = game_id_and_clue_samples[1].split(";")
    game_is_possible = True
    for raw_clue in clue_samples:
        if not is_clue_sample_possible(*parse_clue_sample(raw_clue)):
            # print('not possible')
            game_is_possible = False
            break
        # print('possible!')

    if game_is_possible:
        possible_games.append(game_id)

print("====================== ATTENTION =======================")
print(f"The possible Game IDs add up to: {sum(possible_games)}")
