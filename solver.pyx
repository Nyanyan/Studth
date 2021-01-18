from basic_functions import *

cdef idxes_init(int phase, cp, co, ep, eo, int direction):
    cdef int[4] res
    if phase == 0:
        res[0] = co2idx(co)
        res[1] = eo2idx(eo)
        res[2] = ep2idx_phase0(ep)
    else:
        res[0] = cp2idx(cp)
        res[1] = ep2idx_phase1_1(ep)
        res[2] = ep2idx_phase1_2(ep)
    res[3] = direction
    return res

cdef trans(int phase, int idx1, int idx2, int idx3, int idx4, int twist):
    cdef int[4] res
    if phase == 0:
        res[0] = trans_co[idx1][twist]
        res[1] = trans_eo[idx2][twist]
        res[2] = trans_ep_phase0[idx3][twist]
    else:
        res[0] = trans_cp[idx1][twist]
        res[1] = trans_ep_phase1_1[idx2][twist]
        res[2] = trans_ep_phase1_2[idx3][twist]
    res[3] = idx4
    return res

cdef int distance(int phase, int idx1, int idx2, int idx3, int idx4):
    direction_type = dir_type[idx4]
    if phase == 0:
        return max(prun_phase0_co_ep[direction_type][idx3][idx1], prun_phase0_eo_ep[direction_type][idx3][idx2]) # + int(p2 * abs(prun_phase0_co_ep[direction_type][idxes[2]][idxes[0]] - prun_phase0_eo_ep[direction_type][idxes[2]][idxes[1]]) ** p1)
    else:
        return max(prun_phase1_cp_ep[direction_type][idx3][idx1], prun_phase1_ep_ep[direction_type][idx3][idx2]) # + int(p2 * abs(prun_phase1_cp_ep[direction_type][idxes[2]][idxes[0]] - prun_phase1_ep_ep[direction_type][idxes[2]][idxes[1]]) ** p1)
