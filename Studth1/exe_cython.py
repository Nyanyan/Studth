# coding:utf-8
import sys
import subprocess
import os

args = sys.argv

if len(args) != 2:
    print('args error exit')
    exit()


cmd = 'python setup_exe_cython.py build_ext --inplace'
try:
    o = subprocess.run(cmd.split(), input=args[1], encoding='utf-8', stderr=subprocess.STDOUT, timeout=None)
except subprocess.CalledProcessError as e:
    print('ERROR:', e.stdout)
    exit()

print('------------------compile done 2------------------')

from solver_c import main
main()

#os.remove('exe_cython_cmp.cp38-win_amd64.pyd')