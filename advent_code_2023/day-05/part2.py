"""    (  )   /\   _                 (     
    \ |  (  \ ( \.(               )                      _____
  \  \ \  `  `   ) \             (  ___                 / _   \
 (_`    \+   . x  ( .\            \/   \____-----------/ (o)   \_
- .-               \+  ;          (  O                           \____
                          )        \_____________  `              \  /
(__                +- .( -'.- <. - _  VVVVVVV VV V\                 \/
(_____            ._._: <_ - <- _  (--  _AAAAAAA__A_/                  |
  .    /./.+-  . .- /  +--  - .     \______________//_              \_______
  (__ ' /x  / x _/ (                                  \___'          \     /
 , x / ( '  . / .  /                                      |           \   /
    /  /  _/ /    +                                      /              \/
   '  (__/                                             /                  \ 
   
This isn't actually the solution, check part2_electric_boogaloo
      
"""


from dataclasses import dataclass
from itertools import chain
import importlib

helpers = importlib.import_module("advent_code_2023.day-05.helpers")

INPUT_PATH = "advent_code_2023/day-05/test-input.txt"
# INPUT_PATH = "advent_code_2023/day-05/input.txt"


def print_with_arrow(c):
    print(f"{c:02d} -> ", end="")


@dataclass(frozen=True, order=True)
class ListDefinition:
    range_start: int
    range_length: int


class FrozenLazyIntList:
    list_defs: list[ListDefinition]

    def __init__(self, seed_list: list[int]):
        list_defs = []
        for i in range(0, len(seed_list), 2):
            list_defs.append(ListDefinition(seed_list[i], seed_list[i + 1]))
        self.list_defs = sorted(list_defs)

    def __contains__(self, item: int) -> bool:
        for defintion in self.list_defs:
            if item < defintion.range_start:
                return False
            if item in range(
                defintion.range_start, defintion.range_start + defintion.range_length
            ):
                return True

        return False

    def __len__(self) -> int:
        return sum([l.range_length for l in self.list_defs])

    def __iter__(self):
        return chain(
            *[
                range(
                    defintion.range_start,
                    defintion.range_start + defintion.range_length,
                )
                for defintion in self.list_defs
            ]
        )


class AlmanacLocationToSeedDFS:
    seeds: FrozenLazyIntList
    soil_to_seed: helpers.FrozenLazyIntToIntMapping
    fertilizer_to_soil: helpers.FrozenLazyIntToIntMapping
    water_to_fertilizer: helpers.FrozenLazyIntToIntMapping
    light_to_water: helpers.FrozenLazyIntToIntMapping
    temperature_to_light: helpers.FrozenLazyIntToIntMapping
    humidity_to_temperature: helpers.FrozenLazyIntToIntMapping
    location_to_humidity: helpers.FrozenLazyIntToIntMapping

    def __init__(self, part1_almanac: helpers.ParsedAlmanac):
        self.seeds = FrozenLazyIntList(part1_almanac.seeds)
        self.soil_to_seed = part1_almanac.seed_to_soil.get_reverse_mapping()
        self.fertilizer_to_soil = part1_almanac.soil_to_fertilizer.get_reverse_mapping()
        self.water_to_fertilizer = (
            part1_almanac.fertilizer_to_water.get_reverse_mapping()
        )
        self.light_to_water = part1_almanac.water_to_light.get_reverse_mapping()
        self.temperature_to_light = (
            part1_almanac.light_to_temperature.get_reverse_mapping()
        )
        self.humidity_to_temperature = (
            part1_almanac.temperature_to_humidity.get_reverse_mapping()
        )
        self.location_to_humidity = (
            part1_almanac.humidity_to_location.get_reverse_mapping()
        )

    def solve(self) -> int:
        for location in self.location_to_humidity:
            print_with_arrow(location)
            humidity = self.location_to_humidity[location]
            print_with_arrow(humidity)
            temperature = self.humidity_to_temperature[humidity]
            print_with_arrow(temperature)
            light = self.temperature_to_light[temperature]
            print_with_arrow(light)
            water = self.light_to_water[light]
            print_with_arrow(water)
            fertilizer = self.water_to_fertilizer[water]
            print_with_arrow(fertilizer)
            soil = self.fertilizer_to_soil[fertilizer]
            print_with_arrow(soil)
            potential_seed = self.soil_to_seed[fertilizer]
            if potential_seed in self.seeds:
                print(potential_seed)
                return potential_seed
            else:
                print("XX")

        return -1

    def solve1(self) -> int:
        print(self.location_to_humidity.mapping_defs)
        print(self.humidity_to_temperature.mapping_defs)
        print(self.temperature_to_light.mapping_defs)
        print(self.light_to_water.mapping_defs)
        print(self.water_to_fertilizer.mapping_defs)
        for location in self.location_to_humidity:
            print()
            print_with_arrow(location)
            if self.location_to_humidity[location] in self.humidity_to_temperature:
                humidity = self.location_to_humidity[location]
                print_with_arrow(humidity)
                if self.humidity_to_temperature[humidity] in self.temperature_to_light:
                    temperature = self.humidity_to_temperature[humidity]
                    print_with_arrow(temperature)
                    if self.temperature_to_light[temperature] in self.light_to_water:
                        light = self.temperature_to_light[temperature]
                        print_with_arrow(light)
                        if location == 46:
                            self.water_to_fertilizer.pretty_print()
                        if self.light_to_water[light] in self.water_to_fertilizer:
                            water = self.light_to_water[light]
                            print_with_arrow(water)
                            if (
                                self.water_to_fertilizer[water]
                                in self.fertilizer_to_soil
                            ):
                                fertilizer = self.water_to_fertilizer[water]
                                print_with_arrow(fertilizer)
                                if (
                                    self.fertilizer_to_soil[fertilizer]
                                    in self.soil_to_seed
                                ):
                                    soil = self.fertilizer_to_soil[fertilizer]
                                    print_with_arrow(soil)
                                    if self.soil_to_seed[soil] in self.seeds:
                                        return self.soil_to_seed[soil]
        return -1


part1_almanac = helpers.parse_file(INPUT_PATH)
min_location = 99999999999999999999999999999999999999999999999999999999999999999999
dfs = AlmanacLocationToSeedDFS(part1_almanac)
for i in dfs.seeds:
    location = part1_almanac.get_location_for_seed(i)
    min_location = min(min_location, location)


print("====================== ATTENTION =======================")
print(f"The lowest location is: {min_location}")


# print(dfs.solve1())
# print(part1_almanac.humidity_to_location.mapping_defs)
# print([i for i in part1_almanac.humidity_to_location])
# part1_almanac.humidity_to_location.pretty_print()
# print()
# print(dfs.location_to_humidity.mapping_defs)
# print([i for i in dfs.location_to_humidity])
# dfs.location_to_humidity.pretty_print()


# Refined Target Seed Range: [range(3630312398, 3636923144), range(3673953799, 3674442872)]
# Refined Target Seed Range: [range(3630312398, 3636923144), range(3673953799, 3674442872)]
# Refined Target Seed Range: [range(3630312398, 3636923144), range(3673953799, 3674442872)]
# Refined Target Seed Range: [range(3894936731, 3898796985)]
# 82 -> 84 -> 84 -> 84 -> 77 -> 45 -> 46 -> 46
