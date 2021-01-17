from basic_functions import *
import csv
from collections import deque

inf = 1000

def table_phase0():
    sorted_candidate = sorted(list(candidate[0]))
    pre_ans_idx = []
    with open('pre_ans_phase0_idx.csv', mode='r') as f:
        for line in map(str.strip, f):
            pre_ans_idx = [int(i) for i in line.replace('\n', '').split(',')]
    
    trans_ep = []
    with open('trans_ep_phase0.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans_ep.append([int(i) for i in line.replace('\n', '').split(',')])

    trans = []
    with open('trans_co.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans.append([int(i) for i in line.replace('\n', '').split(',')])
    table = [[[inf for _ in range(2187)] for _ in range(495)] for _ in range(3)]
    que = deque([])
    for idx in pre_ans_idx:
        idx1 = idx % (24 * 495 * 2187) % (24 * 495) // 24
        idx2 = idx % (24 * 495 * 2187) // (24 * 495)
        direction = idx % (24 * 495 * 2187) % (24 * 495) % 24
        que.append([0, idx1, idx2, direction, True])
        table[dir_type[direction]][idx1][idx2] = 0
    cnt = 0
    while que:
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt, len(que))
        cost, idx1, idx2, direction, last_rotated = que.popleft()
        n_cost = cost + 1
        for twist_idx, twist in enumerate(sorted_candidate):
            if not can_rotate[direction][twist // 6]:
                continue
            n_dirs = [direction]
            n_idx1 = trans_ep[idx1][twist_idx]
            n_idx2 = trans[idx2][twist_idx]
            for n_direction in n_dirs:
                if table[dir_type[n_direction]][n_idx1][n_idx2] > n_cost:
                    table[dir_type[n_direction]][n_idx1][n_idx2] = n_cost
                    que.append([n_cost, n_idx1, n_idx2, n_direction, False])
        if last_rotated:
            continue
        for rotate in range(12, 14):
            n_idx1 = idx1
            n_idx2 = idx2
            n_direction = move_dir(direction, rotate)
            if table[dir_type[n_direction]][n_idx1][n_idx2] > n_cost:
                table[dir_type[n_direction]][n_idx1][n_idx2] = n_cost
                que.append([n_cost, n_idx1, n_idx2, n_direction, True])
    for i in range(3):
        with open('prun_phase0_co_ep_' + str(i) + '.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for arr in table[i]:
                writer.writerow(arr)

    trans = []
    with open('trans_eo.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans.append([int(i) for i in line.replace('\n', '').split(',')])
    table = [[[inf for _ in range(2048)] for _ in range(495)] for _ in range(3)]
    que = deque([])
    for idx in pre_ans_idx:
        idx1 = idx % (24 * 495 * 2187) % (24 * 495) // 24
        idx2 = idx // (24 * 495 * 2187)
        direction = idx % (24 * 495 * 2187) % (24 * 495) % 24
        que.append([0, idx1, idx2, direction, True])
        table[dir_type[direction]][idx1][idx2] = 0
    cnt = 0
    while que:
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt, len(que))
        cost, idx1, idx2, direction, last_rotated = que.popleft()
        n_cost = cost + 1
        for twist_idx, twist in enumerate(sorted_candidate):
            n_last_rotated = False
            if not can_rotate[direction][twist // 6]:
                continue
            n_dirs = [direction]
            n_idx1 = trans_ep[idx1][twist_idx]
            n_idx2 = trans[idx2][twist_idx]
            for n_direction in n_dirs:
                if table[dir_type[n_direction]][n_idx1][n_idx2] > n_cost:
                    table[dir_type[n_direction]][n_idx1][n_idx2] = n_cost
                    que.append([n_cost, n_idx1, n_idx2, n_direction, n_last_rotated])
        if last_rotated:
            continue
        for rotate in range(12, 14):
            n_idx1 = idx1
            n_idx2 = idx2
            n_direction = move_dir(direction, rotate)
            n_last_rotated = True
            if table[dir_type[n_direction]][n_idx1][n_idx2] > n_cost:
                table[dir_type[n_direction]][n_idx1][n_idx2] = n_cost
                que.append([n_cost, n_idx1, n_idx2, n_direction, n_last_rotated])
    for i in range(3):
        with open('prun_phase0_eo_ep_' + str(i) + '.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for arr in table[i]:
                writer.writerow(arr)


def table_phase1():
    sorted_candidate = sorted(list(candidate[1]))
    pre_ans_idx = []
    with open('pre_ans_phase0_idx.csv', mode='r') as f:
        for line in map(str.strip, f):
            pre_ans_idx = [int(i) for i in line.replace('\n', '').split(',')]
    
    trans_ep = []
    with open('trans_ep_phase1_2.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans_ep.append([int(i) for i in line.replace('\n', '').split(',')])
    trans = []
    with open('trans_cp.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans.append([int(i) for i in line.replace('\n', '').split(',')])
    table = [[[inf for _ in range(40320)] for _ in range(24)] for _ in range(3)]
    solved1 = ep2idx_phase1_2(list(range(12)))
    solved2 = cp2idx(list(range(8)))
    que = deque([[solved1, solved2, 0, i, True] for i in range(24)])
    for i in range(3):
        table[i][solved1][solved2] = 0
    cnt = 0
    while que:
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt, len(que))
        idx1, idx2, cost, direction, last_rotated = que.popleft()
        n_cost = cost + 1
        for twist_idx, twist in enumerate(sorted_candidate):
            if not can_rotate[direction][twist // 6]:
                continue
            n_dirs = [direction]
            n_idx1 = trans_ep[idx1][twist_idx]
            n_idx2 = trans[idx2][twist_idx]
            for n_direction in n_dirs:
                if table[dir_type[n_direction]][n_idx1][n_idx2] > n_cost:
                    table[dir_type[n_direction]][n_idx1][n_idx2] = n_cost
                    que.append([n_idx1, n_idx2, n_cost, n_direction, False])
        if last_rotated:
            continue
        for rotate in range(12, 14):
            n_idx1 = idx1
            n_idx2 = idx2
            n_direction = move_dir(direction, rotate)
            if table[dir_type[n_direction]][n_idx1][n_idx2] > n_cost:
                table[dir_type[n_direction]][n_idx1][n_idx2] = n_cost
                que.append([n_idx1, n_idx2, n_cost, n_direction, True])
    for i in range(3):
        with open('prun_phase1_cp_ep_' + str(i) + '.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for arr in table[i]:
                writer.writerow(arr)
    
    trans = []
    with open('trans_ep_phase1_1.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans.append([int(i) for i in line.replace('\n', '').split(',')])
    table = [[[inf for _ in range(40320)] for _ in range(24)] for _ in range(3)]
    solved1 = ep2idx_phase1_2(list(range(12)))
    solved2 = ep2idx_phase1_1(list(range(12)))
    que = deque([[solved1, solved2, 0, i, True] for i in range(24)])
    for i in range(3):
        table[i][solved1][solved2] = 0
    cnt = 0
    while que:
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt, len(que))
        idx1, idx2, cost, direction, last_rotated = que.popleft()
        n_cost = cost + 1
        for twist_idx, twist in enumerate(sorted_candidate):
            if not can_rotate[direction][twist // 6]:
                continue
            n_dirs = [direction]
            n_idx1 = trans_ep[idx1][twist_idx]
            n_idx2 = trans[idx2][twist_idx]
            for n_direction in n_dirs:
                if table[dir_type[n_direction]][n_idx1][n_idx2] > n_cost:
                    table[dir_type[n_direction]][n_idx1][n_idx2] = n_cost
                    que.append([n_idx1, n_idx2, n_cost, n_direction, False])
        if last_rotated:
            continue
        for rotate in range(12, 14):
            n_idx1 = idx1
            n_idx2 = idx2
            n_direction = move_dir(direction, rotate)
            if table[dir_type[n_direction]][n_idx1][n_idx2] > n_cost:
                table[dir_type[n_direction]][n_idx1][n_idx2] = n_cost
                que.append([n_idx1, n_idx2, n_cost, n_direction, True])
    for i in range(3):
        with open('prun_phase1_ep_ep_' + str(i) + '.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for arr in table[i]:
                writer.writerow(arr)

#table_phase0()
table_phase1()