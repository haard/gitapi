gitapi
======
gitapi is a pure-Python API to git, which uses the command-line
interface. It has a really permissive license (do whatever you want, don't
blame me).

So far, the API supports::

 git init
 git branch
 git id (git log --pretty=format:%H)
 git add
 git commit
 git status
 git log
 git checkout
 git reset
 git merge (fails on conflict)
 git push
 git pull
 git fetch
 git clone


You also have access to the configuration (config, configbool,
configlist).

Example usage::
    >>> import gitapi
    >>> repo = gitapi.Repo("test_gitapi") #existing folder
    >>> repo.git_init()
    >>> repo.git_add("file.txt") #already created but not added file
    >>> repo.git_commit("Adding file.txt", user="me <me@example.com>")
    >>> str(repo['HEAD'].desc)
    'Adding file.txt'

Installation
============

Super easy::

 pip install gitapi

Easy: download the source, make sure you have setuptools
installed, and then run::

 python setup.py install

License
=======

Copyright (c) Fredrik Håård 

Do whatever you want, don't blame me. You may also use this software
as licensed under the MIT or BSD licenses, or the more permissive license below:

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
