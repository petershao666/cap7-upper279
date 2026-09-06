import sys,importlib.util
from pathlib import Path
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W.parent));sys.path.insert(0,str(W.parent/'h3'))
import joint as J
from joint import np,O,E,V,C,OLD,COMP,ANCH,SUP,ROOT,SEEDS,T,Q,en,signal,limit,math,json,itertools,time,sparse,linprog,R
import structural40 as S40
sp=importlib.util.spec_from_file_location('h11_readonly_pair',W.parent/'h11/actualpair.py');R41=importlib.util.module_from_spec(sp);sp.loader.exec_module(R41);R41.W=W
sp=importlib.util.spec_from_file_location('h11_readonly_run',W.parent/'h11/single.py');R106=importlib.util.module_from_spec(sp);sp.loader.exec_module(R106)
SAVE=lambda z,n:(W/n).write_text(json.dumps(z,indent=2)+'\n')
ST=json.loads((W.parent/'h10/full18_states.json').read_text());T18=sorted({tuple(t)for h in ST for t in h['types']});IX18={t:i for i,t in enumerate(T18)}
TS={18:T18,40:S40.D.SUP40,41:R106.T41,106:SUP[106]};ND={18:40,40:121,41:121,106:364};D={40:40,41:40,106:121}
H18=np.array([[dict(zip(map(tuple,h['types']),h['histogram'])).get(t,0)for t in T18]for h in ST],np.int64)

def base40(key,i):
 ix=np.full((21,21),-1,np.int64)
 for t,j in S40.D.IX40.items():ix[t[:2]]=j
 top=E.make_top(20,40,np.array(S40.D.SUP40[:i],np.int64).reshape(-1,3));ar=S40.raw_enum(*key,S40.D.A4,top,ix);ar=ar[S40.filter_clashes(ar,S40.PS)]
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
 return dict(m=40,key=key,X=X,F=F,W=(X-F/40)/sc,scale=sc,extra=extra,pos=pos,deps=deps,tops=ar[:,16:19].copy(),anchor=S40.D.IX40[key],empty=False)

CP=json.loads((W/'histogram_pair_capacity_v2.json').read_text())

def low40_states(key,i):
 base=base40(key,i);cols=[j for j,N in enumerate(key)if N==18]
 if key==(18,18,4):states=CP['allowed_18184_ordered_pairs']
 elif key==(20,18,2):states=[(a,)for a in CP['allowed_20182_full18_states']]
 else:states=list(itertools.product(range(17),repeat=len(cols)))
 out=[]
 for states18 in states:
  fs=[None]*3
  for col,hid in zip(cols,states18):fs[col]=int(hid)
  metadata=dict(m=40,key=key,full18_state=fs,state18=[None if h is None else ST[h]['partial']for h in fs],class41=None)
  if base['empty']:out.append(dict(metadata,empty=True));continue
  keep=np.ones(len(base['X']),bool)
  for parent,ids,col in base['deps']:keep &= H18[fs[col],ids]>0
  if not keep.any():out.append(dict(metadata,empty=True));continue
  X=base['X'][keep].copy();F=list(map(int,base['F']));extra=list(base['extra']);pos=list(base['pos'])
  for parent,ids,col in base['deps']:
   h=H18[fs[col]]
   for ti,bd in enumerate(h):
    if bd:X=np.c_[X,(ids[keep]==ti).astype(np.int64)];F.append(int(bd));extra.append((col,'exact_full18',T18[ti],int(bd)))
  F=np.array(F,np.int64);sc=np.maximum(np.max(abs(X-F/40),axis=0),1)
  out.append(dict(metadata,X=X,F=F,W=(X-F/40)/sc,scale=sc,extra=extra,pos=pos,deps=[],tops=base['tops'][keep].copy(),anchor=base['anchor'],empty=False))
 return out

def inner106(key,i):
 z=R106.inner106(key,i);ix={t:j for j,t in enumerate(SUP[106])};index=np.full((46,46),-1,np.int64)
 for t,j in ix.items():index[t[:2]]=j
 ar=O.ien(*key,J.ADM5,E.make_top(45,106,np.array(OLD+COMP+ANCH[106][:i],np.int64)),index);assert len(ar)==len(z['X']);z['deps']=[]
 for j,N in enumerate(key):
  if N in(40,41):
   mp={t:k for k,t in enumerate(TS[N])};z['deps'].append((N,np.array([mp[tuple(t)]for t in ar[:,7+3*j:10+3*j]],np.int32),j))
 return z

