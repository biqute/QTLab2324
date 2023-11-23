from setuptools import setup, find_packages

setup(
    name='h5_and',
    version='0.1',
    author='Riccardo Maifredi',
    packages=find_packages(),
    install_requires='numpy','h5py'
)

!pip install . #type: ignore