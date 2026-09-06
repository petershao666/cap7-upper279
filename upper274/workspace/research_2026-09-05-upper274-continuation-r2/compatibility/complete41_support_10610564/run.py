import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import hashlib
import sys,importlib.util
from pathlib import Path
W=Path(__file__).resolve().parent;H=W.parents[1]/'hist105106';sys.path.insert(0,str(H));sys.path.insert(0,str(H/'h3'))
sys.dont_write_bytecode=True
os.environ['NUMBA_CACHE_DIR']=str(W/'numba_cache')
_original_write_text=Path.write_text
def _owned_write_text(path,data,*args,**kwargs):
 resolved=path.resolve()
 if not resolved.is_relative_to(W):
  assert resolved.is_relative_to(W.parents[1]),resolved
  path=W/'redirected'/resolved.relative_to(W.parents[1]);path.parent.mkdir(parents=True,exist_ok=True)
 return _original_write_text(path,data,*args,**kwargs)
Path.write_text=_owned_write_text
import joint as J
from joint import np,O,E,V,C,OLD,COMP,ANCH,SUP,ROOT,SEEDS,T,Q,en,signal,limit,math,json,itertools,time,sparse,linprog,R
import structural40 as S40
sp=importlib.util.spec_from_file_location('h11_readonly_pair',H/'h11/actualpair.py');R41=importlib.util.module_from_spec(sp);sp.loader.exec_module(R41);R41.W=W
sp=importlib.util.spec_from_file_location('h11_readonly_run',H/'h11/single.py');R106=importlib.util.module_from_spec(sp);sp.loader.exec_module(R106)
SAVE=lambda z,n:(W/n).write_text(json.dumps(z,indent=2)+'\n')
ST=json.loads((H/'h10/full18_states.json').read_text());T18=sorted({tuple(t)for h in ST for t in h['types']});IX18={t:i for i,t in enumerate(T18)}
TS={18:T18,40:S40.D.SUP40,41:R106.T41,106:SUP[106]};ND={18:40,40:121,41:121,106:364};D={40:40,41:40,106:121}
CP=json.loads((H/'h13/histogram_pair_capacity_v2.json').read_text());PAIR=CP['allowed_18184_ordered_pairs'];COND=CP['allowed_20182_full18_states']
ORDER40=list(reversed(S40.D.SUP40))
H18=np.array([[dict(zip(map(tuple,h['types']),h['histogram'])).get(t,0)for t in T18]for h in ST],np.int64)

INPUT17=json.loads((H/'h16/input.json').read_text());T17=list(map(tuple,INPUT17['direction_types17']));IX17={t:i for i,t in enumerate(T17)};ANCH17=list(map(tuple,INPUT17['anchor_order17']))
TS[17]=T17;ND[17]=40;D[17]=13
MODEL_INPUT=json.loads((W/'MODEL_INPUT.json').read_text());assert MODEL_INPUT['root_accepted'] is True
_packet_path=W.parents[1]/MODEL_INPUT['input41_path'];assert hashlib.sha256(_packet_path.read_bytes()).hexdigest()==MODEL_INPUT['input41_sha256']
ACTUAL41=json.loads(_packet_path.read_text());assert ACTUAL41['status']=='ACCEPTED_COMPLETE_5D41_HISTOGRAM_FAMILY_WITH_PUBLISHED_PREMISES'
TS[41]=list(map(tuple,ACTUAL41['types']));H41=np.array([h['counts']for h in ACTUAL41['histograms']],np.int64);assert H41.shape==(44,40)
assert all(sum(map(int,h))==121 and sum(int(v)*(a*b+a*c+b*c)for v,(a,b,c)in zip(h,TS[41]))==66420 and sum(int(v)*a*b*c for v,(a,b,c)in zip(h,TS[41]))==287820 for h in H41)
assert all(not H41[:,TS[41].index(t)].any()for t in [(20,19,2),(20,18,3),(19,19,3),(19,18,4)])
M17={(a*b+a*c+b*c,a*b*c):i for i,(a,b,c)in enumerate(T17)};assert len(M17)==len(T17)
ACTUAL16=json.loads((W.parents[1]/'root_audit/actual16/ACCEPTED_HISTOGRAMS.json').read_text());T16=list(map(tuple,ACTUAL16['types']));H16=np.array(ACTUAL16['histograms'],np.int64);assert H16.shape==(376,14)
TS[16]=T16;ND[16]=40;D[16]=13
M16={(a*b+a*c+b*c,a*b*c):i for i,(a,b,c)in enumerate(T16)};assert len(M16)==14
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

