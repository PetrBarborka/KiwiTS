from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

extensions = [  Extension("CAsyncBackTracker", ["CAsyncBackTracker.pyx"]),
             ]

setup (
    ext_modules = cythonize(extensions)
)
