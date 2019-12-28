#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='snakai',  
    version='1.0.dev1',
    scripts=[] ,
    author="fishshrimp",
    author_email="readonlyfile@hotmail.com",
    description="snake with ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/memeda/snakeWithAI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License"
    ],
 )