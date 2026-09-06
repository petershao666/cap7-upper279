from pathlib import Path
import os;os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import sys,json,itertools,time
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from search_stage import en
import probe as p
from engine import separate,force
W=Path(__file__).resolve().parent/'outputs';W.mkdir(exist_ok=True)
def Q(t):return 9*p.old.e3(t)-911*p.old.e2(t)+16306924
alltypes=[(a,b,278-a-b) for a in range(113) for b in range(a+1) if 0<=278-a-b<=b]
c=json.load(open(W/'new_certificate.json'))
ex=[(112,112,29),(112,111,35)]+[p.old.parse_key(k) for st in c['stages'] for k in st]
keys=sorted([t for t in alltypes if Q(t)<0 and p.old.downwards_allowed(t,ex)],key=Q)
print('EXTREMAL TARGETS',keys,flush=True)
out={}
for key in keys:
 banned=ex+[t for t in alltypes if Q(t)<Q(key)]
 arr=en(key,banned);rec=separate(arr[:,:7],force(key),364)
 print('CASE',key,'rows',len(arr),'Q',Q(key),'CERT',rec,flush=True)
 if rec:out[','.join(map(str,key))]=rec
 else:
  elig=[j for j,N in enumerate(key) if 103<=N<109];br=[]
  for st in itertools.product((0,1),repeat=len(elig)):
   status=tuple(st[elig.index(j)] if j in elig else (1 if N>=109 else -1) for j,N in enumerate(key))
   rr,tot,exf=p.prepare(arr,key,status,True);rec=separate(rr,tot,364)
   print('BRANCH',key,status,len(rr),'CERT',rec,flush=True)
   if rec:br.append(dict(rec,status=status,extra_features=exf))
  out[','.join(map(str,key))]={'branches':br,'required':2**len(elig),'success':len(br)==2**len(elig)}
 (W/'extremal_certificate.json').write_text(json.dumps(out,indent=2))
print('DONE',flush=True)
