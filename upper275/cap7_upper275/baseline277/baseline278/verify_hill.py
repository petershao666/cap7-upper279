#!/usr/bin/env python3
"""Exact check for the lemma: two parallel 112-point slices leave at most
28 possible points in the third slice. See HILL_PROOF.md for the reduction.
Uses only Python's standard library. Published input: uniqueness of the
112-cap in F_3^6. The 56 finite inequalities are checked, not assumed.
"""
from itertools import product,combinations
from collections import Counter
from math import comb
from pathlib import Path
import json

def require(ok,msg):
 if not ok:raise AssertionError(msg)
def dot(a,b):return sum(x*y for x,y in zip(a,b))%3
def neg(a):return tuple((-x)%3 for x in a)
def projective(v):return next((a for a in v if a),0)==1
def capcheck(S):
 ss=set(S);require(len(ss)==len(S),'duplicates')
 for a,b in combinations(S,2):require(tuple((-x-y)%3 for x,y in zip(a,b)) not in ss,'not a cap')

def representative_checks():
 space=list(product(range(3),repeat=6));zero=(0,)*6
 blocks={frozenset(int(x)-1 for x in word) for word in ('123','124','135','146','156','236','245','256','345','346')}
 S=[v for v in space if (all(v) and v.count(2)%2==0) or frozenset(i for i,x in enumerate(v) if x) in blocks]
 require(len(S)==112 and zero not in S and set(map(neg,S))==set(S),'representative')
 capcheck(S)
 D=[]
 for w in space[1:]:
  h=Counter(dot(w,v) for v in S)
  require(h[1]==h[2],'central symmetry projections')
  require((h[0],h[1],h[2]) in ((22,45,45),(40,36,36)),'Fourier levels')
  if h[0]-h[1]==-23:D.append(w)
 require(len(D)==112 and set(map(neg,D))==set(D),'dual size or symmetry')
 capcheck(D)
 pd=[v for v in D if projective(v)]
 require(len(pd)==56,'dual projective size')
 hyperplanes={w:{v for v in S if dot(w,v)==0} for w in pd}
 for a,b in combinations(pd,2):
  require(len(hyperplanes[a]&hyperplanes[b])==4,'pair incidence is not four')
 ss=set(S)
 for x in space[1:]:
  h=Counter(dot(x,v) for v in D)
  require(h[1]==h[2] and h[0]-h[1]==4-27*int(x in ss),'dual Fourier formula')
 print('Hill representative: S and D are central 112-caps; both Fourier formulas and all 1540 pair incidences verified.',flush=True)

def row(h,u,p):return (int(u==0),int(u==1),int(u==2),p,comb(p,2),comb(p,3),u*p,u*comb(p,2))
def rhs(h):return (252+h,112-2*h,h,121*h,40*comb(h,2),13*comb(h,3),22*h,4*comb(h,2))
def inequality_checks(path=None):
 if path is None:path=Path(__file__).with_name('hill_certificate.json')
 recs=json.loads(Path(path).read_text());require([r['h'] for r in recs]==list(range(1,57)),'incomplete h list')
 checked=0
 for r in recs:
  h=r['h'];states=[(u,p) for u in range(3) for p in range(21 if u==0 else 12) if p<=h and h-p<=45]
  if r.get('infeasible',False):
   q=r['coeff'];K=r['K'];require(len(q)==8 and all(type(v)is int for v in q+[K]),'noninteger certificate')
   require(all(sum(a*b for a,b in zip(q,row(h,u,p)))>=K for u,p in states),'h exclusion local failure')
   F=sum(a*b for a,b in zip(q,rhs(h)));gap=364*K-F
   require(F==r['forced'] and gap==r['gap'] and gap>0,'h exclusion gap')
   print(f'h={h}: intersection impossible, gap={gap}.',flush=True)
  else:
   q=r['q'];L=r['L'];require(len(q)==8 and all(type(v)is int for v in q+[L]) and L>0,'invalid zero-count certificate')
   for u,p in states:
    g=int(16+4*u+3*p-h==0)
    require(sum(a*b for a,b in zip(q,row(h,u,p)))>=L*g,'zero-count local failure')
   F=sum(a*b for a,b in zip(q,rhs(h)));gap=15*L-F
   require(F==r['upper'] and gap==r['gap'] and gap>0,'zero-count gap')
   print(f'h={h}: zero directions <= {F}/{L} < 15, exact gap={gap}.',flush=True)
  checked+=len(states)
 print(f'HILL LEMMA PASS: 56 cases and {checked} integer state inequalities; at most 28 zero-convolution points (h=0 gives one).',flush=True)
 return checked
if __name__=='__main__':representative_checks();inequality_checks()
