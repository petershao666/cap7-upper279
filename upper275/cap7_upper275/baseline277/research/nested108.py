import os;os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import sys,json,itertools,time,math
from pathlib import Path
import numpy as np
from numba import njit
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe as p
from search_stage import en
from engine import make_adm,make_top,sorted3,e2,separate,force
W=Path(__file__).resolve().parent/'outputs';W.mkdir(exist_ok=True)
T=[(a,b,108-a-b) for a in range(46) for b in range(a+1) if 0<=108-a-b<=b and p.old.downwards_allowed((a,b,108-a-b),p.F6+p.comp)]
ix={t:i for i,t in enumerate(T)}
RARE=[(45,41,22),(44,43,21),(43,43,22)]
@njit(cache=True)
def inner_enum(A,B,C,adm,top,index):
 aa=[];bb=[];cc=[]
 for a in range(21):
  for b in range(21):
   c=A-a-b
   if 0<=c<=b<=a and adm[a,b,c]:aa.append((a,b,c))
   c=B-a-b
   if 0<=c<=20 and adm[a,b,c] and (a,b,c)>=(b,c,a) and (a,b,c)>=(c,a,b):bb.append((a,b,c))
   c=C-a-b
   if 0<=c<=20 and adm[a,b,c]:cc.append((a,b,c))
 rows=[]
 for a in aa:
  for b in bb:
   for c in cc:
    ok=True
    for i in range(3):
     for j in range(3):
      if not adm[a[i],b[j],c[(-i-j)%3]]:ok=False
    if not ok:continue
    tt=np.zeros(3,np.int64)
    for s in range(3):
     x=a[0]+b[s]+c[2*s%3];y=a[1]+b[(1+s)%3]+c[(1+2*s)%3]
     if x>45 or y>45 or not top[x,y]:ok=False;break
     so=sorted3(x,y,A+B+C-x-y);tt[s]=index[so[0],so[1]]
    if not ok:continue
    cr=0
    for i in range(3):
     for j in range(3):cr+=a[i]*b[j]*c[(-i-j)%3]
    bs=sorted3(*b);cs=sorted3(*c)
    rows.append((cr,e2(*a),a[0]*a[1]*a[2],e2(*b),b[0]*b[1]*b[2],e2(*c),c[0]*c[1]*c[2],a[0],a[1],a[2],bs[0],bs[1],bs[2],cs[0],cs[1],cs[2],tt[0],tt[1],tt[2]))
 arr=np.empty((len(rows),19),np.int64)
 for i in range(len(rows)):
  for j in range(19):arr[i,j]=rows[i][j]
 return arr

def inner_data(key):
 adm=make_adm(5,np.empty((0,3),np.int64));top=make_top(45,108,np.array(p.F6+p.comp,np.int64))
 index=np.full((46,46),-1,np.int64)
 for t,i in ix.items():index[t[0],t[1]]=i
 arr=inner_enum(*key,adm,top,index);rows=arr[:,:7].copy();tot=list(force(key,6));extras=[]
 for j,N in enumerate(key):
  if str(N) not in p.cert['spectrum5']:continue
  hh=p.cert['spectrum5'][str(N)]
  # use exact histogram when unique, no spectral inequalities needed for chosen rare cases
  assert len(hh['spectra'])==1
  for k,t in enumerate(hh['types']):
   rows=np.c_[rows,np.all(arr[:,7+3*j:10+3*j]==t,axis=1).astype(np.int64)]
   tot.append(hh['spectra'][0][k]);extras.append((j,t))
 return arr,rows,np.array(tot,np.int64),extras

