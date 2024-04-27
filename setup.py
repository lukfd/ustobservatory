from setuptools import setup, find_packages

PROJECT_NAME = 'ustobservatory'

setup(
    name=PROJECT_NAME,
    version='0.0.1',
    install_requires=[
        'requests',
        'importlib-metadata; python_version<"3.10"',
    ],
    packages=find_packages(
        where='src',
        include=[f'{PROJECT_NAME}*'],
        exclude=[f'{PROJECT_NAME}.tests'],
    ),
    entry_points={
        'console_scripts': [
            f'ust-observatory-cli = {PROJECT_NAME}.cli',
        ]
    }
)