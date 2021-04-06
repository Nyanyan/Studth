# coding:utf-8
'''
corner numbering
  0 1
   U
0 3 2 1
 L F R
7 4 5 6
   D
  7 6

edge numbering
       0
     3 U 1
       2
11 L 8 F 9 R 10
       4
     7 D 5
       6

sticker numbering
              U
           0  1  2
           3  4  5
           6  7  8
    L         F         R         B
36 37 38   9 10 11  18 19 20  27 28 29
39 40 41  12 13 14  21 22 23  30 31 32
42 43 44  15 16 17  24 25 26  33 34 35
              D
          45 46 47
          48 49 50
          51 52 53

color numbering
white: 0
green: 1
red: 2
blue: 3
orange: 4
yellow: 5

rotation:
U F number
w g 0
o g 1
y g 2
r g 3
w r 4
g r 5
y r 6
b r 7
w b 8
r b 9
y b 10
o b 11
w o 12
b o 13
y o 14
g o 15
b w 16
o w 17
g w 18
r w 19
g y 20
o y 21
b y 22
r y 23

rotated face
R 0 (0-2)
L 1 (3-5)
U 2 (6-8)
D 3 (9-11)
F 4 (12-14)
B 5 (15-17)
'''
# twists that Studth can do
'''
twists_key = [
    [[[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 1, 0]]],                                                                                                                                 # 0 R
    [[[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 1, 0]], [[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 1, 0]]],                                                                       # 1 R2
    [[[0, 1, 1]], [[0, 1, 2000]], [[0, 1, 0]]],                                                                                                                                                 # 2 R'
    [[[1, 1, 2000]], [[1, 1, 1]], [[1, 1, 1000]], [[1, 1, 0]]],                                                                                                                                 # 3 L
    [[[1, 1, 2000]], [[1, 1, 1]], [[1, 1, 1000]], [[1, 1, 0]], [[1, 1, 2000]], [[1, 1, 1]], [[1, 1, 1000]], [[1, 1, 0]]],                                                                       # 4 L2
    [[[1, 1, 1]], [[1, 1, 2000]], [[1, 1, 0]]],                                                                                                                                                 # 5 L'
    [[[0, 0, 2000]], [[0, 0, 1]], [[0, 0, 1000]], [[0, 0, 0]]],                                                                                                                                 # 6 F
    [[[0, 0, 2000]], [[0, 0, 1]], [[0, 0, 1000]], [[0, 0, 0]], [[0, 0, 2000]], [[0, 0, 1]], [[0, 0, 1000]], [[0, 0, 0]]],                                                                       # 7 F2
    [[[0, 0, 1]], [[0, 0, 2000]], [[0, 0, 0]]],                                                                                                                                                 # 8 F'
    [[[1, 0, 2000]], [[1, 0, 1]], [[1, 0, 1000]], [[1, 0, 0]]],                                                                                                                                 # 9 B
    [[[1, 0, 2000]], [[1, 0, 1]], [[1, 0, 1000]], [[1, 0, 0]], [[1, 0, 2000]], [[1, 0, 1]], [[1, 0, 1000]], [[1, 0, 0]]],                                                                       # 10 B2
    [[[1, 0, 1]], [[1, 0, 2000]], [[1, 0, 0]]],                                                                                                                                                 # 11 B'
    [[[0, 1, 2000]], [[0, 1, 1]], [[0, 1, 1000]], [[0, 0, 2000], [1, 0, 2000]], [[0, 1, 0], [1, 1, 1]], [[0, 0, 1000], [1, 0, 1000]], [[1, 1, 2000]], [[1, 1, 0]]],                             # 12 x
    [[[0, 0, 2000]], [[0, 0, 1]], [[0, 0, 1000]], [[0, 1, 2000], [1, 1, 2000]], [[0, 0, 0], [1, 0, 1]], [[0, 1, 1000], [1, 1, 1000]], [[1, 0, 2000]], [[1, 0, 0]]]                              # 13 z
    ]
'''
twists_key = [
    [[[1, 2000]], [[1, 1]], [[1, 1000]], [[1, 0]]]
    [[[1, 2000]], [[1, 1]], [[1, 1000]], [[1, 0]], [[1, 2000]], [[1, 1]], [[1, 1000]], [[1, 0]]]
    [[[1, 1]], [[1, 2000]], [[1, 0]]]
    [[[3, 2000]], [[3, 1]], [[3, 1000]], [[3, 0]]]
    [[[3, 2000]], [[3, 1]], [[3, 1000]], [[3, 0]], [[3, 2000]], [[3, 1]], [[3, 1000]], [[3, 0]]]
    [[[3, 1]], [[3, 2000]], [[3, 0]]]
    [[[0, 2000]], [[0, 1]], [[0, 1000]], [[0, 0]]]
    [[[0, 2000]], [[0, 1]], [[0, 1000]], [[0, 0]], [[0, 2000]], [[0, 1]], [[0, 1000]], [[0, 0]]]
    [[[0, 1]], [[0, 2000]], [[0, 0]]]
    [[[2, 2000]], [[2, 1]], [[2, 1000]], [[2, 0]]]
    [[[2, 2000]], [[2, 1]], [[2, 1000]], [[2, 0]], [[2, 2000]], [[2, 1]], [[2, 1000]], [[2, 0]]]
    [[[2, 1]], [[2, 2000]], [[2, 0]]]
    [[[1, 2000]], [[1, 1]], [[1, 1000]], [[0, 2000], [2, 2000]], [[1, 0], [3, 1]], [[0, 1000], [2, 1000]], [[3, 2000]], [[3, 0]]]
    [[[0, 2000]], [[0, 1]], [[0, 1000]], [[1, 2000], [3, 2000]], [[0, 0], [2, 1]], [[1, 1000], [3, 1000]], [[2, 2000]], [[2, 0]]]
]

