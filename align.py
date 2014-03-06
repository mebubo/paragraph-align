#!/usr/bin/env python

import numpy, math, os
from operator import itemgetter
from os.path import join

MISMATCH_PENALTY = 10
GAP_PENALTY = 100
MAX_MERGE = 1

def penalty(e1, e2):
    if e1 == e2:
        return 0
    return MISMATCH_PENALTY

def length_penalty(e1, e2):
    return 100 * abs(len(e1) - len(e2))/(len(e1) + len(e2))

def candidates(s1, s2, i, j, r, penalty):
    p = penalty(s1[i], s2[j])
    yield (-1, -1), r[i-1, j-1] + p
    yield (-1, 0), r[i-1, j] + GAP_PENALTY
    yield (0, -1), r[i, j-1] + GAP_PENALTY
    for k in range(2, MAX_MERGE + 1):
        if i-k >= 0:
            pm = penalty("".join(s1[i-k+1:i+1]), s2[j])
            if pm < p:
                yield (-k, -1), r[i-k, j-1] + 10 + pm
        if j-k >= 0:
            pm = penalty(s1[i], "".join(s2[j-k+1:j+1]))
            if pm < p:
                yield (-1, -k), r[i-1, j-k] + 10 + pm

def fill_matrix(s1, s2, penalty):
    l1, l2 = map(len, (s1, s2))
    r = numpy.zeros((l1, l2))
    for i in range(l1):
        r[i, 0] = GAP_PENALTY * i
    for i in range(l2):
        r[0, i] = GAP_PENALTY * i
    for i in range(1, l1):
        for j in range(1, l2):
            r[i, j] = min(candidates(s1, s2, i, j, r, penalty), key=itemgetter(1))[1]
    print r
    return r

def reconstruct_solution(s1, s2, r, penalty):
    i, j = map(lambda s: len(s) - 1, (s1, s2))
    print "++", i, j
    result = []
    while i >= 0 and j >= 0:
        di, dj = min(candidates(s1, s2, i, j, r, penalty), key=itemgetter(1))[0]
        def take(s, k, dk):
            return "".join(s[k+dk+1:k+1])
        result.append((take(s1, i, di), take(s2, j, dj)))
        i, j = i+di, j+dj
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

def align(s1, s2, penalty=length_penalty):
    r = fill_matrix(s1, s2, penalty)
    return reconstruct_solution(s1, s2, r, penalty)

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
        paths = map(lambda x: join(*x), zip(inputs, files))
        sequences = map(read_file, paths)
        out_path = join(out, files[0])
        write_table(align(*sequences), out_path)

merge("hpmor_fren", "hpmor_fr", "hpmor_en")
# merge("hpmor_ruen", "hpmor_ru", "hpmor")
