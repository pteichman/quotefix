#!/usr/bin/env python

import os
from setuptools import setup

setup(
    name="quotefix",
    version="1.0.1",
    author="Peter Teichman",
    author_email="peter@teichman.org",
    description="Insert matching punctuation in strings",
    license="MIT",
    url="https://github.com/pteichman/quotefix",
    py_modules=["quotefix"],
    use_2to3=True,
    test_suite="quotefix_test"
)
