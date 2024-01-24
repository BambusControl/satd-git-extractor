from pathlib import Path
from typing import Optional

import pandas as pd

from ..tools import get_repository, print_progress, consume_commit, get_repositories
from ..data import RepositoryInfo


def run_extractor(repositories_filepath: Path, commits_filepath: Path, output_dir: Path, clone_dir: Optional[Path] = None):
    if not repositories_filepath.is_file():
        raise FileNotFoundError(f"Repositories file {repositories_filepath.absolute()} doesn't exist.")

    if not commits_filepath.is_file():
        raise FileNotFoundError(f"Commits file {commits_filepath.absolute()} doesn't exist.")

    if not output_dir.is_dir():
        raise FileNotFoundError(f"Output directory {output_dir.absolute()} doesn't exist.")

    if (clone_dir is not None) and (not clone_dir.is_dir()):
        raise FileNotFoundError(f"Clone directory {clone_dir.absolute()} doesn't exist.")

    commit_messages = pd.read_csv(
        commits_filepath,
        dtype={
            "project": str,
            "sha": str,
        },
        usecols=[
            "project",
            "sha"
        ],
    )

    hproj = set(commit_messages.project.unique())

    repositories = (pd.read_csv(
        repositories_filepath,
        dtype={
            "project": str,
            "git_url": str,
        },
        usecols=[
            "project",
            "git_url"
        ],
    ))

    rproj = set(repositories.project.unique())

    dif = hproj - rproj
    if len(dif) > 0:
        print(f"Missing {len(dif)} repositories: {dif}")

    repo_infos = [
        RepositoryInfo(name, url)
        for (_, (name, url)) in repositories.iterrows()
        if name in hproj
    ]
    repos_left = len(repo_infos)

    for repo in repo_infos:
        try:
            repos_left = repos_left - 1
            output_filepath = output_dir / f"{repo.name}.csv"

            if output_filepath.is_file():
                print(f"Skipping extracted repository [{repos_left}] ({repo.name})")
                continue

            commit_hashes = set(commit_messages[commit_messages.project == repo.name].sha.to_list())
            number_of_commits = len(commit_hashes)
            repository = get_repository(commit_hashes, repo, clone_dir)

            print(f"Extracting repository [{repos_left}] ({repo.name}) with [{number_of_commits}] commits")

            print_progress(number_of_commits)
            commits = [
                consume_commit(commit, commit_hashes, number_of_commits)
                for commit in repository.traverse_commits()
            ]
            print("")

            if len(commit_hashes) > 0:
                # Some commits are missing, we must search for them individually
                commits = commits + [
                    consume_commit(commit, commit_hashes, number_of_commits)
                    for repo in get_repositories(clone_dir, commit_hashes, repo)
                    for commit in repo.traverse_commits()
                ]
                print("")

            df_commits = pd.DataFrame(commits)
            df_commits["project"] = repo.name
            df_commits.to_csv(output_filepath, index=False)

            if len(commit_hashes) > 0:
                print(f"Missing [{len(commit_hashes)}] commits: {commit_hashes}")
        except Exception as e:
            print(f"Failed to extract repository [{repos_left}] ({repo.name}): {repo.url}")
            print(e)
