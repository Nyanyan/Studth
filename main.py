# coding:utf-8
from basic_functions import *
from solver import solver
from controller import controller
from detector import detector
from time import sleep, time


stickers = detector()
for i in range(6):
    print(stickers[i * 9:i * 9 + 9])

#sleep(5)
#solution = [0, 3, 13, 6, 17, 2, 11] # R L F2 U B' R' D'
#controller(solution)
#exit()
try:
    # R F2 R2 B2 L F2 R2 B2 R D2 L D' F U' B' R2 D2 F' U2 F' solved in 55.71 sec
    solution = solver(stickers)
    print(solution)
    strt = time()
    controller(solution)
    print('done in', time() - strt, 'sec')
except:
    exit()