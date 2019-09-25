from setuptools import setup, find_packages


console_scripts='''
    [console_scripts]
    mapswipe_workers=mapswipe_workers.mapswipe_workers:cli
    '''

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='mapswipe-workers',
    version='3.0',
    description='Install script for the mapswipe Python workers.',
    author='B. Herfort, M. Schaub, M. Reinmuth',
    author_email='',
    url='www.mapswipe.org',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=requirements,
    entry_points=console_scripts
)