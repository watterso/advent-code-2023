from dataclasses import dataclass
import os.path

# INPUT_PATH = "advent_code_2023/day-06/test-input.txt"
INPUT_PATH = "advent_code_2023/day-06/input.txt"


@dataclass(frozen=True)
class RaceRecord:
    time_for_race: int
    distance: int

    def get_button_press_durations_to_beat(self) -> list[int]:
        durations = []
        for i in range(self.time_for_race):
            if i * (self.time_for_race - i) > self.distance:
                durations.append(i)
        return durations


def parse_race_records(path: str) -> list[RaceRecord]:
    lines = []
    with open(os.path.expanduser(path), "r") as input_file:
        lines = input_file.readlines()

    times = map(int, filter(None, lines[0].split(":")[1].strip().split(" ")))
    distances = map(int, filter(None, lines[1].split(":")[1].strip().split(" ")))

    return [RaceRecord(*pair) for pair in zip(times, distances)]


records = parse_race_records(INPUT_PATH)
running_multiplication = 1
for r in records:
    running_multiplication = running_multiplication * len(
        r.get_button_press_durations_to_beat()
    )

print("====================== ATTENTION =======================")
print(f"The margin of error is: {running_multiplication}")
