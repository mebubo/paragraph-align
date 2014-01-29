#!/usr/bin/env python

import numpy, math, os
from operator import itemgetter
from os.path import join

MISMATCH_PENALTY = 10
GAP_PENALTY = 100

def penalty(e1, e2):
    if e1 == e2:
        return 0
    return MISMATCH_PENALTY

def length_penalty(e1, e2):
    return 100 * abs(len(e1) - len(e2))/(len(e1) + len(e2))

def align(s1, s2, penalty=length_penalty):
    l1, l2 = map(len, (s1, s2))
    r = numpy.zeros((l1, l2))
    def candidates(i, j):
        return (r[i-1, j-1] + penalty(s1[i], s2[j]),
                r[i-1, j] + GAP_PENALTY,
                r[i, j-1] + GAP_PENALTY)
    for i in range(l1):
        r[i, 0] = GAP_PENALTY * i
    for i in range(l2):
        r[0, i] = GAP_PENALTY * i
    for i in range(1, l1):
        for j in range(1, l2):
            r[i, j] = min(candidates(i, j))
    print r
    def min_index(seq):
        return min(enumerate(seq), key=itemgetter(1))[0]
    i, j = l1-1, l2-1
    result = []
    while i >= 0 and j >= 0:
        m = min_index(candidates(i, j))
        if m == 0:
            result.append((s1[i], s2[j]))
            i, j = i-1, j-1
        elif m == 1:
            result.append((s1[i], None))
            i -= 1
        elif m == 2:
            result.append((None, s2[j]))
            j -= 1
    if i < 0:
        i = 0
    if j < 0:
        j = 0
    if i > 0:
        while i >= 0:
            result.append((s1[i], None))
            i -= 1
    elif j > 0:
        while j >= 0:
            result.append((None, s2[j]))
            j -= 1
    return list(reversed(result))

def format(aligned):
    for p in aligned:
        print p[0] if p[0] is not None else ".",
    print
    for p in aligned:
        print p[1] if p[1] is not None else ".",

def read_file(name):
    def generator():
        with open(name) as f:
            for line in f:
                yield line
    return list(generator())[1:-1]

def write_table(pairs, name="table.html"):
    with open(name, 'w') as f:
        f.write('<html><head><meta charset="utf-8"></head><body><table border="1" style="border-collapse: collapse">\n')
        for p1, p2 in pairs:
            f.write('<tr><td>%s</td><td>%s</td></tr>\n' % (p1, p2))
        f.write('</table></body></html>')

def merge(out, *inputs):
    for files in zip(*map(os.listdir, inputs)):
        write_table(align(*map(read_file, map(lambda x: join(*x), zip(inputs, files)))), join(out, files[0]))

merge("hpmor_fren", "hpmor_fr", "hpmor_en")
# merge("hpmor_ruen", "hpmor_ru", "hpmor")
