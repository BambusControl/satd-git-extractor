from pathlib import Path


def next_available_filepath(path: Path):
    # Create a unique path to a file that doesn't exist.
    i = 0

    if path.is_file():
        path = path.with_stem(f"{path.stem}_{i + 1}")

    while path.is_file():
        i += 1
        prev_suffix = f"_{i}"
        next_suffix = f"_{i + 1}"
        pure_stem = path.stem[:-len(prev_suffix)]
        path = path.with_stem(f"{pure_stem}{next_suffix}")

    return path
