"""Exact puncturing-transfer tables from audited histogram functions."""
import sys,os
sys.dont_write_bytecode=True
for n in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[n]='1'
from pathlib import Path
from math import comb,gcd
import json,itertools
P=Path(__file__).resolve().parent
R=P.parents[1]/'research_2026-09-05-capset-round1-r1/route_a'
sys.path.insert(0,str(R));import minimum as M
def nc(t):return M.ADM[t] and not any(all(x>=y for x,y in zip(t,u)) for u in M.COMP)
out=[]
for N in [107,108]:
    tt=[(a,b,N-a-b) for a in range(46) for b in range(a+1) if 0<=N-a-b<=b and nc((a,b,N-a-b))]
    for h in M.H:
        m=h['m']
        if not (m in [106,107] and m<N):continue
        phi=dict(zip(map(tuple,h['types']),h['phi']))
        d=N-m;values=[];valid=[];missing=[]
        for t in tt:
            acc=0;absent=[];multsum=0
            for r0 in range(d+1):
                for r1 in range(d-r0+1):
                    r=(r0,r1,d-r0-r1)
                    if any(a<b for a,b in zip(t,r)):continue
                    u=tuple(sorted([a-b for a,b in zip(t,r)],reverse=True))
                    mult=comb(t[0],r[0])*comb(t[1],r[1])*comb(t[2],r[2]);multsum+=mult
                    if u not in phi:absent.append(u)
                    else:acc+=mult*phi[u]
            assert multsum==comb(N,d)
            if absent:missing.append({'parent':t,'missing_subprofiles':sorted(set(absent))})
            else:valid.append(t);values.append(acc)
        bound=comb(N,m)*h['bound'];factor=gcd(*values,bound)
        out.append({'id':h['id']+'_to'+str(N),'source_id':h['id'],'source_dimension':6,'source_m':m,'m':N,'deleted':d,'all_parent_types':tt,'types':valid,'phi':[v//factor for v in values],'bound':bound//factor,'positive_gcd':factor,'missing':missing,'source_bound':h['bound'],'source_types':h['types'],'source_phi':h['phi'],'derivation':'sum over every M-subset; all M-subcaps non-completable by103-extension rigidity'})
        print(out[-1]['id'],'types',len(tt),'missing',len(missing),'gcd',factor,'bound',bound//factor,flush=True)
(P/'transfer_tables.json').write_text(json.dumps({'status':'EXACT_DERIVED_TABLES_ROOT_AUDIT_PENDING','functions':out},indent=2)+'\n')
