hgapi
=====
hgapi is a pure-Python API to Mercurial, that uses the command-line
interface instead of the internal Mercurial API. The rationale for
this is twofold: the internal API is unstable, and it is GPL.

So far, the API supports::
 hg init
 hg id
 hg add <file>
 hg commit [files] [-u name] [--close-branch]
 hg update <rev>
 hg heads
 hg log

Example usage::
    >>> import hgapi, shutil, os
    >>> os.mkdir("./test_hgapi")
    >>> repo = hgapi.Repo("test_hgapi")
    >>> repo.hg_init()
    >>> open("test_hgapi/file.txt", "w").write("stuff")
    >>> repo.hg_add("file.txt")
    >>> repo.hg_commit("Adding file.txt", user="me")
    >>> repo['tip'].desc
    u'Adding file.txt'
    >>> shutil.rmtree("test_hgapi")



License
=======

Copyright (c) 2011, Fredrik Håård

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
