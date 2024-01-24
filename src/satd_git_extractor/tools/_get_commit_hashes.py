import csv
from pathlib import Path
from typing import Optional, Set


def get_commit_hashes(path: Path, commit_hashes: Optional[Set[str]] = None) -> Set[str]:
    if commit_hashes is None:
        commit_hashes = set()

    if not path.is_file():
        raise FileNotFoundError(f"Filepath {path.absolute()} doesn't exist.")

    with path.open("rt", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')

        for row in reader:
            # TODO
            if row[0] == "camel":
                commit_hashes.add(row[1])

    return commit_hashes
