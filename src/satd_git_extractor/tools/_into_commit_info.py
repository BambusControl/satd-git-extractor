from pydriller import Commit

from ..data import CommitInfo


def into_commit_info(commit: Commit):
    return CommitInfo(
        sha=commit.hash,
        message=commit.msg,
        author_name=commit.author.name,
        author_email=commit.author.email,
        author_date=commit.author_date,
        author_tz=commit.author_timezone,
        committer_name=commit.committer.name,
        committer_email=commit.committer.email,
        committer_date=commit.committer_date,
        committer_tz=commit.committer_timezone,
        in_main=commit.in_main_branch,
        is_merge=commit.merge,
        num_deletes=commit.deletions,
        num_inserts=commit.insertions,
        net_lines=commit.insertions - commit.deletions,
        num_files=commit.files,
        branches=', '.join(commit.branches),
        files=', '.join((file.new_path for file in commit.modified_files if file.new_path is not None)),
        parents=', '.join(commit.parents),
        dmm_unit_size=commit.dmm_unit_size,
        dmm_unit_complexity=commit.dmm_unit_complexity,
        dmm_unit_interfacing=commit.dmm_unit_interfacing
    )
