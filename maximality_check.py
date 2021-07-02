from z3 import *
from itertools import *

hard_input = [
    "ACDFGIJKLNOP MNOP",
    "GKLP BCDHIJKLMNOP",
    "DJLO EFGHIJKLMNOP",
]

sample_input = [
    "M UP UP UP",
    "U U U U"
]

den_input = ["ABCD ABCD ABCD ABCD ABCD"]

if len(sys.argv) == 2:
    with open(sys.argv[1], "rb") as f:
        user_input = list(map(lambda x: x.decode("utf-8"), f))
else:
    user_input = hard_input

passive = [line.split() for line in user_input]
alphabet = sorted(set(chain(*chain(*passive))))
degree = len(passive[0])

print("generating perms")
all_permutations = set(chain(*(chain(*map(permutations, product(*line))) for line in passive)))
print("generated", len(all_permutations), "permutations")
all_bad = tuple(set(product(*[alphabet] * degree)) - all_permutations)
print("generated", len(all_bad), "forbidden ones")

def sym_at(sym, pos):
    return Bool("{}{}".format(sym, pos))

def not_dominated_by(line):
    syms = set(sym_at(sym, i) for i, s in enumerate(line) for sym in s)
    syms_inv = [sym_at(sym, i) for sym in alphabet for i in range(degree) if sym_at(sym, i) not in syms]
    return And([
        Or(syms_inv),
    ])

solver = Solver()

solver.add(And([not_dominated_by(line) for line_orig in passive for line in permutations(line_orig)]))

solver.add(And([Or([sym_at(s, i) for s in alphabet]) for i in range(degree)]))

# disallow combos that aren't in the passive
solver.add(Not(Or([
    And(tuple(sym_at(sym, i) for i, sym in enumerate(p)))
    for p in all_bad
])))

if solver.check() == sat:
    m = solver.model()

    print(' '.join(''.join(filter(lambda sym: m[sym_at(sym, i)], alphabet)) for i in range(degree)))
else:
    print("maximal!")
