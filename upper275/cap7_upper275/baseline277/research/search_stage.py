import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import sys,json,math,time,itertools
from pathlib import Path
import numpy as np
from numba import njit
sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe as p
from engine import make_adm,make_top,sorted3,e2,separate,root,force
W=Path(__file__).resolve().parent/'outputs';W.mkdir(exist_ok=True);CACHE=W/'cache';CACHE.mkdir(exist_ok=True)
@njit(cache=True)
def fast_enum(A,B,C,adm,top):
 U=adm.shape[0]-1
 aa=[];bb=[];cc=[]
 for a in range(U+1):
  for b in range(U+1):
   c=A-a-b
   if 0<=c<=b<=a and adm[a,b,c]:aa.append((a,b,c))
   c=B-a-b
   if 0<=c<=U and adm[a,b,c] and (a,b,c)>=(b,c,a) and (a,b,c)>=(c,a,b):bb.append((a,b,c))
   c=C-a-b
   if 0<=c<=U and adm[a,b,c]:cc.append((a,b,c))
 rows=[]
 for a0,a1,a2 in aa:
  ea=e2(a0,a1,a2);pa=a0*a1*a2
  for b0,b1,b2 in bb:
   eb=e2(b0,b1,b2);pb=b0*b1*b2
   bs=sorted3(b0,b1,b2)
   w0=a0*b0+a1*b2+a2*b1;w1=a0*b2+a1*b1+a2*b0;w2=a0*b1+a1*b0+a2*b2
   for c0,c1,c2 in cc:
    if not(adm[a0,b0,c0] and adm[a1,b2,c0] and adm[a2,b1,c0] and adm[a0,b2,c1] and adm[a1,b1,c1] and adm[a2,b0,c1] and adm[a0,b1,c2] and adm[a1,b0,c2] and adm[a2,b2,c2]):continue
    x=a0+b0+c0;y=a1+b1+c1
    if x>=top.shape[0] or y>=top.shape[0] or not top[x,y]:continue
    x=a0+b1+c2;y=a1+b2+c0
    if x>=top.shape[0] or y>=top.shape[0] or not top[x,y]:continue
    x=a0+b2+c1;y=a1+b0+c2
    if x>=top.shape[0] or y>=top.shape[0] or not top[x,y]:continue
    cs=sorted3(c0,c1,c2)
    rows.append((w0*c0+w1*c1+w2*c2,ea,pa,eb,pb,e2(c0,c1,c2),c0*c1*c2,a0,a1,a2,bs[0],bs[1],bs[2],cs[0],cs[1],cs[2]))
 arr=np.empty((len(rows),16),np.int32)
 for i in range(len(rows)):
  for j in range(16):arr[i,j]=rows[i][j]
 return arr

def en(key,excluded,f6=None,n=7):
 if f6 is None:f6=p.F6+p.univ
 adm=make_adm(n-1,np.asarray(f6 if n==7 else [],np.int64).reshape(-1,3))
 top=make_top(112 if n==7 else 45,sum(key),np.asarray(excluded,np.int64).reshape(-1,3))
 return fast_enum(*key,adm,top)

if __name__=='__main__':
 path=W/'new_certificate.json'
 result=json.loads(path.read_text()) if path.exists() else {'target':278,'stages':[]}
 excluded=[(112,112,29)]+[tuple(map(int,k.split(','))) for st in result['stages'] for k in st]
 # every target-size type with small third slice, useful support types included
 keys=[(a,b,278-a-b) for a in range(113) for b in range(a+1) if 0<=278-a-b<=b and 278-a-b<=72 and p.old.downwards_allowed((a,b,278-a-b),excluded)]
 keys.sort(key=lambda t:(t[2],-t[0]))
 mode=sys.argv[1] if len(sys.argv)>1 else 'ordinary'
 stage={}
 for key in keys:
  t=time.time();arr=en(key,excluded);label=','.join(map(str,key))
  rec=separate(arr[:,:7],force(key),364)
  print('CASE',key,len(arr),'CERT',rec,'sec',round(time.time()-t,2),flush=True)
  if rec:
   stage[label]=rec
  elif mode=='branches' and key[0]>=103 and key[1]>=103:
   eligibility=[j for j,N in enumerate(key) if 103<=N<109]
   br=[]
   for st in itertools.product((0,1),repeat=len(eligibility)):
    status=tuple(st[eligibility.index(j)] if j in eligibility else -1 for j in range(3))
    rr,tot,ex=p.prepare(arr,key,status,True)
    q=separate(rr,tot,364)
    print('BRANCH',key,status,len(rr),'CERT',q,flush=True)
    if q:br.append(dict(q,status=status,extra_features=ex))
   if len(br)==2**len(eligibility):stage[label]={'branches':br}
   # save partial branch proposals for future use
   (W/'partial').mkdir(exist_ok=True)
   (W/'partial'/f'{label}.json').write_text(json.dumps(br,indent=2))
  if stage:
   tmp=dict(result);tmp['stages']=result['stages']+[stage]
   path.write_text(json.dumps(tmp,indent=2))
 print('STAGE COMPLETE',len(stage),flush=True)
 print('ROOT',root(278,excluded+[tuple(map(int,k.split(','))) for k in stage])[::2],flush=True)
