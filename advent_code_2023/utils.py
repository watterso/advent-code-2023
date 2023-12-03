import os.path
import typing

def yield_lines_from_path(path: str) -> typing.Generator[str, None, None]:
    with open(os.path.expanduser(path), 'r') as input_file:
        for line in input_file:
            yield line