#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from setuptools import setup, find_packages


short_descr = "Generating high-quality meshes of cell tissue from 3D segmented images"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


# find version number in src/vplants/draco_stem/version.py
version = {}
with open("src/vplants/draco_stem/version.py") as fp:
    exec(fp.read(), version)


setup_kwds = dict(
    name='vplants.draco_stem',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="Guillaume Cerutti, ",
    author_email="guillaume.cerutti@inria.fr, ",
    url='https://github.com/Guillaume Cerutti/draco_stem',
    license='cecill-c',
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        ],
    tests_require=[
        "coverage",
        "mock",
        "nose",
        "sphinx",
        ],
    entry_points={},
    keywords='',
    test_suite='nose.collector',
)
# #}
# change setup_kwds below before the next pkglts tag

setup_kwds['entry_points']['wralea'] = ['draco_stem = openalea.draco_stem_wralea']
setup_kwds['entry_points']['oalab.applet'] = ['oalab.applet/draco = openalea.draco_stem.draco_oalab.plugin.applet']

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
