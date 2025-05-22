'''
IMPORTS
python.exe -m build (NÅR MAN STÅR I PROJEKTFOLDEREN)
'''
from setuptools import setup, find_packages

setup(
    name='NKDatabase',
    version='1.0.1',
    packages=find_packages(),
    install_requires=["psycopg2>=2.9.9",],
    author = 'Mads Lindeholm & Lars Kasper',
    author_email='madvli@naestved.dk & lakas@naestved.dk',
    description='Module for NK database utilities',
)
