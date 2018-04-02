from enum import Enum


class output_type(Enum):
    wasd = 1
    on_lab = 2
    text = 3


def out(lab, way, bombs, alpha, time):
    if len(way) == 1:
        # print("No way!")
        return
    if lab.output_type == output_type.wasd.name:
        out_WASD(way)
    if lab.output_type == output_type.on_lab.name:
        out_on_lab(lab, way)
    if lab.output_type == output_type.text.name:
        out_text(way, alpha, bombs, time)


def out_WASD(way):
    print(choose_direction(way))


def out_on_lab(lab, way):
    lab_way = []
    for i in range(len(lab.lab)):
        lab_way.append([])
        for j in range(len(lab.lab[i])):
            lab_way[i].append(' ')

    for i in range(len(lab.lab)):
        lab_way[i][0] = 'x'
        lab_way[i][len(lab.lab[0]) - 1] = 'x'
    for i in range(len(lab.lab[0])):
        lab_way[0][i] = 'x'
        lab_way[len(lab.lab) - 1][i] = 'x'

    for (i, step) in enumerate(way):
        lab_way[way[i].i][way[i].j] = '#'

    for i in range(len(lab_way)):
        for j in range(len(lab_way[i])):
            print(lab_way[i][j], end='')
        print('')


def out_text(way, alpha, bombs, time):
    print("Minimal way for this alpha {} consists of {} bombs and {} time\n"
          .format(alpha, bombs, time))
    print("Way to exit contains:")
    for i in range(0, len(way)):
        print('step {} : i: {}, j: {} with bombs: {}'
              .format(i + 1, way[i].i, way[i].j, way[i].bombs))


def choose_direction(way):
    a = ""
    first = True
    cur = ""
    for next_step in way:
        if first:
            first = False
            cur = next_step
            continue
        if cur.i == next_step.i:
            if cur.j > next_step.j:
                a += 'a'
            else:
                a += 'd'
        else:
            if cur.i > next_step.i:
                a += 'w'
            else:
                a += 's'
        cur = next_step
    return a
