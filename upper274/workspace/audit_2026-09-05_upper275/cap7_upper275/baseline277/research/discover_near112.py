from pathlib import Path
W=Path(__file__).resolve().parent/"outputs";W.mkdir(exist_ok=True)
import os;os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,json,math,numpy as np
from fractions import Fraction
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'baseline278/research'))
from engine import separate
OUT=[]
for h in range(1,52):
 ts=[(u,p) for u in range(3) for p in range(21 if u==0 else 12) if p<=h and h-p<=45 and 16+4*u+3*p-h>=0]
 X=np.array([[int(u==0),int(u==1),int(u==2),p,math.comb(p,2),math.comb(p,3),u*p,u*math.comb(p,2)] for u,p in ts],np.int64)
 rhs=np.array([252+h,112-2*h,h,121*h,40*math.comb(h,2),13*math.comb(h,3),22*h,4*math.comb(h,2)],np.int64)
 goal=np.array([int(16+4*u+3*p-h<=1) for u,p in ts],np.int64)
 sc=np.maximum(np.max(abs(X),axis=0),1)
 lp=linprog(-goal,A_eq=(X/sc).T,b_eq=rhs/sc,bounds=(0,None),method='highs')
 if lp.success:
  rd=-lp.eqlin.marginals/sc
  rec=None
  for lim in [10,100,1000,10000,100000,1000000,10000000]:
   r=[Fraction(float(v)).limit_denominator(lim) for v in rd];L=math.lcm(*[t.denominator for t in r]);q=[int(v*L) for v in r]
   lower=[sum(int(a)*b for a,b in zip(row,q))-L*int(g) for row,g in zip(X,goal)]
   ub=sum(int(a)*b for a,b in zip(rhs,q));gap=18*L-ub
   if min(lower)>=0 and gap>0:
    rec={'h':h,'q':q,'L':L,'upper':ub,'gap':gap};break
  if rec is None:raise ValueError(('recovery',h))
 else:
  rec=separate(X,rhs,364)
  if not rec:raise ValueError(('farkas',h))
  rec['h']=h;rec['infeasible']=True
 OUT.append(rec);print(h,rec,flush=True)
open(W/'near112_certificate.json','w').write(json.dumps(OUT,indent=2))
print('EXACT candidate: 112 and111 layers leave at most34 third-slice positions.')
