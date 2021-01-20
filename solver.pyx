# distutils: language=c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True

import cython
from libcpp.vector cimport vector
from libcpp cimport bool

from basic_functions import *

cdef idxes_init(int phase, cp, co, ep, eo):
    cdef int[3] res
    if phase == 0:
        res[0] = co2idx(co)
        res[1] = eo2idx(eo)
        res[2] = ep2idx_phase0(ep)
    else:
        res[0] = cp2idx(cp)
        res[1] = ep2idx_phase1_1(ep)
        res[2] = ep2idx_phase1_2(ep)
    return res

cdef int trans1(int phase, int idx1, int twist):
    if phase == 0:
        return trans_co[idx1][twist]
    else:
        return trans_cp[idx1][twist]

cdef int trans2(int phase, int idx2, int twist):
    if phase == 0:
        return trans_eo[idx2][twist]
    else:
        return trans_ep_phase1_1[idx2][twist]

cdef int trans3(int phase, int idx3, int twist):
    if phase == 0:
        return trans_ep_phase0[idx3][twist]
    else:
        return trans_ep_phase1_2[idx3][twist]

cdef int distance(int phase, int idx1, int idx2, int idx3):
    if phase == 0:
        return max(prun_phase0_co_ep[idx3][idx1], prun_phase0_eo_ep[idx3][idx2])
    else:
        return max(prun_phase1_cp_ep[idx3][idx1], prun_phase1_ep_ep[idx3][idx2])

cdef vector[vector[int]] phase_search(int phase, int idx1, int idx2, int idx3, int depth, int dis, int len_phase_solution):
    global phase_solution
    cdef vector[vector[int]] res
    if depth == 0:
        if dis == 0:
            res.push_back(phase_solution)
        return res
    elif dis == 0:
        return res
    cdef int l1_twist, l2_twist, twist_idx, twist, n_idx1, n_idx2, n_idx3, n_dis
    cdef vector[vector[int]] sol
    depth -= 1
    l1_twist = phase_solution[len_phase_solution - 1] if len_phase_solution >= 1 else -10
    l2_twist = phase_solution[len_phase_solution - 2] if len_phase_solution >= 2 else -10
    for twist_idx, twist in enumerate(candidate[phase]):
        if twist // 3 == l1_twist // 3: # don't turn same face twice
            continue
        if twist // 3 == l2_twist // 3 and twist // 6 == l1_twist // 6: # don't turn opposite face 3 times
            continue
        if twist // 6 == l1_twist // 6 and twist < l1_twist: # for example, permit R L but not L R
            continue
        n_idx1 = trans1(phase, idx1, twist_idx)
        n_idx2 = trans2(phase, idx2, twist_idx)
        n_idx3 = trans3(phase, idx3, twist_idx)
        n_dis = distance(phase, n_idx1, n_idx2, n_idx3)
        if n_dis > depth:
            continue
        phase_solution.push_back(twist)
        sol = phase_search(phase, n_idx1, n_idx2, n_idx3, depth, n_dis, len_phase_solution + 1)
        sol_size = sol.size()
        if phase == 1 and sol_size: # only one solution needed
            return sol
        for idx in range(sol_size):
            res.push_back(sol[idx])
        if res.size() > 50:
            return res
        phase_solution.pop_back()
    return res

cdef robotize(vector[int] arr, int idx, int direction):
    cdef int twist_ax, twist_face, twist_direction
    if idx == len(arr):
        return []
    res = []
    twist_ax = arr[idx] // 6
    twist_face = arr[idx] // 3
    twist_direction = arr[idx] % 3
    if can_rotate[direction][twist_ax]:
        res.append(actual_face[direction].index(twist_face) * 3 + twist_direction)
        res.extend(robotize(arr, idx + 1, direction))
    else:
        for rotation in range(12, 14):
            n_direction = move_dir(direction, rotation)
            twist_arm = actual_face[n_direction].index(twist_face) * 3 + twist_direction
            n_res = [rotation, twist_arm]
            n_res.extend(robotize(arr, idx + 1, n_direction))
            if len(res) == 0 or len(res) > len(n_res):
                res = [i for i in n_res]
    return res


