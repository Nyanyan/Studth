# coding:utf-8
from basic_functions import *
import serial
from time import time, sleep

def grab(num):
    s = str(num) + ' ' + '1000'
    ser_motor[num // 2].write((s + '\n').encode())

def release(num):
    s = str(num) + ' ' + '2000'
    ser_motor[num // 2].write((s + '\n').encode())

def release_big(num):
    s = str(num) + ' ' + '3000'
    ser_motor[num // 2].write((s + '\n').encode())

def send_command(cmd):
    send_num = cmd[0]
    s = ' '.join(str(i) for i in cmd[1:])
    ser_motor[send_num].write((s + '\n').encode())

def controller(solution):
    for twist in solution:
        for i in range(4):
            grab(i)
        sleep(0.1)
        #print(twist, twists_key[twist])
        for action in twists_key[twist]:
            for each_action in action:
                send_command(each_action)
            if action[0][2] >= 1000:
                sleep(0.15)
            else:
                sleep(0.3)
        #sleep(1)

ser_motor = [None, None]
#ser_motor[0] = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01, write_timeout=0)
#ser_motor[1] = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.01, write_timeout=0)
ser_motor[0] = serial.Serial('/dev/tty.usbserial', 115200, timeout=0.01, write_timeout=0)
ser_motor[1] = serial.Serial('/dev/tty.usbserial', 115200, timeout=0.01, write_timeout=0)
sleep(2)
