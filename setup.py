#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Public Domain

"""
Simple "state machine" library
============================
"""

VERSION = "0.1-git"

from setuptools import setup, find_packages


setup(
    name="Simple statemachine",
    version=VERSION,
    description="A Simple state machine framework",
    long_description=__doc__,
    author="Ronan Dunklau",
    author_email="ronan.dunklau@kozea.fr",
    url="http://www.dyko.org/",
    download_url="http://www.dyko.org/src/dyko/Dyko-%s.tar.gz" % VERSION,
    license="GNU iLGPL v3",
    platforms="Any",
    packages=find_packages(
        exclude=["*._test", "*._test.*", "test.*", "test"]),
    provides=["statemachine"],
    keywords=["web", "framework", "database"])