def solver():
    global phase_solution
    min_phase0_depth = 0
    res = []
    l = 27
    '''
    s_cp, s_co, s_ep, s_eo = sticker2arr(stickers)
    if s_cp.count(-1) == 1 and len((set(range(8)) - set(s_cp))) == 1:
        s_cp[s_cp.index(-1)] = list(set(range(8)) - set(s_cp))[0]
    if s_ep.count(-1) == 1 and len((set(range(12)) - set(s_ep))) == 1:
        s_ep[s_ep.index(-1)] = list(set(range(12)) - set(s_ep))[0]
    if s_co.count(-1) == 1:
        s_co[s_co.index(-1)] = (3 - (sum(s_co) + 1) % 3) % 3
    if s_eo.count(-1) == 1:
        s_eo[s_eo.index(-1)] = (2 - (sum(s_eo) + 1) % 2) % 2
    '''
    s_cp = list(range(8))
    s_co = [0 for _ in range(8)]
    s_ep = list(range(12))
    s_eo = [0 for _ in range(12)]
    from random import randint
    for _ in range(40):
        twist = randint(0, 17)
        s_cp = move_cp(s_cp, twist)
        s_co = move_co(s_co, twist)
        s_ep = move_ep(s_ep, twist)
        s_eo = move_eo(s_eo, twist)
    while True:
        search_lst = [[s_cp, s_co, s_ep, s_eo, []]]
        n_search_lst = []
        for phase in range(2):
            for cp, co, ep, eo, last_solution in search_lst:
                idx1, idx2, idx3 = idxes_init(phase, cp, co, ep, eo)
                dis = distance(phase, idx1, idx2, idx3)
                phase_solution = []
                strt_depth = dis if phase == 1 else max(dis, min_phase0_depth)
                for depth in range(strt_depth, l - len(last_solution)):
                    sol = phase_search(phase, idx1, idx2, idx3, depth, dis, 0)
                    if sol.size():
                        for solution in sol:
                            n_cp = [i for i in cp]
                            n_co = [i for i in co]
                            n_ep = [i for i in ep]
                            n_eo = [i for i in eo]
                            n_solution = [i for i in last_solution]
                            for twist in solution:
                                n_cp = move_cp(n_cp, twist)
                                n_co = move_co(n_co, twist)
                                n_ep = move_ep(n_ep, twist)
                                n_eo = move_eo(n_eo, twist)
                                n_solution.append(twist)
                            n_search_lst.append([n_cp, n_co, n_ep, n_eo, n_solution])
                            if phase == 1:
                                l = min(l, len(n_solution))
                        if phase == 0:
                            min_phase0_depth = depth + 1
                        break
            search_lst = [[i for i in j] for j in n_search_lst]
            n_search_lst = []
            print('max len', l, 'phase', phase, 'depth', depth, 'found solutions', len(search_lst))
        if search_lst:
            len_res = 1000
            res = []
            for _, _, _, _, res_candidate in search_lst:
                robotized_res_can = robotize(res_candidate, 0, 0)
                if len(robotized_res_can) < len_res:
                    res = [i for i in robotized_res_can]
        #else:
        break
    return res

cdef vector[int] phase_solution = []
cdef int[2187][14] trans_co
with open('trans_co.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        for idx2, i in enumerate(line.replace('\n', '').split(',')):
            trans_co[idx][idx2] = int(i)
cdef int[40320][10] trans_cp
with open('trans_cp.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        for idx2, i in enumerate(line.replace('\n', '').split(',')):
            trans_cp[idx][idx2] = int(i)
cdef int[2048][14] trans_eo
with open('trans_eo.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        for idx2, i in enumerate(line.replace('\n', '').split(',')):
            trans_eo[idx][idx2] = int(i)
cdef int[495][14] trans_ep_phase0
with open('trans_ep_phase0.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        for idx2, i in enumerate(line.replace('\n', '').split(',')):
            trans_ep_phase0[idx][idx2] = int(i)
cdef int[40320][10] trans_ep_phase1_1
with open('trans_ep_phase1_1.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        for idx2, i in enumerate(line.replace('\n', '').split(',')):
            trans_ep_phase1_1[idx][idx2] = int(i)
cdef int[24][10] trans_ep_phase1_2
with open('trans_ep_phase1_2.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        for idx2, i in enumerate(line.replace('\n', '').split(',')):
            trans_ep_phase1_2[idx][idx2] = int(i)

cdef int[495][2187] prun_phase0_co_ep
with open('prun_phase0_co_ep.csv', mode='r') as f:
    for idx2, line in enumerate(map(str.strip, f)):
        for idx3, i in enumerate(line.replace('\n', '').split(',')):
            prun_phase0_co_ep[idx2][idx3] = int(i)
cdef int[495][2048] prun_phase0_eo_ep
with open('prun_phase0_eo_ep.csv', mode='r') as f:
    for idx2, line in enumerate(map(str.strip, f)):
        for idx3, i in enumerate(line.replace('\n', '').split(',')):
            prun_phase0_eo_ep[idx2][idx3] = int(i)
cdef int[24][40320] prun_phase1_cp_ep
with open('prun_phase1_cp_ep.csv', mode='r') as f:
    for idx2, line in enumerate(map(str.strip, f)):
        for idx3, i in enumerate(line.replace('\n', '').split(',')):
            prun_phase1_cp_ep[idx2][idx3] = int(i)
cdef int[24][40320] prun_phase1_ep_ep
with open('prun_phase1_ep_ep.csv', mode='r') as f:
    for idx2, line in enumerate(map(str.strip, f)):
        for idx3, i in enumerate(line.replace('\n', '').split(',')):
            prun_phase1_ep_ep[idx2][idx3] = int(i)
print('initialize done')


''' TEST '''
def main():
    from time import time
    num = 100
    tim = []
    lns = []
    for i in range(num):
        strt = time()
        ln = len(solver())
        print(i)
        end = time()
        tim.append(end - strt)
        lns.append(ln)
    print('avg tim', sum(tim) / num)
    print('max tim', max(tim))
    print('min tim', min(tim))
    print('avg len', sum(lns) / num)
    print('max len', max(lns))
    print('min len', min(lns))
    '''
    w, g, r, b, o, y = range(6)
    arr = arr = [y, b, r, y, w, w, w, r, y, r, g, g, y, g, r, y, o, o, o, b, y, y, r, w, w, b, b, b, o, r, g, b, r, r, b, o, g, g, g, w, o, o, b, g, o, b, w, g, o, y, y, w, r, w] # R F2 R2 B2 L F2 R2 B2 R D2 L D' F U' B' R2 D2 F' U2 F'
    strt = time()
    tmp = solver(arr)
    print(len(tmp), tmp)
    print(time() - strt)
    '''