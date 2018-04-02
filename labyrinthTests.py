#!/usr/bin/python

import os.path
import unittest

import generator
import modules.fileinput as fileinput
import modules.parsing as parsing
import modules.ways as ways
from labyrinth import LabyrinthClass as labth


class LabTests(unittest.TestCase):
    def setUp(self):
        self.lab = labth()
        self.lab.alpha = 1
        self.lab.bombs = 4
        self.lab.landtypes['c'] = 3
        self.lab.landtypes['b'] = 2
        self.lab.kwalls[(2, 1)] = 2
        self.timebomb = 2

        with open(os.path.join("Tests", "test_input.txt"), 'r') as lab_:
            self.lab = fileinput.process_file(self.lab, lab_)

    def test_exit_parse(self):
        a = parsing.exit_parse(["2,3", "55,77"])
        res = [(2, 3), (55, 77)]
        self.assertListEqual(a, res)

    def test_walls_parse(self):
        a = parsing.wall_coef_parse(["2,3:32", "55,77:1"])
        res = {(2, 3): 32, (55, 77): 1}
        self.assertDictEqual(a, res)

    def test_land_parse(self):
        a = parsing.land_parse(["c:3", "k:44"])
        res = {'c': 3, 'k': 44}
        self.assertDictEqual(a, res)

    def test_neighbours(self):
        t = ways.neighbours(self.lab, 1, 1)
        res = [(2, 1), (1, 2)]
        self.assertListEqual(t, res)

    def test_process_file(self):
        for (i, row) in enumerate(self.lab.lab):
            for (j, cell) in enumerate(row):
                if cell == '*':
                    self.assertEqual(self.lab.start, (i, j))
                elif cell == '.':
                    self.assertIn((i, j), self.lab.finish)
                elif cell == 'w' and (i, j) in self.lab.kwalls:
                    self.assertEqual(self.lab.coefs[i][j],
                                     self.lab.kwalls[(i, j)])
                elif cell in self.lab.landtypes:
                    c = self.lab.lab[i][j]
                    self.assertEqual(self.lab.coefs[i][j],
                                     self.lab.landtypes[c])
                else:
                    self.assertEqual(self.lab.coefs[i][j], 1)

    def test_all_updates(self):
        ways.evaluate_ways(self.lab)
        for i in range(len(self.lab.lab)):
            for j in range(len(self.lab.lab[i])):
                if self.lab.lab[i][j] == 'x':
                    continue
                for bombs_, st in self.lab.dp[i][j].items():
                    prev_st = self.lab.dp[i][j][bombs_].prev_state
                    if prev_st.i == -1:
                        continue
                    prev_bombs = prev_st.bombs
                    prev_time = \
                        self.lab.dp[prev_st.i][prev_st.j][prev_bombs].time
                    if self.lab.lab == 'w':
                        self.assertEqual(bombs_,
                                         prev_bombs + self.lab.coefs[i][j])
                        self.assertEqual(st.time, prev_time + 1)
                    elif self.lab.lab[i][j] in self.lab.landtypes:
                        self.assertEqual(bombs_, prev_bombs)
                        self.assertEqual(st.time,
                                         prev_time + self.lab.coefs[i][j])

    def test_bad_argument_alpha(self):
        self.lab.alpha = -2
        with self.assertRaises(ValueError):
            parsing.correct_input(self.lab)
        self.lab.alpha = 1.1
        with self.assertRaises(ValueError):
            parsing.correct_input(self.lab)

    def test_bad_argument_bombs(self):
        self.lab.bombs = -2
        with self.assertRaises(ValueError):
            parsing.correct_input(self.lab)

    def test_bad_argument_filename(self):
        self.lab.filename = 'dfsdfsdf'
        with self.assertRaises(ValueError):
            parsing.correct_input(self.lab)

    def test_bad_argument_timebomb(self):
        self.lab.timebomb = -2
        with self.assertRaises(ValueError):
            parsing.correct_input(self.lab)

    def test_bad_argument_good(self):
        self.assertTrue(parsing.correct_input(self.lab))

    def test_output_WASD(self):
        ways.evaluate_ways(self.lab)
        ways.find_exit(self.lab)
        way = ways.way_to_exit(self.lab)[0]
        self.assertEqual(self.lab.start[0], way[0].i)
        self.assertEqual(self.lab.start[1], way[0].j)
        finish = False
        for exit in self.lab.finish:
            if exit[0] == \
                    way[len(way) - 1].i and exit[1] == way[len(way) - 1].j:
                finish = True
        self.assertTrue(finish)
        cur = 0
        first = True
        for next in way:
            if first:
                first = False
                cur = next
                continue
            dif = abs(cur.i - next.i) + abs(cur.j - next.j)
            self.assertLess(dif, 2)
            self.assertGreaterEqual(dif, 0)
            cur = next

    def test_impassable_labyrinth(self):
        lab = labth()
        lab.alpha = 1
        lab.bombs = 1
        with open(os.path.join("Tests",
                               "impassable_lab_input.txt"), 'r') as lab_:
            lab = fileinput.process_file(lab, lab_)
        ways.evaluate_ways(lab)
        self.assertEqual(-1, ways.way_to_exit(lab)[2])

    def test_diff_alpha_labyrinth(self):
        ways.evaluate_ways(self.lab)
        ways.find_exit(self.lab)
        self.lab.alpha = 1
        way = ways.way_to_exit(self.lab)[0]
        self.assertEqual(11, len(way))
        self.lab.alpha = 0
        way = ways.way_to_exit(self.lab)[0]
        self.assertEqual(3, len(way))

    def test_two_exits(self):
        lab = labth()
        lab.alpha = 1
        lab.bombs = 0
        with open(os.path.join("Tests", "two_exits_input.txt"), 'r') as lab_:
            lab = fileinput.process_file(lab, lab_)
        ways.evaluate_ways(lab)
        way = ways.way_to_exit(lab)[0]
        self.assertEqual((1, 5), (way[len(way) - 1].i, way[len(way) - 1].j))

    def test_dif_surfaces(self):
        lab = labth()
        lab.alpha = 1
        lab.bombs = 0
        lab.landtypes['c'] = 3
        lab.landtypes['b'] = 2
        with open(os.path.join("Tests", "dif_surf_input.txt"), 'r') as lab_:
            lab = fileinput.process_file(lab, lab_)
        ways.evaluate_ways(lab)
        time = ways.way_to_exit(lab)[2]
        self.assertEqual(11, time)

    def check_generator(self):
        lab, add_inf = generator.make_lab(7, 4, True, True)
        have_start = False
        have_finish = False
        have_open_place = False
        have_walls = False
        outer_walls = True
        too_much_walls = False
        for i in range(len(lab)):
            for j in range(len(lab[i])):
                if (not i or not j):
                    if lab[i][j] != 'x':
                        outer_walls = False
                else:
                    if lab[i][j] == '*':
                        have_start = True
                    if lab[i][j] == '.':
                        have_finish = True
                    if lab[i][j] == 'w':
                        have_walls = True
                    if lab[i][j] == ' ':
                        have_open_place = True
                nn = generator.neighbours(i, j, lab, lambda x, y: True)
                wamount = 0
                for n in nn:
                    if lab[n[0]][n[1]] == 'w':
                        wamount += 1
                if wamount == 8:
                    too_much_walls = True
            self.assertTrue(have_start and have_finish and have_open_place and
                            have_walls and outer_walls and not too_much_walls)


if __name__ == '__main__':
    unittest.main()
