"""Python API to Git
"""
from . gitapi as _gitapi
Repo = _gitapi.Repo
git_clone = Repo.git_clone
git_command = Repo.command