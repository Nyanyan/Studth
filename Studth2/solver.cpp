//#pragma GCC target("avx2")
//#pragma GCC optimize("O3")
//#pragma GCC optimize("unroll-loops")
//#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx")

#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <chrono>
#include <string>
#include <unordered_map>
#include <random>
#include <queue>

using namespace std;

// 各フェーズの制限時間
// 制限時間いっぱい解を探索する
// 制限時間超過時に解が1つ以上見つかっていれば探索終了
// 制限時間を超過しても解が見つからない場合はノード数上限値まで探索を継続し、1つ解が見つかった時点で探索終了
#define TIME_LIMIT_PHASE0 1000
#define TIME_LIMIT_PHASE1 2000

// phase0での最大ノード訪問回数
#define N_MAX_PHASE0_NODES 50000

// phase1での最大ノード訪問回数
#define N_MAX_PHASE1_NODES 100000

// phase0で受け入れる最大の解の個数(1000000000など大きな値に設定すれば、ノード訪問回数がN_MAX_PHASE1_NODESに達するまで探索することになります)
#define N_MAX_PHASE0_SOLUTIONS 5000

// ついでに行った高速化を使うかどうか(使う場合、trans_*.txtのファイルが必要になります)
#define USE_FAST_MODIFICATION true

#define c_h 1.6
#define table_weight 0.9

#define n_stickers 54
#define n_edge_stickers 24
#define n_phase0_moves 18
#define n_phase1_moves 10

#define n_phase0_in 80
#define n_phase0_dense0 32
#define n_phase0_dense1 16
#define n_phase0_dense_residual 16
#define n_phase0_n_residual 2

#define n_phase1_in 182
#define n_phase1_dense0 32
#define n_phase1_dense1 32
#define n_phase1_dense_residual 32
#define n_phase1_n_residual 2

#define n_phase0_idxes 3
#define n_phase1_idxes 3
#define n_corners 8
#define n_edges 12
#define n_co 2187
#define n_cp 40320
#define n_ep_phase0 495
#define n_ep_phase1_0 40320
#define n_ep_phase1_1 24
#define n_eo 2048

#define IDX_UNDEFINED -1

// 解を安定して得るための定数
const int USE_HEURISTIC_NODE_THRESHOLD_PHASE0 = N_MAX_PHASE0_NODES * 0.5;
const int USE_HEURISTIC_NODE_THRESHOLD_PHASE1 = N_MAX_PHASE1_NODES * 0.5;
#define USE_HEURISTIC_THRESHOLD_PHASE0 4.0
#define USE_HEURISTIC_THRESHOLD_PHASE1 4.0

/*
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
*/

const int edges[n_edge_stickers] = {1, 3, 5, 7, 10, 12, 14, 16, 19, 21, 23, 25, 28, 30, 32, 34, 37, 39, 41, 43, 46, 48, 50, 52};
const int sticker_moves[6][5][4] = {
    {{5, 30, 50, 14},  {19, 23, 25, 21}, {2, 33, 47, 11},  {27, 53, 17, 8},  {20, 26, 24, 18}}, // R
    {{3, 12, 48, 32},  {37, 41, 43, 39}, {0, 9, 45, 35},   {6, 15, 51, 29},  {36, 38, 44, 42}}, // L
    {{28, 19, 10, 37}, {1, 5, 7, 3},     {29, 20, 11, 38}, {27, 18, 9, 36},  {0, 2, 8, 6}    }, // U
    {{16, 25, 34, 43}, {46, 50, 52, 48}, {15, 24, 33, 42}, {17, 26, 35, 44}, {45, 47, 53, 51}}, // D
    {{7, 21, 46, 41},  {10, 14, 16, 12}, {6, 18, 47, 44},  {8, 24, 45, 38},  {9, 11, 17, 15} }, // F
    {{1, 39, 52, 23},  {28, 32, 34, 30}, {2, 36, 51, 26},  {0, 42, 53, 20},  {27, 29, 35, 33}}  // B
};
const string notation[18] = {"R", "R2", "R'", "L", "L2", "L'", "U", "U2", "U'", "D", "D2", "D'", "F", "F2", "F'", "B", "B2", "B'"};
const int edge_pair[n_stickers] = {-1, 28, -1, 37, -1, 19, -1, 10, -1, -1, 7, -1, 41, -1, 21, -1, 46, -1, -1, 5, -1, 14, -1, 30, -1, 50, -1, -1, 1, -1, 23, -1, 39, -1, 52, -1, -1, 3, -1, 32, -1, 12, -1, 48, -1, -1, 16, -1, 43, -1, 25, -1, 34, -1};
const int corner_places[n_corners][3] = {{0, 36, 29}, {2, 27, 20}, {8, 18, 11}, {6, 9, 38}, {45, 44, 15}, {47, 17, 24}, {53, 26, 33}, {51, 35, 42}};
const int corner_colors[n_corners][3] = {{0, 4, 3},   {0, 3, 2},   {0, 2, 1},   {0, 1, 4},  {5, 4, 1},    {5, 1, 2},    {5, 2, 3},    {5, 3, 4}   };
const int edge_places[n_edges][2] = {{1, 28}, {5, 19}, {7, 10}, {3, 37}, {46, 16}, {50, 25}, {52, 34}, {48, 43}, {12, 41}, {14, 21}, {30, 23}, {32, 39}};
const int edge_colors[n_edges][2] = {{0, 3},  {0, 2},  {0, 1},  {0, 4},  {5, 1},   {5, 2},   {5, 3},   {5, 4},   {1, 4},   {1, 2},   {3, 2},   {3, 4}  };