def main():
 signal.signal(signal.SIGALRM,limit);signal.alarm(590);start=time.monotonic();old=json.loads((R/'certificates.json').read_text());ban=SEEDS+[(112,109,51),(111,110,51)]+[V.parse_key(k)for s in old['stages']for k in s]
 a40=[z for i,t in enumerate(TS[40])for z in low40_states(t,i)];assert len(a40)==453;a41=R41.all_branches();assert len(a41)==58;ALL=a40+a41
 INS=[z for z in ALL if not z['empty']]+[inner106(t,i)for i,t in enumerate(ANCH[106])]
 for z in INS:z.setdefault('deps',[])
 OUT=[J.outer((106,106,63),ban)];empty=[dict(m=z['m'],type=z['key'],class41=z.get('class41'),full18_state=z.get('full18_state'),state18=z.get('state18'))for z in ALL if z['empty']]
 print('DOMAINS',len(T18),len(ST),len(a40),len(a41),[(m,sum(z['m']==m for z in INS),sum(len(z['X'])for z in INS if z['m']==m))for m in[40,41,106]],len(OUT[0]['X']),flush=True)
 SAVE({'lower':[{'m':z['m'],'type':z['key'],'class41':z.get('class41'),'full18_state':z.get('full18_state'),'empty':z['empty'],'count':0 if z['empty']else len(z['X'])}for z in ALL],'spectra18':ST},'all_case_coverage.json')
 pofs={};bofs={};off=0;bounds=[]
 for m in [40,41,106]:pofs[m]=off;off+=len(TS[m]);bounds +=[(-1,1)]*len(TS[m]);bofs[m]=off;off+=1;bounds.append((None,None))
 for z in INS+OUT:z['offset']=off;off+=z['X'].shape[1];bounds +=[(0,1)if j in z['pos']else(-1,1)for j in range(z['X'].shape[1])]
 nv=off+1;dof=off;bounds.append((None,None));obj=np.zeros(nv);obj[-1]=-1
 for z in INS+OUT:z['inds']=np.unique(np.r_[np.argmin(z['W'],axis=0),np.argmax(z['W'],axis=0)])
 finite=sparse.csr_matrix((0,nv))
 sol=None;reason='ITERATION_LIMIT';history=[]
 for it in range(220):
  chunks=[finite]
  for z in INS:
   ii=z['inds'];m=z['m'];rr=np.zeros((len(ii),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W'][ii]
   for j in range(3):rr[np.arange(len(ii)),pofs[m]+z['tops'][ii,j]]+=1
   rr[:,pofs[m]+z['anchor']]+=1/D[m];rr[:,bofs[m]]=-ND[m]/D[m]
   for parent,ids,col in z['deps']:rr[np.arange(len(ii)),pofs[parent]+ids[ii]]-=1;rr[:,bofs[parent]]+=1
   chunks.append(sparse.csr_matrix(rr))
  for z in OUT:
   ii=z['inds'];rr=np.zeros((len(ii),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W'][ii]
   for m,ids in z['ids']:rr[np.arange(len(ii)),pofs[m]+ids[ii]]-=1;rr[:,bofs[m]]+=1
   rr[:,dof]=1;chunks.append(sparse.csr_matrix(rr))
  if time.monotonic()-start>=550:reason='BATCH_WALL_LIMIT';break
  A=sparse.vstack(chunks,format='csr');res=linprog(obj,A_ub=A,b_ub=np.zeros(A.shape[0]),bounds=bounds,method='highs',options={'time_limit':max(1,min(120,570-(time.monotonic()-start)))})
  if not res.success:reason=res.message;break
  x=res.x;gap=x[-1];done=True;inmin=0;mins=[]
  for z in INS:
   m=z['m'];vals=z['W']@x[z['offset']:z['offset']+z['X'].shape[1]]+ND[m]*x[bofs[m]]/D[m]-x[pofs[m]+z['anchor']]/D[m]
   for j in range(3):vals-=x[pofs[m]+z['tops'][:,j]]
   for parent,ids,col in z['deps']:vals+=x[pofs[parent]+ids]-x[bofs[parent]]
   inmin=min(inmin,float(vals.min()))
   if vals.min()<-1e-8:done=False;add=np.argpartition(vals,min(19,len(vals)-1))[:20];z['inds']=np.unique(np.r_[z['inds'],add])
  for z in OUT:
   vals=z['W']@x[z['offset']:z['offset']+z['X'].shape[1]]
   for m,ids in z['ids']:vals+=x[pofs[m]+ids]-x[bofs[m]]
   mins.append(float(vals.min()))
   if vals.min()<gap-1e-8:done=False;add=np.argpartition(vals,min(29,len(vals)-1))[:30];z['inds']=np.unique(np.r_[z['inds'],add])
  print('ITER',it,'rows',A.shape[0],'delta',gap,'inner_min',inmin,'outer_min',mins,'elapsed',round(time.monotonic()-start,2),flush=True);history.append(dict(iteration=it,rows=A.shape[0],delta=gap,inner_min=inmin,outer_min=mins))
  if gap<1e-8:reason='COMPLETE_PARALLEL18_STATE40_NO_POSITIVE_DUAL';break
  if done:sol=x;reason='POSITIVE_FLOAT_CANDIDATE';break
 report=dict(target=[106,106,63],empty_cases=empty,counts=[dict(m=z['m'],type=z['key'],count=len(z['X']))for z in INS],outer_count=len(OUT[0]['X']),iterations=it+1,numerical_status=reason,claim='NO_NEW_MATH',elapsed=time.monotonic()-start,history=history)
 if sol is not None:
  floats=sol.copy()
  for z in INS+OUT:floats[z['offset']:z['offset']+z['X'].shape[1]]/=z['scale']
  for mul in [10**i for i in range(4,17)]:
   qi=np.rint(floats*mul).astype(np.int64);hist={};safe=True
   for m in [40,41,106]:
    ph=qi[pofs[m]:bofs[m]];ic=[];bs=[]
    for z in [z for z in INS if z['m']==m]:
     q=qi[z['offset']:z['offset']+z['X'].shape[1]]
     ceiling=sum(int(a)*int(b)for a,b in zip(np.max(abs(z['X']),axis=0),abs(q)))+3*max(map(abs,ph))+sum(max(map(abs,hist[parent]['phi']))for parent,ids,col in z['deps'])
     if ceiling>8*10**18:safe=False;break
     vv=z['X']@q-ph[z['tops']].sum(axis=1)
     for parent,ids,col in z['deps']:vv+=np.array(hist[parent]['phi'],np.int64)[ids]
     K=int(vv.min());bd=int(ph[z['anchor']])+sum(int(a)*int(b)for a,b in zip(q,z['F']))+sum(hist[parent]['bound']for parent,ids,col in z['deps'])-D[m]*K;bs.append(bd);ic.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,bound=bd,extra=z['extra'],count=len(z['X']),dependencies=[dict(m=parent,column=col,coefficient=1)for parent,ids,col in z['deps']],class41=z.get('class41'),state18=z.get('state18'),full18_state=z.get('full18_state')))
    if not safe:break
    hist[m]=dict(types=TS[m],phi=list(map(int,ph)),bound=max(bs),inner=ic,root=ROOT[106]if m==106 else'COMPLETE_FIRST_ANCHOR_CASE_COVER')
   if not safe:continue
   oc=[]
   for z in OUT:
    q=qi[z['offset']:z['offset']+z['X'].shape[1]]
    if sum(int(a)*int(b)for a,b in zip(np.max(abs(z['X']),axis=0),abs(q)))+sum(max(map(abs,hist[m]['phi']))for m,ids in z['ids'])>8*10**18:safe=False;break
    vv=z['X']@q
    for m,ids in z['ids']:vv+=np.array(hist[m]['phi'],np.int64)[ids]
    K=int(vv.min());U=sum(int(a)*int(b)for a,b in zip(q,z['F']))+sum(hist[m]['bound']for m,ids in z['ids']);g=364*K-U;oc.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,forced=U,gap=g,count=len(z['X'])))
   if not safe:continue
   print('INTEGER',mul,[r['gap']for r in oc],flush=True)
   if all(r['gap']>0 for r in oc):report.update(claim='CANDIDATE_EXACT_CERTIFICATE',histograms=hist,outer=oc,upper5={name:dict(m=m,types=list(phi),phi=list(phi.values()),bound=bd)for name,(m,phi,bd)in (O.U5|R106.H4.NEW).items()},full18_states=ST,named_pair_input=R41.IN,table1=json.loads((W/'table1_input_v2.json').read_text()),histogram_pair_capacity=CP);break
 SAVE(report,'h13_result.json');print('RESULT',report['claim'],reason,flush=True)
if __name__=='__main__':main()
