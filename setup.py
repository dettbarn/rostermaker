from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='rostermaker',
    version='0.1.0',
    description='Automatic work schedule generator',
    long_description=readme,
    author='Michael Dettbarn',
    author_email='michael.dettbarn@physik.uni-wuerzburg.de',
    url='https://github.com/dettbarn/rostermaker',
    license=license,
    packages=find_packages()
)
