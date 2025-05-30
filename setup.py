#!/usr/bin/env python3
"""
Setup script for memlayout package
"""

from setuptools import setup, find_packages

setup(
    name="memlayout",
    version="0.1.0",
    description="A lightweight, dependency-free Python library for managing memory layouts through interval-based allocation",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'memlayout=memlayout.main:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 