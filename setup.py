from setuptools import setup, find_packages

setup(
    name='betweenle_solver',
    version='1.0.0',
    description='A solver for the Betweenle word game',
    author='llucid-97',
    author_email='hexxagon6@gmail.com',
    packages=find_packages(),
    install_requires=[
        'nltk',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'betweenle_solver = betweenle_solver.solver:main',
        ],
    },
)