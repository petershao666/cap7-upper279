#!/usr/bin/env python3
"""Rediscover the 56 two-112-slice integer inequalities. Numerical proposals
are accepted only after every proposed inequality is checked with integers.
The geometry and representative checks remain in the parent proof/verifiers.
"""
import argparse
from engine import *
from fractions import Fraction
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('rediscovered_two112.json'))
args=parser.parse_args()
OUT=[]
for h in range(1,57):
 ts=[(u,p) for u in range(3) for p in range(0,21 if u==0 else 12) if p<=h and h-p<=45]
 X=np.array([[int(u==0),int(u==1),int(u==2),p,math.comb(p,2),math.comb(p,3),u*p,u*math.comb(p,2)] for u,p in ts],dtype=np.int64)
 rhs=np.array([252+h,112-2*h,h,121*h,40*math.comb(h,2),13*math.comb(h,3),22*h,4*math.comb(h,2)],dtype=np.int64)
 goal=np.array([int(16+4*u+3*p-h==0) for u,p in ts],dtype=np.int64)
 sc=np.maximum(np.max(abs(X),axis=0),1)
 lp=linprog(-goal,A_eq=(X/sc).T,b_eq=rhs/sc,bounds=(0,None),method='highs')
 if lp.success:
  rd=-lp.eqlin.marginals/sc
  for lim in [100,1000,10000,100000,1000000,10000000]:
   r=[Fraction(float(v)).limit_denominator(lim) for v in rd];L=math.lcm(*[t.denominator for t in r]);q=[int(v*L) for v in r]
   lower=[sum(int(a)*b for a,b in zip(row,q))-L*int(g) for row,g in zip(X,goal)]
   ub=sum(int(a)*b for a,b in zip(rhs,q));gap=15*L-ub
   if min(lower)>=0 and gap>0:break
  else:raise RuntimeError(('recover fail',h,rd))
  rec={'h':h,'q':q,'L':L,'upper':ub,'gap':gap}
 else:
  rec=separate(X,rhs,364)
  if not rec:raise RuntimeError(('Farkas fail',h))
  rec['h']=h;rec['infeasible']=True
 OUT.append(rec)
 print(h,rec,flush=True)
args.output.write_text(json.dumps(OUT,indent=2))
print('ALL 56 INTEGER CERTIFICATES PASS')
