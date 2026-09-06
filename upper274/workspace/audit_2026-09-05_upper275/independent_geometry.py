"""Audit geometry using coordinate tuples; no imports from the certificate package."""
from pathlib import Path
from itertools import product,combinations
from collections import Counter
D=Path(__file__).resolve().parent
V=list(product(range(3),repeat=6));zero=(0,)*6
blocks={tuple(int(i)-1 for i in w) for w in ['123','124','135','146','156','236','245','256','345','346']}
S={v for v in V if (0 not in v and sum(x==2 for x in v)%2==0) or tuple(i for i,x in enumerate(v) if x)!=() and tuple(i for i,x in enumerate(v) if x) in blocks}
assert len(S)==112
add=lambda a,b:tuple((x+y)%3 for x,y in zip(a,b))
neg=lambda a:tuple(-x%3 for x in a)
dot=lambda a,b:sum(x*y for x,y in zip(a,b))%3
assert {neg(v) for v in S}==S and zero not in S
hits=Counter(neg(add(a,b)) for a,b in combinations(S,2))
assert not S.intersection(hits)
assert Counter(hits[v] for v in V if v not in S)=={10:616,56:1}
P=[v for v in V if next((x for x in v if x),0)==1]
assert len(P)==364
spec=Counter();dual=set();incsmall=Counter();inclarge=Counter()
for v in P:
    counts=Counter(dot(v,x) for x in S);t=tuple(counts[i] for i in range(3));spec[tuple(sorted(t,reverse=True))]+=1
    assert t in ((22,45,45),(40,36,36))
    if t[0]==22:dual.update((v,neg(v)))
    for x in S:
        if dot(v,x)==0:
            (incsmall if t[0]==22 else inclarge)[x]+=1
assert spec=={(45,45,22):56,(40,36,36):308}
assert set(incsmall.values())=={11} and set(inclarge.values())=={110}
assert len(dual)==112
assert all(neg(add(a,b)) not in dual for a,b in combinations(dual,2))
for x in V[1:]:
    counts=Counter(dot(x,v) for v in dual)
    assert counts[1]==counts[2] and counts[0]-counts[1]==4-27*(x in S)
hyper=[{x for x in S if dot(v,x)==0} for v in P if v in dual]
assert len(hyper)==56
assert all(len(a&b)==4 for a,b in combinations(hyper,2))
print('INDEPENDENT GEOMETRY PASS: 112-cap; all exterior secants; 364 directions; two Fourier identities; 1540 pair incidences; deletion incidences 11 and 110.')
points=[tuple(map(int,line.strip())) for line in (D/'cap7_upper275/baseline277/baseline278/cap236.txt').read_text().splitlines() if line.strip() and not line.startswith('#')]
assert len(set(points))==len(points)==236 and all(len(v)==7 and set(v)<=set(range(3)) for v in points)
points=set(points)
assert all(neg(add(a,b)) not in points for a,b in combinations(points,2))
print('INDEPENDENT LOWER BOUND PASS: 236 points, all 27730 pairs.')
