from dataclasses import dataclass
from itertools import chain
import importlib

helpers = importlib.import_module("advent_code_2023.day-05.helpers")

# INPUT_PATH = "advent_code_2023/day-05/test-input.txt"
INPUT_PATH = "advent_code_2023/day-05/input.txt"


def fill_in_the_start_and_any_gaps_in_mappings(
    mappings: list[helpers.MappingDefinition],
) -> list[helpers.MappingDefinition]:
    last_covered_index = 0
    filled_mapping_list = []
    mappings = sorted(mappings)
    for mapping in mappings:
        if last_covered_index < mapping.source_range_start:
            filled_mapping_list.append(
                helpers.MappingDefinition(
                    last_covered_index,
                    last_covered_index,
                    mapping.source_range_start - last_covered_index,
                )
            )
        filled_mapping_list.append(mapping)
        last_covered_index = mapping.source_range_start + mapping.range_length

    return filled_mapping_list


def get_relevant_mappings_for_source_range(
    source_range: range, mappings: list[helpers.MappingDefinition]
) -> list[helpers.MappingDefinition]:
    last_covered_index = source_range.start
    relevant_mappings = []
    mappings = sorted(mappings)
    # print(f"Input Mappings: {mappings}")
    for mapping in mappings:
        mapping_source_range = range(
            mapping.source_range_start,
            mapping.source_range_start + mapping.range_length,
        )
        if ranges_overlap(source_range, mapping_source_range):
            delta_of_starts = max((source_range.start - mapping.source_range_start), 0)
            relevant_mappings.append(
                helpers.MappingDefinition(
                    max(mapping.source_range_start, source_range.start),
                    mapping.destination_range_start + delta_of_starts,
                    min(
                        mapping.range_length - delta_of_starts,
                        (
                            source_range.stop
                            - max(mapping.source_range_start, source_range.start)
                        ),
                    ),
                )
            )
        last_covered_index = mapping.source_range_start + mapping.range_length

    if (
        relevant_mappings
        and relevant_mappings[0].source_range_start > source_range.start
    ):
        relevant_mappings = [
            helpers.MappingDefinition(
                source_range.start,
                source_range.start,
                relevant_mappings[0].source_range_start - source_range.start,
            )
        ] + relevant_mappings
    if last_covered_index < source_range.stop:
        relevant_mappings.append(
            helpers.MappingDefinition(
                last_covered_index,
                last_covered_index,
                source_range.stop - last_covered_index,
            )
        )
    if not relevant_mappings:
        relevant_mappings = [
            helpers.MappingDefinition(
                source_range.start,
                source_range.start,
                source_range.stop - source_range.start,
            )
        ]
    # print(f"Source Range: {source_range} | Relevant Mappings: {relevant_mappings}")
    # print()
    return relevant_mappings


def convert_seed_list_to_seed_ranges(seeds: list[int]) -> list[range]:
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append(range(seeds[i], seeds[i] + seeds[i + 1]))
    return sorted(seed_ranges, key=lambda x: x.start)


def is_number_in_any_of_these_ranges(number: int, input_ranges: list[range]) -> bool:
    for input_range in input_ranges:
        if number in input_range:
            return True

    return False


def ranges_overlap(l: range, r: range) -> bool:
    # print(f"{l} ? {r}")
    left_ends_within_right = (l.stop - 1) > r.start and l.stop < r.stop
    right_ends_within_left = (r.stop - 1) > l.start and r.stop < l.stop
    left_envelops_right = l.start < r.start and l.stop > r.stop
    right_envelops_left = r.start < l.start and r.stop > l.stop
    return (
        left_ends_within_right
        or right_ends_within_left
        or left_envelops_right
        or right_envelops_left
    )


def seed_range_is_overlap_with_input_seed_ranges(
    seed_range: range, input_ranges: list[range]
) -> bool:
    # print(f"{seed_range} ? {input_ranges}")
    for in_range in input_ranges:
        if ranges_overlap(seed_range, in_range):
            return True
    return False


def get_exact_overlapping_ranges(
    seed_range: range, input_ranges: list[range]
) -> list[range]:
    overlapping_ranges = []
    for in_range in input_ranges:
        if ranges_overlap(seed_range, in_range):
            overlapping_ranges.append(
                range(
                    max(seed_range.start, in_range.start),
                    min(seed_range.stop, in_range.stop),
                )
            )
    return overlapping_ranges


(
    seeds,
    seed_to_soil,
    soil_to_fertilizer,
    fertilizer_to_water,
    water_to_light,
    light_to_temperature,
    temperature_to_humidity,
    humidity_to_location,
) = helpers._parse_file(INPUT_PATH)

input_seed_ranges = convert_seed_list_to_seed_ranges(seeds)
# print(input_seed_ranges)

target_seed_range = None

