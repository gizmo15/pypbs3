#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pypbs3 setup script."""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypbs3",
    version="0.0.1",
    author="Boris Tassou",
    author_email="boris.tassou@securmail.fr",
    description="""Handle proxmox backup server operations via api""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gizmo15/pypbs3",
    py_modules=['pypbs3'],
    project_urls={
        "Bug Tracker": "https://github.com/gizmo15/pypbs3/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3",
    install_requires=[
        'requests'
    ],
)
