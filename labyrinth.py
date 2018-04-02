#!/usr/bin/python3

import modules.fileinput as fileinput
import modules.output as output
import modules.parsing as parsing
import modules.ways as ways


class LabyrinthClass:
    def __init__(self):
        self.lab = []
        self.dp = []
        self.used = set()
        self.start = (0, 0)
        self.finish = []
        self.bombs = 0
        self.landtypes = {}
        self.kwalls = {}
        self.coefs = []
        self.filename = ''
        self.all_states = set()
        self.alpha = 1
        self.timebomb = 0
        self.output_type = output.output_type.on_lab.name
        self.generator_input = False


def main():
    try:
        labth = LabyrinthClass()
        labth = parsing.parse_input(labth)
        if not parsing.correct_input(labth):
            return
        labth = fileinput.input_file(labth)
        if not labth or not len(labth.finish):
            return
        ways.evaluate_ways(labth)
        way, bombs, time = ways.way_to_exit(labth)
        output.out(labth, way, bombs, labth.alpha, time)
    except (ValueError) as e:
        print(e)


if __name__ == "__main__":
    main()

    # xxxxxxxx
    # x*     x
    # xwwww  x
    # x.     x
    # xxxxxxxx

    # xxxxxxxxxxxxxxxxx
    # x*     www      x
    # xwwwwww       wwx
    # x    wwwwww     x
    # x  w        wwwwx
    # xwwwwwwwww     .x
    # xxxxxxxxxxxxxxxxx
