# coding:utf-8
import cv2
from time import sleep

from basic_functions import *
from controller import *

def release_half(mode):
    release(mode)
    release(mode + 2)

def release_big_half(mode):
    release_big(mode)
    release_big(mode + 2)

def grab_half(mode):
    grab(mode)
    grab(mode + 2)

def detector():
    for i in range(4):
        grab(i)
    sleep(1)
    capture = cv2.VideoCapture(0)
    #color: wgrboy
    color_low = [[-1 for _ in range(3)] for _ in range(6)]
    color_hgh = [[-1 for _ in range(3)] for _ in range(6)]
    #circlecolor = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 170, 255), (0, 255, 255), (255, 255, 255)]
    vals = [[-1, -1, -1] for _ in range(54)]
    for idx in range(6):
        for i in range(4):
            grab(i)
        sleep(0.1)
        release_big_half(0)
        sleep(0.2)
        for _ in range(5):
            ret, frame = capture.read()
        frame = cv2.resize(frame, (size_x, size_y))
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        for val_coord_idx in val_coord_idxes[0]:
            val_idx = idx * 9 + val_coord_idx
            coord_idx = val_coord_idx
            x = center[0] + dx[coord_idx] * d
            y = center[1] + dy[coord_idx] * d
            vals[val_idx] = [i for i in hsv[y][x]]
        '''
        if idx == 5:
            for dr in range(9):
                cv2.circle(frame, (center[0] + dx[dr] * d, center[1] + dy[dr] * d), 2, (0, 0, 0), 2)
            cv2.imshow('frame', frame)
            cv2.waitKey(0)
        '''
        grab_half(0)
        sleep(0.3)
        release_big_half(1)
        sleep(0.2)
        for _ in range(5):
            ret, frame = capture.read()
        frame = cv2.resize(frame, (size_x, size_y))
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        for val_coord_idx in val_coord_idxes[1]:
            val_idx = idx * 9 + val_coord_idx
            coord_idx = val_coord_idx
            x = center[0] + dx[coord_idx] * d
            y = center[1] + dy[coord_idx] * d
            for dr in range(9):
                for i in range(3):
                    vals[val_idx][i] += hsv[y + dy[dr]][x + dy[dr]][i]
            for i in range(3):
                vals[val_idx][i] /= 9
        for i in range(4):
            grab(i)
        sleep(0.2)
        for action in rotate_cube[idx]:
            for each_action in action:
                send_command(each_action)
            if action[0][2] >= 1000:
                sleep(0.07)
            else:
                sleep(0.3)
    #cv2.destroyAllWindows()
    capture.release()
    for color in range(6):
        #print(vals[center_stickers[color]])
        color_low[color] = [j - offset[i] for i, j in enumerate(vals[center_stickers[color]])]
        color_hgh[color] = [j + offset[i] for i, j in enumerate(vals[center_stickers[color]])]
    res = [-1 for _ in range(54)]
    for i in range(54):
        for color in reversed(range(6)):
            for k in range(3):
                if color == 0 and k == 0:
                    continue
                if not color_low[color][k] <= vals[i][k] <= color_hgh[color][k]:
                    break
            else:
                res[i] = color
                break
    return res

d = 45
size_x = 130
size_y = 100
center = [size_x // 2, size_y // 2]
dx = (-1, 0, 1, -1, 0, 1, -1, 0, 1)
dy = (-1, -1, -1, 0, 0, 0, 1, 1, 1)
val_coord_idxes = [
    [0, 1, 2, 4, 6, 7, 8],
    [3, 5]
]
rotate_cube = [
    [[[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 0, 2000], [1, 0, 2000]], [[0, 1, 0], [1, 1, 1]], [[0, 0, 1000], [1, 0, 1000]], [[1, 1, 2000]], [[1, 1, 0]], [[1, 1, 1000]]],
    [[[1, 0, 2000]], [[1, 0, 1]], [[1, 0, 1000]], [[0, 1, 2000], [1, 1, 2000]], [[0, 0, 1], [1, 0, 0]], [[0, 1, 1000], [1, 1, 1000]], [[0, 0, 2000]], [[0, 0, 0]], [[0, 0, 1000]]],
    [[[1, 0, 2000]], [[1, 0, 1]], [[1, 0, 1000]], [[0, 1, 2000], [1, 1, 2000]], [[0, 0, 1], [1, 0, 0]], [[0, 1, 1000], [1, 1, 1000]], [[0, 0, 2000]], [[0, 0, 0]], [[0, 0, 1000]]],
    [[[1, 0, 2000]], [[1, 0, 1]], [[1, 0, 1000]], [[0, 1, 2000], [1, 1, 2000]], [[0, 0, 1], [1, 0, 0]], [[0, 1, 1000], [1, 1, 1000]], [[0, 0, 2000]], [[0, 0, 0]], [[0, 0, 1000]]],
    [[[1, 0, 2000]], [[1, 0, 1]], [[1, 0, 1000]], [[0, 1, 2000], [1, 1, 2000]], [[0, 0, 1], [1, 0, 0]], [[0, 1, 1000], [1, 1, 1000]], [[0, 0, 2000]], [[0, 0, 0]], [[0, 0, 1000]], [[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 0, 2000], [1, 0, 2000]], [[0, 1, 0], [1, 1, 1]], [[0, 0, 1000], [1, 0, 1000]], [[1, 1, 2000]], [[1, 1, 0]], [[1, 1, 1000]]],
    [[[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 0, 2000], [1, 0, 2000]], [[0, 1, 0], [1, 1, 1]], [[0, 0, 1000], [1, 0, 1000]], [[1, 1, 2000]], [[1, 1, 0]], [[1, 1, 1000]], [[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 0, 2000], [1, 0, 2000]], [[0, 1, 0], [1, 1, 1]], [[0, 0, 1000], [1, 0, 1000]], [[1, 1, 2000]], [[1, 1, 0]], [[1, 1, 1000]]]
]
center_stickers = (4, 13, 22, 31, 40, 49)
offset = (10, 160, 160)

print('detector initialized')

'''
colors[0] = ['', '', 'w', 'g', '', '', '', '']
colors[1] = ['', '', 'o', 'o', '', '', '', '']
colors[2] = ['o', 'y', 'g', 'g', 'w', 'r', 'w', 'b']
colors[3] = ['o', 'b', 'y', 'y', 'g', 'r', 'w', 'b']
colors[4] = ['', '', 'r', 'r', '', '', '', '']
colors[5] = ['', '', 'y', 'b', '', '', '', '']
'''