def inner106(key,i):
 z=R106.inner106(key,i);ix={t:j for j,t in enumerate(SUP[106])};index=np.full((46,46),-1,np.int64)
 for t,j in ix.items():index[t[:2]]=j
 ar=O.ien(*key,J.ADM5,E.make_top(45,106,np.array(OLD+COMP+ANCH[106][:i],np.int64)),index);assert len(ar)==len(z['X']);z['deps']=[]
 for j,N in enumerate(key):
  if N in(40,41):
   mp={t:k for k,t in enumerate(TS[N])};z['deps'].append((N,np.array([mp[tuple(t)]for t in ar[:,7+3*j:10+3*j]],np.int32),j))
 return z

def localize_supports(INS):
 leaves={}
 for ci,z in enumerate(INS):
  keep=[];z['leafdeps']=[]
  for parent,ids,col in z['deps']:
   if parent in(16,17,18,41):
    name=f"support_{z['m']}_{ci}_c{col}_n{parent}"
    leaves[name]=dict(m=parent,case_index=ci,case_dimension_size=z['m'],anchor=z['key'],column=col,class41=z.get('class41'),full18_state=z.get('full18_state'))
    z['leafdeps'].append((name,ids,col))
   else:keep.append((parent,ids,col))
  z['deps']=keep
 return leaves

FIXED6=json.loads((W.parents[1]/'compatibility/r105_fixed_outer/FUNCTIONS.json').read_text())
def outer_new(key,ban):
 z=J.outer(key,ban);X=z['X'];F=list(z['F']);extra=[];pos=[]
 used=[]
 for col,(m,ids)in enumerate(z['ids']):
  for fn in FIXED6['functions']:
   if fn['size']!=m:continue
   lut=dict(zip(map(tuple,fn['types']),fn['values']))
   vals=np.array([lut[t]for t in SUP[m]],np.int64)[ids]
   X=np.c_[X,vals];pos.append(len(F));F.append(fn['bound']);extra.append((col,'fixed6_upper',fn['id'],fn['bound']));used.append(dict(column=col,**fn))
 z['ids']=[(m,ids)for m,ids in z['ids']if m==106];assert len(z['ids'])==1
 F=np.array(F,np.int64);scale=np.maximum(np.max(abs(X-F/364),axis=0),1)
 z.update(X=X,F=F,scale=scale,W=(X-F/364)/scale,pos=pos,extra=extra,fixed_functions=used)
 return z

