#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Setup tools wrapper
"""

from setuptools import find_packages, setup

setup(
    name='deplyai-cli',
    maintainer="DeplyAI",
    maintainer_email="support@deplyai.com",
    version='0.1',
    zip_safe=False,
    description='DeplyAI CLI',
    long_description="",
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
    scripts=['deply']
)