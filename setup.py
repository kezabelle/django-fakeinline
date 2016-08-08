#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from setuptools import setup
from setuptools.command.test import test as TestCommand
if sys.version_info[0] == 2:
    # get the Py3K compatible `encoding=` for opening files.
	from io import open


HERE = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def make_readme(root_path):
    consider_files = ("README.rst", "LICENSE", "CHANGELOG", "CONTRIBUTORS")
    for filename in consider_files:
        filepath = os.path.realpath(os.path.join(root_path, filename))
        if os.path.isfile(filepath):
            with open(filepath, mode="r", encoding="utf-8") as f:
                yield f.read()


LICENSE = "BSD License"
URL = "https://github.com/kezabelle/django-fakeinline"
LONG_DESCRIPTION = "\r\n\r\n----\r\n\r\n".join(make_readme(HERE))
SHORT_DESCRIPTION = "fakeinline provides enough of the methods and attributes to trick the Django Admin into displaying it when mounted as part of an inlines declaration on a ModelAdmin"
KEYWORDS = (
    "django",
    "inline",
    "admin",
    "fake",
)

setup(
    name="django-fakeinline",
    version="0.1.1",
    author="Keryn Knight",
    author_email="python-fakeinline@kerynknight.com",
    maintainer="Keryn Knight",
    maintainer_email="python-fakeinline@kerynknight.com",
    description=SHORT_DESCRIPTION[0:200],
    long_description=LONG_DESCRIPTION,
    packages=[
        "fakeinline",
    ],
    include_package_data=True,
    install_requires=[
        "Django>=1.8",
    ],
    tests_require=[
        "pytest>=2.6",
        "pytest-django>=2.8",
        "pytest-cov>=1.8",
        "pytest-remove-stale-bytecode>=1.0",
        "pytest-catchlog>=1.2",
    ],
    cmdclass={"test": PyTest},
    zip_safe=False,
    keywords=" ".join(KEYWORDS),
    license=LICENSE,
    url=URL,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: {}".format(LICENSE),
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Django",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
    ],
)
