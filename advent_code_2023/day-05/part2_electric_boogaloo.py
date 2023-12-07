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


def seed_mapping_is_overlap_with_input_seed_ranges(
    seed_mapping: helpers.MappingDefinition, input_ranges: list[range]
) -> bool:
    seed_range = range(
        seed_mapping.destination_range_start,
        seed_mapping.destination_range_start + seed_mapping.range_length,
    )
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


def _should_prepend_list_to_match_source_range_start(
    sorted_mapping_list: list[helpers.MappingDefinition], source_range: range
) -> bool:
    return (
        sorted_mapping_list
        and sorted_mapping_list[0].source_range_start > source_range.start
    )


def get_relevant_mappings_for_source_range(
    source_range: range, mappings: list[helpers.MappingDefinition]
) -> list[helpers.MappingDefinition]:
    last_covered_index = source_range.start
    relevant_mappings = []
    mappings = sorted(mappings)
    # print(f"Input Mappings: {mappings}")
    for mapping in mappings:
        if ranges_overlap(source_range, mapping.to_source_range()):
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

    if _should_prepend_list_to_match_source_range_start(
        relevant_mappings, source_range
    ):
        relevant_mappings = [
            helpers.MappingDefinition(
                source_range.start,
                source_range.start,
                relevant_mappings[0].source_range_start - source_range.start,
            )
        ] + relevant_mappings
    if last_covered_index < source_range.stop:
        # _should_append_list_to_match_source_range_stop
        relevant_mappings.append(
            helpers.MappingDefinition(
                last_covered_index,
                last_covered_index,
                source_range.stop - last_covered_index,
            )
        )
    if not relevant_mappings:
        # If none of the mappings overlapped with the source range,
        # that means the entire source range maps transparently throught to destination
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


def get_relevant_reversed_mappings(
    source_mapping: helpers.MappingDefinition,
    forwards_mappings: list[helpers.MappingDefinition],
) -> list[helpers.MappingDefinition]:
    mappings_reversed = [mapping.reverse() for mapping in forwards_mappings]
    return get_relevant_mappings_for_source_range(
        source_mapping.to_destination_range(), mappings_reversed
    )


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
target_seed_range = None

location_to_humidity_mappings = [mapping.reverse() for mapping in humidity_to_location]
location_to_humidity_mappings = fill_in_the_start_and_any_gaps_in_mappings(
    location_to_humidity_mappings
)
for l_to_h in location_to_humidity_mappings:
    if target_seed_range:
        break
    for h_to_t in get_relevant_reversed_mappings(
        l_to_h,
        temperature_to_humidity,
    ):
        if target_seed_range:
            break
        for t_to_l in get_relevant_reversed_mappings(
            h_to_t,
            light_to_temperature,
        ):
            if target_seed_range:
                break
            for l_to_w in get_relevant_reversed_mappings(t_to_l, water_to_light):
                if target_seed_range:
                    break
                for w_to_f in get_relevant_reversed_mappings(
                    l_to_w, fertilizer_to_water
                ):
                    if target_seed_range:
                        break
                    for f_to_s in get_relevant_reversed_mappings(
                        w_to_f, soil_to_fertilizer
                    ):
                        if target_seed_range:
                            break
                        for s_to_s in get_relevant_reversed_mappings(
                            f_to_s, seed_to_soil
                        ):
                            if target_seed_range:
                                break
                            if seed_mapping_is_overlap_with_input_seed_ranges(
                                s_to_s, input_seed_ranges
                            ):
                                target_seed_range = s_to_s.to_destination_range()

almanac = helpers.parse_file(INPUT_PATH)
locations = []
valid_seeds = []
# print(f"Target Seed Range: {target_seed_range}")
refined_target_range = get_exact_overlapping_ranges(
    target_seed_range, input_seed_ranges
)
# print(f"Input Seeds: {input_seed_ranges}")
# print(f"Refined Target Seed Range: {refined_target_range}")
for seed in chain(*refined_target_range):
    if is_number_in_any_of_these_ranges(seed, input_seed_ranges):
        valid_seeds.append(seed)
        locations.append(almanac.get_location_for_seed(seed))
    if seed % 1000000 == 0:
        print(f"{seed/1000000} Million")
print("====================== ATTENTION =======================")
# print(f"{len(valid_seeds)} items, {len(set(valid_seeds))} uniques")
print(f"The lowest location is: {sorted(locations)[0]}")
