from plex_database import __version__

from setuptools import setup, find_packages

setup(
    name='plex.database.py',
    version=__version__,
    license='MIT',
    url='https://github.com/fuzeman/plex.database.py',

    author='Dean Gardiner',
    author_email='me@dgardiner.net',

    description='Database extension for plex.py',
    packages=find_packages(exclude=[
        'examples',
        'tests'
    ]),
    platforms='any',

    install_requires=[
        'plex.py'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
