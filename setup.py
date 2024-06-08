#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Setup tools wrapper
"""

from setuptools import find_packages, setup
import os
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
requirement_path = "requirements.txt"
install_requires = [] # Here we'll add: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name='deplyai-cli',
    maintainer="DeplyAI",
    maintainer_email="support@deplyai.com",
    version='0.3.2',
    zip_safe=False,
    description='DeplyAI CLI',
    platforms=['Linux', 'Windows', 'MacOS'],
    include_package_data=True,
    keywords='deplyai',
    packages=find_packages(),
    project_urls={
        "Bug Tracker": "https://github.com/deply-ai/cli/issues",
        "Documentation": "https://github.com/deply-ai/cli",
        "Source Code": "https://github.com/deply-ai/cli",
    },
    license='BSD-3-Clause',
    scripts=['deply'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=install_requires
)