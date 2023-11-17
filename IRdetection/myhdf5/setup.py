from setuptools import setup, find_packages

setup(
    name='mylibrary',
    version='0.1',
    author='Riccardo Maifredi',
    packages=find_packages(),
    install_requires='numpy','h5py'
)

!pip install .