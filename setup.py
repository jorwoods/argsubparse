import sys
from pathlib import Path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

this_directory = Path(__file__).absolute().parent
with open((this_directory / 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='argsubparse',
    version='0.0.1',
    author='Jordan Woods',
    author_email='jor.e.woods@gmail.com',
    url='https://github.com/jorwoods/argsubparse',
    packages=['argsubparse'],
    license='GNU GPL-3.0',
    description='A Python module for composing command line options.',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