def main():
 source_inputs=json.loads((W/'INPUTS.json').read_text())
 for name,sha in source_inputs['source_hashes'].items():assert hashlib.sha256((W.parents[1]/name).read_bytes()).hexdigest()==sha
 activation=json.loads((W/'ACTIVATION.json').read_text());assert activation['root_authorized'] is True and activation['target']==[106,105,64]
 signal.signal(signal.SIGALRM,limit);start=time.monotonic()-(time.time()-activation['started_unix']);assert time.monotonic()-start<580;signal.alarm(max(1,int(590-(time.monotonic()-start))));old=json.loads((R/'certificates.json').read_text());ban=SEEDS+[(112,109,51),(111,110,51)]+[V.parse_key(k)for s in old['stages']for k in s]
 a40=[low40(t,i)for i,t in enumerate(ORDER40)];a41=[];ALL=a40
 INS=[z for z in ALL if not z['empty']]+[inner106(t,i)for i,t in enumerate(ANCH[106])]
 for z in INS:z.setdefault('deps',[]);z.setdefault('pairdeps',[])
 LEAF=localize_supports(INS);SAVE(LEAF,'local_support_layout.json');print('LOCAL_SUPPORTS',len(LEAF),{m:sum(l['m']==m for l in LEAF.values())for m in[16,17,18,41]},flush=True)
 assert set(ban)==set(map(tuple,FIXED6['ordinary_bans'])) and len(ban)==18
 ban=list(map(tuple,FIXED6['ordinary_bans']))
 OUT=[outer_new((106,105,64),ban)];empty=[dict(m=z['m'],type=z['key'],class41=z.get('class41'),full18_state=z.get('full18_state'),state18=z.get('state18'),state8=z.get('state8'))for z in ALL if z['empty']]
 print('DOMAINS',len(T18),len(ST),len(a40),len(a41),[(m,sum(z['m']==m for z in INS),sum(len(z['X'])for z in INS if z['m']==m))for m in[40,106]],len(OUT[0]['X']),flush=True)
 SAVE({'lower':[{'m':z['m'],'type':z['key'],'class41':z.get('class41'),'full18_state':z.get('full18_state'),'state8':z.get('state8'),'empty':z['empty'],'count':0 if z['empty']else len(z['X'])}for z in ALL],'spectra18':ST,'anchor_order40':ORDER40},'all_case_coverage.json')
 assert len(a40)==44 and len(a41)==0 and sum(len(z['X'])for z in INS if z['m']==40)==36455 and sum(len(z['X'])for z in INS if z['m']==106)==95343 and len(OUT[0]['X'])==2571792
 assert {m:sum(l['m']==m for l in LEAF.values())for m in[16,17,18,41]}=={16:10,17:10,18:8,41:6}
 assert [(tuple(l['anchor']),l['column'])for l in LEAF.values()if l['m']==41]==[((41,41,24),0),((41,41,24),1),((42,41,23),1),((43,41,22),1),((44,41,21),1),((45,41,20),1)]
 for name,sha in source_inputs['source_hashes'].items():assert hashlib.sha256((W.parents[1]/name).read_bytes()).hexdigest()==sha
 SAVE({'status':'ACCEPTED_INPUT_INTERFACE_PASS_NO_OPTIMIZATION_YET','input41':MODEL_INPUT,'case_features':[dict(m=z.get('m',275),key=z['key'],feature_count=len(z['F']),features=z['extra'],upper_indices=z['pos'],count=len(z['X']))for z in INS+OUT],'optimizations_run':0,'elapsed':time.monotonic()-start},'INTERFACE_CHECK.json')
 if '--precheck-only' in sys.argv:return
 pofs={};bofs={};off=0;bounds=[]
 for m in [40,106]:pofs[m]=off;off+=len(TS[m]);bounds +=[(-1,1)]*len(TS[m]);bofs[m]=off;off+=1;bounds.append((None,None))
 for name in ['left18','right18','cond18']:pofs[name]=off;off+=len(T18);bounds +=[(-1,1)]*len(T18)
 for name in ['pair18','cond18']:bofs[name]=off;off+=1;bounds.append((None,None))
 for name,l in LEAF.items():pofs[name]=off;off+=len(TS[l['m']]);bounds +=[(-1,1)]*len(TS[l['m']]);bofs[name]=off;off+=1;bounds.append((None,None))
 for z in INS+OUT:z['offset']=off;off+=z['X'].shape[1];bounds +=[(0,1)if j in z['pos']else(-1,1)for j in range(z['X'].shape[1])]
 nv=off+1;dof=off;bounds.append((None,None));obj=np.zeros(nv);obj[-1]=-1
 for z in INS+OUT:z['inds']=np.unique(np.r_[np.argmin(z['W'],axis=0),np.argmax(z['W'],axis=0)])
 ff=[];rr=np.zeros((len(PAIR),nv))
 for i,(a,b)in enumerate(PAIR):rr[i,pofs['left18']:pofs['left18']+len(T18)]=H18[a];rr[i,pofs['right18']:pofs['right18']+len(T18)]=H18[b]
 rr[:,bofs['pair18']]=-40;ff.append(sparse.csr_matrix(rr));rr=np.zeros((len(COND),nv));rr[:,pofs['cond18']:pofs['cond18']+len(T18)]=H18[COND];rr[:,bofs['cond18']]=-40;ff.append(sparse.csr_matrix(rr));
 for name,l in LEAF.items():
  hh={16:H16,17:H17,18:H18,41:H41}[l['m']];rr=np.zeros((len(hh),nv));rr[:,pofs[name]:bofs[name]]=hh;rr[:,bofs[name]]=-ND[l['m']];ff.append(sparse.csr_matrix(rr))
 finite=sparse.vstack(ff,format='csr');assert finite.shape[0]==5463;SAVE({'variables':nv,'fixed_support_rows':finite.shape[0],'unfiltered_domains':True},'MODEL_SIZE.json')
 sol=None;reason='ITERATION_LIMIT';history=[]
 for it in range(220):
  chunks=[finite]
  for z in INS:
   ii=z['inds'];m=z['m'];rr=np.zeros((len(ii),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W'][ii]
   for j in range(3):rr[np.arange(len(ii)),pofs[m]+z['tops'][ii,j]]+=1
   rr[:,pofs[m]+z['anchor']]+=1/D[m];rr[:,bofs[m]]=-ND[m]/D[m]
   for parent,ids,col in z['deps']:rr[np.arange(len(ii)),pofs[parent]+ids[ii]]-=1;rr[:,bofs[parent]]+=1
   for name,ids,col in z['leafdeps']:rr[np.arange(len(ii)),pofs[name]+ids[ii]]-=1;rr[:,bofs[name]]+=1
   for fn,ids,col in z['pairdeps']:rr[np.arange(len(ii)),pofs[fn]+ids[ii]]-=1
   if z['pairdeps']:rr[:,bofs[z['pairbound']]]+=1
   chunks.append(sparse.csr_matrix(rr))
  for z in OUT:
   ii=z['inds'];rr=np.zeros((len(ii),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W'][ii]
   for m,ids in z['ids']:rr[np.arange(len(ii)),pofs[m]+ids[ii]]-=1;rr[:,bofs[m]]+=1
   rr[:,dof]=1;chunks.append(sparse.csr_matrix(rr))
  if time.monotonic()-start>=550:reason='BATCH_WALL_LIMIT';break
  A=sparse.vstack(chunks,format='csr');res=linprog(obj,A_ub=A,b_ub=np.zeros(A.shape[0]),bounds=bounds,method='highs',options={'time_limit':max(1,min(90,570-(time.monotonic()-start)))})
  if not res.success:reason=res.message;break
  x=res.x;gap=x[-1];done=True;inmin=0;mins=[]
  for z in INS:
   m=z['m'];vals=z['W']@x[z['offset']:z['offset']+z['X'].shape[1]]+ND[m]*x[bofs[m]]/D[m]-x[pofs[m]+z['anchor']]/D[m]
   for j in range(3):vals-=x[pofs[m]+z['tops'][:,j]]
   for parent,ids,col in z['deps']:vals+=x[pofs[parent]+ids]-x[bofs[parent]]
   for name,ids,col in z['leafdeps']:vals+=x[pofs[name]+ids]-x[bofs[name]]
   for fn,ids,col in z['pairdeps']:vals+=x[pofs[fn]+ids]
   if z['pairdeps']:vals-=x[bofs[z['pairbound']]]
   inmin=min(inmin,float(vals.min()))
   if vals.min()<-1e-8:done=False;add=np.argpartition(vals,min(19,len(vals)-1))[:20];z['inds']=np.unique(np.r_[z['inds'],add])
  for z in OUT:
   vals=z['W']@x[z['offset']:z['offset']+z['X'].shape[1]]
   for m,ids in z['ids']:vals+=x[pofs[m]+ids]-x[bofs[m]]
   mins.append(float(vals.min()))
   if vals.min()<gap-1e-8:done=False;add=np.argpartition(vals,min(29,len(vals)-1))[:30];z['inds']=np.unique(np.r_[z['inds'],add])
  print('ITER',it,'rows',A.shape[0],'delta',gap,'inner_min',inmin,'outer_min',mins,'elapsed',round(time.monotonic()-start,2),flush=True);history.append(dict(iteration=it,rows=A.shape[0],delta=gap,inner_min=inmin,outer_min=mins))
  if gap<1e-8:reason='COMPLETE41_PHYSICAL_SUPPORT_NO_POSITIVE_DUAL';break
  if done:sol=x;reason='POSITIVE_FLOAT_CANDIDATE';break
 report=dict(target=[106,105,64],empty_cases=empty,counts=[dict(m=z['m'],type=z['key'],count=len(z['X']))for z in INS],outer_count=len(OUT[0]['X']),iterations=it+1,numerical_status=reason,claim='NO_NEW_MATH',elapsed=time.monotonic()-start,history=history)
 if sol is not None:
  floats=sol.copy()
  for z in INS+OUT:floats[z['offset']:z['offset']+z['X'].shape[1]]/=z['scale']
  for mul in [10**i for i in range(4,17)]:
   qi=np.rint(floats*mul).astype(np.int64);hist={};safe=True;local={}
   for name,l in LEAF.items():
    ph=qi[pofs[name]:bofs[name]];hh={16:H16,17:H17,18:H18,41:H41}[l['m']]
    local[name]=dict(l,types=TS[l['m']],phi=list(map(int,ph)),bound=max(sum(int(a)*int(b)for a,b in zip(h,ph))for h in hh))
   conditional={fn:list(map(int,qi[pofs[fn]:pofs[fn]+len(T18)]))for fn in ['left18','right18','cond18']}
   cbounds={'pair18':max(sum(int(h)*int(v)for h,v in zip(H18[a],conditional['left18']))+sum(int(h)*int(v)for h,v in zip(H18[b],conditional['right18']))for a,b in PAIR),'cond18':max(sum(int(h)*int(v)for h,v in zip(H18[a],conditional['cond18']))for a in COND)}
   for m in [40,106]:
    ph=qi[pofs[m]:bofs[m]];ic=[];bs=[]
    for z in [z for z in INS if z['m']==m]:
     q=qi[z['offset']:z['offset']+z['X'].shape[1]]
     assert all(q[j]>=0 for j in z['pos'])
     ceiling=sum(int(a)*int(b)for a,b in zip(np.max(abs(z['X']),axis=0),abs(q)))+3*max(map(abs,ph))+sum(max(map(abs,hist[parent]['phi']))for parent,ids,col in z['deps'])+sum(max(map(abs,conditional[fn]))for fn,ids,col in z['pairdeps'])+sum(max(map(abs,local[name]['phi']))for name,ids,col in z['leafdeps'])
     if ceiling>8*10**18:safe=False;break
     vv=z['X']@q-ph[z['tops']].sum(axis=1)
     for parent,ids,col in z['deps']:vv+=np.array(hist[parent]['phi'],np.int64)[ids]
     for name,ids,col in z['leafdeps']:vv+=np.array(local[name]['phi'],np.int64)[ids]
     for fn,ids,col in z['pairdeps']:vv+=np.array(conditional[fn],np.int64)[ids]
     K=int(vv.min());bd=int(ph[z['anchor']])+sum(int(a)*int(b)for a,b in zip(q,z['F']))+sum(hist[parent]['bound']for parent,ids,col in z['deps'])+sum(local[name]['bound']for name,ids,col in z['leafdeps'])+(cbounds[z['pairbound']]if z['pairdeps']else 0)-D[m]*K;bs.append(bd);ic.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,bound=bd,extra=z['extra'],count=len(z['X']),dependencies=[dict(m=parent,column=col,coefficient=1)for parent,ids,col in z['deps']],class41=z.get('class41'),state18=z.get('state18'),full18_state=z.get('full18_state'),conditional_dependencies=[dict(function=fn,column=col,coefficient=1)for fn,ids,col in z['pairdeps']],conditional_bound=z.get('pairbound'),state8=z.get('state8'),local_supports=[dict(id=name,column=col,coefficient=1)for name,ids,col in z['leafdeps']]))
    if not safe:break
    hist[m]=dict(types=TS[m],phi=list(map(int,ph)),bound=max(bs),inner=ic,root=ROOT[106]if m==106 else'COMPLETE_FIRST_ANCHOR_CASE_COVER')
   if not safe:continue
   oc=[]
   for z in OUT:
    q=qi[z['offset']:z['offset']+z['X'].shape[1]]
    assert all(q[j]>=0 for j in z['pos'])
    if sum(int(a)*int(b)for a,b in zip(np.max(abs(z['X']),axis=0),abs(q)))+sum(max(map(abs,hist[m]['phi']))for m,ids in z['ids'])>8*10**18:safe=False;break
    vv=z['X']@q
    for m,ids in z['ids']:vv+=np.array(hist[m]['phi'],np.int64)[ids]
    K=int(vv.min());U=sum(int(a)*int(b)for a,b in zip(q,z['F']))+sum(hist[m]['bound']for m,ids in z['ids']);g=364*K-U;oc.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,forced=U,gap=g,count=len(z['X'])))
   if not safe:continue
   print('INTEGER',mul,[r['gap']for r in oc],flush=True)
   if all(r['gap']>0 for r in oc):report.update(claim='CANDIDATE_EXACT_CERTIFICATE',histograms=hist,outer=oc,upper5={name:dict(m=m,types=list(phi),phi=list(phi.values()),bound=bd)for name,(m,phi,bd)in (O.U5|R106.H4.NEW).items()},full18_states=ST,named_pair_input=R41.IN,table1=json.loads((H/'h13/table1_input_v2.json').read_text()),conditional_functions=conditional,conditional_bounds=cbounds,conditional_types=T18,histogram_pair_capacity=CP,input17=INPUT17,actual17=ACTUAL17,actual16=ACTUAL16,actual41=ACTUAL41,input41=MODEL_INPUT,local_supports=local,fixed6_functions=OUT[0]['fixed_functions'],ordinary_bans=ban);break
 report.update(input41=MODEL_INPUT,actual41_histogram_count=44,actual41_support_count=6)
 for name,sha in source_inputs['source_hashes'].items():assert hashlib.sha256((W.parents[1]/name).read_bytes()).hexdigest()==sha
 SAVE(report,'RESULT.json');print('RESULT',report['claim'],reason,flush=True)
if __name__=='__main__':main()
