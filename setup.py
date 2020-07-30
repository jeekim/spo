# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='spo',
    version='0.0.1',
    description='',
    long_description=readme,
    author='',
    author_email='',
    url='',
    packages=find_packages(exclude=('tests', 'docs'))
)
