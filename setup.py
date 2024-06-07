#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Setup tools wrapper
"""

from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='deplyai-cli',
    maintainer="DeplyAI",
    maintainer_email="support@deplyai.com",
    version='0.2.1',
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
    long_description_content_type='text/markdown'
)