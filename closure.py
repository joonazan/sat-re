import sys
from itertools import *

hard_input = [
    "ACDFGIJKLNOP MNOP",
    "GKLP BCDHIJKLMNOP",
    "DJLO EFGHIJKLMNOP",
]

if len(sys.argv) == 2:
    with open(sys.argv[1], "rb") as f:
        user_input = list(map(lambda x: x.decode("utf-8"), f))
else:
    user_input = hard_input

def canonicalize(xs):
    return tuple(sorted(xs, key=lambda x: ''.join(sorted(x))))

lines = set(canonicalize(frozenset(s) for s in line.split()) for line in user_input)

def print_line(line):
    print(' '.join(map(lambda x: ''.join(sorted(x)), line)))

def maximize(line):
    a, b = line
    for a2, b2 in lines:
        if a <= a2:
            b |= b2
        if a <= b2:
            b |= a2
        if b <= a2:
            a |= b2
        if b <= b2:
            a |= a2

    return a, b

while True:
    new_lines = lines.copy()
    def try_add(a, b):
        a_ = a[0] & b[0]
        if a_:
            line = (a_, a[1] | b[1])
            new_lines.add(canonicalize(maximize(line)))

    for a, b in combinations(lines, 2):
        try_add(a, b)
        try_add(b, a)
        try_add(a, (b[1], b[0]))
        try_add((a[1], a[0]), (b[1], b[0]))

    if len(new_lines) == len(lines):
        break
    lines = new_lines

for line in set(map(maximize, lines)):
    print_line(line)
