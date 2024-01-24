from datetime import datetime
from typing import NamedTuple, Optional


class CommitInfo(NamedTuple):
    sha: str
    message: str
    author_name: str
    author_email: str
    author_date: datetime
    author_tz: int
    committer_name: str
    committer_email: str
    committer_date: datetime
    committer_tz: int
    in_main: bool
    is_merge: bool
    num_deletes: int
    num_inserts: int
    net_lines: int
    num_files: int
    branches: str
    files: str
    parents: str
    dmm_unit_size: Optional[float]
    dmm_unit_complexity: Optional[float]
    dmm_unit_interfacing: Optional[float]
