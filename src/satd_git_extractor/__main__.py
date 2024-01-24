import argparse
from pathlib import Path

from .api import run_extractor, run_merger

DIRECTORY = r"C:\Users\Moyo\Projects\private\gitlab\school\rug\evidence-based-software-engineering\satd-git-extractor\.ignore"


def main():
    parser = argparse.ArgumentParser(
        prog="satd-git-extractor",
        description="Extracts commit information from git repositories into a CSV file.",
        epilog="For more information, visit [https://github.com/BambusControl/satd-git-extractor]."
    )

    subparsers = parser.add_subparsers(
        title="modes",
        description="Available modes",
        dest="mode",
        required=True,
        help="Available modes"
    )

    # Subparser for the extract mode
    extract_parser = subparsers.add_parser("extract", help="Extract mode")
    extract_parser.add_argument("--repositories", type=str, required=True, help="Path to the CSV file with GIT repositories.")
    extract_parser.add_argument("--commits", type=str, required=True, help="Path to the SATD CSV file with commit messages.")
    extract_parser.add_argument("--output", type=str, required=True, help="Path for the output CSV file.")
    extract_parser.add_argument("--clone-dir", type=str, required=True, help="")

    # Subparser for the merge mode
    merge_parser = subparsers.add_parser("merge", help="Merge mode")
    merge_parser.add_argument("--input", type=str, required=True, help="Path to the input CSV file.")
    merge_parser.add_argument("--output", type=str, required=True, help="Path to the output CSV file.")

    args = parser.parse_args()

    if args.mode == "extract":
        extract_mode(args)
    elif args.mode == "merge":
        merge_mode(args)

    run_extractor(
        Path(rf"{DIRECTORY}\modified\repositories.csv"),
        Path(rf"{DIRECTORY}\sources\satd-dataset-commit_messages.csv"),
        Path(rf"{DIRECTORY}\export"),
        Path(rf"{DIRECTORY}\repos"),
    )

    run_merger(
        Path(rf"{DIRECTORY}\export"),
        Path(rf"{DIRECTORY}\sources\satd-dataset-commit_messages.csv"),
        Path(rf"{DIRECTORY}\merged\satd-commits-merged-dataset.csv"),
    )

if __name__ == "__main__":
    main()
