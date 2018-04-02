import sys


def input_file(labth):
    if not labth.filename:
        labth_input = []
        for line in sys.stdin:
            line = line.strip()
            if not line:
                break
            labth_input.append(line)
        if labth.generator_input:
            inform = []
            for line in sys.stdin:
                line = line.strip()
                if line:
                    inform.append(line)
            labth = process_generator_inf(labth, inform)
        labth = process_file(labth, labth_input)
    else:
        with open(labth.filename, 'r') as labyrinth:
            labb = []
            inform = []
            for line in labyrinth:
                line = line.strip()
                if line and line[0] != 'x':
                    inform.append(line)
                elif line:
                    labb.append(line)
            if labth.generator_input:
                labth = process_generator_inf(labth, inform)
            labth = process_file(labth, labb)
    return labth


def process_generator_inf(labth, inputt):
    def proc_elem_land(elem):
        symbol, val = elem.split(': ')
        if symbol and symbol[0] == '{':
            symbol = symbol[1:]
        if val and val[len(val) - 1] == '}':
            val = val[:-1]
        labth.landtypes[symbol[1:-1]] = int(val)

    def proc_elem_kwall(elem):
        point, val = elem.split(': ')
        x, y = point.split(', ')
        if x and x[0] == '{':
            x = x[1:]
        if val and val[len(val) - 1] == '}':
            val = val[:-1]
        x = int(x[1:])
        y = int(y[:-1])
        val = int(val)
        labth.kwalls[(x, y)] = val

    for line in inputt:
        line = line.strip()
        if line[0] != '{':
            continue
        if line[1] == "'":
            line = line.split(',')
            for elem in line:
                proc_elem_land(elem)
        else:
            count = 1
            line = list(line)
            for i in range(len(line)):
                if line[i] == ',':
                    if count % 2 == 0:
                        line[i] = ';'
                    count += 1
            line = "".join(line)
            line = line.split('; ')
            for elem in line:
                proc_elem_kwall(elem)

    labth.bombs = max(labth.bombs, 4)
    return labth


def process_file(labth, labth_input):
    i = 0
    for line in labth_input:
        line = line.strip()
        labth.lab.append(list())
        labth.dp.append(list())
        labth.coefs.append(list())
        j = 0
        for c in line:
            if c == '*':
                labth.start = (i, j)
            if c == '.':
                labth.finish.append((i, j))
            if c in labth.landtypes:
                labth.coefs[i].append(labth.landtypes[c])
            elif c == 'w' and (i, j) in labth.kwalls:
                labth.coefs[i].append(labth.kwalls[(i, j)])
            else:
                labth.coefs[i].append(1)
            labth.lab[i].append(c)
            labth.dp[i].append(dict())
            j += 1
        i += 1
    return labth