# for each direction, the rotated face will be change for example, rotating R (0) in direction 14 is actually B (3).
actual_face = [
    (0, 1, 4, 5), # 0
    (2, 3, 4, 5), # 1
    (1, 0, 4, 5), # 2
    (3, 2, 4, 5), # 3
    (5, 4, 0, 1), # 4
    (2, 3, 0, 1), # 5
    (4, 5, 0, 1), # 6
    (3, 2, 0, 1), # 7
    (1, 0, 5, 4), # 8
    (2, 3, 5, 4), # 9
    (0, 1, 5, 4), # 10
    (3, 2, 5, 4), # 11
    (4, 5, 1, 0), # 12
    (2, 3, 1, 0), # 13
    (5, 4, 1, 0), # 14
    (3, 2, 1, 0), # 15
    (0, 1, 2, 3), # 16
    (5, 4, 2, 3), # 17
    (1, 0, 2, 3), # 18
    (4, 5, 2, 3), # 19
    (0, 1, 3, 2), # 20
    (4, 5, 3, 2), # 21
    (1, 0, 3, 2), # 22
    (5, 4, 3, 2), # 23
]

# changing direction using z turning is very simple, so all we need is the table for x turning
change_direction_x = (20, 5, 18, 15, 23, 9, 19, 3, 22, 13, 16, 7, 21, 1, 17, 11, 0, 4, 8, 12, 10, 6, 2, 14)

candidate = [
    set((0, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 17)), # phase0
    set((1, 4, 6, 7, 8, 9, 10, 11, 13, 16))                # phase1
]

rev_twists = (2, 1, 0, 5, 4, 3, 8, 7, 6, 11, 10, 9, 14, 13, 12, 17, 16, 15)

twist2phase_idx = [
    (0, -1, 1, 2, -1, 3, 4, 5, 6, 7, 8, 9, 10, -1, 11, 12, -1, 13), # phase0
    (-1, 0, -1, -1, 1, -1, 2, 3, 4, 5, 6, 7, -1, 8, -1, -1, 9, -1), # phase1
]

can_rotate = [
    (1, 0, 1), # 0
    (0, 1, 1), # 1
    (1, 0, 1), # 2
    (0, 1, 1), # 3
    (1, 0, 1), # 4
    (1, 1, 0), # 5
    (1, 0, 1), # 6
    (1, 1, 0), # 7
    (1, 0, 1), # 8
    (0, 1, 1), # 9
    (1, 0, 1), # 10
    (0, 1, 1), # 11
    (1, 0, 1), # 12
    (1, 1, 0), # 13
    (1, 0, 1), # 14
    (1, 1, 0), # 15
    (1, 1, 0), # 16
    (0, 1, 1), # 17
    (1, 1, 0), # 18
    (0, 1, 1), # 19
    (1, 1, 0), # 20
    (0, 1, 1), # 21
    (1, 1, 0), # 22
    (0, 1, 1), # 23
]

dir_type = []
for i in can_rotate:
    if i == (1, 0, 1):
        dir_type.append(0)
    elif i == (0, 1, 1):
        dir_type.append(1)
    else:
        dir_type.append(2)

