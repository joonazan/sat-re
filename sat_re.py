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
alphabet = set(chain(*chain(*passive)))

print("generating perms")
all_permutations = list(set(chain(*(chain(*map(permutations, product(*line))) for line in passive))))
print("generated", len(all_permutations), "permutations")

delta = len(all_permutations[0])

def choice(n, s):
    return Bool("choice_{}_{}".format(n, s))

def exactly_one(xs):
    return And([
        Or(xs),
        And([Not(And([a, b])) for i, a in enumerate(xs) for b in xs[:i]])
    ])

s = Solver()
s.add(And([exactly_one([choice(i, s) for s in alphabet]) for i in range(delta)]))
print("only one done")

# choice must be bad
s.add(And([
    Not(And([choice(i, sym) for i, sym in enumerate(p)])) for p in all_permutations
]))
print("choice must be bad done")

def is_allowed(forbidden_syms):
    s.push()
    for i, syms in enumerate(forbidden_syms):
        s.add(And([Not(choice(i, sym)) for sym in syms]))

    res = False if s.check() == sat else True
    s.pop()
    return res

def one_less(xs):
    return combinations(xs, len(xs) - 1)

stack = []
stack.extend(filter(is_allowed, combinations_with_replacement(one_less(alphabet), delta)))
visited = set()
mem = {}

while stack:
    orig = stack.pop()
    if orig in visited:
        continue
    visited.add(orig)

    forbidden_syms = list(orig)

    maximal = True
    for i in range(delta):
        if not forbidden_syms[i]:
            continue

        for x in one_less(forbidden_syms[i]):
            forbidden_syms[i] = x
            canonical = tuple(sorted(forbidden_syms))
            if canonical not in mem:
                mem[canonical] = is_allowed(canonical)

            if mem[canonical]:
                stack.append(canonical)
                maximal = False
        forbidden_syms[i] = orig[i]

    if maximal:
        print(' '.join(map(
            lambda x: ''.join(sorted(set(alphabet) - set(x))),
            forbidden_syms
        )))
