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


def parse_race_record(path: str) -> list[RaceRecord]:
    lines = []
    with open(os.path.expanduser(path), "r") as input_file:
        lines = input_file.readlines()

    time = int("".join(filter(None, lines[0].split(":")[1].strip().split(" "))))
    distance = int("".join(filter(None, lines[1].split(":")[1].strip().split(" "))))

    return RaceRecord(time, distance)


record = parse_race_record(INPUT_PATH)
print("====================== ATTENTION =======================")
print(f"The margin of error is: {len(record.get_button_press_durations_to_beat())}")
