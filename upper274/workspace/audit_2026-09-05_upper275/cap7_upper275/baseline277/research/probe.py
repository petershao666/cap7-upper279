import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import sys,json,itertools,time,math
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[1]/'baseline278'
sys.path.insert(0,str(BASE/'research'))
from engine import enum,separate,force,root,F6,old
cert=json.loads((BASE/'certificate.json').read_text())
comp=[tuple(t) for t in cert['completion_seeds']]+[old.parse_key(k) for st in cert['completion_stages'] for k in st]
def sub112(t):
    return t[2]<=22 or (t[0]<=40 and t[1]<=36)
univ=[t for t in comp if not sub112(t)]

def prepare(arr,key,status,label=True):
    mask=np.ones(len(arr),dtype=bool)
    for j,s in enumerate(status):
        tt=arr[:,7+3*j:10+3*j]
        if s==1:mask &= (tt[:,2]<=22)|((tt[:,0]<=40)&(tt[:,1]<=36))
        elif s==0:
            for t in comp:mask &= ~np.all(tt>=t,axis=1)
    arr=arr[mask];rows=arr[:,:7].astype(np.int64);totals=list(force(key));ex=[]
    for j,s in enumerate(status):
        if s!=1:continue
        tt=arr[:,7+3*j:10+3*j];f=tt[:,2]<=22;d=112-key[j]
        rows=np.c_[rows,f.astype(np.int64),np.where(f,22-tt[:,2],0)]
        totals.extend([56,11*d]);ex.extend([(j,'fam'),(j,'small')])
        if label:
            # min and max possible deletion from distinguished 40 section
            mn=np.where(f,0,40-tt[:,0]);mx=np.where(f,0,np.where(tt[:,0]>36,40-tt[:,0],40-tt[:,2]))
            # expand the two endpoints, all intermediate states redundant for affine inequalities
            rows=np.c_[rows,mn]
            inds=np.where(mn!=mx)[0]
            extra=rows[inds].copy();extra[:,-1]=mx[inds]
            rows=np.r_[rows,extra]
            # replicate metadata to keep other columns aligned
            arr=np.r_[arr,arr[inds]]
            totals.append(110*d);ex.append((j,'label40'))
        elif key[j]>=108:
            rows=np.c_[rows,np.where(f,0,40-tt[:,0])];totals.append(110*d);ex.append((j,'label40'))
    return rows,np.asarray(totals),ex

if __name__=='__main__':
 key=tuple(map(int,sys.argv[1:4])) if len(sys.argv)>1 else (106,106,66)
 t=time.time();arr,count=enum(key,n=7,f6=F6+univ,top_forbidden=[(112,112,29)])
 print('ENUM',key,count,len(arr),'sec',time.time()-t,flush=True)
 print('ordinary',separate(arr[:,:7],force(key),364),flush=True)
 for s in itertools.product((0,1),repeat=2):
  for label in [False,True]:
   if not any(s) and label:continue
   rows,tot,ex=prepare(arr,key,s+(-1,),label)
   t=time.time();rec=separate(rows,tot,364)
   print(s,'label',label,'rows',len(rows),'cert',rec,'sec',time.time()-t,flush=True)
