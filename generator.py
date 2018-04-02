#!/usr/bin/python3

import argparse
import queue
from random import randint


class additional:
    def __init__(self, n=0, m=0):
        self.coefs = []
        self.kwalls = {}
        self.landtypes = {}
        for i in range(n):
            self.coefs.append([])
            for j in range(m):
                self.coefs[i] = [1] * m


def neighbours(i, j, lab, condition):
    s = (1, 0, -1)
    res = list()
    for ii in s:
        for jj in s:
            if 0 <= j + jj < len(lab[i]) and 0 <= i + ii < len(lab) \
                    and condition(i + ii, j + jj) \
                    and any((ii, jj)):
                res.append((i + ii, j + jj))
    return res


def choose_object(i, j, lab):
    neibs = neighbours(i, j, lab,
                       lambda x, y: lab[x][y] != 'x' and lab[x][y] != 'w')
    if len(neibs) < randint(3, 5):
        return ' '
    return 'w'


def dfs_add_walls(lab):
    n = len(lab)
    m = len(lab[0])
    used = []
    all_el = n * m
    curi = 1
    curj = 1
    for i in range(n):
        used.append([])
        for j in range(m):
            used[i].append(False)
    q = queue.Queue()
    cur_am = 1
    cur_from_q = False
    while cur_am < all_el:
        used[curi][curj] = True
        if not cur_from_q:
            q.put((curi, curj))
            lab[curi][curj] = choose_object(curi, curj, lab)
        neibs = neighbours(curi, curj, lab,
                           lambda x, y: (lab[x][y] != 'x' and
                                         lab[x][y] != 'w' and not used[x][y]))
        if len(neibs) == 0:
            if q.empty():
                break
            else:
                curi, curj = q.get()
                cur_from_q = True
        else:
            cur_am += 1
            curi, curj = neibs[randint(0, len(neibs) - 1)]
            cur_from_q = False
    return lab


def make_lab(n, m, lands=True, kwalls=True):
    lab = []
    inf = additional(n, m)
    for i in range(n):
        lab.append([])
        for j in range(m):
            lab[i].append(' ')

    def add_outer_walls():
        for i in range(n):
            lab[i][0] = 'x'
            lab[i][m - 1] = 'x'
        for i in range(m):
            lab[0][i] = 'x'
            lab[n - 1][i] = 'x'

    def add_start():
        stop = False
        for i in range(n):
            if stop:
                break
            for j in range(m):
                if lab[i][j] == ' ':
                    lab[i][j] = '*'
                    stop = True
                    break

    def add_finish():
        stop = False
        for i in range(n - 1, 0, -1):
            if stop:
                break
            for j in range(m - 1, 0, -1):
                if lab[i][j] == ' ':
                    lab[i][j] = '.'
                    stop = True
                    break

    def add_k_walls():
        for i in range(n):
            for j in range(m):
                if lab[i][j] == 'w' and not randint(0, 3):
                    val = randint(1, 3)
                    inf.kwalls[(i, j)] = val
                    inf.coefs[i][j] = val

    def add_landtypes():
        for i in range(n):
            for j in range(m):
                if lab[i][j] == ' ' and not randint(0, 5):
                    val = randint(1, 5)
                    letter = chr(val + ord('a') - 1)
                    lab[i][j] = letter
                    inf.landtypes[letter] = val
                    inf.coefs[i][j] = val

    add_outer_walls()
    lab = dfs_add_walls(lab)
    add_start()
    add_finish()
    if kwalls:
        add_k_walls()
    if lands:
        add_landtypes()
    return lab, inf


def arguments():
    def add_args(parser):
        parser.add_argument('-a', '--add',
                            help="Can add 'lands' or(and) 'kwalls'",
                            nargs='*', default=[])
        parser.add_argument('-d', '--dim',
                            help='Write labyrinth dimensions in arguments: '
                                 'n m (default: 10,10)',
                            nargs='*', default=(8, 8))
        parser.add_argument('-o', '--out',
                            help="Output with additional information "
                                 "about kwalls and lands", action='store_true')

    parser = argparse.ArgumentParser(
        description='Generator: input n and m dimensions to get labyrinth')
    add_args(parser)
    args = parser.parse_args()
    n, m = vars(args)['dim']
    if not args.out:
        args.add = []
    return args.add, int(n) + 2, int(m) + 2, args.out


def output_addit(inf):
    print("\nAdditional information:")
    if len(inf.landtypes):
        print(inf.landtypes)
    if len(inf.kwalls):
        print(inf.kwalls)


def main():
    addit_parse, n, m, outt = arguments()
    labth, additional_inf = make_lab(n, m,
                                     'lands' in addit_parse,
                                     'kwalls' in addit_parse)
    print('\n'.join(''.join(row) for row in labth))
    if outt:
        output_addit(additional_inf)


if __name__ == "__main__":
    main()
