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
all_permutations = set(chain(*(chain(*map(permutations, product(*line))) for line in passive)))
print("generated", len(all_permutations), "permutations")

delta = len(passive[0])

def allowed(n, s):
    return Bool("allowed_{}_{}".format(n, s))

def causes_trouble(i, sym):
    def var(j, sym2):
        return Bool("trouble_{}_{}_{}_{}".format(i, sym, j, sym2))

    must_allow = And([
        Or([Not(var(j, sym2)), allowed(j, sym2)])
        for j in range(delta) if i != j for sym2 in alphabet
    ])

    not_in_passives = And([
        Or([And([Not(var(j, sym2)) for sym2 in line[j]]) for j in range(delta) if i != j])
        for line in chain(*map(permutations, passive)) if sym in line[i]
    ])

    return And([
        must_allow, not_in_passives,
        *(Or([var(j, sym2) for sym2 in alphabet]) for j in range(delta) if i != j)
    ])

s = Solver()

# maximality – All added symbols lead to trouble
s.add(And([
    Or([allowed(i, sym), causes_trouble(i, sym)]) for sym in alphabet for i in range(delta)
]))
print("maximality done")

# disallow combos that aren't in the passive
s.add(And([
    Not(And([allowed(i, sym) for i, sym in enumerate(p)]))
    for p in product(*[alphabet] * delta) if p not in all_permutations
]))
print("being in passive done")

# must allow at least one symbol in each place
s.add(And([Or([allowed(i, sym) for sym in alphabet]) for i in range(delta)]))

sorted_alphabet = sorted(alphabet)

# enforce alphabetical order
def build_order(i, order):
    if order:
        return Or([
            And([allowed(i, order[0]), Not(allowed(i+1, order[0]))]),
            And([allowed(i, order[0]) == allowed(i+1, order[0]), build_order(i, order[1:])])
        ])
    else:
        return True

s.add(And([build_order(i, sorted_alphabet) for i in range(delta - 1)]))

print("starting search")

while s.check() == sat:
    m = s.model()

    print(' '.join(''.join(filter(lambda sym: m[allowed(i, sym)], sorted_alphabet)) for i in range(delta)))

    rule = Or([allowed(i, sym) != m[allowed(i, sym)] for i in range(delta) for sym in alphabet if m[allowed(i, sym)] != None])
    s.add(rule)
