#!/usr/bin/env python

from distutils.core import setup

setup(
    name='j2lint',
    version='1.1',
    description='jinja2 linter',
    author='Gerard van Helden',
    author_email='drm@melp.nl',
    license='DBAD',
    url='https://github.com/drm/jinja2-lint',
    entry_points={
        'console_scripts': [
            'j2lint=j2lint:main',
            'jinja2lint=j2lint:main',
        ]
    },
    packages=[
        'j2lint',
    ],
    install_requires=[
        'jinja2',
        'click',
    ],
)
