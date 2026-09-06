import time as _walltime
PROCESS_START=_walltime.monotonic()
import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import hashlib,resource
import sys,importlib.util
from pathlib import Path
W=Path(__file__).resolve().parent;ROOTDIR=W.parents[1];H=ROOTDIR/'hist105106';sys.path.insert(0,str(H));sys.path.insert(0,str(H/'h3'))
sys.dont_write_bytecode=True
os.environ['NUMBA_CACHE_DIR']=str(W/'numba_cache')
_original_write_text=Path.write_text
def _owned_write_text(path,data,*args,**kwargs):
 resolved=path.resolve()
 if not resolved.is_relative_to(W):
  assert resolved.is_relative_to(ROOTDIR),resolved
  path=W/'redirected'/resolved.relative_to(ROOTDIR);path.parent.mkdir(parents=True,exist_ok=True)
 return _original_write_text(path,data,*args,**kwargs)
Path.write_text=_owned_write_text
import joint as J
from joint import np,O,E,V,C,OLD,COMP,ANCH,SUP,ROOT,SEEDS,T,Q,en,signal,limit,math,json,itertools,time,sparse,R
import structural40 as S40
sp=importlib.util.spec_from_file_location('h11_readonly_run',H/'h11/single.py');R106=importlib.util.module_from_spec(sp);sp.loader.exec_module(R106)
SAVE=lambda z,n:(W/n).write_text(json.dumps(z,indent=2)+'\n')
ST=json.loads((H/'h10/full18_states.json').read_text());T18=sorted({tuple(t)for h in ST for t in h['types']});IX18={t:i for i,t in enumerate(T18)}
TS={18:T18,40:S40.D.SUP40,41:R106.T41,106:SUP[106]};ND={18:40,40:121,41:121,106:364};D={40:40,41:40,106:121}
CP=json.loads((H/'h13/histogram_pair_capacity_v2.json').read_text());PAIR=CP['allowed_18184_ordered_pairs'];COND=CP['allowed_20182_full18_states']
ORDER40=list(reversed(S40.D.SUP40))
TIERS=[400,401,402]
TIER_PARENT={400:(43,40,23),401:(44,40,22),402:(45,40,21)}
TIER_FOR_PARENT={t:m for m,t in TIER_PARENT.items()}
for m in TIERS:TS[m]=TS[40];ND[m]=121;D[m]=40
COND_FUNCTIONS=[f't{m}_{n}'for m in TIERS for n in ['left18','right18','cond18']]
COND_BOUNDS=[f't{m}_{n}'for m in TIERS for n in ['pair18','cond18']]
H18=np.array([[dict(zip(map(tuple,h['types']),h['histogram'])).get(t,0)for t in T18]for h in ST],np.int64)

INPUT17=json.loads((H/'h16/input.json').read_text());T17=list(map(tuple,INPUT17['direction_types17']));IX17={t:i for i,t in enumerate(T17)};ANCH17=list(map(tuple,INPUT17['anchor_order17']))
TS[17]=T17;ND[17]=40;D[17]=13
M17={(a*b+a*c+b*c,a*b*c):i for i,(a,b,c)in enumerate(T17)};assert len(M17)==len(T17)
ACTUAL16=json.loads((ROOTDIR/'root_audit/actual16/ACCEPTED_HISTOGRAMS.json').read_text());T16=list(map(tuple,ACTUAL16['types']));H16=np.array(ACTUAL16['histograms'],np.int64);assert H16.shape==(376,14)
TS[16]=T16;ND[16]=40;D[16]=13
M16={(a*b+a*c+b*c,a*b*c):i for i,(a,b,c)in enumerate(T16)};assert len(M16)==14
ACTUAL41=json.loads((ROOTDIR/'root_audit/complete41/ACCEPTED_HISTOGRAMS.json').read_text());assert ACTUAL41['status']=='ACCEPTED_COMPLETE_5D41_HISTOGRAM_FAMILY_WITH_PUBLISHED_PREMISES'
T41=list(map(tuple,ACTUAL41['types']));H41=np.array([h['counts']for h in ACTUAL41['histograms']],np.int64);assert H41.shape==(44,40)
TS[41]=T41;assert all(int(h.sum())==121 for h in H41)
ACTUAL42=C['spectrum5']['42'];T42=list(map(tuple,ACTUAL42['types']));H42=np.array(ACTUAL42['spectra'],np.int64);assert H42.shape==(4,13)
TS[42]=T42;ND[42]=121
assert all(int(h.sum())==121 for h in H42)
ZERO41=[t for i,t in enumerate(T41)if not np.any(H41[:,i])];assert len(ZERO41)==14
OLD_ADM5=J.ADM5.copy()
for t in itertools.product(range(21),repeat=3):
 if not V.downwards_allowed(t,ZERO41):J.ADM5[t]=False
PRUNING=dict(ordinary5D41_zero_types=ZERO41,ordinary5D_old_admissible_ordered_profiles=int(OLD_ADM5.sum()),ordinary5D_new_admissible_ordered_profiles=int(J.ADM5.sum()),scope='Only 5D profiles of the NC106 refinement grid; no outer6D transfer')
BASE106={tuple(c['type']):c['count']for c in json.loads((H/'h21/h21_result.json').read_text())['counts']if c['m']==106}
ACTUAL17=json.loads((H/'h17/histograms17.json').read_text());assert list(map(tuple,ACTUAL17['types']))==T17
H17=np.array([h['counts']for h in ACTUAL17['histograms']],np.int64);assert H17.shape==(102,13)

