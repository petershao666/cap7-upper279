import os,sys
sys.dont_write_bytecode=True
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import json,time,signal
W=Path(__file__).resolve().parent;R=W.parent
sys.path.insert(0,str(R.parent/'research_2026-09-05-capset-round1-r1/route_a'))
import minimum as M
np=M.np
read=lambda p:json.loads(p.read_text())
old=read(R.parent/'research_2026-09-05-capset-round1-r1/route_a/certificates.json')
ban=M.SEEDS+[(112,109,51),(111,110,51)]+[M.V.parse_key(k) for st in old['stages'] for k in st]
new=read(W/'incidence_histograms_independent.json')['functions'];new=[h for h in new if h['m']==107 and not h['id'].endswith('10710761_j0')]
extra=read(W/'h3_transport_tables.json')['functions']+new
out=[];start=time.monotonic();signal.alarm(295)
for key in [(107,106,62),(107,105,63)]:
 ar=M.en(key,ban+[t for t in M.T if M.Q(t)<M.Q(key)])
 mask=np.ones(len(ar),bool)
 for j in (0,1):
  for t in M.COMP:mask &= ~np.all(ar[:,7+3*j:10+3*j]>=t,axis=1)
 ar=ar[mask];rows,tot,extras,pos=M.prepare(ar,key,(0,0,-1));assert len(rows)==len(ar)
 for j in (0,1):
  for h in extra:
   if h['m']!=key[j]:continue
   look=np.zeros((46,46),np.int64)
   for t,v in zip(h['types'],h['phi']):look[t[0],t[1]]=v
   tt=ar[:,7+3*j:10+3*j];vals=look[tt[:,0],tt[:,1]]
   rows=np.c_[rows,vals];pos.append(len(tot));tot=np.r_[tot,h['bound']];extras.append((j,h['id']))
 rec=M.sep(rows,tot,pos)
 z=dict(key=key,state=[0,0,-1],count=len(rows),extras=extras,certificate=rec)
 out.append(z);print(key,len(rows),rec,'elapsed',time.monotonic()-start,flush=True)
 (W/'incidence_hist_outer.json').write_text(json.dumps(dict(cases=out,claim='EXACT_CANDIDATES_REQUIRE_INDEPENDENT_REPLAY'),indent=2)+'\n')
