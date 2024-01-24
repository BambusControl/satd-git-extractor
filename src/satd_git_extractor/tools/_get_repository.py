from pathlib import Path
from typing import Iterable

from pydriller import Repository

from ..data import RepositoryInfo


def get_repository(clone_dir: Path, only_commits: Iterable[str], repo: RepositoryInfo) -> Repository:
    project_dir = clone_dir / repo.name
    commits = list(only_commits)

    if project_dir.is_dir():
        print(f"Using local repository ({repo.name})")
        return Repository(str(project_dir.absolute()), only_commits=commits)

    print(f"Cloning repository ({repo.name}): {repo.url}")
    return Repository(repo.url, only_commits=commits, clone_repo_to=str(clone_dir.absolute()))
