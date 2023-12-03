from advent_code_2023 import utils

INPUT_PATH = "advent_code_2023/day-02/input.txt"


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


game_cube_powers: list[int] = []

for game_line in utils.yield_lines_from_path(INPUT_PATH):
    game_id_and_clue_samples = game_line.split(":")

    clue_samples = game_id_and_clue_samples[1].split(";")
    max_red, max_green, max_blue = (0, 0, 0)

    for raw_clue in clue_samples:
        red, green, blue = parse_clue_sample(raw_clue)
        max_red = max(red, max_red)
        max_green = max(green, max_green)
        max_blue = max(blue, max_blue)

    game_cube_powers.append(max_red * max_green * max_blue)

print("====================== ATTENTION =======================")
print(f"The possible Game IDs add up to: {sum(game_cube_powers)}")
