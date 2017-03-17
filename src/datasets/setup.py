from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

extensions = [  Extension("CMatrixDataset", ["CMatrixDataset.pyx"],
                            include_dirs=[numpy.get_include()]),
                Extension("CDictDataset", ["CDictDataset.pyx"]),
                Extension("CListDataset", ["CListDataset.pyx"]),
                Extension("CFlight", ["CFlight.pyx"]),
             ]

setup (
    ext_modules = cythonize(extensions)
)