'''
def search(phase, num):
    l = 0
    r = len(pre_ans_idx[phase]) - 1
    while r - l > 1:
        c = (r + l) // 2
        if pre_ans_idx[phase][c] > num:
            r = c
        elif pre_ans_idx[phase][c] < num:
            l = c
        else:
            r = c
            l = c
    if pre_ans_idx[phase][l] == num:
        return l
    elif pre_ans_idx[phase][r] == num:
        return r
    else:
        return -1

def search_idx(phase, idxes):
    if phase == 0:
        idx = idxes[3] + idxes[2] * 24 + idxes[0] * 24 * 495 + idxes[1] * 24 * 495 * 2187
    else:
        idx = idxes[3] + idxes[2] * 24 + idxes[0] * 24 * 24 + idxes[1] * 24 * 24 * 40320
    return search(phase, idx)
'''
#cdef int last_rotated, l2_rotated, l1_twist, l2_twist, n_pre_direction, n_dis
cdef phase_search(int phase, int idx1, int idx2, int idx3, int direction, int depth, int dis, int pre_direction):
    global phase_solution, n_idxes, cnt #, last_rotated, l2_rotated, l1_twist, l2_twist, n_pre_direction, n_dis
    cdef int twist_idx, twist, last_rotated, l2_rotated, l1_twist, l2_twist, n_pre_direction, n_dis
    cnt += 1
    '''
    if dis <= max_pre_ans[phase] <= depth:
        pre_idx = search_idx(phase, idxes)
        if pre_idx != -1:
            #print(depth, len(phase_solution), pre_idx)
            res = [i for i in phase_solution]
            res.extend(pre_ans_ans[phase][pre_idx])
            res_notation = [i for i in phase_solution_notation]
            res_notation.extend(pre_ans_not[phase][pre_idx])
            return [[res, res_notation]]
    if depth <= max_pre_ans[phase]:
        return []
    '''
    if dis == 0:
        return [[[i for i in phase_solution], [i for i in phase_solution_notation]]]
    if depth == 0:
        return []
    
    #print(dis, depth, phase_solution_notation)
    res = []
    depth -= 1
    last_rotated = phase_solution[-1] if phase_solution and phase_solution[-1] >= 12 else -10
    l2_rotated = phase_solution[-2] if len(phase_solution) >= 2 and phase_solution[-2] >= 12 else -10
    l1_twist = phase_solution_notation[-1] if phase_solution_notation else -10
    l2_twist = phase_solution_notation[-2] if len(phase_solution_notation) >= 2 else -10
    can_twist = can_twists[direction][pre_direction]
    n_pre_direction = direction
    for twist_idx in range(14):
        if twist_idx <= 11:
            twist = actual_face[direction][twist_idx // 3] * 3 + twist_idx % 3
            if twist // 3 == l1_twist // 3: # don't turn same face twice
                continue
            if twist // 6 == l1_twist // 6 == l2_twist // 6: # don't turn opposite face 3 times
                continue
            if twist // 6 == l1_twist // 6 and twist > l1_twist: # for example, permit R L but not L R
                continue
            if not twist in candidate[phase]:
                continue
            if not actual_face[direction][twist_idx // 3] in can_twist:
                continue
            n_idx1, n_idx2, n_idx3, n_direction = trans(phase, idx1, idx2, idx3, direction, twist2phase_idx[phase][twist])
        else:
            if last_rotated != -10: # don't rotate whole cube more than once
                continue
            if l2_rotated != -10: # don't rotate whole cube before twisting faces 2 or more times
                continue
            n_idx1, n_idx2, n_idx3 = idx1, idx2, idx3
            n_direction = move_dir(direction, twist_idx)
        n_dis = distance(phase, n_idx1, n_idx2, n_idx3, n_direction)
        if n_dis > depth: # or (n_dis > dis + 1 and random() < 0.5):
            continue
        phase_solution.append(twist_idx)
        if twist_idx <= 11:
            phase_solution_notation.append(twist)
        sol = phase_search(phase, n_idx1, n_idx2, n_idx3, n_direction, depth, n_dis, n_pre_direction)
        if sol: # only one solution needed
            return sol
        '''
        res.extend(sol)
        if len(res) > 50:
            return res
        '''
        phase_solution.pop()
        if twist_idx <= 11:
            phase_solution_notation.pop()
    return res

def solver(stickers):
    global phase_solution, phase_solution_notation
    res = []
    l = 35
    s_cp, s_co, s_ep, s_eo = sticker2arr(stickers)
    if s_cp.count(-1) == 1 and len((set(range(8)) - set(s_cp))) == 1:
        s_cp[s_cp.index(-1)] = list(set(range(8)) - set(s_cp))[0]
    if s_ep.count(-1) == 1 and len((set(range(12)) - set(s_ep))) == 1:
        s_ep[s_ep.index(-1)] = list(set(range(12)) - set(s_ep))[0]
    if s_co.count(-1) == 1:
        s_co[s_co.index(-1)] = (3 - (sum(s_co) + 1) % 3) % 3
    if s_eo.count(-1) == 1:
        s_eo[s_eo.index(-1)] = (2 - (sum(s_eo) + 1) % 2) % 2
    s_dir = 0
    #print(s_cp)
    #print(s_ep)
    if -1 in s_cp or -1 in s_co or -1 in s_ep or -1 in s_eo:
        raise Exception('Error')
    while True:
        search_lst = [[s_cp, s_co, s_ep, s_eo, s_dir, []]]
        n_search_lst = []
        for phase in range(2):
            for cp, co, ep, eo, direction, last_solution in search_lst:
                idx1, idx2, idx3, idx4 = idxes_init(phase, cp, co, ep, eo, direction)
                dis = distance(phase, idx1, idx2, idx3, idx4)
                phase_solution = []
                phase_solution_notation = []
                strt_depth = dis
                for depth in range(strt_depth, l - len(last_solution)):
                    #print(depth)
                    sol = phase_search(phase, idx1, idx2, idx3, idx4, depth, dis, 24)
                    if sol:
                        for solution, solution_notation in sol:
                            n_cp = [i for i in cp]
                            n_co = [i for i in co]
                            n_ep = [i for i in ep]
                            n_eo = [i for i in eo]
                            n_dir = direction
                            n_solution = [i for i in last_solution]
                            for twist in solution_notation:
                                n_cp = move_cp(n_cp, twist)
                                n_co = move_co(n_co, twist)
                                n_ep = move_ep(n_ep, twist)
                                n_eo = move_eo(n_eo, twist)
                            for twist_arm in solution:
                                n_dir = move_dir(n_dir, twist_arm)
                            n_solution.extend(solution)
                            n_search_lst.append([n_cp, n_co, n_ep, n_eo, n_dir, n_solution])
                            if phase == 1:
                                l = min(l, len(n_solution))
                        if phase == 0:
                            min_phase0_depth = depth + 1
                        break
            search_lst = [[i for i in j] for j in n_search_lst]
            n_search_lst = []
            print('max len', l, 'phase', phase, 'depth', depth, 'found solutions', len(search_lst))
            print(cnt)
        if search_lst:
            res = [i for i in search_lst[-1][5]]
        #else:
        break
    return res

phase_solution = []
phase_solution_notation = []

cdef int[2187][14] trans_co
with open('trans_co.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        trans_co[idx] = [int(i) for i in line.replace('\n', '').split(',')]
cdef int[40320][10] trans_cp
with open('trans_cp.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        trans_cp[idx] = [int(i) for i in line.replace('\n', '').split(',')]
cdef int[2048][14] trans_eo
with open('trans_eo.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        trans_eo[idx] = [int(i) for i in line.replace('\n', '').split(',')]
cdef int[495][14] trans_ep_phase0
with open('trans_ep_phase0.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        trans_ep_phase0[idx] = [int(i) for i in line.replace('\n', '').split(',')]
cdef int[40320][10] trans_ep_phase1_1
with open('trans_ep_phase1_1.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        trans_ep_phase1_1[idx] = [int(i) for i in line.replace('\n', '').split(',')]
cdef int[24][10] trans_ep_phase1_2
with open('trans_ep_phase1_2.csv', mode='r') as f:
    for idx, line in enumerate(map(str.strip, f)):
        trans_ep_phase1_2[idx] = [int(i) for i in line.replace('\n', '').split(',')]

cdef int[3][495][2187] prun_phase0_co_ep
for idx in range(3):
    with open('prun_phase0_co_ep_' + str(idx) + '.csv', mode='r') as f:
        for idx2, line in enumerate(map(str.strip, f)):
            prun_phase0_co_ep[idx][idx2] = [int(i) for i in line.replace('\n', '').split(',')]
cdef int[3][495][2048] prun_phase0_eo_ep
for idx in range(3):
    with open('prun_phase0_eo_ep_' + str(idx) + '.csv', mode='r') as f:
        for idx2, line in enumerate(map(str.strip, f)):
            prun_phase0_eo_ep[idx][idx2] = [int(i) for i in line.replace('\n', '').split(',')]
cdef int[3][24][40320] prun_phase1_cp_ep
for idx in range(3):
    with open('prun_phase1_cp_ep_' + str(idx) + '.csv', mode='r') as f:
        for idx2, line in enumerate(map(str.strip, f)):
            prun_phase1_cp_ep[idx][idx2] = [int(i) for i in line.replace('\n', '').split(',')]
cdef int[3][24][40320] prun_phase1_ep_ep
for idx in range(3):
    with open('prun_phase1_ep_ep_' + str(idx) + '.csv', mode='r') as f:
        for idx2, line in enumerate(map(str.strip, f)):
            prun_phase1_ep_ep[idx][idx2] = [int(i) for i in line.replace('\n', '').split(',')]
'''
pre_ans_idx = [[] for _ in range(2)]
pre_ans_ans = [[] for _ in range(2)]
pre_ans_not = [[] for _ in range(2)]
for phase in range(2):
    with open('pre_ans_phase' + str(phase) + '_idx.csv', mode='r') as f:
        for line in map(str.strip, f):
            pre_ans_idx[phase] = [int(i) for i in line.replace('\n', '').split(',')]
    with open('pre_ans_phase' + str(phase) + '_ans.csv', mode='r') as f:
        for line in map(str.strip, f):
            if line == '':
                pre_ans_ans[phase].append([])
            else:
                pre_ans_ans[phase].append([int(i) for i in line.replace('\n', '').split(',')])
    with open('pre_ans_phase' + str(phase) + '_not.csv', mode='r') as f:
        for line in map(str.strip, f):
            if line == '':
                pre_ans_not[phase].append([])
            else:
                pre_ans_not[phase].append([int(i) for i in line.replace('\n', '').split(',')])
'''

can_twists = [[] for _ in range(25)]
for direction in range(24):
    now_face = set(actual_face[direction])
    for pre_direction in range(24):
        pre_face = set() if pre_direction == direction else set(actual_face[pre_direction])
        can_twists[direction].append(now_face - pre_face)
    can_twists[direction].append(now_face)

print('solver initialized')

''' TEST '''
p1 = 2.0
p2 = 0.05
from time import time
w, g, r, b, o, y = range(6)
#arr = [y, b, r, y, w, w, w, r, y, r, g, g, y, g, r, y, o, o, o, b, y, y, r, w, w, b, b, b, o, r, g, b, r, r, b, o, g, g, g, w, o, o, b, g, o, b, w, g, o, y, y, w, r, w] # R F2 R2 B2 L F2 R2 B2 R D2 L D' F U' B' R2 D2 F' U2 F'
#arr = [b, g, r, y, w, w, g, b, b, o, w, o, r, g, o, r, y, b, w, g, w, w, r, w, o, y, y, g, y, w, r, b, b, o, b, y, r, b, w, r, o, g, r, o, g, y, r, y, g, y, o, b, o, g] # U B2 L2 U F2 R2 U R2 B2 D' F2 D2 R' D' U2 B' R B2 L2 F U2
arr = [w, b, w, o, w, r, w, g, w, g, w, g, o, g, r, g, y, g, r, w, r, g, r, b, r, y, r, b, w, b, r, b, o, b, y, b, o, w, o, b, o, g, o, y, o, y, g, y, o, y, r, y, b, y] # super flip U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2
#arr = [w, w, w, w, w, w, o, o, y, g, g, r, g, g, r, y, y, r, g, b, b, g, r, r, g, r, r, o, o, o, w, b, b, w, b, b, g, g, y, o, o, y, o, o, b, r, r, w, y, y, b, y, y, b] # R U F
#arr = [o, w, w, o, w, w, o, g, g, w, r, r, g, g, g, y, y, y, w, b, b, w, r, r, g, r, r, o, o, y, w, b, b, w, b, b, g, g, g, o, o, y, o, o, b, r, r, r, y, y, b, y, y, b] # R F U
#arr = [w, w, g, w, w, g, w, w, g, g, g, y, g, g, y, g, g, y, r, r, r, r, r, r, r, r, r, w, b, b, w, b, b, w, b, b, o, o, o, o, o, o, o, o, o, y, y, b, y, y, b, y, y, b] # R
#arr = [w, w, o, w, w, g, w, w, g, g, g, y, g, g, w, g, g, g, r, r, w, b, r, r, w, r, r, b, r, r, b, b, b, b, b, b, b, o, o, o, o, o, o, o, o, y, y, r, y, y, y, y, y, y]  # R U R' U'
#arr = [w, w, w, w, w, w, o, o, b, g, g, w, r, g, g, w, g, g, r, g, g, r, r, r, r, r, r, r, b, b, b, b, b, b, b, b, o, o, y, o, o, w, o, o, o, g, y, y, y, y, y, y, y, y] # F U F' U'
#arr = [y, y, w, w, w, y, w, y, w, o, o, g, g, g, b, r, r, b, r, b, r, o, r, r, o, g, g, b, r, b, g, b, b, o, g, o, r, b, b, r, o, o, g, o, g, y, w, y, w, y, w, y, y, w] # U R2 L2 D2 F2 U' L2
#arr = [y, y, g, w, w, b, w, y, b, o, o, y, g, g, w, r, r, w, o, o, r, g, r, b, g, r, r, w, r, b, y, b, b, w, g, o, r, b, b, r, o, o, g, o, g, y, w, o, w, y, g, y, y, b] # U R2 L2 D2 F2 U' L2 R
strt = time()
cnt = 0
tmp = solver(arr)
print(len(tmp), tmp)
print('time:', time() - strt)
exit()

'''
# find the most efficient parameter
p1 = 1.0
p2 = 0.01
cnt = 0
solver(arr)
p_cnt = cnt
pp1 = p1
p1 = pp1 + 0.5
pp2 = p2
p2 = pp2 + 0.5

threshold = 0.01
flag = 0
while flag < 3:
    cnt = 0
    if 28 <= len(solver(arr)) <= 29:
        pp1 = p1
        pp2 = p2
        p1 += (p_cnt - cnt) * 0.00002
        p1 = max(1, p1)
        p2 += (p_cnt - cnt) * 0.00002
        p2 = max(0.1, p2)
        print(cnt, p_cnt, p_cnt - cnt, ' ', p1, pp1, p1 - pp1, ' ', p2, pp2, p2 - pp2)
        p_cnt = cnt
        if abs(p1 - pp1) > threshold or abs(p2 - pp2) > threshold:
            flag = 0
        else:
            flag += 1
    else:
        print('answer not found')

min_p1 = 0
min_p2 = 0
num = 0
min_cnt = 100000

p1_ans = p1
p2_ans = p2
p1 = p1_ans - 0.2
while p1 < p1_ans + 0.2:
    p2 = p2_ans - 0.2
    while p2 < p2_ans + 0.2:
        cnt = 0
        solver(arr)
        print(cnt, p1, p2)
        if cnt < min_cnt:
            min_p1 = p1
            min_p2 = p2
            num = 1
            min_cnt = cnt
        elif cnt == min_cnt:
            min_p1 += p1
            min_p2 += p2
            num += 1
        p2 += 0.03
    p1 += 0.03

print(min_p1 / num, min_p2 / num, min_cnt)
'''