def attach16_17(z):
 if z['empty']:return z
 z.setdefault('deps',[])
 for j,n in enumerate(z['key']):
  if n in (16,17):
   lookup=M16 if n==16 else M17
   ids=np.array([lookup[tuple(v)]for v in z['X'][:,1+2*j:3+2*j]],np.int32);z['deps'].append((n,ids,j))
 return z

def low40(key,i):
 ix=np.full((21,21),-1,np.int64)
 for t,j in S40.D.IX40.items():ix[t[:2]]=j
 top=E.make_top(20,40,np.array(ORDER40[:i],np.int64).reshape(-1,3));ar=S40.raw_enum(*key,S40.D.A4,top,ix);ar=ar[S40.filter_clashes(ar,S40.PS)]
 mask=np.ones(len(ar),bool)
 for j,N in enumerate(key):
  if N==18:mask&=np.array([tuple(t)in IX18 for t in ar[:,7+3*j:10+3*j]],bool)
 ar=ar[mask]
 if not len(ar):return dict(m=40,key=key,empty=True)
 X=ar[:,:7].copy();F=list(E.force(key,5));extra=[];pos=[];deps=[]
 for j,N in enumerate(key):
  tt=ar[:,7+3*j:10+3*j]
  if str(N)in S40.HIST:
   h=S40.HIST[str(N)]
   for t,bd in zip(h['types'],h['histogram']):X=np.c_[X,np.all(tt==t,axis=1).astype(np.int64)];F.append(bd);extra.append((j,'exact4',t,bd))
  if N==18:deps.append((18,np.array([IX18[tuple(t)]for t in tt],np.int32),j))
  if N==17:
   cover=[(9,8,0),(9,7,1),(8,8,1)];X=np.c_[X,-sum(np.all(tt==t,axis=1).astype(np.int64)for t in cover)];pos.append(len(F));F.append(-1);extra.append((j,'direction_cover',cover,-1))
 F=np.array(F,np.int64);sc=np.maximum(np.max(abs(X-F/40),axis=0),1)
 z=dict(m=40,key=key,X=X,F=F,W=(X-F/40)/sc,scale=sc,extra=extra,pos=pos,deps=deps,tops=ar[:,16:19].copy(),anchor=S40.D.IX40[key],empty=False)
 if key==(18,18,4):
  z['pairdeps']=[('left18' if col==0 else 'right18',ids,col)for parent,ids,col in deps];z['pairbound']='pair18';z['deps']=[]
 elif key==(20,18,2):
  z['pairdeps']=[('cond18',ids,col)for parent,ids,col in deps];z['pairbound']='cond18';z['deps']=[]
 return attach16_17(z)

def clone40(base,tier):
 z=dict(base,m=tier,mathematical_size=40,tier_parent=TIER_PARENT[tier])
 z['deps']=list(base.get('deps',[]))
 z['pairdeps']=[(f't{tier}_{name}',ids,col)for name,ids,col in base.get('pairdeps',[])]
 if base.get('pairbound'):z['pairbound']=f"t{tier}_{base['pairbound']}"
 return z

def inner106(key,i):
 ix={t:j for j,t in enumerate(SUP[106])};index=np.full((46,46),-1,np.int64)
 for t,j in ix.items():index[t[:2]]=j
 ar=O.ien(*key,J.ADM5,E.make_top(45,106,np.array(OLD+COMP+ANCH[106][:i],np.int64)),index)
 if not len(ar):return dict(m=106,key=key,empty=True,before=BASE106[key])
 z=R106.inner106(key,i);assert len(ar)==len(z['X']);z['deps']=[];z['empty']=False;z['before']=BASE106[key]
 for j,N in enumerate(key):
  if N in(40,41,42):
   mp={t:k for k,t in enumerate(TS[N])};parent=TIER_FOR_PARENT[key]if N==40 else N
   if N==40:assert j==1
   z['deps'].append((parent,np.array([mp[tuple(t)]for t in ar[:,7+3*j:10+3*j]],np.int32),j))
 return z

def localize_supports(INS):
 leaves={}
 for ci,z in enumerate(INS):
  keep=[];z['leafdeps']=[]
  for parent,ids,col in z['deps']:
   if parent in(16,17,18,41,42):
    name=f"support_{z['m']}_{ci}_c{col}_n{parent}"
    leaves[name]=dict(m=parent,case_index=ci,case_dimension_size=z['m'],anchor=z['key'],column=col,class41=z.get('class41'),full18_state=z.get('full18_state'))
    z['leafdeps'].append((name,ids,col))
   else:keep.append((parent,ids,col))
  z['deps']=keep
 return leaves

FIXED6=json.loads((H/'h23_r105_transfer/FIXED_INPUTS.json').read_text())
assert len(FIXED6['functions'])==6 and all(f['size']==106 for f in FIXED6['functions'])
def outer_new(key,ban):
 z=J.outer(key,ban);columns=[z['X']];F=list(z['F']);extra=list(z['extra']);pos=list(z['pos']);used=[]
 for col,(m,ids)in enumerate(z['ids']):
  for fn in FIXED6['functions']:
   if fn['size']!=m:continue
   lut=dict(zip(map(tuple,fn['types']),fn['values']));assert set(lut)==set(SUP[m])
   vals=np.array([lut[t]for t in SUP[m]],np.int64)[ids]
   columns.append(vals[:,None]);pos.append(len(F));F.append(fn['bound']);extra.append((col,'fixed6_upper',fn['id'],fn['bound']));used.append(dict(fn,column=col))
 X=np.hstack(columns);del columns;F=np.array(F,np.int64);scale=np.maximum(np.max(abs(X-F/364),axis=0),1)
 z.update(X=X,F=F,scale=scale,W=(X-F/364)/scale,pos=pos,extra=extra,fixed_functions=used)
 return z
