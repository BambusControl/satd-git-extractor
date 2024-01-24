from pathlib import Path
from typing import Iterable, Generator

from pydriller import Repository

from ..data import RepositoryInfo


def get_repositories(clone_dir: Path, all_commits: Iterable[str], repo: RepositoryInfo) -> Generator[Repository, None, None]:
    project_dir = clone_dir / repo.name
    commits = list(all_commits)

    if project_dir.is_dir():
        print(f"Using local repository ({repo.name}) for single commit search")
        return (
            Repository(str(project_dir.absolute()), single=commit_hash)
            for commit_hash in commits
        )

    print(f"Cloning repository ({repo.name}) for single commit search: {repo.url}")
    return (
        Repository(repo.url, single=commit_hash, clone_repo_to=str(clone_dir.absolute()))
        for commit_hash in commits
    )
