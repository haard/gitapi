# -*- coding: utf-8 -*- 
from setuptools import setup


setup(
    name = "hgapi",
    version = "1.1.0",
    packages = ['hgapi'],
    test_suite = "hgapi.testhgapi.TestHgAPI",
    author = "Fredrik Håård",
    author_email = "fredrik@haard.se",
    description = "Python API to Mercurial using the command-line interface",
    license = "Do whatever you want, don't blame me",
    keywords = "mercurial api",
    url = "https://bitbucket.org/haard/hgapi",   # project home page, if any
    long_description = """
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
exclusively."""
)
