hgapi
=====
hgapi is a pure-Python API to Mercurial, that uses the command-line
interface instead of the internal Mercurial API. The rationale for
this is twofold: the internal API is unstable, and it is GPL.

hgapi works for Mercurial < 1.9, and will instantly reflect any
changes to the repository, unlike interfaces based on the
CommandServer (http://mercurial.selenic.com/wiki/CommandServer). It
also has a really permissive license (do whatever you want, don't
blame me).

For example of code that uses this API, take a look at
https://bitbucket.org/haard/autohook which now uses hgapi
exclusively. Add any feature requests or bugs found to the issue tracker.

So far, the API supports::

 hg init
 hg id
 hg add <file>
 hg commit [files] [-u name] [--close-branch]
 hg update <rev>
 hg heads
 hg log

You also have access to the configuration (config, configbool,
configlist) just as in the internal Mercurial API.

Example usage::
    >>> import hgapi
    >>> repo = hgapi.Repo("test_hgapi") #existing folder
    >>> repo.hg_init()
    >>> repo.hg_add("file.txt") #already created but not added file
    >>> repo.hg_commit("Adding file.txt", user="me")
    >>> str(repo['tip'].desc)
    'Adding file.txt'

Installation
============

Easiest is easy_install or pip from PyPy::

 pip install hgapi

or::

 easy_install hgapi

Otherwise, download the source, make sure you have setuptools
installed, and then run::

 python setup.py install

License
=======

Copyright (c) 2011, Fredrik Håård 

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
