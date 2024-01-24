from pathlib import Path
from typing import Iterable, Optional, List

from pydriller import Repository

from ..data import RepositoryInfo


def get_repository(only_commits: Iterable[str], repo: RepositoryInfo, clone_dir: Optional[Path] = None) -> Repository:
    commits = list(only_commits)

    return _remote_repo(commits, repo) if clone_dir is None \
        else _local_repo(clone_dir, commits, repo)


def _local_repo(clone_dir: Path, commits: List[str], repo: RepositoryInfo) -> Repository:
    project_dir = clone_dir / repo.name

    if project_dir.is_dir():
        print(f"Using local repository ({repo.name})")
        return Repository(str(project_dir.absolute()), only_commits=commits)

    print(f"Cloning repository ({repo.name}): {repo.url}")
    return Repository(repo.url, only_commits=commits, clone_repo_to=str(clone_dir.absolute()))


def _remote_repo(commits: List[str], repo: RepositoryInfo) -> Repository:
    print(f"Using remote repository ({repo.name})")
    return Repository(repo.url, only_commits=commits)
