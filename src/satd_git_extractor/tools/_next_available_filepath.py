from pathlib import Path


def next_available_filepath(path: Path):
    # Create a unique path to a file that doesn't exist.
    i = 1

    while path.is_file():
        path = path.with_stem(f"{path.stem}_{i}")
        i += 1

    return path
