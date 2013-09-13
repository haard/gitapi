"""Python API to Git
"""
from . import gitapi as _gitapi
Repo = _gitapi.Repo
git_clone = Repo.git_clone
git_command = Repo.command