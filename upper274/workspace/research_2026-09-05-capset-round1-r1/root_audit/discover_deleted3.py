"""Discover exact dual bounds; no imported certificate or predecessor kernel."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import json, math, time
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
W=Path(__file__).resolve().parent
start=time.monotonic()
out=[]
for h in range(1,52):
    assert time.monotonic()-start<180
    states=[(u,p) for u in range(3) for p in range(21 if u==0 else 12)
            if p<=h and h-p<=45 and 16+4*u+3*p-h>=0]
    X=[[int(u==j) for j in range(3)]+[p,math.comb(p,2),math.comb(p,3),u*p,u*math.comb(p,2)] for u,p in states]
    R=[252+h,112-2*h,h,121*h,40*math.comb(h,2),13*math.comb(h,3),22*h,4*math.comb(h,2)]
    goal=[int(16+4*u+3*p-h<=3) for u,p in states]
    # Feasible dual: sum q X >= goal. This directly returns a bound, or
    # the primal infeasibility branch below searches a constant certificate.
    xx=np.array(X,dtype=float); rr=np.array(R,dtype=float)
    scale=np.maximum(np.max(abs(xx),axis=0),1)
    lp=linprog(-np.array(goal),A_eq=(xx/scale).T,b_eq=rr/scale,bounds=(0,None),method='highs',options={'time_limit':10})
    record={'h':h,'state_count':len(X),'solver_status':int(lp.status)}
    if lp.success:
        approx=-lp.eqlin.marginals/scale
        for denominator in [10,100,1000,10000,100000,1000000]:
            fq=[Fraction(float(q)).limit_denominator(denominator) for q in approx]
            L=math.lcm(*(q.denominator for q in fq)); q=[int(v*L) for v in fq]
            deficits=[L*g-sum(a*b for a,b in zip(row,q)) for row,g in zip(X,goal)]
            # Exact constant repair maintains the three indicator columns.
            repair=max(0,max(deficits)); q=[x+repair if i<3 else x for i,x in enumerate(q)]
            upper=sum(a*b for a,b in zip(q,R))
            if Fraction(upper,L)<Fraction(str(-lp.fun))+Fraction(1,1000):
                record.update(kind='count',q=q,L=L,upper=upper,bound_floor=upper//L,
                              minimum_slack=min(sum(a*b for a,b in zip(row,q))-L*g for row,g in zip(X,goal)))
                break
        else: record.update(kind='unrecovered')
    elif lp.status==2:
        # Bounded dual separator qX >= 0, qR < 0. Exact check decides validity.
        sep=linprog(rr/scale,A_ub=-xx/scale,b_ub=np.zeros(len(X)),bounds=[(-1,1)]*8,method='highs',options={'time_limit':10})
        if sep.success:
            for denominator in [10,100,1000,10000,100000,1000000]:
                fq=[Fraction(float(v)).limit_denominator(denominator) for v in sep.x/scale]
                L=math.lcm(*(q.denominator for q in fq)); q=[int(v*L) for v in fq]
                repair=max(0,-min(sum(a*b for a,b in zip(row,q)) for row in X))
                q=[x+repair if i<3 else x for i,x in enumerate(q)]
                upper=sum(a*b for a,b in zip(q,R))
                if upper<0:
                    record.update(kind='impossible',q=q,upper=upper,minimum_slack=min(sum(a*b for a,b in zip(row,q)) for row in X)); break
            else: record.update(kind='unrecovered')
        else:record.update(kind='unrecovered')
    else:record.update(kind='unrecovered')
    out.append(record)
    print(h,record.get('kind'),record.get('bound_floor'),record.get('upper'),flush=True)
(W/'deleted3_certificate.json').write_text(json.dumps({'threshold':3,'records':out},indent=2)+'\n')
print('maximum projective count bound',max(r['bound_floor'] for r in out if r['kind']=='count'))
print('elapsed',time.monotonic()-start)
