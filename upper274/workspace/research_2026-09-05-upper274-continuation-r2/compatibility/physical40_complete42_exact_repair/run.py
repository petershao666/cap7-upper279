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

def main():
 source_inputs=json.loads((W/'INPUTS.json').read_text())
 for name,sha in source_inputs['source_hashes'].items():assert hashlib.sha256((ROOTDIR/name).read_bytes()).hexdigest()==sha
 signal.signal(signal.SIGALRM,limit);signal.alarm(max(1,int(590-(_walltime.monotonic()-PROCESS_START))));start=PROCESS_START;old=json.loads((R/'certificates.json').read_text());ban=SEEDS+[(112,109,51),(111,110,51)]+[V.parse_key(k)for s in old['stages']for k in s]
 base40=[low40(t,i)for i,t in enumerate(ORDER40)];a40=[clone40(z,tier)for tier in TIERS for z in base40];nc=[inner106(t,i)for i,t in enumerate(ANCH[106])];ALL=a40+nc
 INS=[z for z in ALL if not z['empty']]
 for z in INS:z.setdefault('deps',[]);z.setdefault('pairdeps',[])
 LEAF=localize_supports(INS);SAVE(LEAF,'local_support_layout.json');print('LOCAL_SUPPORTS',len(LEAF),{m:sum(l['m']==m for l in LEAF.values())for m in[16,17,18,41,42]},flush=True)
 PRUNING['nc106_cases']=[dict(type=z['key'],before=z['before'],after=0 if z['empty']else len(z['X']),empty=z['empty'])for z in nc];SAVE(PRUNING,'ordinary5D_pruning.json')
 assert json.loads(json.dumps(PRUNING))==json.loads((H/'h22_complete41/ordinary5D_pruning.json').read_text())
 OUT=[outer_new((106,106,63),ban)];empty=[dict(m=z['m'],type=z['key'],class41=z.get('class41'),full18_state=z.get('full18_state'),state18=z.get('state18'),state8=z.get('state8'))for z in ALL if z['empty']]
 assert len(OUT[0]['X'])==2460769 and sum(len(z['X'])for z in nc if not z['empty'])==94242
 assert len(OUT[0]['fixed_functions'])==12
 SAVE(dict(outer_fixed_instances=OUT[0]['fixed_functions'],outer_extra=OUT[0]['extra'],outer_upper_indices=OUT[0]['pos'],outer_feature_count=OUT[0]['X'].shape[1],inner=[dict(m=z['m'],anchor=z['key'],extra=z['extra'],upper_indices=z['pos'],feature_count=z['X'].shape[1])for z in INS]),'SIGNS_AND_FEATURES.json')
 print('DOMAINS',len(T18),len(ST),len(a40),len(nc),[(m,sum(z['m']==m for z in INS),sum(len(z['X'])for z in INS if z['m']==m))for m in TIERS+[106]],len(OUT[0]['X']),flush=True)
 SAVE({'lower':[{'m':z['m'],'type':z['key'],'empty':z['empty'],'count':0 if z['empty']else len(z['X'])}for z in ALL],'spectra18':ST,'anchor_order40':ORDER40,'ordinary5D_pruning':PRUNING},'all_case_coverage.json')
 pofs={};bofs={};off=0;bounds=[]
 for m in TIERS+[106]:pofs[m]=off;off+=len(TS[m]);bounds +=[(-1,1)]*len(TS[m]);bofs[m]=off;off+=1;bounds.append((None,None))
 for name in COND_FUNCTIONS:pofs[name]=off;off+=len(T18);bounds +=[(-1,1)]*len(T18)
 for name in COND_BOUNDS:bofs[name]=off;off+=1;bounds.append((None,None))
 for name,l in LEAF.items():pofs[name]=off;off+=len(TS[l['m']]);bounds +=[(-1,1)]*len(TS[l['m']]);bofs[name]=off;off+=1;bounds.append((None,None))
 for z in INS+OUT:z['offset']=off;off+=z['X'].shape[1];bounds +=[(0,1)if j in z['pos']else(-1,1)for j in range(z['X'].shape[1])]
 nv=off+1;dof=off;bounds.append((None,None));obj=np.zeros(nv);obj[-1]=-1
 for z in INS+OUT:z['inds']=np.unique(np.r_[np.argmin(z['W'],axis=0),np.argmax(z['W'],axis=0)])
 ff=[]
 for tier in TIERS:
  left=f't{tier}_left18';right=f't{tier}_right18';cond=f't{tier}_cond18';pair=f't{tier}_pair18'
  rr=np.zeros((len(PAIR),nv))
  for i,(a,b)in enumerate(PAIR):rr[i,pofs[left]:pofs[left]+len(T18)]=H18[a];rr[i,pofs[right]:pofs[right]+len(T18)]=H18[b]
  rr[:,bofs[pair]]=-40;ff.append(sparse.csr_matrix(rr));rr=np.zeros((len(COND),nv));rr[:,pofs[cond]:pofs[cond]+len(T18)]=H18[COND];rr[:,bofs[cond]]=-40;ff.append(sparse.csr_matrix(rr))
 for name,l in LEAF.items():
  hh={16:H16,17:H17,18:H18,41:H41,42:H42}[l['m']];rr=np.zeros((len(hh),nv));rr[:,pofs[name]:bofs[name]]=hh;rr[:,bofs[name]]=-ND[l['m']];ff.append(sparse.csr_matrix(rr))
 finite=sparse.vstack(ff,format='csr');assert finite.shape[0]==15885 and nv==3291
 assert sum(l['m']==42 for l in LEAF.values())==6
 assert len(base40)==44 and len(a40)==132 and len(nc)==14
 assert all(sum(len(z['X'])for z in INS if z['m']==m)==36455 for m in TIERS)
 assert {m:sum(l['m']==m for l in LEAF.values())for m in [16,17,18,41,42]}=={16:30,17:30,18:24,41:6,42:6}
 parent_occ=[dict(parent_anchor=z['key'],function=parent,column=col)for z in nc for parent,ids,col in z['deps']if parent in TIERS]
 assert parent_occ==[dict(parent_anchor=TIER_PARENT[m],function=m,column=1)for m in TIERS]
 assert len(set(z['offset']for z in INS+OUT))==len(INS+OUT)
 assert len(set(pofs[n]for n in COND_FUNCTIONS))==9 and len(set(bofs[n]for n in COND_BOUNDS))==6
 realized={'tier_mapping':{m:dict(mathematical_size=40,parent=t,physical_column=1)for m,t in TIER_PARENT.items()},'parent_occurrences':parent_occ,'main_offsets':{m:[pofs[m],bofs[m]]for m in TIERS+[106]},'conditional_function_offsets':{n:pofs[n]for n in COND_FUNCTIONS},'conditional_bound_offsets':{n:bofs[n]for n in COND_BOUNDS},'case_coefficients':[dict(function=z['m'],anchor=z['key'],offset=z['offset'],width=z['X'].shape[1])for z in INS],'leaf_functions':LEAF,'variables':nv,'finite_support_rows':finite.shape[0]}
 SAVE(realized,'REALIZED_COPY_LAYOUT.json')
 planned=json.loads((W/'PLANNED_COPY_LAYOUT.json').read_text());assert json.loads(json.dumps(LEAF))==planned['leaf_functions']
 for name,sha in source_inputs['source_hashes'].items():assert hashlib.sha256((ROOTDIR/name).read_bytes()).hexdigest()==sha

 SAVE(dict(status='EXACT_REPAIR_LAYOUT_MATCH',finite_rows=finite.shape[0],variables=nv,physical41_supports=[dict(id=n,**l)for n,l in LEAF.items()if l['m']==41],physical42_supports=[dict(id=n,**l)for n,l in LEAF.items()if l['m']==42],ordinary5D_pruning=PRUNING,domain_reconstruction_elapsed=time.monotonic()-start),'interface_check.json')
 if '--check-only' in sys.argv:return
 checkpoint_path=ROOTDIR/'compatibility/physical40_complete42_10610663/LAST_FLOAT_CHECKPOINT.json'
 checkpoint=json.loads(checkpoint_path.read_text());sol=np.array(checkpoint['values'],float)
 assert len(sol)==nv and np.isfinite(sol).all()
 reason='FIXED_CHECKPOINT_EXACT_BOTTOM_UP_REPAIR';repairs=[]
 report=dict(tier_mapping={m:dict(mathematical_size=40,parent=t,physical_column=1)for m,t in TIER_PARENT.items()},target=[106,106,63],empty_cases=empty,counts=[dict(m=z['m'],type=z['key'],count=len(z['X']))for z in INS],outer_count=len(OUT[0]['X']),numerical_status=reason,claim='NO_NEW_MATH',checkpoint_sha256=hashlib.sha256(checkpoint_path.read_bytes()).hexdigest(),checkpoint_iteration=checkpoint['iteration'],scales=[10**i for i in range(10,15)],repairs=repairs,optimizer_calls=0)
 if sol is not None:
  floats=sol.copy()
  for z in INS+OUT:floats[z['offset']:z['offset']+z['X'].shape[1]]/=z['scale']
  for i in bofs.values():floats[i]=0
  floats[-1]=0
  for mul in [10**i for i in range(10,15)]:
   assert time.monotonic()-start<590
   assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<2147483648
   assert np.max(abs(floats))*mul<8*10**18
   current_ceiling=0
   qi=np.rint(floats*mul).astype(np.int64);hist={};safe=True;local={}
   for name,l in LEAF.items():
    ph=qi[pofs[name]:bofs[name]];hh={16:H16,17:H17,18:H18,41:H41,42:H42}[l['m']]
    local[name]=dict(l,types=TS[l['m']],phi=list(map(int,ph)),bound=max(sum(int(a)*int(b)for a,b in zip(h,ph))for h in hh))
   conditional={fn:list(map(int,qi[pofs[fn]:pofs[fn]+len(T18)]))for fn in COND_FUNCTIONS}
   cbounds={}
   for tier in TIERS:
    left=f't{tier}_left18';right=f't{tier}_right18';cond=f't{tier}_cond18';pair=f't{tier}_pair18'
    cbounds[pair]=max(sum(int(h)*int(v)for h,v in zip(H18[a],conditional[left]))+sum(int(h)*int(v)for h,v in zip(H18[b],conditional[right]))for a,b in PAIR)
    cbounds[cond]=max(sum(int(h)*int(v)for h,v in zip(H18[a],conditional[cond]))for a in COND)

   for m in TIERS+[106]:
    ph=qi[pofs[m]:bofs[m]];ic=[];bs=[]
    for z in [z for z in INS if z['m']==m]:
     q=qi[z['offset']:z['offset']+z['X'].shape[1]]
     if any(q[j]<0 for j in z['pos']):safe=False;break
     ceiling=sum(int(a)*int(b)for a,b in zip(np.max(abs(z['X']),axis=0),abs(q)))+3*max(map(abs,ph))+sum(max(map(abs,hist[parent]['phi']))for parent,ids,col in z['deps'])+sum(max(map(abs,conditional[fn]))for fn,ids,col in z['pairdeps'])+sum(max(map(abs,local[name]['phi']))for name,ids,col in z['leafdeps'])
     current_ceiling=max(current_ceiling,int(ceiling))
     if ceiling>8*10**18:safe=False;break
     vv=z['X']@q-ph[z['tops']].sum(axis=1)
     for parent,ids,col in z['deps']:vv+=np.array(hist[parent]['phi'],np.int64)[ids]
     for name,ids,col in z['leafdeps']:vv+=np.array(local[name]['phi'],np.int64)[ids]
     for fn,ids,col in z['pairdeps']:vv+=np.array(conditional[fn],np.int64)[ids]
     K=int(vv.min());bd=int(ph[z['anchor']])+sum(int(a)*int(b)for a,b in zip(q,z['F']))+sum(hist[parent]['bound']for parent,ids,col in z['deps'])+sum(local[name]['bound']for name,ids,col in z['leafdeps'])+(cbounds[z['pairbound']]if z['pairdeps']else 0)-D[m]*K;bs.append(bd);ic.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,bound=bd,extra=z['extra'],count=len(z['X']),dependencies=[dict(m=parent,column=col,coefficient=1)for parent,ids,col in z['deps']],class41=z.get('class41'),state18=z.get('state18'),full18_state=z.get('full18_state'),conditional_dependencies=[dict(function=fn,column=col,coefficient=1)for fn,ids,col in z['pairdeps']],conditional_bound=z.get('pairbound'),state8=z.get('state8'),local_supports=[dict(id=name,column=col,coefficient=1)for name,ids,col in z['leafdeps']]))
    if not safe:break
    hist[m]=dict(mathematical_size=106 if m==106 else 40,tier_parent=None if m==106 else TIER_PARENT[m],types=TS[m],phi=list(map(int,ph)),bound=max(bs),inner=ic,root=ROOT[106]if m==106 else'COMPLETE_FIRST_ANCHOR_CASE_COVER')
   if not safe:
    repairs.append(dict(scale=mul,status='ARITHMETIC_SAFETY_REJECTED',integer_product_ceiling=current_ceiling));SAVE(report,'PROGRESS.json');continue
   oc=[]
   for z in OUT:
    q=qi[z['offset']:z['offset']+z['X'].shape[1]]
    if any(q[j]<0 for j in z['pos']):safe=False;break
    ceiling=sum(int(a)*int(b)for a,b in zip(np.max(abs(z['X']),axis=0),abs(q)))+sum(max(map(abs,hist[m]['phi']))for m,ids in z['ids']);current_ceiling=max(current_ceiling,int(ceiling))
    if ceiling>8*10**18:safe=False;break
    vv=z['X']@q
    for m,ids in z['ids']:vv+=np.array(hist[m]['phi'],np.int64)[ids]
    K=int(vv.min());U=sum(int(a)*int(b)for a,b in zip(q,z['F']))+sum(hist[m]['bound']for m,ids in z['ids']);g=364*K-U;oc.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,forced=U,gap=g,count=len(z['X']),extra=z['extra'],fixed_functions=z['fixed_functions']))
   if not safe:
    repairs.append(dict(scale=mul,status='ARITHMETIC_SAFETY_REJECTED',integer_product_ceiling=current_ceiling));SAVE(report,'PROGRESS.json');continue
   repairs.append(dict(scale=mul,status='EXACT_COMPLETE_SIGNED_GAP',gaps=[r['gap']for r in oc],main_bounds={m:h['bound']for m,h in hist.items()},outer=oc,integer_product_ceiling=current_ceiling,elapsed=time.monotonic()-start));SAVE(report,'PROGRESS.json')
   print('INTEGER',mul,[r['gap']for r in oc],{m:h['bound']for m,h in hist.items()},'elapsed',time.monotonic()-start,flush=True)
   if all(r['gap']>0 for r in oc):report.update(claim='CANDIDATE_EXACT_CERTIFICATE',histograms=hist,outer=oc,upper5={name:dict(m=m,types=list(phi),phi=list(phi.values()),bound=bd)for name,(m,phi,bd)in (O.U5|R106.H4.NEW).items()},full18_states=ST,table1=json.loads((H/'h13/table1_input_v2.json').read_text()),conditional_functions=conditional,conditional_bounds=cbounds,conditional_types=T18,histogram_pair_capacity=CP,input17=INPUT17,actual17=ACTUAL17,actual16=ACTUAL16,complete41=ACTUAL41,complete42=ACTUAL42,ordinary5D_pruning=PRUNING,fixed6=FIXED6,local_supports=local);break
 for name,sha in source_inputs['source_hashes'].items():assert hashlib.sha256((ROOTDIR/name).read_bytes()).hexdigest()==sha
 report['elapsed']=time.monotonic()-start;report['recovery_scale']=repairs[-1]['scale']if report['claim']=='CANDIDATE_EXACT_CERTIFICATE'else None
 SAVE(report,'RESULT.json')
 frozen=dict(status=report['claim'],result_sha256=hashlib.sha256((W/'RESULT.json').read_bytes()).hexdigest(),checkpoint_sha256=report['checkpoint_sha256'],source_hashes={n:hashlib.sha256((W/n).read_bytes()).hexdigest()for n in ['run.py','verify.py','INPUTS.json','SCOPE.md','PLANNED_COPY_LAYOUT.json','REALIZED_COPY_LAYOUT.json']},elapsed=report['elapsed'],scales_attempted=[v['scale']for v in repairs],optimizer_calls=0)
 SAVE(frozen,'CANDIDATE_FROZEN.json'if report['claim']=='CANDIDATE_EXACT_CERTIFICATE'else'TERMINAL_FROZEN.json');print('RESULT',report['claim'],frozen['result_sha256'],flush=True)
if __name__=='__main__':main()
