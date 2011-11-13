# -*- encoding: utf-8 -*- 
from setuptools import setup

def read(fname):
    """Nice idea stolen from example project"""
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hgapi",
    version = "1.0.0",
    packages = ['hgapi'],
    test_suite = "testhgapi.TestHgAPI",

    # metadata
    author = "Fredrik Håård",
    author_email = "fredrik@haard.se",
    description = "Python API to Mercurial using the command-line interface",
    license = "MIT or BSD or WTF",
    keywords = "mercurial api",
    url = "https://bitbucket.org/haard/hgapi",   # project home page, if any
    long_description = read("README.rst")
)
