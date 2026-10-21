from setuptools import setup
from Cython.Build import cythonize

setup(
    name='COLDEV_EEG_VIZ',
    version='0.0.1',
    ext_modules=cythonize("main.py"),
)