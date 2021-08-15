#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='snakai',  
    version='1.1',
    entry_points={
        'console_scripts': [
            'run_snake=snakai.run:main',
        ],
    },
    author="fishshrimp",
    author_email="readonlyfile@hotmail.com",
    description="snake with ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fseasy/snakai",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'tqdm'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires='>=3.6'
 )
