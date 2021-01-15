from basic_functions import *

def idxes_init(phase, cp, co, ep, eo, direction):
    if phase == 0:
        res1 = co2idx(co)
        res2 = eo2idx(eo)
        res3 = ep2idx_phase0(ep)
        return (res1, res2, res3, direction)
    else:
        res1 = cp2idx(cp)
        res2 = ep2idx_phase1_1(ep)
        res3 = ep2idx_phase1_2(ep)
        return (res1, res2, res3, direction)

def trans(phase, idxes, twist):
    if phase == 0:
        res1 = trans_co[idxes[0]][twist]
        res2 = trans_eo[idxes[1]][twist]
        res3 = trans_ep_phase0[idxes[2]][twist]
        return (res1, res2, res3, idxes[3])
    else:
        res1 = trans_cp[idxes[0]][twist]
        res2 = trans_ep_phase1_1[idxes[1]][twist]
        res3 = trans_ep_phase1_2[idxes[2]][twist]
        return (res1, res2, res3, idxes[3])

def distance(phase, idxes):
    if phase == 0:
        return max(prun_phase0_co_ep[idxes[2]][idxes[0]], prun_phase0_eo_ep[idxes[2]][idxes[1]])
    else:
        return max(prun_phase1_cp_ep[idxes[2]][idxes[0]], prun_phase1_ep_ep[idxes[2]][idxes[1]])

