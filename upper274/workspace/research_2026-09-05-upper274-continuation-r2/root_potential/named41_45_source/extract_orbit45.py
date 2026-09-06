"""Finite orbit of two published affine formulas; no foreign code is executed."""
from collections import Counter, deque
import hashlib
import itertools
import json
from pathlib import Path

here=Path(__file__).resolve().parent
space=list(itertools.product(range(3),repeat=5))
def T(x):
    a,b,c,d,e=x
    return ((a-b+1)%3,(b+1)%3,e,c,d)
def R(x):
    a,b,c,d,e=x
    return ((-a)%3,c,(-b)%3,(d+e)%3,(-d+e)%3)
maps={'T':T,'R':R}
for f in maps.values():
    assert len({f(p) for p in space})==243
origin=(0,0,0,0,0)
parent={origin:None}
queue=deque([origin])
while queue:
    p=queue.popleft()
    for name,f in maps.items():
        q=f(p)
        if q not in parent:
            parent[q]=(p,name)
            queue.append(q)
    assert len(parent)<=243
cap=sorted(parent)
assert len(cap)==45
lookup=set(cap)
assert all(f(p) in lookup for f in maps.values() for p in cap)
checks=0
for a,b in itertools.combinations(cap,2):
    assert tuple((-x-y)%3 for x,y in zip(a,b)) not in lookup
    checks+=1
assert checks==990
raw=Counter()
for d in space[1:]:
    counts=Counter(sum(x*y for x,y in zip(d,p))%3 for p in cap)
    raw[tuple(sorted((counts[i] for i in range(3)),reverse=True))]+=1
assert all(n%2==0 for n in raw.values())
hist={t:n//2 for t,n in raw.items()}
assert hist=={(18,18,9):55,(15,15,15):66}
witnesses=[]
for p in cap:
    item={'point':p}
    if parent[p] is None:
        item['root']=True
    else:
        before,name=parent[p]
        item.update(parent=before,generator=name)
        assert maps[name](before)==p
    witnesses.append(item)
out={
    'status':'PUBLISHED45_ORBIT_EXTRACTED_AND_EXACTLY_CHECKED',
    'source':'Thackeray arXiv:2206.09719v1, Remark after Theorem 4.3, printed page 12',
    'source_tex_sha256':hashlib.sha256((here/'CapSetProblem5S41.tex').read_bytes()).hexdigest(),
    'coordinate_order':['x1','x2','x3','x4','x5'],
    'residues':[0,1,2],
    'encoding':'i=x1+3*x2+9*x3+27*x4+81*x5; point array lexicographic in coordinates',
    'generators':{'T':'(x1-x2+1,x2+1,x5,x3,x4) mod 3','R':'(-x1,x3,-x2,x4+x5,-x4+x5) mod 3'},
    'ambient_points':243,
    'orbit_size':len(cap),
    'pair_checks':checks,
    'nonzero_normal_evaluations':242,
    'histogram':[{'type':t,'count':n} for t,n in sorted(hist.items())],
    'points':cap,
    'point_indices':[sum(x*3**k for k,x in enumerate(p)) for p in cap],
    'orbit_parent_witnesses':witnesses,
    'diagram_coordinate_identity_assumed':False,
    'canonical_by':'Exact cap check plus accepted affine uniqueness of all 45-caps',
    'publication_novelty_claim':False,
    'four_deletion_enumeration_run':False,
}
(here/'ORBIT45_POINTS.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: orbit 45, pairs 990, directions 121, spectrum 18189:55 / 151515:66')
print('SHA256',hashlib.sha256((here/'ORBIT45_POINTS.json').read_bytes()).hexdigest())
