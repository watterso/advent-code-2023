from dataclasses import dataclass
from itertools import chain
import os.path
import typing


@dataclass(frozen=True, order=True)
class MappingDefinition:
    source_range_start: int
    destination_range_start: int
    range_length: int

    def reverse(self) -> typing.Self:
        return MappingDefinition(
            source_range_start=self.destination_range_start,
            destination_range_start=self.source_range_start,
            range_length=self.range_length,
        )

    def to_source_range(self) -> range:
        return range(
            self.source_range_start, self.source_range_start + self.range_length
        )

    def to_destination_range(self) -> range:
        return range(
            self.destination_range_start,
            self.destination_range_start + self.range_length,
        )


class FrozenLazyIntToIntMapping:
    mapping_defs: list[MappingDefinition]

    def __init__(self, definitions: list[MappingDefinition]):
        self.mapping_defs = sorted(definitions)

    def __getitem__(self, key: int) -> int:
        for definition in self.mapping_defs:
            if key < definition.source_range_start:
                return key
            if key in range(
                definition.source_range_start,
                definition.source_range_start + definition.range_length,
            ):
                return (
                    key - definition.source_range_start
                ) + definition.destination_range_start

        return key

    def get_reverse_mapping(self):
        return FrozenLazyIntToIntMapping(
            [
                MappingDefinition(
                    m.destination_range_start, m.source_range_start, m.range_length
                )
                for m in self.mapping_defs
            ]
        )

    def __iter__(self):
        return chain(
            range(0, self.mapping_defs[0].source_range_start),
            *[
                range(
                    defintion.source_range_start,
                    defintion.source_range_start + defintion.range_length,
                )
                for defintion in self.mapping_defs
            ],
        )

    def pretty_print(self):
        for i in self:
            print(f"{i} -> {self[i]}")


@dataclass(frozen=True)
class ParsedAlmanac:
    seeds: list[int]
    seed_to_soil: FrozenLazyIntToIntMapping
    soil_to_fertilizer: FrozenLazyIntToIntMapping
    fertilizer_to_water: FrozenLazyIntToIntMapping
    water_to_light: FrozenLazyIntToIntMapping
    light_to_temperature: FrozenLazyIntToIntMapping
    temperature_to_humidity: FrozenLazyIntToIntMapping
    humidity_to_location: FrozenLazyIntToIntMapping

    def get_location_for_seed(self, seed: int) -> int:
        soil = self.seed_to_soil[seed]
        fertilizer = self.soil_to_fertilizer[soil]
        water = self.fertilizer_to_water[fertilizer]
        light = self.water_to_light[water]
        temperature = self.light_to_temperature[light]
        humidity = self.temperature_to_humidity[temperature]
        location = self.humidity_to_location[humidity]
        if False:
            print(
                " -> ".join(
                    map(
                        str,
                        [
                            seed,
                            soil,
                            fertilizer,
                            water,
                            light,
                            temperature,
                            humidity,
                            location,
                        ],
                    )
                )
            )

        return location


def _read_until_next_blank_line(input_file) -> list[str]:
    lines: list[str] = []
    while (line := input_file.readline()) not in ["\n", ""]:
        lines.append(line)
    return lines


def _parse_triplet_into_mapping_definition(triplet_str) -> MappingDefinition:
    triplet_list = triplet_str.strip().split(" ")
    return MappingDefinition(
        source_range_start=int(triplet_list[1]),
        destination_range_start=int(triplet_list[0]),
        range_length=int(triplet_list[2]),
    )


def _parse_file(path: str) -> list:
    seeds: list[int] = []
    seed_to_soil: list[MappingDefinition] = []
    soil_to_fertilizer: list[MappingDefinition] = []
    fertilizer_to_water: list[MappingDefinition] = []
    water_to_light: list[MappingDefinition] = []
    light_to_temperature: list[MappingDefinition] = []
    temperature_to_humidity: list[MappingDefinition] = []
    humidity_to_location: list[MappingDefinition] = []

    with open(os.path.expanduser(path), "r") as input_file:
        seeds_str = input_file.readline()
        seeds = list(
            map(
                lambda x: int(x),
                filter(None, seeds_str.split(":")[1].strip().split(" ")),
            )
        )
        # Expect empty line
        input_file.readline()
        seed_to_soil = list(
            map(
                _parse_triplet_into_mapping_definition,
                _read_until_next_blank_line(input_file)[1:],
            )
        )
        soil_to_fertilizer = list(
            map(
                _parse_triplet_into_mapping_definition,
                _read_until_next_blank_line(input_file)[1:],
            )
        )
        fertilizer_to_water = list(
            map(
                _parse_triplet_into_mapping_definition,
                _read_until_next_blank_line(input_file)[1:],
            )
        )
        water_to_light = list(
            map(
                _parse_triplet_into_mapping_definition,
                _read_until_next_blank_line(input_file)[1:],
            )
        )
        light_to_temperature = list(
            map(
                _parse_triplet_into_mapping_definition,
                _read_until_next_blank_line(input_file)[1:],
            )
        )
        temperature_to_humidity = list(
            map(
                _parse_triplet_into_mapping_definition,
                _read_until_next_blank_line(input_file)[1:],
            )
        )
        humidity_to_location = list(
            map(
                _parse_triplet_into_mapping_definition,
                _read_until_next_blank_line(input_file)[1:],
            )
        )
        return (
            seeds,
            seed_to_soil,
            soil_to_fertilizer,
            fertilizer_to_water,
            water_to_light,
            light_to_temperature,
            temperature_to_humidity,
            humidity_to_location,
        )


def parse_file(path: str) -> ParsedAlmanac:
    parsed_tuple = _parse_file(path)
    return ParsedAlmanac(
        parsed_tuple[0], *[FrozenLazyIntToIntMapping(l) for l in parsed_tuple[1:]]
    )