location_to_humidity = [mapping.reverse() for mapping in humidity_to_location]
location_to_humidity = fill_in_the_start_and_any_gaps_in_mappings(location_to_humidity)
for l_to_h in location_to_humidity:
    if target_seed_range:
        break
    location_range = range(
        l_to_h.source_range_start, l_to_h.source_range_start + l_to_h.range_length
    )
    humidity_range = range(
        l_to_h.destination_range_start,
        l_to_h.destination_range_start + l_to_h.range_length,
    )

    humidity_to_temperature = [mapping.reverse() for mapping in temperature_to_humidity]
    relevant_humidity_to_temperature_mappings = get_relevant_mappings_for_source_range(
        humidity_range, humidity_to_temperature
    )
    for h_to_t in relevant_humidity_to_temperature_mappings:
        if target_seed_range:
            break
        temperature_range = range(
            h_to_t.destination_range_start,
            h_to_t.destination_range_start + h_to_t.range_length,
        )

        temperature_to_light = [mapping.reverse() for mapping in light_to_temperature]
        relevant_temperature_to_light_mappings = get_relevant_mappings_for_source_range(
            temperature_range, temperature_to_light
        )
        for t_to_l in relevant_temperature_to_light_mappings:
            if target_seed_range:
                break
            light_range = range(
                t_to_l.destination_range_start,
                t_to_l.destination_range_start + t_to_l.range_length,
            )

            light_to_water = [mapping.reverse() for mapping in water_to_light]
            relevant_light_to_water_mappings = get_relevant_mappings_for_source_range(
                light_range, light_to_water
            )
            for l_to_w in relevant_light_to_water_mappings:
                if target_seed_range:
                    break
                water_range = range(
                    l_to_w.destination_range_start,
                    l_to_w.destination_range_start + l_to_w.range_length,
                )

                water_to_fertilizer = [
                    mapping.reverse() for mapping in fertilizer_to_water
                ]
                relevant_water_to_fertilizer_mappings = (
                    get_relevant_mappings_for_source_range(
                        water_range, water_to_fertilizer
                    )
                )
                for w_to_f in relevant_water_to_fertilizer_mappings:
                    if target_seed_range:
                        break
                    fertilizer_range = range(
                        w_to_f.destination_range_start,
                        w_to_f.destination_range_start + w_to_f.range_length,
                    )

                    fertilizer_to_soil = [
                        mapping.reverse() for mapping in soil_to_fertilizer
                    ]
                    relevant_fertilizer_to_soil_mappings = (
                        get_relevant_mappings_for_source_range(
                            fertilizer_range, fertilizer_to_soil
                        )
                    )
                    for f_to_s in relevant_fertilizer_to_soil_mappings:
                        if target_seed_range:
                            break
                        soil_range = range(
                            f_to_s.destination_range_start,
                            f_to_s.destination_range_start + f_to_s.range_length,
                        )

                        soil_to_seed = [mapping.reverse() for mapping in seed_to_soil]
                        relevant_soil_to_seed_mappings = (
                            get_relevant_mappings_for_source_range(
                                soil_range, soil_to_seed
                            )
                        )
                        for s_to_s in relevant_soil_to_seed_mappings:
                            if target_seed_range:
                                break
                            seed_range = range(
                                s_to_s.destination_range_start,
                                s_to_s.destination_range_start + s_to_s.range_length,
                            )

                            if False:
                                print(
                                    " -> ".join(
                                        map(
                                            str,
                                            [
                                                location_range,
                                                humidity_range,
                                                temperature_range,
                                                light_range,
                                                water_range,
                                                fertilizer_range,
                                                soil_range,
                                                seed_range,
                                            ],
                                        )
                                    )
                                )
                            if seed_range_is_overlap_with_input_seed_ranges(
                                seed_range, input_seed_ranges
                            ):
                                if False:
                                    print(
                                        " -> ".join(
                                            map(
                                                str,
                                                [
                                                    location_range,
                                                    humidity_range,
                                                    temperature_range,
                                                    light_range,
                                                    water_range,
                                                    fertilizer_range,
                                                    soil_range,
                                                    seed_range,
                                                ],
                                            )
                                        )
                                    )
                                target_seed_range = seed_range

almanac = helpers.parse_file(INPUT_PATH)
locations = []
valid_seeds = []
print(f"Target Seed Range: {target_seed_range}")
refined_target_range = get_exact_overlapping_ranges(
    target_seed_range, input_seed_ranges
)
print(f"Input Seeds: {input_seed_ranges}")
print(f"Refined Target Seed Range: {refined_target_range}")
for seed in chain(*refined_target_range):
    if is_number_in_any_of_these_ranges(seed, input_seed_ranges):
        valid_seeds.append(seed)
        locations.append(almanac.get_location_for_seed(seed))
    if seed % 1000000 == 0:
        print(f"{seed/1000000} Million")
print("====================== ATTENTION =======================")
print(f"{len(valid_seeds)} items, {len(set(valid_seeds))} uniques")
print(f"The lowest location is: {sorted(locations)[0]}")
