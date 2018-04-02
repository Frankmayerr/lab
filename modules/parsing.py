#!/usr/bin/python3

import argparse


def land_parse(s):
    lands = {}
    # example: a:3 b:10 c:231
    for item in s:
        land, coef = item.split(':')
        lands[land] = int(coef)
    return lands


def wall_coef_parse(s):
    # example: 2,3:4 1,1:53
    wall_dict = {}
    for w in s:
        koord, k = w.split(':')
        i, j = koord.split(',')
        wall_dict[(int(i), int(j))] = int(k)
    return wall_dict


def exit_parse(s):
    ans = []
    for item in s:
        i, j = item.split(',')
        ans.append((int(i), int(j)))
    return ans


def add_args(parser):
    parser.add_argument('-b', '--bombs',
                        help='maximum amount of bombs', default=0, type=int)

    parser.add_argument('-f', '--inputfile',
                        help='labyrinth file name. it contains:'
                             'w - inner walls'
                             'x - outer walls'
                             '* - start'
                             '. - finish (exit from labyrinth)'
                             '\' \'  - free place\')')

    parser.add_argument('-a', '--alpha',
                        help='coefficient to choose characteristic '
                             'of minimal way; '
                             'function=alpha*bombs+(1-alpha)*steps',
                        default=0, type=float)

    parser.add_argument('-e', '--exits',
                        help='cells with exits,format:(i,j); '
                             "it also can be added in labyrinth as '.'",
                        nargs='*', default=[])

    parser.add_argument('-s', '--starts',
                        help='cells with initial position, '
                             'format: (i,j); '
                             "it also can be added in labyrinth as '*'",
                        nargs='*', default=[])

    parser.add_argument('-l', '--lands', nargs='*', type=str, default={},
                        help='cells with not standard speed to go; '
                             'format: c,k; '
                             'where k is coef of speed and c is the symbol '
                             'in labyrinth for this land type')

    parser.add_argument('-w', '--walls', nargs='*', type=str, default=[],
                        help='walls with K bombs to damage; format: '
                             'i,j:k where k is amount of bombs')

    parser.add_argument('--timebomb', help='time to use 1 bomb',
                        type=int, default=0)

    parser.add_argument('-o', '--output',
                        help="you can choose 'wasd', "
                             "'on_lab' and 'text' - point out it with ",
                        type=str, default='on_lab')
    parser.add_argument('-g', '--generator',
                        help="when yot input labyrinth from generator "
                             "with additional information",
                        action='store_true')


def parse_input(labth):
    parser = argparse.ArgumentParser('labyrinth')
    add_args(parser)
    args = parser.parse_args()
    labth.filename = None
    labth.filename = args.inputfile
    labth.bombs = args.bombs
    labth.finish = exit_parse(args.exits)
    labth.alpha = args.alpha
    labth.timebomb = args.timebomb
    labth.start = args.starts
    labth.landtypes = land_parse(args.lands)
    labth.kwalls = wall_coef_parse(args.walls)
    labth.output_type = args.output
    if args.generator:
        labth.generator_input = True
    return labth


def correct_input(labth):
    if labth.filename:
        try:
            with open(labth.filename, 'r') as labyrinth:
                pass
        except (FileNotFoundError, FileExistsError) as e:
            raise ValueError("No such file or directory: " + labth.filename)
            # sys.stderr.write("No such file or directory: " + labth.filename)
            return False

    for coord, k in labth.kwalls.items():
        i, j = coord
        if labth.lab[i][j] != 'w' or k < 0:
            raise ValueError("Incorrect Argument: walls")
            return False

    for symbol, k in labth.landtypes.items():
        if len(symbol) > 1 or k < 0:
            raise ValueError("Incorrect Argument: land types")
            return False

    if not 0 <= labth.alpha <= 1:
        raise ValueError("Incorrect Argument: alpha should be in [0,1]")
        return False

    if labth.bombs < 0:
        raise ValueError("Incorrect Argument: bombs should be positive number")
        return False

    if labth.timebomb < 0:
        raise ValueError("Incorrect Argument: "
                         "time to make bomb should be positive number")
        return False

    if labth.output_type not in ('on_lab', 'wasd', 'text'):
        raise ValueError("Incorrect output type: "
                         "should be \'wasd\', \'on_lab\' or \'text\'")
        return False

    return True