def phase_search(phase, idxes, depth, dis):
    global phase_solution
    if depth == 0:
        if dis == 0:
            return [[[i for i in phase_solution], [i for i in phase_solution_notation]]]
        else:
            return []
    elif dis == 0:
        return []
    #print(dis, depth, phase_solution_notation)
    res = []
    depth -= 1
    direction = idxes[3]
    last_rotated = phase_solution[-1] if phase_solution and phase_solution[-1] >= 12 else -10
    l1_twist = phase_solution_notation[-1] if phase_solution_notation else -10
    l2_twist = phase_solution_notation[-2] if len(phase_solution_notation) >= 2 else -10
    l1_twist_type = l1_twist // 3
    l2_twist_type = l2_twist // 3
    for twist_idx in range(14):
        if twist_idx <= 11:
            twist = actual_face[direction][twist_idx // 3] * 3 + twist_idx % 3
            if twist // 3 == l1_twist_type: # don't turn same face twice
                continue
            if twist // 3 == l2_twist_type and twist // 6 == l1_twist // 6: # don't turn opposite face 3 times
                continue
            if not twist in candidate[phase]:
                continue
            n_idxes = trans(phase, idxes, twist2phase_idx[phase][twist])
            n_dis = distance(phase, n_idxes)
        else:
            if last_rotated == twist_idx:
                continue
            n_idxes = [i for i in idxes]
            n_idxes[3] = move_dir(direction, twist_idx)
            n_dis = dis
        if n_dis > depth:
            continue
        phase_solution.append(twist_idx)
        if twist_idx <= 11:
            phase_solution_notation.append(twist)
        sol = phase_search(phase, n_idxes, depth, n_dis)
        if sol: # only one solution needed
            return sol
        res.extend(sol)
        if len(res) > 50:
            return res
        phase_solution.pop()
        if twist_idx <= 11:
            phase_solution_notation.pop()
    return res

def solver(stickers):
    global phase_solution, phase_solution_notation
    res = []
    l = 30
    s_cp, s_co, s_ep, s_eo = sticker2arr(stickers)
    s_dir = 0
    print(s_cp)
    print(s_ep)
    if -1 in s_cp or -1 in s_co or -1 in s_ep or -1 in s_eo:
        raise Exception('Error')
    while True:
        search_lst = [[s_cp, s_co, s_ep, s_eo, s_dir, []]]
        n_search_lst = []
        for phase in range(2):
            for cp, co, ep, eo, direction, last_solution in search_lst:
                idxes = idxes_init(phase, cp, co, ep, eo, direction)
                dis = distance(phase, idxes)
                phase_solution = []
                phase_solution_notation = []
                strt_depth = dis
                for depth in range(strt_depth, l - len(last_solution)):
                    sol = phase_search(phase, idxes, depth, dis)
                    if sol:
                        for solution, solution_notation in sol:
                            n_cp = [i for i in cp]
                            n_co = [i for i in co]
                            n_ep = [i for i in ep]
                            n_eo = [i for i in eo]
                            n_dir = direction
                            n_solution = [i for i in last_solution]
                            for twist, twist_arm in zip(solution_notation, solution):
                                n_cp = move_cp(n_cp, twist)
                                n_co = move_co(n_co, twist)
                                n_ep = move_ep(n_ep, twist)
                                n_eo = move_eo(n_eo, twist)
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
        if search_lst:
            res = [i for i in search_lst[-1][5]]
        else:
            break
    return res

phase_solution = []
phase_solution_notation = []
trans_co = []
with open('trans_co.csv', mode='r') as f:
    for line in map(str.strip, f):
        trans_co.append([int(i) for i in line.replace('\n', '').split(',')])
trans_cp = []
with open('trans_cp.csv', mode='r') as f:
    for line in map(str.strip, f):
        trans_cp.append([int(i) for i in line.replace('\n', '').split(',')])
trans_eo = []
with open('trans_eo.csv', mode='r') as f:
    for line in map(str.strip, f):
        trans_eo.append([int(i) for i in line.replace('\n', '').split(',')])
trans_ep_phase0 = []
with open('trans_ep_phase0.csv', mode='r') as f:
    for line in map(str.strip, f):
        trans_ep_phase0.append([int(i) for i in line.replace('\n', '').split(',')])
trans_ep_phase1_1 = []
with open('trans_ep_phase1_1.csv', mode='r') as f:
    for line in map(str.strip, f):
        trans_ep_phase1_1.append([int(i) for i in line.replace('\n', '').split(',')])
trans_ep_phase1_2 = []
with open('trans_ep_phase1_2.csv', mode='r') as f:
    for line in map(str.strip, f):
        trans_ep_phase1_2.append([int(i) for i in line.replace('\n', '').split(',')])
prun_phase0_co_ep = []
with open('prun_phase0_co_ep.csv', mode='r') as f:
    for line in map(str.strip, f):
        prun_phase0_co_ep.append([int(i) for i in line.replace('\n', '').split(',')])
prun_phase0_eo_ep = []
with open('prun_phase0_eo_ep.csv', mode='r') as f:
    for line in map(str.strip, f):
        prun_phase0_eo_ep.append([int(i) for i in line.replace('\n', '').split(',')])
prun_phase1_cp_ep = []
with open('prun_phase1_cp_ep.csv', mode='r') as f:
    for line in map(str.strip, f):
        prun_phase1_cp_ep.append([int(i) for i in line.replace('\n', '').split(',')])
prun_phase1_ep_ep = []
with open('prun_phase1_ep_ep.csv', mode='r') as f:
    for line in map(str.strip, f):
        prun_phase1_ep_ep.append([int(i) for i in line.replace('\n', '').split(',')])

print('solver initialized')


''' TEST '''
w, g, r, b, o, y = range(6)
arr = [y, b, r, y, w, w, w, r, y, r, g, g, y, g, r, y, o, o, o, b, y, y, r, w, w, b, b, b, o, r, g, b, r, r, b, o, g, g, g, w, o, o, b, g, o, b, w, g, o, y, y, w, r, w] # R F2 R2 B2 L F2 R2 B2 R D2 L D' F U' B' R2 D2 F' U2 F'
#arr = [y, b, r, y, w, w, w, r, y, r, g, g, y, g, r, y, o, o, o, b, y, y, r, w, w, b, b, b, o, r, g, b, r, r, b, o, g, g, g, w, o, o, b, g, o, b, w, g, o, y, y, w, r, w] # R F2 R2 B2 L F2 R2 B2 R D2 L D' F U' B' R2 D2 F' U2 F'
#arr = [w, w, g, w, w, g, w, w, g, g, g, y, g, g, y, g, g, y, r, r, r, r, r, r, r, r, r, w, b, b, w, b, b, w, b, b, o, o, o, o, o, o, o, o, o, y, y, b, y, y, b, y, y, b] # R
print('solved', solver(arr))