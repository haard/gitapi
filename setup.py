# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name = "gitapi",
    version = "1.0.1a2",
    packages = ['gitapi'],
    test_suite = "gitapi.testgitapi.TestGitAPI",
    author = "Fredrik Håård",
    author_email = "fredrik@metallapan.se",
    description = "Python API to Git using the command-line interface",
    license = "Do whatever you want, don't blame me",
    keywords = "git api",
    url = "https://bitbucket.org/haard/gitapi",   # project home page, if any
    long_description = """
gitapi is a pure-Python API to Git, that uses the command-line
interface. This is a fork of https://bitbucket.org/haard/ with the
intention of making a unified API for a subset of git and hg
functionality possible"""
)