def run():
 rootrows=np.array([(p.old.e2(t),p.old.e3(t)) for t in T if t not in RARE],np.int64)
 root=separate(rootrows,np.array([243*math.comb(108,2),81*math.comb(108,3)]),364)
 print('RARE EXISTENCE',root,flush=True)
 assert root
 c=json.load(open(W/'new_certificate.json'));ex=[(112,112,29),(112,111,35)]+[p.old.parse_key(k) for st in c['stages'] for k in st]
 key=(108,108,62)
 Q=lambda t:9*p.old.e3(t)-911*p.old.e2(t)+16306924
 ex += [(a,b,278-a-b) for a in range(113) for b in range(a+1) if 0<=278-a-b<=b and Q((a,b,278-a-b))<Q(key)]
 arr=en(key,ex)
 mask=np.ones(len(arr),bool)
 for j in (0,1):
  tt=arr[:,7+3*j:10+3*j]
  for t in p.comp:mask &= ~np.all(tt>=t,axis=1)
 arr=arr[mask]
 X=np.c_[arr[:,0],arr[:,1]+arr[:,3],arr[:,2]+arr[:,4],arr[:,5],arr[:,6]].astype(np.int64)
 F=force(key);F=np.array([F[0],F[1]+F[3],F[2]+F[4],F[5],F[6]])
 V=X-F/364;scale=np.maximum(np.max(abs(V),axis=0),1);V/=scale
 ia=np.array([ix[tuple(t)] for t in arr[:,7:10]],np.int32);ib=np.array([ix[tuple(t)] for t in arr[:,10:13]],np.int32)
 print('OUTER',len(arr),'TYPES',len(T),flush=True)
 # unknowns: q_outer(5), phi(len T), beta, q_inner[each], delta
 phi_off=5;beta_off=5+len(T);offset=beta_off+1;inner=[]
 for t in RARE:
  aa,rr,ff,extras=inner_data(t);vv=rr-ff/121;sc=np.maximum(np.max(abs(vv),axis=0),1);vv/=sc
  inner.append(dict(key=t,arr=aa,rows=rr,totals=ff,W=vv,scale=sc,offset=offset,extras=extras));offset+=rr.shape[1]
 nv=offset+1;delta=offset
 print('VARIABLES',nv,'INNER',[len(z['arr']) for z in inner],flush=True)
 fixed=[]
 for z in inner:
  R=np.zeros((len(z['arr']),nv));R[:,z['offset']:z['offset']+z['rows'].shape[1]]=-z['W']
  for i,tr in enumerate(z['arr'][:,16:19]):
   for k in tr:R[i,phi_off+k]+=1
  R[:,phi_off+ix[z['key']]]+=1/121
  R[:,beta_off]=-364/121
  fixed.append(R)
 fixed=np.concatenate(fixed)
 inds=np.unique(np.r_[np.argmin(V,axis=0),np.argmax(V,axis=0)])
 sol=None
 for it in range(400):
  R=np.zeros((len(inds),nv));R[:,:5]=-V[inds];R[np.arange(len(inds)),phi_off+ia[inds]]-=1;R[np.arange(len(inds)),phi_off+ib[inds]]-=1;R[:,beta_off]=2;R[:,delta]=1
  res=linprog(np.r_[np.zeros(nv-1),-1.],A_ub=np.r_[fixed,R],b_ub=np.zeros(len(fixed)+len(R)),bounds=[(-1,1)]*beta_off+[(None,None)]+[(-1,1)]*(nv-beta_off-2)+[(None,None)],method='highs')
  if not res.success:print('SOLVER',res.message,flush=True);break
  x=res.x;gap=x[-1]
  vals=V@x[:5]+x[phi_off+ia]+x[phi_off+ib]-2*x[beta_off]
  m=vals.min();print('ITER',it,'rows',len(inds),'gap',gap,'minimum',m,flush=True)
  if gap<1e-9:break
  if m>=gap-1e-9:sol=x;break
  add=np.argpartition(vals,min(99,len(vals)-1))[:100];inds=np.unique(np.r_[inds,add])
 if sol is None:
  np.savez_compressed(W/'nested108_last.npz',solution=res.x,indices=inds)
  print('NO CERT',flush=True);return
 print('FOUND numerical certificate',gap,flush=True)
 # Common scaling makes phi and every inner/outer vector integer consistently.
 floats=sol.copy();floats[:5]/=scale
 for z in inner:floats[z['offset']:z['offset']+z['rows'].shape[1]]/=z['scale']
 for mul in [1000,10000,100000,1000000,10000000,100000000,1000000000,10000000000]:
  qi=np.rint(floats*mul).astype(np.int64);q=qi[:5];phi=qi[phi_off:beta_off]
  # q_inner W >= phi tops - B/121 etc -> exact B from minima of q_inner*g - phi tops
  inner_c=[];Bs=[]
  for z in inner:
   qin=qi[z['offset']:z['offset']+z['rows'].shape[1]]
   val=z['rows']@qin-np.sum(phi[z['arr'][:,16:19]],axis=1)
   K=int(val.min());B=int(phi[ix[z['key']]])+sum(int(a)*int(b) for a,b in zip(qin,z['totals']))-121*K
   Bs.append(B);inner_c.append(dict(type=z['key'],coeff=list(map(int,qin)),K=K,bound=B,extras=z['extras'],matrices=len(val)))
  B=max(Bs);vals=X@q+phi[ia]+phi[ib];K=int(vals.min());forced=sum(int(a)*int(b) for a,b in zip(q,F))+2*B;g=364*K-forced
  print('RECOVER',mul,'GAP',g,'B',B,flush=True)
  if g>0:
   out=dict(root=root,types=T,inner=inner_c,phi=list(map(int,phi)),bound=B,outer=dict(type=key,coeff=list(map(int,q)),K=K,forced=forced,gap=g,matrices=len(X)),inner_counts=[len(z['arr']) for z in inner])
   (W/'nested108_certificate.json').write_text(json.dumps(out,indent=2));print('EXACT DISCOVERY PASS',g,flush=True);return
 print('INTEGER RECOVERY FAILED',flush=True)
if __name__=='__main__':run()