corner_places = [(0, 36, 29), (2, 27, 20), (8, 18, 11), (6, 9, 38), (45, 44, 15), (47, 17, 24), (53, 26, 33), (51, 35, 42)]
corner_colors = [(0, 4, 3),   (0, 3, 2),   (0, 2, 1),   (0, 1, 4),  (5, 4, 1),    (5, 1, 2),    (5, 2, 3),    (5, 3, 4)   ]
edge_places = [(1, 28), (5, 19), (7, 10), (3, 37), (46, 16), (50, 25), (52, 34), (48, 43), (12, 41), (14, 21), (30, 23), (32, 39)]
edge_colors = [(0, 3),  (0, 2),  (0, 1),  (0, 4),  (5, 1),   (5, 2),   (5, 3),   (5, 4),   (1, 4),   (1, 2),   (3, 2),   (3, 4)  ]

fac = [1]
for i in range(1, 13):
    fac.append(fac[-1] * i)

corner_move_parts = [
    (1, 6, 5, 2), # R
    (3, 4, 7, 0), # L
    (0, 1, 2, 3), # U
    (4, 5, 6, 7), # D
    (2, 5, 4, 3), # F
    (0, 7, 6, 1)  # B
]
co_plus = (2, 1, 2, 1)
edge_move_parts = [
    (1, 10, 5, 9), # R
    (3, 8, 7, 11), # L
    (0, 1, 2, 3),  # U
    (4, 5, 6, 7),  # D
    (2, 9, 4, 8),  # F
    (0, 11, 6, 10) # B
]

def sticker2arr(stickers):
    cp = [-1 for _ in range(8)]
    co = [-1 for _ in range(8)]
    for place in range(8):
        part_color = [stickers[i] for i in corner_places[place]]
        for part in range(8):
            for dr in range(3):
                cnt = 0
                for sticker in range(3):
                    if part_color[sticker] != -1 and part_color[sticker] != corner_colors[part][(sticker - dr) % 3]:
                        break
                    if part_color[sticker] == -1:
                        cnt += 1
                else:
                    if cnt <= 1:
                        cp[place] = part
                        co[place] = dr
                        break
            else:
                continue
            break
    ep = [-1 for _ in range(12)]
    eo = [-1 for _ in range(12)]
    for place in range(12):
        part_color = [stickers[i] for i in edge_places[place]]
        for part in range(12):
            for dr in range(2):
                for sticker in range(2):
                    if part_color[sticker] != edge_colors[part][(sticker - dr) % 2]:
                        break
                else:
                    ep[place] = part
                    eo[place] = dr
                    break
            else:
                continue
            break
    return cp, co, ep, eo

def move_cp(cp, twist):
    twist_type = twist // 3
    twist_amount = twist % 3 + 1
    res = [i for i in cp]
    for _ in range(twist_amount):
        n_res = [i for i in res]
        for i in range(4):
            n_res[corner_move_parts[twist_type][(i + 1) % 4]] = res[corner_move_parts[twist_type][i]]
        res = n_res
    return res

def move_co(co, twist):
    twist_type = twist // 3
    twist_amount = twist % 3 + 1
    res = [i for i in co]
    flip_flag = twist_type != 2 and twist_type != 3 and twist_amount != 2
    for _ in range(twist_amount):
        n_res = [i for i in res]
        for i in range(4):
            n_res[corner_move_parts[twist_type][(i + 1) % 4]] = res[corner_move_parts[twist_type][i]]
            if flip_flag:
                n_res[corner_move_parts[twist_type][(i + 1) % 4]] += co_plus[i]
                n_res[corner_move_parts[twist_type][(i + 1) % 4]] %= 3
        res = n_res
    return res

def move_ep(ep, twist):
    twist_type = twist // 3
    twist_amount = twist % 3 + 1
    res = [i for i in ep]
    for _ in range(twist_amount):
        n_res = [i for i in res]
        for i in range(4):
            n_res[edge_move_parts[twist_type][(i + 1) % 4]] = res[edge_move_parts[twist_type][i]]
        res = n_res
    return res

def move_eo(eo, twist):
    twist_type = twist // 3
    twist_amount = twist % 3 + 1
    res = [i for i in eo]
    flip_flag = (twist_type == 4 or twist_type == 5) and twist_amount != 2
    for _ in range(twist_amount):
        n_res = [i for i in res]
        for i in range(4):
            n_res[edge_move_parts[twist_type][(i + 1) % 4]] = res[edge_move_parts[twist_type][i]]
            if flip_flag:
                n_res[edge_move_parts[twist_type][(i + 1) % 4]] = 1 - n_res[edge_move_parts[twist_type][(i + 1) % 4]]
        res = n_res
    return res