double phase0_dense0[n_phase0_dense0][n_phase0_in];
double phase0_bias0[n_phase0_dense0];
double phase0_dense1[n_phase0_dense1][n_phase0_dense0];
double phase0_bias1[n_phase0_dense1];
double phase0_dense_residual[n_phase0_n_residual][n_phase0_dense_residual][n_phase0_dense_residual];
double phase0_bias_residual[n_phase0_n_residual][n_phase0_dense_residual];
double phase0_dense2[n_phase0_dense_residual];
double phase0_bias2;

double phase1_dense0[n_phase1_dense0][n_phase1_in];
double phase1_bias0[n_phase1_dense0];
double phase1_dense1[n_phase1_dense1][n_phase1_dense0];
double phase1_bias1[n_phase1_dense1];
double phase1_dense_residual[n_phase1_n_residual][n_phase1_dense_residual][n_phase1_dense_residual];
double phase1_bias_residual[n_phase1_n_residual][n_phase1_dense_residual];
double phase1_dense2[n_phase1_dense_residual];
double phase1_bias2;
const int phase1_move_candidate[n_phase1_moves] = {1, 4, 6, 7, 8, 9, 10, 11, 13, 16};
#if USE_FAST_MODIFICATION
    int trans_co[n_co][n_phase0_moves];
    int trans_cp[n_cp][n_phase1_moves];
    int trans_ep_phase0[n_ep_phase0][n_phase0_moves];
    int trans_ep_phase1_0[n_ep_phase1_0][n_phase1_moves];
    int trans_ep_phase1_1[n_ep_phase1_1][n_phase1_moves];
    int trans_eo[n_eo][n_phase0_moves];
#endif
double prune_phase0_ep_co[n_ep_phase0][n_co];
double prune_phase0_ep_eo[n_ep_phase0][n_eo];
double prune_phase1_ep_cp[n_ep_phase1_1][n_cp];
double prune_phase1_ep_ep[n_ep_phase1_1][n_ep_phase1_0];

int fac[13];

inline long long tim(){
    return chrono::duration_cast<chrono::milliseconds>(chrono::high_resolution_clock::now().time_since_epoch()).count();
}

inline int calc_face(int mov){
    return mov / 3;
}

inline int calc_axis(int mov){
    return mov / 6;
}

inline double get_element(char *cbuf, FILE *fp){
    if (!fgets(cbuf, 1024, fp)){
        cerr << "param file broken" << endl;
        exit(1);
    }
    return atof(cbuf);
}

