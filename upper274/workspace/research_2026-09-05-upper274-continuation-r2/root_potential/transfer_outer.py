"""Bounded outer certificate discovery using all puncturing transfers."""
import os,sys
sys.dont_write_bytecode=True
for n in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[n]='1'
from pathlib import Path
import json,time,signal,itertools,math
import numpy as np
P=Path(__file__).resolve().parent
R=P.parents[1]/'research_2026-09-05-capset-round1-r1/route_a'
sys.path.insert(0,str(R));import minimum as M
start=time.monotonic()
def timeout(*a):raise TimeoutError('P2 discovery batch deadline')
signal.signal(signal.SIGALRM,timeout);signal.alarm(1150)
tables=json.loads((P/'transfer_tables.json').read_text())['functions']
ordinary=list(map(tuple,json.loads((P/'arrangement.json').read_text())['ordinary_bans']))
targets=[(108,107,60),(108,106,61),(107,107,61),(107,106,62),(107,105,63)]
out={'status':'DISCOVERY_PENDING_EXACT_REPLAY','root_parameter':67,'ordinary_bans':ordinary,'targets':[],'source_tables':'transfer_tables.json','shared_kernel':str(R/'minimum.py')}
def save():
    out['seconds']=time.monotonic()-start
    (P/'transfer_outer.json').write_text(json.dumps(out,indent=2)+'\n')
for base in targets:
    ban=ordinary+[t for t in M.T if M.Q(t)<M.Q(base)]
    arr=M.en(base,ban)
    rows,tot,extra,pos=M.prepare(arr,base,(0,0,-1))
    keep=np.ones(len(arr),dtype=bool)
    for j in (0,1):
        for t in M.COMP:keep&=~np.all(arr[:,7+3*j:10+3*j]>=t,axis=1)
    arr=arr[keep]
    assert len(rows)==len(arr)
    # Any absent source-domain subprofile excludes that parent profile by the
    # puncturing lemma; retain explicit missing lists in the source tables.
    valid=np.ones(len(arr),dtype=bool)
    for j in (0,1):
        for h in tables:
            if h['m']!=base[j]:continue
            for miss in h['missing']:valid&=~np.all(arr[:,7+3*j:10+3*j]==miss['parent'],axis=1)
    rows=rows[valid];arr=arr[valid]
    for j in (0,1):
        for h in tables:
            if h['m']!=base[j]:continue
            phi=dict(zip(map(tuple,h['types']),h['phi']))
            look=np.zeros((46,46),np.int64)
            for t,v in phi.items():look[t[:2]]=v
            vv=look[arr[:,7+3*j],arr[:,8+3*j]]
            rows=np.c_[rows,vv];pos.append(len(tot));tot=np.r_[tot,h['bound']];extra.append((j,h['id']))
    print('MODEL',base,'rows',len(rows),'features',len(tot),'elapsed',time.monotonic()-start,flush=True)
    cert=M.sep(rows,tot,pos)
    result={'base':base,'state':[0,0,-1],'rows':len(rows),'extra_features':extra,'positive_features':pos,'totals':list(map(int,tot)),'certificate':cert,'status':'INTEGER_CANDIDATE_NEEDS_EXHAUSTIVE_REPLAY' if cert else 'NO_NEW_CERTIFICATE_NO_INFERENCE'}
    out['targets'].append(result);save()
    print('RESULT',base,json.dumps(result),'elapsed',time.monotonic()-start,flush=True)
    del rows,arr
out['status']='BOUNDED_DISCOVERY_COMPLETE';save()
