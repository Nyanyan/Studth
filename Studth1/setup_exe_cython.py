# coding:utf-8
from distutils.core import setup, Extension
from Cython.Build import cythonize
from numpy import get_include

filename = input()

ext = Extension("solver_c", sources=[filename], include_dirs=['.', get_include()])
setup(name="solver_c", ext_modules=cythonize([ext]))

#f = open('solver_c.cp38-win_amd64.pyd')
#f.close()

print('------------------compile done 1------------------')
