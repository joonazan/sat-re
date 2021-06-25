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

def print_syms(x):
    print(' '.join(map(lambda x: ''.join(sorted(set(alphabet) - set(x))), x)))

def can(fs):
    return tuple(sorted(map(lambda x: tuple(sorted(x)), fs)))

visited = {}
candidates = []
forbidden_syms = [set() for _ in range(delta)]

def rec():
    visited[can(forbidden_syms)] = 1

    if s.check() != sat:
        candidates.append(can(forbidden_syms))
    else:
        visited_by_me = set()
        for i in range(delta):
            if len(forbidden_syms[i]) + 1 == len(alphabet):
                continue
            for sym in alphabet - forbidden_syms[i]:
                forbidden_syms[i].add(sym)
                key = can(forbidden_syms)
                if key not in visited:
                    s.push()
                    s.add(Not(choice(i, sym)))
                    rec()
                    s.pop()
                elif key not in visited_by_me:
                    visited[key] += 1
                visited_by_me.add(key)
                forbidden_syms[i].remove(sym)

rec()
visited[can(forbidden_syms)] = 0

for c in candidates:
    parents = set()
    c2 = list(c)
    for i in range(delta):
        if not c[i]:
            continue
        for syms in combinations(c[i], len(c[i]) - 1):
            c2[i] = syms
            parents.add(can(c2))
        c2[i] = c[i]

    if len(parents) == visited[can(c)]:
        print_syms(c)
