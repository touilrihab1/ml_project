#setup.py is used to install the package and its dependencies. It also provides metadata about the package.
#it is useful for distributing the package to others and for installing it in different environments.
from setuptools import setup, find_packages
from typing import List
def get_requirements(file_path:str)->List[str]:
    '''
    the functions return the list of requirements from the given file path.
    '''
    requirement= []
    with open(file_path) as file:
        requirement=file.read().splitlines()
        requirement=[req.replace("\n","") for req in requirement]
        if '-e .' in requirement:
            requirement.remove('-e .')
    return requirement
         
setup(
    name='mlproject',
    version='0.1.0',
    packages=find_packages(),
    install_requires=get_requirements('requirement.txt'),
    author='rihab',
    description='A sample Python package for machine learning.'
)