# coding:utf-8
from basic_functions import *
from solver import solver
from controller import controller
from detector import detector
from time import sleep

'''
cp = [0, 2, 5, 3, 4, 6, 1, 7]
co = [0, 1, 2, 0, 0, 1, 2, 0]
ep = [0, 9;, 2, 3, 4, 10, 6, 7, 8, 5, 1, 11]
eo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
solution = solver()
'''
stickers = detector()
for i in range(6):
    print(stickers[i * 9:i * 9 + 9])
#sleep(5)
#solution = [0, 3, 13, 6, 17, 2, 11] # R L F2 U B' R' D'
try:
    solution = solver(stickers)
    print(solution)
    controller(solution)
except:
    exit()