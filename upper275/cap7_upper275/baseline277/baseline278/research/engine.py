"""Discovery helpers. Floating-point optimization proposes; exact checks decide."""
import sys,json,math,itertools,time
# This discovery model uses the 109-completion theorem proved by the parent
# certificate. It must not be used to prove that theorem circularly. For
# dimension-six completion searches, only the dimension-five predicate is used.
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from numba import njit
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
import core as old
CERT=json.loads(Path(__file__).with_name('base_certificate.json').read_text())
F6=[old.parse_key(k) for st in CERT['six_stages'] for k in st]
@njit
def sorted3(a,b,c):
    if a<b:a,b=b,a
    if b<c:b,c=c,b
    if a<b:a,b=b,a
    return a,b,c
@njit
def make_adm(n,forbidden):
    U=20 if n==5 else 45
    adm=np.zeros((U+1,U+1,U+1),np.bool_)
    delta=((20,16,6),(18,18,6),(18,17,7),(18,12,12),(16,15,11),(16,14,12),(15,15,12),(14,14,14))
    for x in range(U+1):
      for y in range(U+1):
       for z in range(U+1):
        a,b,c=sorted3(x,y,z);s=a+b+c
        if n==5:
            if s>45:continue
            ok=s<42 or (a<=18 and b<=18 and c<=9) or a<=15
            if s==42:
                for t in delta:
                    if (a,b,c)==t:ok=True
        else:
            ok=s<=112 and (s<109 or c<=22 or (a<=40 and b<=36))
        if not ok:continue
        for t in forbidden:
            if a>=t[0] and b>=t[1] and c>=t[2]:ok=False;break
        adm[x,y,z]=ok
    return adm
@njit
def make_top(upper,total,forbidden):
    top=np.zeros((upper+1,upper+1),np.bool_)
    for x in range(upper+1):
      for y in range(upper+1):
        z=total-x-y
        if z<0 or z>upper:continue
        a,b,c=sorted3(x,y,z);ok=True
        for t in forbidden:
            if a>=t[0] and b>=t[1] and c>=t[2]:ok=False;break
        top[x,y]=ok
    return top
@njit
def e2(a,b,c):return a*b+a*c+b*c
@njit
def enumerate_features(A,B,C,adm,top,extra_types=False):
    U=adm.shape[0]-1;S=A+B+C
    alphas=[];betas=[];gammas=[]
    for a in range(U+1):
      for b in range(U+1):
        c=A-a-b
        if 0<=c<=b<=a and adm[a,b,c]:alphas.append((a,b,c))
        c=B-a-b
        if 0<=c<=U and adm[a,b,c]:betas.append((a,b,c))
        c=C-a-b
        if 0<=c<=U and adm[a,b,c]:gammas.append((a,b,c))
    # Cache transverse masks as boolean, loop allowed first two entries.
    features=[]
    count=0
    for aa in alphas:
      a0,a1,a2=aa;ea=e2(a0,a1,a2);pa=a0*a1*a2
      for bb in betas:
        b0,b1,b2=bb;eb=e2(b0,b1,b2);pb=b0*b1*b2
        w0=a0*b0+a1*b2+a2*b1;w1=a0*b2+a1*b1+a2*b0;w2=a0*b1+a1*b0+a2*b2
        # symmetry: keep b lexicographically minimal under rotations if a not sorted? no added symmetry.
        for c0,c1,c2 in gammas:
          if not(adm[a0,b0,c0] and adm[a1,b2,c0] and adm[a2,b1,c0] and adm[a0,b2,c1] and adm[a1,b1,c1] and adm[a2,b0,c1] and adm[a0,b1,c2] and adm[a1,b0,c2] and adm[a2,b2,c2]):continue
          x=a0+b0+c0;y=a1+b1+c1
          if x>=top.shape[0] or y>=top.shape[0] or not top[x,y]:continue
          x=a0+b1+c2;y=a1+b2+c0
          if x>=top.shape[0] or y>=top.shape[0] or not top[x,y]:continue
          x=a0+b2+c1;y=a1+b0+c2
          if x>=top.shape[0] or y>=top.shape[0] or not top[x,y]:continue
          T=w0*c0+w1*c1+w2*c2
          bsort=sorted3(b0,b1,b2);csort=sorted3(c0,c1,c2)
          features.append((T,ea,pa,eb,pb,e2(c0,c1,c2),c0*c1*c2,
                           aa[0],aa[1],aa[2],bsort[0],bsort[1],bsort[2],csort[0],csort[1],csort[2]))
          count+=1
    arr=np.empty((len(features),16),np.int32)
    for i in range(len(features)):
      for j in range(16):arr[i,j]=features[i][j]
    return arr