inline void init(){
    int i, j, ri;
    FILE *fp;
    char cbuf[1024];
    if ((fp = fopen("param/phase0.txt", "r")) == NULL){
        printf("param file not exist");
        exit(1);
    }
    for (i = 0; i < n_phase0_in; ++i){
        for (j = 0; j < n_phase0_dense0; ++j){
            phase0_dense0[j][i] = get_element(cbuf, fp);
        }
    }
    for (i = 0; i < n_phase0_dense0; ++i)
        phase0_bias0[i] = get_element(cbuf, fp);
    for (i = 0; i < n_phase0_dense0; ++i){
        for (j = 0; j < n_phase0_dense1; ++j){
            phase0_dense1[j][i] = get_element(cbuf, fp);
        }
    }
    for (i = 0; i < n_phase0_dense1; ++i)
        phase0_bias1[i] = get_element(cbuf, fp);
    for (ri = 0; ri < n_phase0_n_residual; ++ri){
        for (i = 0; i < n_phase0_dense_residual; ++i){
            for (j = 0; j < n_phase0_dense_residual; ++j){
                phase0_dense_residual[ri][j][i] = get_element(cbuf, fp);
            }
        }
        for (i = 0; i < n_phase0_dense_residual; ++i)
            phase0_bias_residual[ri][i] = get_element(cbuf, fp);
    }
    for (i = 0; i < n_phase0_dense_residual; ++i)
        phase0_dense2[i] = get_element(cbuf, fp);
    phase0_bias2 = get_element(cbuf, fp);

    if ((fp = fopen("param/phase1.txt", "r")) == NULL){
        printf("param file not exist");
        exit(1);
    }
    for (i = 0; i < n_phase1_in; ++i){
        for (j = 0; j < n_phase1_dense0; ++j){
            phase1_dense0[j][i] = get_element(cbuf, fp);
        }
    }
    for (i = 0; i < n_phase1_dense0; ++i)
        phase1_bias0[i] = get_element(cbuf, fp);
    for (i = 0; i < n_phase1_dense0; ++i){
        for (j = 0; j < n_phase1_dense1; ++j){
            phase1_dense1[j][i] = get_element(cbuf, fp);
        }
    }
    for (i = 0; i < n_phase1_dense1; ++i)
        phase1_bias1[i] = get_element(cbuf, fp);
    for (ri = 0; ri < n_phase1_n_residual; ++ri){
        for (i = 0; i < n_phase1_dense_residual; ++i){
            for (j = 0; j < n_phase1_dense_residual; ++j){
                phase1_dense_residual[ri][j][i] = get_element(cbuf, fp);
            }
        }
        for (i = 0; i < n_phase1_dense_residual; ++i)
            phase1_bias_residual[ri][i] = get_element(cbuf, fp);
    }
    for (i = 0; i < n_phase1_dense_residual; ++i)
        phase1_dense2[i] = get_element(cbuf, fp);
    phase1_bias2 = get_element(cbuf, fp);
    if ((fp = fopen("param/prune_phase0_ep_co.txt", "r")) == NULL){
        printf("param file not exist");
        exit(1);
    }
    for (i = 0; i < n_ep_phase0; ++i)
        for (j = 0; j < n_co; ++j)
            prune_phase0_ep_co[i][j] = get_element(cbuf, fp);
    
    if ((fp = fopen("param/prune_phase0_ep_eo.txt", "r")) == NULL){
        printf("param file not exist");
        exit(1);
    }
    for (i = 0; i < n_ep_phase0; ++i)
        for (j = 0; j < n_eo; ++j)
            prune_phase0_ep_eo[i][j] = get_element(cbuf, fp);
    
    if ((fp = fopen("param/prune_phase1_ep_cp.txt", "r")) == NULL){
        printf("param file not exist");
        exit(1);
    }
    for (i = 0; i < n_ep_phase1_1; ++i)
        for (j = 0; j < n_cp; ++j)
            prune_phase1_ep_cp[i][j] = get_element(cbuf, fp);
    
    if ((fp = fopen("param/prune_phase1_ep_ep.txt", "r")) == NULL){
        printf("param file not exist");
        exit(1);
    }
    for (i = 0; i < n_ep_phase1_1; ++i)
        for (j = 0; j < n_ep_phase1_0; ++j)
            prune_phase1_ep_ep[i][j] = get_element(cbuf, fp);
    #if USE_FAST_MODIFICATION
        if ((fp = fopen("param/trans_co.txt", "r")) == NULL){
            printf("param file not exist");
            exit(1);
        }
        for (i = 0; i < n_co; ++i)
            for (j = 0; j < n_phase0_moves; ++j)
                trans_co[i][j] = get_element(cbuf, fp);
        
        if ((fp = fopen("param/trans_cp.txt", "r")) == NULL){
            printf("param file not exist");
            exit(1);
        }
        for (i = 0; i < n_cp; ++i)
            for (j = 0; j < n_phase1_moves; ++j)
                trans_cp[i][j] = get_element(cbuf, fp);

        if ((fp = fopen("param/trans_ep_phase0.txt", "r")) == NULL){
            printf("param file not exist");
            exit(1);
        }
        for (i = 0; i < n_ep_phase0; ++i)
            for (j = 0; j < n_phase0_moves; ++j)
                trans_ep_phase0[i][j] = get_element(cbuf, fp);
        
        if ((fp = fopen("param/trans_ep_phase1_1.txt", "r")) == NULL){
            printf("param file not exist");
            exit(1);
        }
        for (i = 0; i < n_ep_phase1_0; ++i)
            for (j = 0; j < n_phase1_moves; ++j)
                trans_ep_phase1_0[i][j] = get_element(cbuf, fp);
        
        if ((fp = fopen("param/trans_ep_phase1_2.txt", "r")) == NULL){
            printf("param file not exist");
            exit(1);
        }
        for (i = 0; i < n_ep_phase1_1; ++i)
            for (j = 0; j < n_phase1_moves; ++j)
                trans_ep_phase1_1[i][j] = get_element(cbuf, fp);
        
        if ((fp = fopen("param/trans_eo.txt", "r")) == NULL){
            printf("param file not exist");
            exit(1);
        }
        for (i = 0; i < n_eo; ++i)
            for (j = 0; j < n_phase0_moves; ++j)
                trans_eo[i][j] = get_element(cbuf, fp);
    #endif
    fac[0] = 1;
    for (i = 1; i < 13; ++i)
        fac[i] = fac[i - 1] * i;
}

inline void sticker2arr(const int stickers[n_stickers], int co[n_corners], int cp[n_corners], int eo[n_edges], int ep[n_edges]){
    int i, place, part, dr, sticker;
    bool flag;
    int part_color_corner[3];
    int part_color_edge[2];
    for (place = 0; place < n_corners; ++place){
        for (i = 0; i < 3; ++i)
            part_color_corner[i] = stickers[corner_places[place][i]];
        for (part = 0; part < n_corners; ++part){
            for (dr = 0; dr < 3; ++dr){
                flag = true;
                for (sticker = 0; sticker < 3; ++sticker)
                    flag = flag && part_color_corner[sticker] == corner_colors[part][(sticker - dr + 3) % 3];
                if (flag){
                    cp[place] = part;
                    co[place] = dr;
                }
            }
        }
    }
    for (place = 0; place < n_edges; ++place){
        for (i = 0; i < 2; ++i)
            part_color_edge[i] = stickers[edge_places[place][i]];
        for (part = 0; part < n_edges; ++part){
            for (dr = 0; dr < 2; ++dr){
                flag = true;
                for (sticker = 0; sticker < 2; ++sticker)
                    flag = flag && part_color_edge[sticker] == edge_colors[part][(sticker - dr + 2) % 2];
                if (flag){
                    ep[place] = part;
                    eo[place] = dr;
                }
            }
        }
    }
}

