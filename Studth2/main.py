# coding:utf-8
print('initializing')
from basic_functions import *
from controller import controller
from detector import detector
from time import sleep, time
import subprocess

def robotize(arr, idx, direction, rotated):
    res = []
    res_size = 1000
    if idx == len(arr):
        return res
    twist_ax = arr[idx] // 6
    twist_face = arr[idx] // 3
    twist_direction = arr[idx] % 3
    if can_rotate[direction][twist_ax]:
        sol = robotize(arr, idx + 1, direction, False)
        sol_size = len(sol)
        if sol_size and sol[0] == -1:
            res.append(-1)
            return res
        res.append(actual_face[direction].index(twist_face) * 3 + twist_direction)
        for i in range(sol_size):
            res.append(sol[i])
    else:
        if rotated:
            res.append(-1)
            return res
        for rotation in range(12, 14):
            n_direction = move_dir(direction, rotation)
            twist_arm = actual_face[n_direction].index(twist_face) * 3 + twist_direction
            sol = robotize(arr, idx + 1, n_direction, True)
            sol_size = len(sol)
            if sol_size and sol[0] == -1:
                continue
            if res_size > sol_size + 2:
                res = []
                res.append(rotation)
                res.append(twist_arm)
                for i in range(sol_size):
                    res.append(sol[i])
    return res

def solver(stickers):
    solver_cpp.stdin.write((' '.join([str(i) for i in stickers]) + '\n').encode('utf-8'))
    solver_cpp.stdin.flush()
    n_solutions = int(solver_cpp.stdout.readline().decode())
    solutions = [[int(i) for i in solver_cpp.stdout.readline().decode().split()] for _ in range(n_solutions)]
    solver_cpp.kill()
    if n_solutions == 0:
        print('cannot solve!')
        return []
    min_len_solution = 100000
    res = []
    for solution in solutions:
        robot_solution = robotize(solution, 0, 0, False)
        if len(robot_solution) < min_len_solution:
            min_len_solution = len(robot_solution)
            res = robot_solution
    print('solution length', min_len_solution)
    print(res)
    return res
    


while True:
    solver_cpp = subprocess.Popen('./solver.out'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
    s = input()
    if s == 'exit':
        exit()
    elif s == 'test':
        w, g, r, b, o, y = range(6)
        # R F2 R2 B2 L F2 R2 B2 R D2 L D' F U' B' R2 D2 F' U2 F'
        stickers = [y, b, r, y, w, w, w, r, y, r, g, g, y, g, r, y, o, o, o, b, y, y, r, w, w, b, b, b, o, r, g, b, r, r, b, o, g, g, g, w, o, o, b, g, o, b, w, g, o, y, y, w, r, w]
    else:
        stickers = detector()
    for i in range(6):
        print(stickers[i * 9:i * 9 + 9])
    try:
        # R F2 R2 B2 L F2 R2 B2 R D2 L D' F U' B' R2 D2 F' U2 F' solved in 55.71 sec
        # L U F' U' F D' R' U' D2 R B2 R D2 F2 L' F2 U2 R D2 U' solved in 51.26 sec
        # L B R2 D2 B R2 D2 B' D2 F L2 F U R' D U2 L D' U2 48.25 sec
        # U B2 L2 U F2 R2 U R2 B2 D' F2 D2 R' D' U2 B' R B2 L2 F U2 38.05 sec
        solution = solver(stickers)
        print(solution)
        strt = time()
        controller(solution)
        print('done in', time() - strt, 'sec')
    except:
        print('error')
        continue