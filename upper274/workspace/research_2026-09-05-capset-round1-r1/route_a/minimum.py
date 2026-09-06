from discover import *
from scipy.optimize import linprog
# Bound every numerical call. All such calls only propose coefficients.
_orig_lp=E.linprog
def bounded_lp(*a,**kw):
 kw['options']=dict(kw.get('options',{}),time_limit=60)
 return _orig_lp(*a,**kw)
E.linprog=bounded_lp
# A coupled shear rotates beta by s and gamma by 2s, leaving alpha fixed.
# Use this proven orbit cover only for discovery, full verifier does not.
from numba import njit
src=(B/'baseline277/research/search_stage.py').read_text()
code=src[src.index('@njit(cache=True)'):src.index('\ndef en(')].replace('@njit(cache=True)','@njit')
exec(code,dict(),{}) if False else None
scope={'njit':njit,'np':np,'e2':E.e2,'sorted3':E.sorted3};exec(code,scope);fast=scope['fast_enum']
def en(key,ban):return fast(*key,ADM,E.make_top(112,275,np.array(ban,dtype=np.int64).reshape(-1,3)))
H=P['new_histograms']+[dict(json.loads((B/'baseline277/certificate.json').read_text())['nested108'],id='psi108',m=108)]
REG={h['id']:(h['m'],dict(zip(map(tuple,h['types']),h['phi'])),h['bound']) for h in H}
def prepare(arr,key,state):
 mask=np.ones(len(arr),dtype=bool)
 for j,s in enumerate(state):
  tt=arr[:,7+3*j:10+3*j]
  if s==1:mask&=(tt[:,2]<=22)|((tt[:,0]<=40)&(tt[:,1]<=36))
  if s==0:
   for t in COMP:mask&=~np.all(tt>=t,axis=1)
 arr=arr[mask];rows=arr[:,:7].astype(np.int64);tot=list(E.force(key));extra=[];positive=[]
 for j,s in enumerate(state):
  if s!=1:continue
  tt=arr[:,7+3*j:10+3*j];fam=tt[:,2]<=22;d=112-key[j]
  rows=np.c_[rows,fam.astype(np.int64),np.where(fam,22-tt[:,2],0)];tot.extend([56,11*d]);extra.extend([(j,'fam'),(j,'small')])
  mn=np.where(fam,0,40-tt[:,0]);mx=np.where(fam,0,np.where(tt[:,0]>36,40-tt[:,0],40-tt[:,2]))
  rows=np.c_[rows,mn];inds=np.where(mn!=mx)[0];new=rows[inds].copy();new[:,-1]=mx[inds];rows=np.r_[rows,new];arr=np.r_[arr,arr[inds]];tot.append(110*d);extra.append((j,'label40'))
 for j,s in enumerate(state):
  if s!=0:continue
  tt=arr[:,7+3*j:10+3*j]
  for name,(m,phi,bd) in REG.items():
   if m!=key[j]:continue
   lookup=np.zeros((46,46),np.int64)
   for t,val in phi.items():lookup[t[:2]]=val
   rows=np.c_[rows,lookup[tt[:,0],tt[:,1]]];positive.append(len(tot));tot.append(bd);extra.append((j,name))
 return rows,np.array(tot),extra,positive

def sep(rows,tot,pos):
 if len(rows)==0:return {'empty':True}
 mean=np.array(tot,float)/364;scale=np.maximum(np.max(abs(rows-mean),axis=0),1);Wv=(rows-mean)/scale
 inds=np.unique(np.r_[np.argmin(Wv,axis=0),np.argmax(Wv,axis=0)])
 for it in range(100):
  bnd=[(0,1) if j in pos else (-1,1) for j in range(len(tot))]+[(None,None)]
  res=bounded_lp(np.r_[np.zeros(len(tot)),-1.],A_ub=np.c_[-Wv[inds],np.ones(len(inds))],b_ub=np.zeros(len(inds)),bounds=bnd,method='highs')
  if not res.success or res.x[-1]<1e-9:return None
  q=res.x[:-1];vals=Wv@q
  if vals.min()>=res.x[-1]-1e-9:break
  add=np.argpartition(vals,min(19,len(vals)-1))[:20];inds=np.unique(np.r_[inds,add])
 else:return None
 qs=q/scale;nz=abs(qs)>1e-12
 qs/=np.min(abs(qs[nz]))
 for mul in [1,2,5,10,20,50,100,500,1000,10000,100000,1000000]:
  qi=np.rint(qs*mul).astype(np.int64);g=math.gcd(*map(int,qi));qi//=g
  if max(map(abs,qi))*max(map(abs,rows.min(axis=0))) *len(qi)>7e18:continue
  K=int((rows@qi).min());forced=sum(int(a)*int(b) for a,b in zip(qi,tot));gap=364*K-forced
  if gap>0:return dict(coeff=list(map(int,qi)),K=K,forced=forced,gap=gap)
 return None

def main():
 signal.alarm(570);start=time.monotonic();out=json.loads((W/'certificates.json').read_text());ban=SEEDS+[V.parse_key(k) for st in out['stages'] for k in st]
 keys=sorted([t for t in T if Q(t)<0 and V.downwards_allowed(t,ban)],key=lambda t:(t[2],-t[0]))
 for key in keys:
  forbidden=ban+[t for t in T if Q(t)<Q(key)];arr=en(key,forbidden);rec=separate(arr[:,:7],E.force(key));label=','.join(map(str,key))
  print('MINIMUM',key,len(arr),rec,'elapsed',round(time.monotonic()-start,2),flush=True)
  if rec:out['extremal'][label]=dict(rec,discovery_count=len(arr));save(out,'certificates.json');continue
  eligible=[j for j,n in enumerate(key) if 103<=n<109];branches=[]
  for bits in itertools.product((0,1),repeat=len(eligible)):
   state=tuple(bits[eligible.index(j)] if j in eligible else 1 if n>=109 else -1 for j,n in enumerate(key))
   rows,tot,extras,pos=prepare(arr,key,state);rec=sep(rows,tot,pos)
   print('BRANCH',key,state,len(rows),rec,'elapsed',round(time.monotonic()-start,2),flush=True)
   branches.append(dict(status=state,extra_features=extras,certificate=rec,discovery_count=len(rows)))
  out['extremal'][label]=dict(branches=branches);save(out,'certificates.json')
 print('DONE MINIMUM',flush=True)
if __name__=='__main__':main()
