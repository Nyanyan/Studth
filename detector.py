# coding:utf-8
import cv2
from time import sleep
from copy import deepcopy

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
    #color_low = [[-1 for _ in range(3)] for _ in range(6)]
    #color_hgh = [[-1 for _ in range(3)] for _ in range(6)]
    colors = [[-1 for _ in range(3)] for _ in range(6)]
    #circlecolor = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 170, 255), (0, 255, 255), (255, 255, 255)]
    vals = [[0, 0, 0] for _ in range(54)]
    for _ in range(20):
        ret, frame = capture.read()
    for idx in range(6):
        for i in range(4):
            grab(i)
        sleep(0.1)
        release_big_half(0)
        sleep(0.3)
        frames = []
        for _ in range(5):
            ret, frame = capture.read()
        for _ in range(8):
            frame = cv2.resize(frame, (size_x, size_y))
            frames.append(frame)
        n_frames = []
        while len(frames) > 1:
            for i in range(0, len(frames), 2):
                n_frames.append(cv2.addWeighted(frames[i], 0.5, frames[i + 1], 0.5, 0))
            frames = deepcopy(n_frames)
            n_frames = []
        hsv = cv2.cvtColor(frames[0],cv2.COLOR_BGR2HSV)
        for val_coord_idx in val_coord_idxes[0]:
            val_idx = idx * 9 + val_coord_idx
            coord_idx = val_coord_idx
            x = center[0] + dx[coord_idx] * d
            y = center[1] + dy[coord_idx] * d
            tmp = [[] for _ in range(3)]
            for dr in range(9):
                for i in range(3):
                    tmp[i].append(hsv[y + dy[dr]][x + dy[dr]][i])
                    if i == 0 and tmp[i][-1] > 150:
                        tmp[i][-1] -= 180
            for i in range(3):
                tmp[i].sort()
            for i in range(3):
                vals[val_idx][i] = sum(tmp[i][2:7]) / 5
                if i == 0 and vals[val_idx][i] < 0:
                    vals[val_idx][i] += 180
        
        if idx == 0:
            for dr in range(9):
                cv2.circle(frame, (center[0] + dx[dr] * d, center[1] + dy[dr] * d), 2, (0, 0, 0), 2)
            cv2.imshow('frame', frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        grab_half(0)
        sleep(0.25)
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
            tmp = [[] for _ in range(3)]
            for dr in range(9):
                for i in range(3):
                    tmp[i].append(hsv[y + dy[dr]][x + dy[dr]][i])
                    if i == 0 and tmp[i][-1] > 150:
                        tmp[i][-1] -= 180
            for i in range(3):
                tmp[i].sort()
            for i in range(3):
                vals[val_idx][i] = sum(tmp[i][2:7]) / 5
                if i == 0 and vals[val_idx][i] < 0:
                    vals[val_idx][i] += 180
        for i in range(4):
            grab(i)
        sleep(0.2)
        for action in rotate_cube[idx]:
            for each_action in action:
                send_command(each_action)
            if action[0][2] >= 1000:
                sleep(0.08)
            else:
                sleep(0.25)
    #cv2.destroyAllWindows()
    capture.release()
    white_idx = -1
    s_min = 10000
    for color in range(6):
        colors[color] = [i for i in vals[center_stickers[color]]]
        print(color, vals[center_stickers[color]])
        if vals[center_stickers[color]][1] < s_min:
            white_idx = color
            s_min = vals[center_stickers[color]][1]
    res = [-1 for _ in range(54)]
    for i in range(54):
        if vals[i][1] < 75:
            res[i] = white_idx
            continue
        min_error = 10000000
        for color in range(6):
            if color == white_idx:
                continue
            error = 0
            k = 0
            error = weight[k] * min(abs(vals[i][k] - colors[color][k]), abs(vals[i][k] - colors[color][k] - 180), abs(vals[i][k] - colors[color][k] + 180))
            if min_error > error:
                min_error = error
                res[i] = color
    return res

d = 40
size_x = 130
size_y = 100
center = [size_x // 2, size_y // 2]
dx = (-1, 0, 1, -1, 0, 1, -1, 0, 1)
dy = (-1, -1, -1, 0, 0, 0, 1, 1, 1)
val_coord_idxes = [
    [0, 1, 2, 4, 6, 7, 8],
    [3, 5]
]

'''
rotate_cube = [
    [[[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 0, 2000], [1, 0, 2000]], [[0, 1, 0], [1, 1, 1]], [[0, 0, 1000], [1, 0, 1000]], [[1, 1, 2000]], [[1, 1, 0]], [[1, 1, 1000]]],
    [[[1, 0, 2000]], [[1, 0, 1]], [[1, 0, 1000]], [[0, 1, 2000], [1, 1, 2000]], [[0, 0, 1], [1, 0, 0]], [[0, 1, 1000], [1, 1, 1000]], [[0, 0, 2000]], [[0, 0, 0]], [[0, 0, 1000]]],
    [[[1, 0, 2000]], [[1, 0, 1]], [[1, 0, 1000]], [[0, 1, 2000], [1, 1, 2000]], [[0, 0, 1], [1, 0, 0]], [[0, 1, 1000], [1, 1, 1000]], [[0, 0, 2000]], [[0, 0, 0]], [[0, 0, 1000]]],
    [[[1, 0, 2000]], [[1, 0, 1]], [[1, 0, 1000]], [[0, 1, 2000], [1, 1, 2000]], [[0, 0, 1], [1, 0, 0]], [[0, 1, 1000], [1, 1, 1000]], [[0, 0, 2000]], [[0, 0, 0]], [[0, 0, 1000]]],
    [[[1, 0, 2000]], [[1, 0, 1]], [[1, 0, 1000]], [[0, 1, 2000], [1, 1, 2000]], [[0, 0, 1], [1, 0, 0]], [[0, 1, 1000], [1, 1, 1000]], [[0, 0, 2000]], [[0, 0, 0]], [[0, 0, 1000]], [[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 0, 2000], [1, 0, 2000]], [[0, 1, 0], [1, 1, 1]], [[0, 0, 1000], [1, 0, 1000]], [[1, 1, 2000]], [[1, 1, 0]], [[1, 1, 1000]]],
    [[[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 0, 2000], [1, 0, 2000]], [[0, 1, 0], [1, 1, 1]], [[0, 0, 1000], [1, 0, 1000]], [[1, 1, 2000]], [[1, 1, 0]], [[1, 1, 1000]], [[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 0, 2000], [1, 0, 2000]], [[0, 1, 0], [1, 1, 1]], [[0, 0, 1000], [1, 0, 1000]], [[1, 1, 2000]], [[1, 1, 0]], [[1, 1, 1000]]]
]
'''
rotate_cube = [
    [[[1, 2000]], [[1, 1]], [[1, 1000]], [[0, 2000], [2, 2000]], [[1, 0], [3, 1]], [[0, 1000], [2, 1000]], [[3, 2000]], [[3, 0]], [[3, 1000]]]
    [[[2, 2000]], [[2, 1]], [[2, 1000]], [[1, 2000], [3, 2000]], [[0, 1], [2, 0]], [[1, 1000], [3, 1000]], [[0, 2000]], [[0, 0]], [[0, 1000]]]
    [[[2, 2000]], [[2, 1]], [[2, 1000]], [[1, 2000], [3, 2000]], [[0, 1], [2, 0]], [[1, 1000], [3, 1000]], [[0, 2000]], [[0, 0]], [[0, 1000]]]       
    [[[2, 2000]], [[2, 1]], [[2, 1000]], [[1, 2000], [3, 2000]], [[0, 1], [2, 0]], [[1, 1000], [3, 1000]], [[0, 2000]], [[0, 0]], [[0, 1000]]]       
    [[[2, 2000]], [[2, 1]], [[2, 1000]], [[1, 2000], [3, 2000]], [[0, 1], [2, 0]], [[1, 1000], [3, 1000]], [[0, 2000]], [[0, 0]], [[0, 1000]], [[1, 2000]], [[1, 1]], [[1, 1000]], [[0, 2000], [2, 2000]], [[1, 0], [3, 1]], [[0, 1000], [2, 1000]], [[3, 2000]], [[3, 0]], [[3, 1000]]]
    [[[1, 2000]], [[1, 1]], [[1, 1000]], [[0, 2000], [2, 2000]], [[1, 0], [3, 1]], [[0, 1000], [2, 1000]], [[3, 2000]], [[3, 0]], [[3, 1000]], [[1, 2000]], [[1, 1]], [[1, 1000]], [[0, 2000], [2, 2000]], [[1, 0], [3, 1]], [[0, 1000], [2, 1000]], [[3, 2000]], [[3, 0]], [[3, 1000]]]
]
center_stickers = (4, 13, 22, 31, 40, 49)
#offset = (10, 120, 120)
weight = (5, 1, 3)
weight_white = (0, 5, 4)

print('detector initialized')