def move_dir(direction, arm_twist):
    if arm_twist >= 12:
        if arm_twist == 12: # x
            return change_direction_x[direction]
        else: # z
            return direction // 4 * 4 + (direction % 4 + 1) % 4
    return direction

def rev_move_dir(direction, arm_twist):
    if arm_twist >= 12:
        if arm_twist == 12: # x
            for _ in range(3):
                direction = change_direction_x[direction]
        else: # z
            for _ in range(3):
                direction = direction // 4 * 4 + (direction % 4 + 1) % 4
    return direction

def cmb(n, r):
    return fac[n] // fac[r] // fac[n - r]

def cp2idx(cp):
    res = 0
    for i in range(8):
        cnt = cp[i]
        for j in cp[:i]:
            if j < cp[i]:
                cnt -= 1
        res += fac[7 - i] * cnt
    return res

def idx2cp(idx):
    res = [-1 for _ in range(8)]
    for i in range(8):
        candidate = idx // fac[7 - i]
        marked = [True for _ in range(i)]
        for _ in range(8):
            for j, k in enumerate(res[:i]):
                if k <= candidate and marked[j]:
                    candidate += 1
                    marked[j] = False
        res[i] = candidate
        idx %= fac[7 - i]
    return res

def co2idx(co):
    res = 0
    for i in range(7):
        res *= 3
        res += co[i]
    return res

def idx2co(idx):
    res = [0 for _ in range(8)]
    for i in reversed(range(7)):
        res[i] = idx % 3
        idx //= 3
    res[7] = (3 - sum(res) % 3) % 3
    return res

def ep2idx_phase0(ep):
    res = 0
    cnt = 4
    for i in reversed(range(12)):
        if ep[i] >= 8:
            res += cmb(i, cnt)
            cnt -= 1
    return res

def idx2ep_phase0(idx):
    res = [-1 for _ in range(12)]
    cnt = 4
    for i in reversed(range(12)):
        c = cmb(i, cnt)
        if idx >= c:
            res[i] = 8
            idx -= c
            cnt -= 1
    return res

def ep2idx_phase1_1(ep):
    res = 0
    for i in range(8):
        cnt = ep[i]
        for j in ep[:i]:
            if j < ep[i]:
                cnt -= 1
        res += fac[7 - i] * cnt
    return res

def ep2idx_phase1_2(ep):
    res = 0
    for i in range(4):
        cnt = ep[8 + i] - 8
        for j in ep[8:8 + i]:
            if j < ep[8 + i]:
                cnt -= 1
        res += fac[3 - i] * cnt
    return res

def idx2ep_phase1_1(idx1):
    res = [-1 for _ in range(12)]
    for i in range(8):
        candidate = idx1 // fac[7 - i]
        marked = [True for _ in range(i)]
        for _ in range(8):
            for j, k in enumerate(res[:i]):
                if k <= candidate and marked[j]:
                    candidate += 1
                    marked[j] = False
        res[i] = candidate
        idx1 %= fac[7 - i]
    return res

def idx2ep_phase1_2(idx2):
    res = [-1 for _ in range(12)]
    for i in range(4):
        candidate = idx2 // fac[3 - i]
        marked = [True for _ in range(i)]
        for _ in range(4):
            for j, k in enumerate(res[8:8 + i]):
                if k <= candidate and marked[j]:
                    candidate += 1
                    marked[j] = False
        res[8 + i] = candidate
        idx2 %= fac[3 - i]
    for i in range(4):
        res[8 + i] += 8
    return res

def eo2idx(eo):
    res = 0
    for i in eo[:11]:
        res *= 2
        res += i
    return res

def idx2eo(idx):
    res = [0 for _ in range(12)]
    for i in reversed(range(11)):
        res[i] = idx % 2
        idx //= 2
    res[11] = sum(res) % 2
    return res

'''
# scramble R'
cp = list(range(8))
co = [0 for _ in range(8)]
ep = list(range(12))
eo = [0 for _ in range(12)]
cp = move_cp(cp, 0)
co = move_co(co, 0)
ep = move_ep(ep, 0)
eo = move_eo(eo, 0)
print(cp)
print(co)
print(ep)
print(eo)
'''