inline int cmb(int n, int r){
    if (n < r)
        return 0;
    return fac[n] / fac[r] / fac[n - r];
}

inline void sticker2idx_phase0(const int stickers[n_stickers], int idxes[n_phase0_idxes]){
    int i, cnt;
    int co[n_corners], cp[n_corners], eo[n_edges], ep[n_edges];
    sticker2arr(stickers, co, cp, eo, ep);
    idxes[0] = 0;
    for (i = 0; i < n_corners - 1; ++i){
        idxes[0] *= 3;
        idxes[0] += co[i];
    }
    idxes[1] = 0;
    for (i = 0; i < n_edges - 1; ++i){
        idxes[1] *= 2;
        idxes[1] += eo[i];
    }
    idxes[2] = 0;
    cnt = 4;
    for (i = n_edges - 1; i >= 0; --i){
        if (ep[i] >= 8){
            idxes[2] += cmb(i, cnt--);
        }
    }
}

inline void sticker2idx_phase1(const int stickers[n_stickers], int idxes[n_phase1_idxes]){
    int i, j, cnt;
    int co[n_corners], cp[n_corners], eo[n_edges], ep[n_edges];
    sticker2arr(stickers, co, cp, eo, ep);
    idxes[0] = 0;
    for (i = 0; i < n_corners; ++i){
        cnt = cp[i];
        for (j = 0; j < i; ++j){
            if (cp[j] < cp[i])
                --cnt;
        }
        idxes[0] += fac[7 - i] * cnt;
    }
    idxes[1] = 0;
    for (i = 0; i < 8; ++i){
        cnt = ep[i];
        for (j = 0; j < i; ++j){
            if (ep[j] < ep[i])
                --cnt;
        }
        idxes[1] += fac[7 - i] * cnt;
    }
    idxes[2] = 0;
    for (i = 0; i < 4; ++i){
        cnt = ep[8 + i] - 8;
        for (j = 0; j < i; ++j){
            if (ep[8 + j] < ep[8 + i])
                --cnt;
        }
        idxes[2] += fac[3 - i] * cnt;
    }
}

inline void move_sticker(const int stickers[n_stickers], int res[n_stickers], int mov){
    int face, amount, i, j, k;
    int tmp_stickers[n_stickers];
    face = calc_face(mov);
    amount = mov % 3 + 1;
    for (i = 0; i < n_stickers; ++i){
        tmp_stickers[i] = stickers[i];
        res[i] = stickers[i];
    }
    if (amount <= 2){
        for (i = 0; i < amount; ++i){
            for (j = 0; j < 5; ++j){
                for (k = 0; k < 4; ++k)
                    tmp_stickers[sticker_moves[face][j][(k + 1) % 4]] = res[sticker_moves[face][j][k]];
            }
            for (j = 0; j < n_stickers; ++j)
                res[j] = tmp_stickers[j];
        }
    } else{
        for (j = 0; j < 5; ++j){
            for (k = 0; k < 4; ++k)
                tmp_stickers[sticker_moves[face][j][k]] = res[sticker_moves[face][j][(k + 1) % 4]];
        }
        for (j = 0; j < n_stickers; ++j)
            res[j] = tmp_stickers[j];
    }
}

inline double leaky_relu(double x){
    return max(x, 0.01 * x);
}

