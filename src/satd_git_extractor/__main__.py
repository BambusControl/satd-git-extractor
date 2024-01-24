import argparse
from pathlib import Path

from .api import run_extractor, run_merger


def main() -> None:
    args = _create_parser().parse_args()

    if args.mode == "extract":
        run_extractor(
            Path(args.repositories),
            Path(args.commits),
            Path(args.exports_dir),
            None if args.clone_dir is None else Path(args.clone_dir),
        )

    elif args.mode == "merge":
        run_merger(
            Path(args.exports_dir),
            Path(args.commits),
            Path(args.output),
        )

    else:
        # Should never happen
        raise ValueError(f"Invalid mode: {args.mode}")


def _create_parser():
    parser = argparse.ArgumentParser(
        prog="satd-git-extractor",
        description="Extracts commit information from git repositories into a CSV file.",
        epilog="For more information, visit [https://github.com/BambusControl/satd-git-extractor]."
    )

    subparsers = parser.add_subparsers(
        title="modes",
        description="Available modes",
        dest="mode",
        required=True
    )

    _add_extractor_args(subparsers)
    _add_merger_args(subparsers)

    return parser


def _add_merger_args(subparsers):
    merge_parser = subparsers.add_parser("merge", help="Merge mode")

    merge_parser.add_argument(
        "--exports-dir",
        type=str,
        required=True,
        metavar="./exports",
        help="Path to the directory with the previously exported CSV files to merge."
    )

    merge_parser.add_argument(
        "--commits",
        type=str,
        required=True,
        metavar="./commits.csv",
        help="Path to the SATD CSV file with commit messages."
    )

    merge_parser.add_argument(
        "--output",
        type=str,
        required=True,
        metavar="./merged.csv",
        help="Path to the merged output CSV file. If the file exists, a number will be appended to the filename."
    )


def _add_extractor_args(subparsers):
    extract_parser = subparsers.add_parser("extract", help="Extract mode")

    extract_parser.add_argument(
        "--repositories",
        type=str,
        required=True,
        metavar="./repos.csv",
        help="Path to the CSV file with GIT repositories."
    )

    extract_parser.add_argument(
        "--commits",
        type=str,
        required=True,
        metavar="./commits.csv",
        help="Path to the SATD CSV file with commit messages."
    )

    extract_parser.add_argument(
        "--exports-dir",
        type=str,
        required=True,
        metavar="./exports",
        help="Directory path for the output CSV files."
    )

    extract_parser.add_argument(
        "--clone-dir",
        type=str,
        required=False,
        metavar="./cloned",
        help="Directory path for the cloned repositories a temporary directory is used otherwise."
    )


if __name__ == "__main__":
    main()
