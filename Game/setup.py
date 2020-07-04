from setuptools import setup, find_packages

ROOT_PACKAGE_NAME = 'game'


def parse_requirements():
    with open('requirements.txt') as file:
        return file.read().splitlines()


setup(
    name=ROOT_PACKAGE_NAME,
    version='1.0',
    author=['Alexey S'],
    packages=find_packages(),
    requirements=parse_requirements()
)
