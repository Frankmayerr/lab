#!/usr/bin/python3


class state:
    def __init__(self, i, j, bombs_):
        self.i = i
        self.j = j
        self.bombs = bombs_

    def __eq__(self, other):
        return (self.i, self.j) == (other.i, other.j)

    def __hash__(self):
        return self.i * 10000000 + self.j * 10000 + self.bombs * 1


class dp_value:
    def __init__(self, n, p, i=0, j=0):
        self.time = n
        self.prev_state = p
        self.coor = (i, j)


def neighbours(labth, i, j):
    s = (1, 0, -1)
    res = list()
    for ii in s:
        for jj in s:
            if 0 <= j + jj < len(labth.lab[i]) \
                    and 0 <= i + ii < len(labth.lab) \
                    and (labth.lab[i + ii][j + jj] != 'x') \
                    and (jj == 0 and ii != 0 or jj != 0 and ii == 0):
                res.append((i + ii, j + jj))
    return res


def update_state(labth, cur):
    neighs = neighbours(labth, cur.i, cur.j)
    for i, j in neighs:
        k = labth.coefs[i][j]
        # if lab[i][j] != 'w': k = 0
        newtime = labth.dp[cur.i][cur.j][cur.bombs].time
        newbombs = cur.bombs
        if labth.lab[i][j] == 'w':
            newbombs -= k
            newtime += 1 + k * labth.timebomb
        else:
            newtime += k
        if newbombs >= 0:
            if newbombs not in labth.dp[i][j] \
                    or labth.dp[i][j][newbombs].time > newtime:
                new_val = dp_value(newtime, cur, i, j)
                labth.dp[i][j][newbombs] = new_val
                labth.all_states.add(state(i, j, newbombs))
    return labth


def evaluate_ways(lab_):  # build up all ways
    lab_.dp[lab_.start[0]][lab_.start[1]][lab_.bombs] = \
        dp_value(0, state(-1, -1, 0))
    lab_.all_states.add(state(lab_.start[0], lab_.start[1], lab_.bombs))
    for i in range(len(lab_.lab) * len(lab_.lab[0]) * (lab_.bombs + 1)):
        # перебираем n итераций (кол-во вершин в графе)
        cur = state(-1, -1, -1)
        for st in lab_.all_states:
            newstate = lab_.dp[st.i][st.j][st.bombs]
            condition = cur.i == -1 or \
                newstate.time < lab_.dp[cur.i][cur.j][cur.bombs].time
            if st not in lab_.used and condition:
                cur = st
        if cur.i == -1:
            break
        lab_.used.add(cur)
        lab_ = update_state(lab_, cur)


def find_exit(labth):  # find the exit with shortest way for specific alpha
    exits = list()
    for i, j in labth.finish:
        exits.append(labth.dp[i][j])
    ansforalpha = 9999999999
    alphabombs = -1
    alphatime = -1
    ai = aj = -1
    for exit_point in exits:
        for bomb, item in exit_point.items():
            curbomb = labth.bombs - bomb
            func = labth.alpha * curbomb + (1 - labth.alpha) * item.time
            if func < ansforalpha:
                ansforalpha = func
                alphabombs = bomb
                alphatime = item.time
                ai = item.coor[0]
                aj = item.coor[1]

    return ai, aj, alphabombs, alphatime


def way_to_exit(labth):  # find cell's order in way to specific cell
    i, j, bombs, time = find_exit(labth)
    way = [state(i, j, bombs)]
    cur = state(i, j, bombs)
    if cur.i == -1 or cur.j == -1 or cur.bombs == -1:
        return way, bombs, time

    while labth.dp[cur.i][cur.j][cur.bombs].prev_state.i != -1:
        way.append(labth.dp[cur.i][cur.j][cur.bombs].prev_state)
        cur = labth.dp[cur.i][cur.j][cur.bombs].prev_state
    return list(reversed(way)), bombs, time
