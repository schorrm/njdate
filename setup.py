#!/usr/bin/python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="njdate",
    version="0.0.1",
    author="Moshe Schorr",
    description="Jewish Date parsing and handling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schorrm/njdate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
