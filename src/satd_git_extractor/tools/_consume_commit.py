from typing import Set
from pydriller import Commit

from ..data import CommitInfo
from ._into_commit_info import into_commit_info
from ._print_progress import print_progress


def consume_commit(commit: Commit, project_commit_hashes: Set[str], total_commits: int) -> CommitInfo:
    project_commit_hashes.discard(commit.hash)
    print_progress(total_commits, len(project_commit_hashes))
    return into_commit_info(commit)
