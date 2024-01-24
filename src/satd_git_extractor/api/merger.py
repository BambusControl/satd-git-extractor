from pathlib import Path
from typing import List
import pandas as pd

from ..tools import next_available_filepath


def run_merger(project_export_dirpath: Path, commits_filepath: Path, merged_filepath: Path):
    if not project_export_dirpath.is_dir():
        raise FileNotFoundError(f"Project export directory {project_export_dirpath.absolute()} doesn't exist.")

    if not commits_filepath.is_file():
        raise FileNotFoundError(f"Commits file {commits_filepath.absolute()} doesn't exist.")

    # print([f.stem for f in project_export_dirpath.iterdir() if f.is_file() and f.suffix == ".csv"])

    dataframes = (
        pd.read_csv(
            str(filepath.absolute()),
            # dtype={"sha": str},
        )
        for filepath in project_export_dirpath.iterdir()
        if filepath.is_file() and filepath.suffix == ".csv"
    )

    extension_dataset = pd.concat(dataframes, copy=False)
    extension_dataset.drop(columns="project", inplace=True)

    base_dataset = pd.read_csv(
        commits_filepath,
        # dtype={"sha": str},
    )

    final_dataset = base_dataset.merge(extension_dataset, on="sha", how="left")
    merged_filepath = next_available_filepath(merged_filepath)

    print(f"Saving merged dataset ({merged_filepath.name})")
    final_dataset.to_csv(merged_filepath, index=False)
