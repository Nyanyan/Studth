from basic_functions import *
import csv
from collections import deque

inf = 1000

def table_phase0():
    trans_ep = []
    with open('trans_ep_phase0.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans_ep.append([int(i) for i in line.replace('\n', '').split(',')])
    trans_eo = []
    with open('trans_eo.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans_eo.append([int(i) for i in line.replace('\n', '').split(',')])
    trans_co = []
    with open('trans_co.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans_co.append([int(i) for i in line.replace('\n', '').split(',')])
    table = []
    ep_idx = ep2idx_phase0(list(range(12)))
    co_idx = co2idx([0 for _ in range(8)])
    eo_idx = eo2idx([0 for _ in range(12)])
    que = deque([[i, ep_idx, co_idx, eo_idx, [], []] for i in range(24)])
    idxes = set()
    for direction, ep_idx, co_idx, eo_idx, _, _ in que:
        idx = direction + ep_idx * 24 + co_idx * 24 * 495 + eo_idx * 24 * 495 * 2187
        table.append([idx, [], []])
        idxes.add(idx)
    sorted_candidate = sorted(list(candidate[0]))
    cnt = 0
    while que:
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt, len(que))
        direction, ep_idx, co_idx, eo_idx, ans, notation = que.popleft()
        if len(ans) == max_pre_ans[0]:
            continue
        for twist in sorted_candidate:
            rev_twist = rev_twists[twist]
            twist_idx = sorted_candidate.index(rev_twist)
            if not can_rotate[direction][rev_twist // 6]:
                continue
            if notation and twist // 3 == notation[-1]:
                continue
            if len(notation) >= 2 and twist // 6 == notation[-1] // 6 == notation[-2] // 6:
                continue
            n_direction = direction
            n_ep_idx = trans_ep[ep_idx][twist_idx]
            n_co_idx = trans_co[co_idx][twist_idx]
            n_eo_idx = trans_eo[eo_idx][twist_idx]
            idx = n_direction + n_ep_idx * 24 + n_co_idx * 24 * 495 + n_eo_idx * 24 * 495 * 2187
            if idx in idxes:
                continue
            idxes.add(idx)
            n_ans = [i for i in ans]
            n_ans.append(actual_face[n_direction].index(twist // 3) * 3 + twist % 3)
            n_notation = [i for i in notation]
            n_notation.append(twist)
            table.append([idx, n_ans, n_notation])
            que.append([n_direction, n_ep_idx, n_co_idx, n_eo_idx, n_ans, n_notation])
        for rotate in range(12, 14):
            if ans and ans[-1] >= 12:
                continue
            n_ep_idx = ep_idx
            n_co_idx = co_idx
            n_eo_idx = eo_idx
            n_direction = rev_move_dir(direction, rotate)
            idx = n_direction + n_ep_idx * 24 + n_co_idx * 24 * 495 + n_eo_idx * 24 * 495 * 2187
            if idx in idxes:
                continue
            idxes.add(idx)
            n_ans = [i for i in ans]
            n_ans.append(rotate)
            n_notation = [i for i in notation]
            table.append([idx, n_ans, n_notation])
            que.append([n_direction, n_ep_idx, n_co_idx, n_eo_idx, n_ans, n_notation])
    table.sort(key=lambda x:(x[0], len(x[1])))
    print('bef', len(table))
    n_table = []
    f_idx = -1
    for arr in table:
        if arr[0] == f_idx:
            continue
        n_table.append(arr)
        f_idx = arr[0]
    print('aft', len(n_table))
    print(n_table[:30])
    with open('pre_ans_phase0_idx.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        arr = [i[0] for i in n_table]
        writer.writerow(arr)
    with open('pre_ans_phase0_ans.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        all_arr = [list(reversed(i[1])) for i in n_table]
        for arr in all_arr:
            writer.writerow(arr)
    with open('pre_ans_phase0_not.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        all_arr = [list(reversed(i[2])) for i in n_table]
        for arr in all_arr:
            writer.writerow(arr)
    
def table_phase1():
    trans_ep_2 = []
    with open('trans_ep_phase1_2.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans_ep_2.append([int(i) for i in line.replace('\n', '').split(',')])
    trans_cp = []
    with open('trans_cp.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans_cp.append([int(i) for i in line.replace('\n', '').split(',')])
    trans_ep_1 = []
    with open('trans_ep_phase1_1.csv', mode='r') as f:
        for line in map(str.strip, f):
            trans_ep_1.append([int(i) for i in line.replace('\n', '').split(',')])

    table = []
    ep2_idx = ep2idx_phase1_2(list(range(12)))
    cp_idx = cp2idx(list(range(8)))
    ep1_idx = ep2idx_phase1_1(list(range(12)))
    que = deque([[i, ep2_idx, cp_idx, ep1_idx, [], []] for i in range(24)])
    idxes = set()
    for direction, ep2_idx, cp_idx, ep1_idx, _, _ in que:
        idx = direction + ep2_idx * 24 + cp_idx * 24 * 24 + ep1_idx * 24 * 24 * 40320
        table.append([idx, [], []])
        idxes.add(idx)
    sorted_candidate = sorted(list(candidate[1]))
    cnt = 0
    while que:
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt, len(que))
        direction, ep2_idx, cp_idx, ep1_idx, ans, notation = que.popleft()
        if len(ans) == max_pre_ans[1]:
            continue
        for twist in sorted_candidate:
            rev_twist = rev_twists[twist]
            twist_idx = sorted_candidate.index(rev_twist)
            if not can_rotate[direction][rev_twist // 6]:
                continue
            if notation and twist // 3 == notation[-1]:
                continue
            if len(notation) >= 2 and twist // 6 == notation[-1] // 6 == notation[-2] // 6:
                continue
            n_direction = direction
            n_ep2_idx = trans_ep_2[ep2_idx][twist_idx]
            n_cp_idx = trans_cp[cp_idx][twist_idx]
            n_ep1_idx = trans_ep_1[ep1_idx][twist_idx]
            idx = direction + n_ep2_idx * 24 + n_cp_idx * 24 * 24 + n_ep1_idx * 24 * 24 * 40320
            if idx in idxes:
                continue
            idxes.add(idx)
            n_ans = [i for i in ans]
            n_ans.append(actual_face[n_direction].index(twist // 3) * 3 + twist % 3)
            n_notation = [i for i in notation]
            n_notation.append(twist)
            table.append([idx, n_ans, n_notation])
            que.append([n_direction, n_ep2_idx, n_cp_idx, n_ep1_idx, n_ans, n_notation])
        for rotate in range(12, 14):
            if ans and ans[-1] >= 12:
                continue
            n_ep2_idx = ep2_idx
            n_cp_idx = cp_idx
            n_ep1_idx = ep1_idx
            n_direction = rev_move_dir(direction, rotate)
            idx = direction + n_ep2_idx * 24 + n_cp_idx * 24 * 24 + n_ep1_idx * 24 * 24 * 40320
            if idx in idxes:
                continue
            idxes.add(idx)
            n_ans = [i for i in ans]
            n_ans.append(rotate)
            n_notation = [i for i in notation]
            table.append([idx, n_ans, n_notation])
            que.append([n_direction, n_ep2_idx, n_cp_idx, n_ep1_idx, n_ans, n_notation])
    table.sort(key=lambda x:(x[0], len(x[1])))
    print('bef', len(table))
    n_table = []
    f_idx = -1
    for arr in table:
        if arr[0] == f_idx:
            continue
        n_table.append(arr)
        f_idx = arr[0]
    print('aft', len(n_table))
    print(n_table[:30])
    with open('pre_ans_phase1_idx.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        arr = [i[0] for i in n_table]
        writer.writerow(arr)
    with open('pre_ans_phase1_ans.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        all_arr = [list(reversed(i[1])) for i in n_table]
        for arr in all_arr:
            writer.writerow(arr)
    with open('pre_ans_phase1_not.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        all_arr = [list(reversed(i[2])) for i in n_table]
        for arr in all_arr:
            writer.writerow(arr)

table_phase0()
table_phase1()