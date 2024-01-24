from pathlib import Path

from .api import run_extractor, run_merger

DIRECTORY = r"C:\Users\Moyo\Projects\private\gitlab\school\rug\evidence-based-software-engineering\satd-git-extractor\.ignore"


def main():
    run_extractor(
        Path(rf"{DIRECTORY}\modified\repositories.csv"),
        Path(rf"{DIRECTORY}\sources\satd-dataset-commit_messages.csv"),
        Path(rf"{DIRECTORY}\export"),
        Path(rf"{DIRECTORY}\repos"),
    )

    # run_merger(
    #     Path(rf"{DIRECTORY}\export"),
    #     Path(rf"{DIRECTORY}\sources\satd-dataset-commit_messages.csv"),
    #     Path(rf"{DIRECTORY}\merged\satd-commits-merged-dataset.csv"),
    # )

    # parser = argparse.ArgumentParser()

    # parser.add_argument("--repo", type=str, default="")
    # parser.add_argument("--hash", type=str, default="")
    # parser.add_argument("--output", type=str, default="")
    #
    # args = parser.parse_args()
    # run(args.repo, Path(args.hash), Path(args.output))


if __name__ == "__main__":
    main()
