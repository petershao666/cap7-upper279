"""Bounded inner comparison; only exact recovered majorants prove redundancy."""
import os,sys
sys.dont_write_bytecode=True
for n in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[n]='1'
from pathlib import Path
from math import comb
from fractions import Fraction as F
import json,itertools,numpy as np
from scipy.optimize import linprog
P=Path(__file__).resolve().parent
R=P.parents[1]/'research_2026-09-05-capset-round1-r1/route_a'
sys.path.insert(0,str(R));import minimum as M
hh=json.loads((P/'transfer_tables.json').read_text())['functions']
results=[]
def rational_solve(columns,target):
    n=len(columns);a=[[F(columns[j][i]) for j in range(n)]+[F(target[i])] for i in range(len(target))]
    pivot=[];r=0
    for c in range(n):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None:continue
        a[p],a[r]=a[r],a[p];v=a[r][c];a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]:
                v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        pivot.append((r,c));r+=1
    if r!=n or any(all(x==0 for x in row[:n]) and row[n] for row in a):return None
    out=[F(0)]*n
    for r,c in pivot:out[c]=a[r][-1]
    return out
def e2(t):return sum(a*b for a,b in itertools.combinations(t,2))
def e3(t):a,b,c=t;return a*b*c
for h in hh:
    N=h['m'];types=list(map(tuple,h['types']));direct=[g for g in M.H if g['m']==N]
    funcs=[dict(zip(map(tuple,g['types']),g['phi'])) for g in direct]
    features=[[e2(t),e3(t)]+[f[t] for f in funcs] for t in types]
    totals=[243*comb(N,2),81*comb(N,3)]+[g['bound'] for g in direct]
    A=np.c_[np.ones(len(types)),np.array(features,dtype=float)]
    scale=np.maximum(np.max(abs(A),axis=0),1)
    fscale=max(1,max(map(abs,h['phi'])))
    lp=linprog(np.r_[364,np.array(totals,dtype=float)]/scale/364,A_ub=-A/scale,b_ub=-np.array(h['phi'],dtype=float)/fscale,bounds=[(None,None)]*3+[(0,None)]*len(direct),method='highs',options={'threads':1,'time_limit':120})
    rec={'id':h['id'],'direct_ids':[g['id'] for g in direct],'status':'NO_EXACT_REDUNDANCY_CERTIFICATE','float_status':int(lp.status)}
    if lp.success:
        real=lp.x/scale*fscale
        rec['float_best_bound']=float(lp.fun*364*fscale)
        rec['target_bound']=h['bound']
        for denom in [10**3,10**6,10**9,10**12]:
            coef=[F(float(v)).limit_denominator(denom) for v in real[1:]]
            if any(v<0 for v in coef[2:]):continue
            intercept=max(F(y)-sum(a*b for a,b in zip(coef,x)) for y,x in zip(h['phi'],features))
            bound=364*intercept+sum(a*b for a,b in zip(coef,totals))
            if bound<=h['bound']:
                rec.update(status='EXACT_OLD_MODEL_DOMINATES',coefficients=[str(intercept)]+list(map(str,coef)),exact_upper=str(bound),exact_margin=str(F(h['bound'])-bound));break
        if rec['status']=='NO_EXACT_REDUNDANCY_CERTIFICATE':
            # A finite exact witness can show nonredundancy in the OLD relaxed
            # histogram model, never geometric realizability.
            z=np.array(features,dtype=float);mean=np.array(totals,dtype=float)/364
            sc=np.maximum(np.max(abs(z),axis=0),1)
            pl=linprog(-np.array(h['phi'],dtype=float)/fscale,A_eq=np.r_[np.ones((1,len(types))),(z[:,:2]/sc[:2]).T],b_eq=np.r_[1,mean[:2]/sc[:2]],A_ub=(z[:,2:]/sc[2:]).T,b_ub=mean[2:]/sc[2:],bounds=(0,None),method='highs',options={'threads':1,'time_limit':120})
            if pl.success:
                selected=[int(i) for i in np.where(pl.x>1e-9)[0]]
                active=[j for j in range(2,len(totals)) if abs((z[:,j]@pl.x-mean[j])/sc[j])<1e-9]
                fields=[0,1]+active
                cols=[[1]+[features[i][j] for j in fields] for i in selected]
                lam=rational_solve(cols,[F(1)]+[F(totals[j],364) for j in fields])
                if lam and min(lam)>=0:
                    sums=[sum(w*features[i][j] for w,i in zip(lam,selected)) for j in range(len(totals))]
                    value=sum(w*h['phi'][i] for w,i in zip(lam,selected))
                    if all(sums[j]==F(totals[j],364) for j in [0,1]) and all(sums[j]<=F(totals[j],364) for j in range(2,len(totals))) and value>F(h['bound'],364):
                        rec.update(status='EXACT_NONREDUNDANCY_IN_OLD_HISTOGRAM_RELAXATION',witness=[{'profile':types[i],'weight':str(w)} for w,i in zip(lam,selected)],old_feature_sums=list(map(str,sums)),new_feature_sum=str(value),violation_after364=str(364*value-h['bound']))
    results.append(rec);print(json.dumps(rec),flush=True)
(P/'transfer_redundancy.json').write_text(json.dumps(results,indent=2)+'\n')
