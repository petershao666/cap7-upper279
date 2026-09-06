import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,math,itertools,time,signal
from pathlib import Path
import numpy as np
W=Path(__file__).resolve().parent
B=W.parents[1]/'audit_2026-09-05_upper275/cap7_upper275'
sys.path.insert(0,str(B/'baseline277/baseline278/research'))
import engine as E
V=E.old
C=json.loads((B/'baseline277/baseline278/certificate.json').read_text())
P=json.loads((B/'results/size276/proof.json').read_text())
OLD=[V.parse_key(k) for st in C['six_stages'] for k in st]
COMP=[tuple(t) for t in C['completion_seeds']]+[V.parse_key(k) for st in C['completion_stages'] for k in st]
def sub(t):a,b,c=sorted(t,reverse=True);return c<=22 or (a<=40 and b<=36)
F6=OLD+[t for t in COMP if not sub(t)]
SEEDS=[(112,112,29),(112,111,35),(112,110,45),(111,111,45)]
T=[(a,b,275-a-b) for a in range(113) for b in range(a+1) if 0<=275-a-b<=b]
def Q(t):return 9*V.e3(t)-899*V.e2(t)+15730000
def save(x,name): (W/name).write_text(json.dumps(x,indent=2))
def limit(signum,frame):raise TimeoutError('bounded discovery wall limit')
signal.signal(signal.SIGALRM,limit)
ADM=E.make_adm(6,np.array(F6,dtype=np.int64).reshape(-1,3))
def enum(key,ban):
 top=E.make_top(112,275,np.array(ban,dtype=np.int64).reshape(-1,3))
 return E.enumerate_features(*key,ADM,top)
def separate(rows,tot):return E.separate(rows,tot,364)
def main():
 signal.alarm(570)
 st=time.monotonic();out={'size':275,'k':67,'root_sum':-246950,'seeds':SEEDS,'stages':[],'extremal':{},'shared_kernel':str(B/'baseline277/baseline278/research/engine.py')}
 ban=SEEDS[:]
 for stage_no in range(2):
  snap=ban[:];stage={}
  keys=sorted([t for t in T if Q(t)<0 and V.downwards_allowed(t,ban)],key=lambda t:(t[2],-t[0]))
  for key in keys:
   arr=enum(key,snap);rec=separate(arr[:,:7],E.force(key))
   print('ORDINARY',stage_no,key,len(arr),rec,'elapsed',round(time.monotonic()-st,2),flush=True)
   if rec:stage[','.join(map(str,key))]=dict(rec,discovery_count=len(arr))
   out['pending_stage']=stage;save(out,'certificates.json')
  out['stages'].append(stage);out.pop('pending_stage',None);ban.extend(V.parse_key(k) for k in stage);save(out,'certificates.json')
  if not stage:break
 out['remaining_negative']=[t for t in T if Q(t)<0 and V.downwards_allowed(t,ban)]
 save(out,'certificates.json');print('DONE',out['remaining_negative'],flush=True)
if __name__=='__main__':main()
