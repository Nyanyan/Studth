from distutils.core import setup, Extension
from Cython.Build import cythonize
from numpy import get_include # cimport numpy を使うため

filename = input()

ext = Extension("exe_cython_c", sources=[filename], include_dirs=['.', get_include()])
setup(name="exe_cython_c", ext_modules=cythonize([ext]))

f = open('exe_cython_c.cp38-win_amd64.pyd')
f.close()

print('------------------compile done 1------------------')
