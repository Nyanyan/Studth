# coding:utf-8
from basic_functions import *
import serial
from time import time, sleep

def grab(num):
    s = str(num % 2) + ' ' + '1000'
    ser_motor[num // 2].write((s + '\n').encode())

def release(num):
    s = str(num % 2) + ' ' + '2000'
    ser_motor[num // 2].write((s + '\n').encode())

def release_big(num):
    s = str(num % 2) + ' ' + '3000'
    ser_motor[num // 2].write((s + '\n').encode())

def send_command(cmd):
    send_num = cmd[0]
    s = ' '.join(str(i) for i in cmd[1:])
    ser_motor[send_num].write((s + '\n').encode())

def twist_block_type(twist_block):
    if twist_block[0][2] == 2000:
        return 2
    elif twist_block[0][2] == 1000:
        return 1
    else:
        return 0

def optimise(solution):
    for idx in range(len(solution) - 1):
        twist_block = solution[idx]
        n_twist_block = solution[idx + 1]
        if twist_block_type(twist_block) == twist_block_type(n_twist_block) > 0:
            merged_block = twist_block
            for twist in n_twist_block:
                if not twist in merged_block:
                    merged_block.append(twist)
            del solution[idx]
            del solution[idx + 1]
            solution.insert(idx, merged_block)
            break
    else:
        return solution
    solution = optimise(solution)
    return solution

def controller(solution):
    joined_solution = []
    for twist in solution:
        tmp = []
        for i in range(4):
            tmp.append([i // 2, i % 2, 1000])
        joined_solution.append(tmp)
        joined_solution.extend(twists_key[twist])
    print(joined_solution)
    print(len(joined_solution))
    optimised_solution = optimise(joined_solution)
    print(optimised_solution)
    print(len(optimised_solution))
    for action in optimised_solution:
        for each_action in action:
            send_command(each_action)
        if action[0][2] >= 1000:
            sleep(0.1)
        else:
            sleep(0.35)

ser_motor = [None, None]
'''
ser_motor[0] = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01, write_timeout=0)
ser_motor[1] = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.01, write_timeout=0)
sleep(2)
'''
