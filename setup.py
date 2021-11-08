#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Setup requirements
try:
    from setuptools import setup, find_packages
    from setuptools.command.install import install
except ImportError:
    print(
        "drone-databricks-repos needs setuptools in order to build. Install it using"
        " your package manager (usually python-setuptools) or via pip (pip"
        " install setuptools)."
    )
    sys.exit(1)


def read_file(file_name):
    """Read file and return its contents."""
    with open(file_name, "r") as f:
        return f.read()


def read_requirements(file_name="requirements.txt"):
    """Read requirements file as a list."""
    reqs = read_file(file_name).splitlines()
    if not reqs:
        raise RuntimeError(
            "Unable to read requirements from the %s file"
            "That indicates this copy of the source code is incomplete." % file_name
        )
    return reqs


def get_dynamic_setup_params():
    """Add dynamically calculated setup params to static ones."""

    return {
        # Retrieve the long description from the README
        "long_description": read_file("README.md"),
        "install_requires": read_requirements("requirements.txt"),
    }


static_setup_params = dict(
    name="drone-databricks-repos",
    version="0.1",
    description="Update databricks repo",
    keywords="drone, ci, plugin, aws",
    url="https://bitbucket.org/account/user/gumgum/projects/DP",
    author="Florian Dambrine <florian@gumgum.com>",
    packages=find_packages("plugin"),
    package_data={},
    install_requires=read_requirements(),
    scripts=[],
    zip_safe=False,
)


if __name__ == "__main__":
    setup_params = dict(static_setup_params, **get_dynamic_setup_params())
    setup(**setup_params)