def enum(key,n=7,f6=None,top_forbidden=()):
    if f6 is None:f6=F6
    fs=np.array(f6 if n==7 else [],dtype=np.int64).reshape(-1,3)
    adm=make_adm(n-1,fs)
    top=make_top(112 if n==7 else 45,sum(key),np.array(top_forbidden,dtype=np.int64).reshape(-1,3))
    arr=enumerate_features(*key,adm,top)
    count=len(arr)
    if count:
      # feature deduplication is used only in discovery, not in certificate verifiers.
      arr=np.unique(arr,axis=0)
    return arr,count

def force(key,n=7):return np.array(old.forced(key,n),dtype=np.int64)

def separate(rows,totals,D,extra=None):
    """Find rationally recoverable dual by row generation; rows integer."""
    if len(rows)==0:return {'empty':True}
    mean=np.asarray(totals,dtype=float)/D
    V=rows.astype(float)-mean
    scale=np.max(np.abs(V),axis=0)
    scale[scale<1]=1.
    W=V/scale
    inds=np.unique(np.r_[np.argmin(W,axis=0),np.argmax(W,axis=0)])
    qs=None
    for it in range(200):
      constraints=np.c_[-W[inds],np.ones(len(inds))]
      res=linprog(np.r_[np.zeros(W.shape[1]),-1.],A_ub=constraints,b_ub=np.zeros(len(inds)),bounds=[(-1,1)]*W.shape[1]+[(None,None)],method='highs')
      if not res.success:return None
      q=res.x[:-1];gap=res.x[-1]
      if gap<1e-9:return None
      vals=W@q
      m=np.min(vals)
      if m>=gap-1e-9:
        qs=q/scale
        break
      add=np.argpartition(vals,min(19,len(vals)-1))[:20]
      inds=np.unique(np.r_[inds,add])
    if qs is None:return None
    nz=np.abs(qs)>1e-12
    qs/=np.min(np.abs(qs[nz]))
    for mul in [1,2,3,5,10,20,50,100,200,500,1000,2000,10000,100000,1000000]:
      qi=np.rint(qs*mul).astype(np.int64)
      g=math.gcd(*map(int,qi));qi//=g
      K=int(np.min(rows.astype(np.int64)@qi));forced=sum(int(x)*int(y) for x,y in zip(qi,totals));gap=D*K-forced
      if gap>0:return {'coeff':list(map(int,qi)), 'K':K,'forced':forced,'gap':gap}
    return None

def root(target,excluded=()):
    types=np.array([(a,b,target-a-b) for a in range(113) for b in range(a+1) if 0<=target-a-b<=b and old.downwards_allowed((a,b,target-a-b),excluded)],dtype=np.int64)
    rows=np.array([(old.e2(t),old.e3(t)) for t in types])
    tot=np.array([729*math.comb(target,2),243*math.comb(target,3)])
    cert=separate(rows,tot,1093)
    if cert:return cert,types,None
    # Primal feasible moment mixture reveals important remaining types.
    scale=np.max(np.abs(rows-tot/1093),axis=0)
    rr=(rows-tot/1093)/scale
    lp=linprog(np.zeros(len(rows)),A_eq=np.r_[np.ones((1,len(rows))),rr.T],b_eq=[1,0,0],bounds=(0,None),method='highs')
    support=[] if not lp.success else [(tuple(types[i]),float(lp.x[i])) for i in np.where(lp.x>1e-8)[0]]
    return None,types,support

