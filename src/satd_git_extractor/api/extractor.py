from pathlib import Path
from typing import Optional, Set

import pandas as pd
from pandas import DataFrame
from pydriller import Commit

from ..tools import get_repository, print_progress, get_repositories, into_commit_info
from ..data import RepositoryInfo, CommitInfo


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

    # Check if all repositories are present
    repo_names = _get_repositories_to_extract(commit_messages, repositories)

    repo_infos = [
        RepositoryInfo(name, url)
        for (_, (name, url)) in repositories.iterrows()
        if name in repo_names
    ]
    repos_left = len(repo_infos)

    for repo in repo_infos:
        # Yes this is terrible (I wanted to quickly see the progress because it takes a few hours to complete)

        try:
            repos_left = repos_left - 1
            print(f"[{repos_left}] ", end="", flush=True)

            output_filepath = output_dir / f"{repo.name}.csv"

            if output_filepath.is_file():
                print(f"Skipping extracted repository ({repo.name})")
            else:
                commit_hashes = set(commit_messages[commit_messages.project == repo.name].sha.to_list())
                commit_data = _drill_repository(repo, commit_hashes, clone_dir)
                commit_data.to_csv(output_filepath, index=False)

        except Exception as e:
            # Fail fast, but we want to continue with the other repositories
            print(f"Failed to extract repository [{repos_left}] ({repo.name}): {repo.url}")
            print(e)


def _get_repositories_to_extract(commit_messages, repositories):
    expected_repos = set(commit_messages.project.unique())
    actual_repos = set(repositories.project.unique())
    missing_repos = expected_repos - actual_repos
    if len(missing_repos) > 0:
        print(f"Missing {len(missing_repos)} repositories: {missing_repos}")
    return expected_repos


def _drill_repository(repo: RepositoryInfo, commit_hashes: Set[str], clone_dir: Optional[Path] = None) -> DataFrame:
    # Copy to avoid modifying the original
    commit_hashes = set(commit_hashes)
    number_of_commits = len(commit_hashes)

    repository = get_repository(commit_hashes, repo, clone_dir)

    # Extract commits the easy way
    print(f"Extracting repository ({repo.name}) with [{number_of_commits}] commits")
    print_progress(number_of_commits)
    commits = [
        _consume_commit(commit, commit_hashes, number_of_commits)
        for commit in repository.traverse_commits()
    ]
    print("")

    # Extract commits the hard way
    if len(commit_hashes) > 0:
        # Some commits are missing, we must search for them individually
        commits = commits + [
            _consume_commit(commit, commit_hashes, number_of_commits)
            for repo in get_repositories(clone_dir, commit_hashes, repo)
            for commit in repo.traverse_commits()
        ]
        print("")

    # Unreachable commits, like commits from forks
    if len(commit_hashes) > 0:
        print(f"Missing [{len(commit_hashes)}] commits: {commit_hashes}")

    return pd.DataFrame(commits)


def _consume_commit(commit: Commit, project_commit_hashes: Set[str], total_commits: int) -> CommitInfo:
    project_commit_hashes.discard(commit.hash)
    print_progress(total_commits, len(project_commit_hashes))
    return into_commit_info(commit)
