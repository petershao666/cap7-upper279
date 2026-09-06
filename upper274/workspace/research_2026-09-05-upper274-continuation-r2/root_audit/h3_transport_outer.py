"""New accepted H3 source transported through every puncturing in the gate."""
import os,sys
sys.dont_write_bytecode=True
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[k]='1'
from pathlib import Path
from math import comb,gcd
import json,time
W=Path(__file__).resolve().parent;R=W.parent
sys.path.insert(0,str(R.parent/'research_2026-09-05-capset-round1-r1/route_a'))
import minimum as M
np=M.np
source=json.loads((R/'hist105106/h3/h3_result.json').read_text())['histograms']['105']
sourcephi=dict(zip(map(tuple,source['types']),source['phi']))
funcs=[dict(id='H3_phi105',m=105,types=source['types'],phi=source['phi'],bound=source['bound'])]
for N in [106,107,108]:
 ts=[(a,b,N-a-b) for a in range(46) for b in range(a+1) if 0<=N-a-b<=b and M.V.downwards_allowed((a,b,N-a-b),M.OLD+M.COMP)]
 d=N-105;vals=[]
 for t in ts:
  value=0;count=0
  for a in range(d+1):
   for b in range(d-a+1):
    rem=(a,b,d-a-b)
    if any(x<y for x,y in zip(t,rem)):continue
    mult=comb(t[0],a)*comb(t[1],b)*comb(t[2],d-a-b)
    u=tuple(sorted((x-y for x,y in zip(t,rem)),reverse=True))
    assert u in sourcephi,'missing105source'
    count+=mult;value+=mult*sourcephi[u]
  assert count==comb(N,105);vals.append(value)
 bound=comb(N,105)*source['bound'];g=gcd(*vals,bound)
 funcs.append(dict(id='H3_phi105_to'+str(N),m=N,deleted=d,types=ts,phi=[v//g for v in vals],bound=bound//g,positive_gcd=g))
(W/'h3_transport_tables.json').write_text(json.dumps(dict(source_sha256='cbb4973544cf7e2388097bb333504dc0c53c943d1671605fa300996394dfd294',functions=funcs),indent=2)+'\n')
old=json.loads((R.parent/'research_2026-09-05-capset-round1-r1/route_a/certificates.json').read_text())
ban=M.SEEDS+[(112,109,51),(111,110,51)]+[M.V.parse_key(k) for st in old['stages'] for k in st]
previous=json.loads((R/'root_potential/transfer_tables.json').read_text())['functions']
extra=funcs+previous
out=[];start=time.monotonic()
for key in [(108,107,60),(108,106,61),(107,107,61),(107,106,62),(107,105,63),(106,106,63),(106,105,64)]:
 ar=M.en(key,ban+[t for t in M.T if M.Q(t)<M.Q(key)])
 # prepare preserves NC row order; reconstruct matching column profiles.
 mask=np.ones(len(ar),bool)
 for j in (0,1):
  for t in M.COMP:mask &= ~np.all(ar[:,7+3*j:10+3*j]>=t,axis=1)
 ar=ar[mask];rows,tot,extras,pos=M.prepare(ar,key,(0,0,-1));assert len(rows)==len(ar)
 for j in (0,1):
  for h in extra:
   if h['m']!=key[j]:continue
   phi=dict(zip(map(tuple,h['types']),h['phi']))
   vals=np.array([phi[tuple(t)] for t in ar[:,7+3*j:10+3*j]],np.int64)
   rows=np.c_[rows,vals];pos.append(len(tot));tot=np.r_[tot,h['bound']];extras.append((j,h['id']))
 rec=M.sep(rows,tot,pos)
 z=dict(key=key,state=[0,0,-1],count=len(rows),extras=extras,certificate=rec)
 out.append(z);print(key,len(rows),rec,'elapsed',time.monotonic()-start,flush=True)
 (W/'h3_transport_outer.json').write_text(json.dumps(dict(cases=out,claim='EXACT_CANDIDATES_REQUIRE_INDEPENDENT_REPLAY'),indent=2)+'\n')