def separate_spectral(arr,key,n=6,certificate=None):
    if len(arr)==0:return {'empty':True}
    if certificate is None:certificate=CERT
    totals=force(key,n);D=(3**(n-1)-1)//2
    rows=arr[:,:7].astype(np.int64)
    V=rows-totals/D
    scale=np.max(np.abs(V),axis=0);scale[scale<1]=1.
    W=V/scale
    specs=[];offset=7;indcols=[]
    for j,N in enumerate(key):
      if str(N) not in certificate['spectrum5']:continue
      dd=certificate['spectrum5'][str(N)];types=[tuple(t) for t in dd['types']];index={t:i for i,t in enumerate(types)}
      idx=np.array([index[tuple(t)] for t in arr[:,7+3*j:10+3*j]],dtype=np.int32)
      hh=np.asarray(dd['spectra'],dtype=np.int64)
      specs.append((j,types,hh,offset,idx));offset+=len(types)
    if not specs:return separate(rows,totals,D)
    R=np.zeros((len(arr),offset),dtype=np.float64);R[:,:7]=W
    for j,types,hh,off,idx in specs:R[np.arange(len(arr)),off+idx]=1.
    zoff=offset;nv=offset+len(specs)+1
    spectral=[]
    for jj,(j,types,hh,off,idx) in enumerate(specs):
      for hist in hh:
        c=np.zeros(nv);c[off:off+len(types)]=hist/D;c[zoff+jj]=-1
        spectral.append(c)
    spectral=np.array(spectral)
    inds=np.unique(np.r_[np.argmin(R,axis=0),np.argmax(R,axis=0)])
    qs=None
    for it in range(200):
      cs=np.c_[-R[inds],np.ones((len(inds),len(specs)+1))]
      res=linprog(np.r_[np.zeros(nv-1),-1.],A_ub=np.r_[cs,spectral],b_ub=np.zeros(len(cs)+len(spectral)),bounds=[(-1,1)]*offset+[(None,None)]*(len(specs)+1),method='highs')
      if not res.success:return None
      q=res.x[:offset];z=res.x[zoff:zoff+len(specs)];gap=res.x[-1]
      if gap<1e-9:return None
      vals=R@q-sum(z);m=np.min(vals)
      if m>=gap-1e-9:qs=q.copy();qs[:7]/=scale;break
      add=np.argpartition(vals,min(19,len(vals)-1))[:20];inds=np.unique(np.r_[inds,add])
    if qs is None:return None
    # Check all proposed integer coefficients on the complete deduplicated family.
    nz=np.abs(qs)>1e-10
    qs/=np.min(np.abs(qs[nz]))
    for mul in [1,2,5,10,20,50,100,200,500,1000,2000,10000,100000,1000000]:
      qi=np.rint(qs*mul).astype(np.int64);g=math.gcd(*map(int,qi));qi//=g
      vals=rows@qi[:7];forced=sum(int(x)*int(y) for x,y in zip(qi[:7],totals));extras=[]
      for j,types,hh,off,idx in specs:
        phi=qi[off:off+len(types)]
        bound=int(np.max(hh@phi));vals+=phi[idx];forced+=bound
        extras.append({'column':j,'identity':{'coeff':list(map(int,phi)),'sum':bound,'bound':'upper'}})
      K=int(np.min(vals));gap=D*K-forced
      if gap>0:
        return {'coeff':list(map(int,qi[:7]))+[1]*len(extras),'K':K,'forced':forced,'gap':gap,'extra':extras}
    return None