#if USE_FAST_MODIFICATION
    inline double predict_phase0(const int stickers[n_stickers], int n_nodes, int idxes[]){
#else
    inline double predict_phase0(const int stickers[n_stickers], int n_nodes){
#endif
    double min_res;

    #if !USE_FAST_MODIFICATION
        int idxes[n_phase0_idxes];
        sticker2idx_phase0(stickers, idxes);
    #endif
    min_res = max(prune_phase0_ep_co[idxes[2]][idxes[0]], prune_phase0_ep_eo[idxes[2]][idxes[1]]);
    //return c_h * min_res;
    if (min_res <= USE_HEURISTIC_THRESHOLD_PHASE0 || n_nodes > USE_HEURISTIC_NODE_THRESHOLD_PHASE0)
        return c_h * min_res;
    
    double in_arr[n_phase0_in];
    double hidden0[32], hidden1[32];
    double res;
    int i, j, ri;

    // create input array
    for (i = 0; i < n_stickers; ++i){
        if (stickers[i] == 0 || stickers[i] == 5)
            in_arr[i] = 1.0;
        else
            in_arr[i] = 0.0;
    }
    for (i = 0; i < n_edge_stickers; ++i){
        if (stickers[edges[i]] == 1 || stickers[edges[i]] == 3){
            if (stickers[edge_pair[edges[i]]] == 0 || stickers[edge_pair[edges[i]]] == 5)
                in_arr[n_stickers + i] = 0.0;
            else
                in_arr[n_stickers + i] = 1.0;
        } else
            in_arr[n_stickers + i] = 0.0;
    }
    in_arr[78] = (double)prune_phase0_ep_co[idxes[2]][idxes[0]];
    in_arr[79] = (double)prune_phase0_ep_eo[idxes[2]][idxes[1]];

    // dense0
    for (i = 0; i < n_phase0_dense0; ++i){
        hidden0[i] = phase0_bias0[i];
        for (j = 0; j < n_phase0_in; ++j)
            hidden0[i] += phase0_dense0[i][j] * in_arr[j];
        hidden0[i] = leaky_relu(hidden0[i]);
    }

    // dense1
    for (i = 0; i < n_phase0_dense1; ++i){
        hidden1[i] = phase0_bias1[i];
        for (j = 0; j < n_phase0_dense0; ++j)
            hidden1[i] += phase0_dense1[i][j] * hidden0[j];
        hidden1[i] = leaky_relu(hidden1[i]);
    }

    // residual bloock
    for (ri = 0; ri < n_phase0_n_residual; ++ri){
        for (i = 0; i < n_phase0_dense_residual; ++i){
            hidden0[i] = phase0_bias_residual[ri][i] + hidden1[i];
            for (j = 0; j < n_phase0_dense_residual; ++j)
                hidden0[i] += phase0_dense_residual[ri][i][j] * hidden1[j];
            hidden0[i] = leaky_relu(hidden0[i]);
        }
        swap(hidden0, hidden1);
    }

    // dense2
    res = phase0_bias2;
    for (j = 0; j < n_phase0_dense_residual; ++j)
        res += phase0_dense2[j] * hidden1[j];
    res = max(res, min_res);
    return c_h * (res + table_weight * min_res) / (1.0 + table_weight);
}

#if USE_FAST_MODIFICATION
    inline double predict_phase1(int stickers[n_stickers], int n_nodes, int idxes[]){
#else
    inline double predict_phase1(int stickers[n_stickers], int n_nodes){
#endif
    double min_res;

    #if !USE_FAST_MODIFICATION
        int idxes[n_phase1_idxes];
        sticker2idx_phase1(stickers, idxes);
    #endif
    min_res = max(prune_phase1_ep_cp[idxes[2]][idxes[0]], prune_phase1_ep_ep[idxes[2]][idxes[1]]);
    //return c_h * min_res;
    if (min_res <= USE_HEURISTIC_THRESHOLD_PHASE1 || n_nodes > USE_HEURISTIC_NODE_THRESHOLD_PHASE1)
        return c_h * min_res;
    
    double in_arr[n_phase1_in];
    double hidden0[32], hidden1[32];
    double res;
    int i, j, ri, idx, color;

    // create input array
    idx = 0;
    for (color = 0; color <= 5; color += 5){
        for (i = 0; i < 9; ++i){
            if (stickers[i] == color)
                in_arr[idx++] = 1.0;
            else
                in_arr[idx++] = 0.0;
        }
        for (i = 45; i < 54; ++i){
            if (stickers[i] == color)
                in_arr[idx++] = 1.0;
            else
                in_arr[idx++] = 0.0;
        }
    }
    for (color = 1; color <= 4; ++color){
        for (i = 9; i < 45; ++i){
            if (stickers[i] == color)
                in_arr[idx++] = 1.0;
            else
                in_arr[idx++] = 0.0;
        }
    }
    in_arr[180] = (double)prune_phase1_ep_cp[idxes[2]][idxes[0]];
    in_arr[181] = (double)prune_phase1_ep_ep[idxes[2]][idxes[1]];

    // dense0
    for (i = 0; i < n_phase1_dense0; ++i){
        hidden0[i] = phase1_bias0[i];
        for (j = 0; j < n_phase1_in; ++j)
            hidden0[i] += phase1_dense0[i][j] * in_arr[j];
        hidden0[i] = leaky_relu(hidden0[i]);
    }

    // dense1
    for (i = 0; i < n_phase1_dense1; ++i){
        hidden1[i] = phase1_bias1[i];
        for (j = 0; j < n_phase1_dense0; ++j)
            hidden1[i] += phase1_dense1[i][j] * hidden0[j];
        hidden1[i] = leaky_relu(hidden1[i]);
    }

    // residual bloock
    for (ri = 0; ri < n_phase1_n_residual; ++ri){
        for (i = 0; i < n_phase1_dense_residual; ++i){
            hidden0[i] = phase1_bias_residual[ri][i] + hidden1[i];
            for (j = 0; j < n_phase1_dense_residual; ++j)
                hidden0[i] += phase1_dense_residual[ri][i][j] * hidden1[j];
            hidden0[i] = leaky_relu(hidden0[i]);
        }
        swap(hidden0, hidden1);
    }

    // dense2
    res = phase1_bias2;
    for (j = 0; j < n_phase1_dense_residual; ++j)
        res += phase1_dense2[j] * hidden1[j];
    res = max(res, min_res);
    return c_h * (res + table_weight * min_res) / (1.0 + table_weight);
}


struct a_star_elem{
    double f;
    int stickers[n_stickers];
    vector<int> solution;
    bool first = false;
    #if USE_FAST_MODIFICATION
        int idxes[3];
    #endif
};

bool operator< (const a_star_elem &a, const a_star_elem &b){
    return a.f > b.f;
};

struct solver_elem{
    int stickers[n_stickers];
    vector<int> solution;
};

#if USE_FAST_MODIFICATION
    void move_idxes_phase0(int idxes[], int res[], int mov){
        res[0] = trans_co[idxes[0]][mov];
        res[1] = trans_eo[idxes[1]][mov];
        res[2] = trans_ep_phase0[idxes[2]][mov];
    }

    void move_idxes_phase1(int idxes[], int res[], int mov_idx){
        res[0] = trans_cp[idxes[0]][mov_idx];
        res[1] = trans_ep_phase1_0[idxes[1]][mov_idx];
        res[2] = trans_ep_phase1_1[idxes[2]][mov_idx];
    }
#endif

vector<vector<int>> phase0(const int stickers[n_stickers], int *visited_nodes){
    int i, mov, sol_size;
    double dis;
    priority_queue<a_star_elem> que;
    a_star_elem first_elem, elem;
    vector<vector<int>> res;
    for (i = 0; i < n_stickers; ++i)
        first_elem.stickers[i] = stickers[i];
    #if USE_FAST_MODIFICATION
        sticker2idx_phase0(first_elem.stickers, first_elem.idxes);
    #endif
    #if USE_FAST_MODIFICATION
        first_elem.f = predict_phase0(first_elem.stickers, *visited_nodes, first_elem.idxes);
    #else
        first_elem.f = predict_phase0(first_elem.stickers, *visited_nodes);
    #endif
    if (first_elem.f == 0.0){
        vector<int> solution;
        res.push_back(solution);
        return res;
    }
    first_elem.solution.push_back(-1000);
    que.push(first_elem);
    long long strt = tim();
    while (que.size() && *visited_nodes < N_MAX_PHASE0_NODES && res.size() < N_MAX_PHASE0_SOLUTIONS){
        if (tim() - strt > TIME_LIMIT_PHASE0 && res.size())
            break;
        elem = que.top();
        que.pop();
        sol_size = elem.solution.size();
        for (mov = 0; mov < n_phase0_moves; ++mov){
            if (calc_face(mov) == calc_face(elem.solution[sol_size - 1]))
                continue;
            if (calc_axis(mov) == calc_axis(elem.solution[sol_size - 1]) && mov < elem.solution[sol_size - 1])
                continue;
            a_star_elem n_elem;
            #if USE_FAST_MODIFICATION
                if (*visited_nodes <= USE_HEURISTIC_NODE_THRESHOLD_PHASE0)
                    move_sticker(elem.stickers, n_elem.stickers, mov);
                move_idxes_phase0(elem.idxes, n_elem.idxes, mov);
                dis = predict_phase0(n_elem.stickers, *visited_nodes, n_elem.idxes);
            #else
                move_sticker(elem.stickers, n_elem.stickers, mov);
                dis = predict_phase0(n_elem.stickers, *visited_nodes);
            #endif
            n_elem.f = sol_size + dis;
            for (i = 0; i < sol_size; ++i)
                n_elem.solution.push_back(elem.solution[i]);
            n_elem.solution.push_back(mov);
            if (dis == 0){
                vector<int> solution;
                for (i = 1; i < (int)n_elem.solution.size(); ++i)
                    solution.push_back(n_elem.solution[i]);
                res.push_back(solution);
                //return res;
                //break;
            } else
                que.push(n_elem);
        }
        ++(*visited_nodes);
    }
    return res;
}

vector<vector<int>> phase1(vector<solver_elem> inputs, int *visited_nodes){
    int i, j, mov, mov_idx, sol_size;
    int min_solution_length = 10000000;
    double dis;
    priority_queue<a_star_elem> que;
    a_star_elem elem;
    vector<vector<int>> res;
    for (i = 0; i < (int)inputs.size(); ++i){
        a_star_elem first_elem;
        for (j = 0; j < n_stickers; ++j)
            first_elem.stickers[j] = inputs[i].stickers[j];
        #if USE_FAST_MODIFICATION
            sticker2idx_phase1(first_elem.stickers, first_elem.idxes);
        #endif
        for (j = 0; j < (int)inputs[i].solution.size(); ++j)
            first_elem.solution.push_back(inputs[i].solution[j]);
        #if USE_FAST_MODIFICATION
            dis = predict_phase1(first_elem.stickers, *visited_nodes, first_elem.idxes);
        #else
            dis = predict_phase1(first_elem.stickers, *visited_nodes);
        #endif
        if (dis == 0){
            res.push_back(first_elem.solution);
            continue;
        }
        first_elem.f = (int)inputs[i].solution.size() + dis;
        first_elem.first = true;
        que.push(first_elem);
    }
    long long strt = tim();
    while (que.size() && *visited_nodes < N_MAX_PHASE1_NODES){
        if (tim() - strt > TIME_LIMIT_PHASE1 && res.size())
            break;
        elem = que.top();
        que.pop();
        sol_size = elem.solution.size();
        for (mov_idx = 0; mov_idx < n_phase1_moves; ++mov_idx){
            mov = phase1_move_candidate[mov_idx];
            if (!elem.first){
                if (calc_face(mov) == calc_face(elem.solution[sol_size - 1]))
                    continue;
                if (calc_axis(mov) == calc_axis(elem.solution[sol_size - 1]) && mov < elem.solution[sol_size - 1])
                    continue;
            }
            a_star_elem n_elem;
            #if USE_FAST_MODIFICATION
                if (*visited_nodes <= USE_HEURISTIC_NODE_THRESHOLD_PHASE1)
                    move_sticker(elem.stickers, n_elem.stickers, mov);
                move_idxes_phase1(elem.idxes, n_elem.idxes, mov_idx);
                dis = predict_phase1(n_elem.stickers, *visited_nodes, n_elem.idxes);
            #else
                move_sticker(elem.stickers, n_elem.stickers, mov);
                dis = predict_phase1(n_elem.stickers, *visited_nodes);
            #endif
            n_elem.f = sol_size + 1 + dis;
            for (i = 0; i < sol_size; ++i)
                n_elem.solution.push_back(elem.solution[i]);
            n_elem.solution.push_back(mov);
            if (dis == 0){
                vector<int> solution;
                for (i = 0; i < (int)n_elem.solution.size(); ++i)
                    solution.push_back(n_elem.solution[i]);
                res.push_back(solution);
                min_solution_length = min(min_solution_length, (int)solution.size());
            }
            que.push(n_elem);
        }
        ++(*visited_nodes);
    }
    return res;
}

void fix_sticker_direction(const int stickers[], int res[]){
    int replacement[6];
    replacement[stickers[4]] = 0;
    replacement[stickers[13]] = 1;
    replacement[stickers[22]] = 2;
    replacement[stickers[31]] = 3;
    replacement[stickers[40]] = 4;
    replacement[stickers[49]] = 5;
    for (int i = 0; i < n_stickers; ++i)
        res[i] = replacement[stickers[i]];
}

vector<vector<int>> solver(const int stickers[n_stickers]){
    int rotated_stickers[n_stickers];
    fix_sticker_direction(stickers, rotated_stickers);
    int tmp_stickers[n_stickers];
    int i, j, k;
    int sum_visited_nodes, visited_nodes;
    vector<solver_elem> phase0_solutions;
    vector<vector<int>> empty_res;
    visited_nodes = 0;
    vector<vector<int>> solution0 = phase0(rotated_stickers, &visited_nodes);
    sum_visited_nodes = visited_nodes;
    if (solution0.size() == 0){
        cerr << " no solution found in phase0" << endl;
        return empty_res;
    }
    cerr << " phase0 " << solution0.size() << " solutions found; visiited " << visited_nodes << " nodes" << endl;
    for (i = 0; i < min(50, (int)solution0.size()); ++i){
        solver_elem elem;
        for (j = 0; j < n_stickers; ++j)
            elem.stickers[j] = rotated_stickers[j];
        for (j = 0; j < (int)solution0[i].size(); ++j){
            elem.solution.push_back(solution0[i][j]);
            move_sticker(elem.stickers, tmp_stickers, solution0[i][j]);
            for (k = 0; k < n_stickers; ++k)
                elem.stickers[k] = tmp_stickers[k];
        }
        phase0_solutions.push_back(elem);
    }
    visited_nodes = 0;
    vector<vector<int>> res = phase1(phase0_solutions, &visited_nodes);
    sum_visited_nodes += visited_nodes;
    if (res.size() == 0){
        cerr << " no solution found in phase1" << endl;
        return empty_res;
    }
    cerr << " phase1 " << res.size() << " solutions found; visiited " << visited_nodes << " nodes" << endl;
    //cout << sum_visited_nodes << endl;
    return res;
}

bool check_solvability(int stickers[]){
    int i, j;
    // 1. check the numnber of each colors
    int n_colors[6];
    for (i = 0; i < 6; ++i)
        n_colors[i] = 0;
    for (i = 0; i < n_stickers; ++i){
        if (0 <= stickers[i] && stickers[i] < 6)
            ++n_colors[stickers[i]];
        else
            return false;
    }
    // 2. check all parts appears
    int co[n_corners], cp[n_corners], eo[n_edges], ep[n_edges];
    for (i = 0; i < n_corners; ++i){
        co[i] = IDX_UNDEFINED;
        cp[i] = IDX_UNDEFINED;
    }
    for (i = 0; i < n_edges; ++i){
        eo[i] = IDX_UNDEFINED;
        ep[i] = IDX_UNDEFINED;
    }
    sticker2arr(stickers, co, cp, eo, ep);
    for (i = 0; i < n_corners; ++i){
        if (co[i] == IDX_UNDEFINED || cp[i] == IDX_UNDEFINED)
            return false;
    }
    for (i = 0; i < n_edges; ++i){
        if (eo[i] == IDX_UNDEFINED || ep[i] == IDX_UNDEFINED)
            return false;
    }
    for (i = 0; i < n_corners; ++i){
        for (j = i + 1; j < n_corners; ++j){
            if (cp[i] == cp[j])
                return false;
        }
    }
    for (i = 0; i < n_edges; ++i){
        for (j = i + 1; j < n_edges; ++j){
            if (ep[i] == ep[j])
                return false;
        }
    }
    // 3. check parity
    int eo_sum = 0;
    for (i = 0; i < n_edges; ++i)
        eo_sum += eo[i];
    if (eo_sum % 2)
        return false;
    int co_sum = 0;
    for (i = 0; i < n_corners; ++i)
        co_sum += co[i];
    if (co_sum % 3)
        return false;
    int ep_n_replace = 0;
    for (i = 0; i < n_edges; ++i){
        if (ep[i] != i){
            for (j = i + 1; j < n_edges; ++j){
                if (ep[j] == ep[i]){
                    ++ep_n_replace;
                    swap(ep[i], ep[j]);
                }
            }
        }
    }
    if (ep_n_replace % 2)
        return false;
    int cp_n_replace = 0;
    for (i = 0; i < n_corners; ++i){
        if (cp[i] != i){
            for (j = i + 1; j < n_corners; ++j){
                if (cp[j] == cp[i]){
                    ++cp_n_replace;
                    swap(cp[i], cp[j]);
                }
            }
        }
    }
    if (cp_n_replace % 2)
        return false;
    return true;
}

// set 0 to execute without test
#define TEST_FLAG 8

#if TEST_FLAG != 0
    #define W 0
    #define G 1
    #define R 2
    #define B 3
    #define O 4
    #define Y 5
#endif

int main(){
    init();
    cerr << "solver initialized" << endl;

    #if TEST_FLAG == 0
        int stickers[n_stickers];
    #elif TEST_FLAG == 1
        int stickers[n_stickers] = {4, 4, 5, 2, 0, 2, 1, 5, 0, 0, 1, 3, 5, 1, 0, 2, 3, 4, 4, 0, 4, 4, 2, 3, 0, 1, 2, 3, 1, 5, 5, 3, 0, 3, 0, 0, 1, 5, 2, 3, 4, 4, 3, 2, 1, 5, 4, 1, 3, 5, 2, 2, 1, 5};
    #elif TEST_FLAG == 2
        int stickers[n_stickers] = {5, 2, 2, 4, 0, 5, 0, 5, 1, 4, 1, 5, 3, 1, 0, 1, 5, 1, 2, 3, 5, 3, 2, 4, 0, 5, 2, 3, 1, 1, 1, 3, 0, 0, 2, 3, 4, 3, 3, 4, 4, 2, 4, 1, 0, 4, 4, 2, 0, 5, 2, 5, 0, 3};
    #elif TEST_FLAG == 3 // failed example
        int stickers[n_stickers] = {Y, Y, Y, O, R, O, W, W, W, B, G, G, R, W, O, B, B, G, R, W, R, B, G, B, O, Y, O, G, B, B, R, Y, O, G, G, B, R, Y, R, G, B, G, O, W, O, W, W, W, R, O, R, Y, Y, Y};
    #elif TEST_FLAG == 4 // error example; 1EO at UF
        int stickers[n_stickers] = {W, W, W, W, W, W, W, G, W, G, W, G, G, G, G, G, G, G, R, R, R, R, R, R, R, R, R, B, B, B, B, B, B, B, B, B, O, O, O, O, O, O, O, O, O, Y, Y, Y, Y, Y, Y, Y, Y, Y};
    #elif TEST_FLAG == 5 // error example; 1CO at UFR
        int stickers[n_stickers] = {W, W, W, W, W, W, W, W, G, G, G, R, G, G, G, G, G, G, W, R, R, R, R, R, R, R, R, B, B, B, B, B, B, B, B, B, O, O, O, O, O, O, O, O, O, Y, Y, Y, Y, Y, Y, Y, Y, Y};
    #elif TEST_FLAG == 6 // error example; UR and UF is same
        int stickers[n_stickers] = {W, W, W, W, W, W, W, W, W, G, G, G, G, G, G, G, G, G, R, G, R, R, R, R, R, R, R, B, B, B, B, B, B, B, B, B, O, O, O, O, O, O, O, O, O, Y, Y, Y, Y, Y, Y, Y, Y, Y};
    #elif TEST_FLAG == 7 // error example; UFR and UFL is same
        int stickers[n_stickers] = {W, W, W, W, W, W, W, W, W, G, G, O, G, G, G, G, G, G, G, R, R, R, R, R, R, R, R, B, B, B, B, B, B, B, B, B, O, O, O, O, O, O, O, O, O, Y, Y, Y, Y, Y, Y, Y, Y, Y};
    #elif TEST_FLAG == 8 // phase1 failed
        int stickers[n_stickers] = {B, G, G, B, W, O, W, W, Y, G, G, R, O, O, R, Y, Y, R, G, W, O, W, G, B, W, G, W, Y, O, O, Y, R, R, R, W, O, W, R, O, Y, B, Y, Y, B, B, R, G, B, O, Y, R, B, B, G};
    #endif
    int i, j;
    long long strt;
    bool solvable;
    while (true){
        #if TEST_FLAG == 0
            for (i = 0; i < n_stickers; ++i)
                cin >> stickers[i];
        #endif
        solvable = check_solvability(stickers);
        if (!solvable){
            cout << "ERROR This scramble is not solvable!" << endl;
            #if TEST_FLAG != 0
                break;
            #endif
            continue;
        }
        cerr << "start!" << endl;
        strt = tim();
        vector<vector<int>> solution = solver(stickers);
        cerr << "solved in " << tim() - strt << " ms" << endl;
        cout << solution.size() << endl;
        for (i = 0; i < (int)solution.size(); ++i){
            for (j = 0; j < (int)solution[i].size(); ++j)
                cout << solution[i][j] << " ";
            cout << endl;
        }
        #if TEST_FLAG != 0
            break;
        #endif
    }
    return 0;
}
