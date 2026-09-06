import sys,importlib.util
from pathlib import Path
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W.parent));sys.path.insert(0,str(W.parent/'h3'))
import joint as J
from joint import np,O,E,V,C,OLD,COMP,ANCH,SUP,ROOT,SEEDS,T,Q,en,signal,limit,math,json,itertools,time,sparse,linprog,R
import structural40 as S40
spec=importlib.util.spec_from_file_location('h4_readonly',W.parent/'h4/run.py');H4=importlib.util.module_from_spec(spec);spec.loader.exec_module(H4)
SAVE=lambda x,n:(W/n).write_text(json.dumps(x,indent=2)+'\n')
H18=json.loads((W.parents[1]/'root_audit/h18_input.json').read_text());H1920=json.loads((W.parent/'h3/hist19_20.json').read_text())
BAD41=[(20,19,2),(20,18,3),(19,19,3),(19,18,4)]
T41=[(a,b,41-a-b)for a in range(21)for b in range(a+1)if 0<=41-a-b<=b and(a,b,41-a-b)not in BAD41]
A41=[(20,20,1),(18,18,5),(20,17,4),(20,16,5),(19,17,5),(19,16,6),(18,17,6),(18,16,7),(17,17,7),(17,16,8)];IX41={t:i for i,t in enumerate(T41)}

def lower41(key,i):
 index=np.full((21,21),-1,np.int64)
 for t,j in IX41.items():index[t[:2]]=j
 top=E.make_top(20,41,np.array(BAD41+A41[:i],np.int64).reshape(-1,3));ar=S40.raw_enum(*key,S40.D.A4,top,index);before=len(ar);ar=ar[S40.filter_clashes(ar,S40.PS)];X=ar[:,:7].copy();F=list(E.force(key,5));extra=[];pos=[]
 for j,N in enumerate(key):
  tt=ar[:,7+3*j:10+3*j]
  if str(N)in H1920:
   h=H1920[str(N)]
   for t,b in zip(h['types'],h['histogram']):X=np.c_[X,np.all(tt==t,axis=1).astype(np.int64)];F.append(b);extra.append((j,'exact4',t,b))
  if N==18:
   inds=[np.all(tt==t,axis=1).astype(np.int64)for t in H18['statistics']]
   for fi,fac in enumerate(H18['facets_le']):
    vals=sum(c*x for c,x in zip(fac[:3],inds));X=np.c_[X,vals];pos.append(len(F));F.append(fac[3]);extra.append((j,'upper18',fi,fac[3]))
 F=np.array(F,np.int64)
 if not len(X):return dict(m=41,key=key,empty=True,before=before)
 sc=np.maximum(np.max(abs(X-F/40),axis=0),1);return dict(m=41,key=key,X=X,F=F,W=(X-F/40)/sc,scale=sc,extra=extra,pos=pos,tops=ar[:,16:19].copy(),anchor=IX41[key],empty=False,before=before)

def inner106(key,i):
 z=H4.inner(key,i);ix={t:j for j,t in enumerate(SUP[106])};index=np.full((46,46),-1,np.int64)
 for t,j in ix.items():index[t[:2]]=j
 ar=O.ien(*key,J.ADM5,E.make_top(45,106,np.array(OLD+COMP+ANCH[106][:i],np.int64)),index);assert len(ar)==len(z['X']);z['ids41']=[]
 for j,N in enumerate(key):
  if N==41:z['ids41'].append(np.array([IX41[tuple(t)]for t in ar[:,7+3*j:10+3*j]],np.int32))
 return z

KNOWN105=json.loads((W.parent/'h3/h3_result.json').read_text())['histograms']['105']
def outer_h8(key,ban):
 z=J.outer(key,ban)
 for m,ids in z['ids']:
  if m==105:
   phi=np.array(KNOWN105['phi'],np.int64)+10**10;bd=KNOWN105['bound']+364*10**10
   z['X']=np.c_[z['X'],phi[ids]];z['pos'].append(len(z['F']));z['F']=np.r_[z['F'],bd];z['extra'].append((1,'known105_centered',10**10,int(bd)))
 z['ids']=[(m,ids)for m,ids in z['ids']if m==106]
 z['scale']=np.maximum(np.max(abs(z['X']-z['F']/364),axis=0),1);z['W']=(z['X']-z['F']/364)/z['scale'];return z

def main():
 signal.signal(signal.SIGALRM,limit);signal.alarm(270);start=time.monotonic();old=json.loads((R/'certificates.json').read_text());ban=SEEDS+[(112,109,51),(111,110,51)]+[V.parse_key(k)for s in old['stages']for k in s]
 from full18model import all_branches
 ALL=all_branches();L41=[z for z in ALL if not z['empty']];empty=[dict(type=z['key'],state18=z['state18'],class41=z['class41'],full18_state=z['full18_state'])for z in ALL if z['empty']]
 INS=[inner106(t,i)for i,t in enumerate(ANCH[106])];OUT=[outer_h8({'10610564':(106,105,64),'10610663':(106,106,63)}[sys.argv[1]],ban)];print('DOMAINS',len(ALL),len(L41),sum(len(z['X'])for z in L41),sum(len(z['X'])for z in INS),len(OUT[0]['X']),flush=True)
 pofs={};bofs={};off=0;bounds=[]
 for m,ts in [(41,T41),(106,SUP[106])]:pofs[m]=off;off+=len(ts);bounds += [(-1,1)]*len(ts);bofs[m]=off;off+=1;bounds.append((None,None))
 for z in L41+INS+OUT:z['offset']=off;off+=z['X'].shape[1];bounds += [(0,1)if j in z['pos']else(-1,1)for j in range(z['X'].shape[1])]
 nv=off+1;dof=off;bounds.append((None,None));obj=np.zeros(nv);obj[-1]=-1
 for z in L41+INS+OUT:z['inds']=np.unique(np.r_[np.argmin(z['W'],axis=0),np.argmax(z['W'],axis=0)])
 sol=None;reason='ITERATION_LIMIT';history=[]
 for it in range(180):
  chunks=[]
  for z in L41+INS:
   ii=z['inds'];rr=np.zeros((len(ii),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W'][ii]
   for j in range(3):rr[np.arange(len(ii)),pofs[z['m']]+z['tops'][ii,j]]+=1
   D,DD=(40,121)if z['m']==41 else(121,364)
   rr[:,pofs[z['m']]+z['anchor']]+=1/D;rr[:,bofs[z['m']]]=-DD/D
   for ids in z.get('ids41',[]):rr[np.arange(len(ii)),pofs[41]+ids[ii]]-=1;rr[:,bofs[41]]+=1
   chunks.append(sparse.csr_matrix(rr))
  for z in OUT:
   ii=z['inds'];rr=np.zeros((len(ii),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W'][ii]
   for m,ids in z['ids']:rr[np.arange(len(ii)),pofs[m]+ids[ii]]-=1;rr[:,bofs[m]]+=1
   rr[:,dof]=1;chunks.append(sparse.csr_matrix(rr))
  if time.monotonic()-start>=235:reason='BATCH_WALL_LIMIT';break
  A=sparse.vstack(chunks,format='csr');res=linprog(obj,A_ub=A,b_ub=np.zeros(A.shape[0]),bounds=bounds,method='highs',options={'time_limit':max(1,min(120,250-(time.monotonic()-start)))})
  if not res.success:reason=res.message;break
  x=res.x;gap=x[-1];done=True;inmin=0;mins=[]
  for z in L41+INS:
   D,DD=(40,121)if z['m']==41 else(121,364)
   vals=z['W']@x[z['offset']:z['offset']+z['X'].shape[1]]+DD*x[bofs[z['m']]]/D-x[pofs[z['m']]+z['anchor']]/D
   for j in range(3):vals-=x[pofs[z['m']]+z['tops'][:,j]]
   for ids in z.get('ids41',[]):vals+=x[pofs[41]+ids]-x[bofs[41]]
   inmin=min(inmin,float(vals.min()))
   if vals.min()<-1e-8:done=False;add=np.argpartition(vals,min(19,len(vals)-1))[:20];z['inds']=np.unique(np.r_[z['inds'],add])
  for z in OUT:
   vals=z['W']@x[z['offset']:z['offset']+z['X'].shape[1]]
   for m,ids in z['ids']:vals+=x[pofs[m]+ids]-x[bofs[m]]
   mins.append(float(vals.min()))
   if vals.min()<gap-1e-8:done=False;add=np.argpartition(vals,min(29,len(vals)-1))[:30];z['inds']=np.unique(np.r_[z['inds'],add])
  print('ITER',it,'rows',A.shape[0],'delta',gap,'inner_min',inmin,'outer_min',mins,'elapsed',round(time.monotonic()-start,2),flush=True);history.append(dict(iteration=it,rows=A.shape[0],delta=gap,inner_min=inmin,outer_min=mins))
  if gap<1e-8:reason='FULL20_CLASS18_HIST_MODEL_NO_POSITIVE_DUAL';break
  if done:sol=x;reason='POSITIVE_FLOAT_CANDIDATE';break
 report=dict(targets=[z['key']for z in OUT],lower41_counts=[len(z['X'])for z in L41],lower41_empty=empty,inner_counts=[len(z['X'])for z in INS],outer_counts=[len(z['X'])for z in OUT],iterations=it+1,numerical_status=reason,claim='NO_NEW_MATH',elapsed=time.monotonic()-start,history=history)
 if sol is not None:
  floats=sol.copy()
  for z in L41+INS+OUT:floats[z['offset']:z['offset']+z['X'].shape[1]]/=z['scale']
  for mul in [10**i for i in range(4,17)]:
   qi=np.rint(floats*mul).astype(np.int64);hist={};safe=True
   for m,ls,D in [(41,L41,40),(106,INS,121)]:
    ph=qi[pofs[m]:bofs[m]];ic=[];bs=[]
    for z in ls:
     q=qi[z['offset']:z['offset']+z['X'].shape[1]]
     if sum(int(a)*int(b)for a,b in zip(np.max(abs(z['X']),axis=0),abs(q)))+3*max(map(abs,ph))>8*10**18:safe=False;break
     vv=z['X']@q-ph[z['tops']].sum(axis=1)
     for ids in z.get('ids41',[]):vv+=np.array(hist[41]['phi'],np.int64)[ids]
     K=int(vv.min());bd=int(ph[z['anchor']])+sum(int(a)*int(b)for a,b in zip(q,z['F']))-D*K+len(z.get('ids41',[]))*hist.get(41,{}).get('bound',0);bs.append(bd);ic.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,bound=bd,extra=z['extra'],count=len(z['X']),state18=z.get('state18'),class41=z.get('class41'),full18_state=z.get('full18_state'),theta41_columns=[j for j,N in enumerate(z['key'])if N==41]if m==106 else[]))
    if not safe:break
    hist[m]=dict(types=T41 if m==41 else SUP[106],root='PUBLISHED_TEN_ANCHOR_COVER'if m==41 else ROOT[106],phi=list(map(int,ph)),bound=max(bs),inner=ic)
   if not safe:continue
   oc=[]
   for z in OUT:
    q=qi[z['offset']:z['offset']+z['X'].shape[1]];vv=z['X']@q
    for m,ids in z['ids']:vv+=np.array(hist[m]['phi'],np.int64)[ids]
    K=int(vv.min());U=sum(int(a)*int(b)for a,b in zip(q,z['F']))+sum(hist[m]['bound']for m,ids in z['ids']);g=364*K-U;oc.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,forced=U,gap=g,count=len(z['X'])))
   print('INTEGER',mul,[r['gap']for r in oc],flush=True)
   if all(r['gap']>0 for r in oc):report.update(claim='CANDIDATE_EXACT_CERTIFICATE',histograms=hist,outer=oc,h18_input=H18,known105=KNOWN105,source_input=json.loads((W.parent/'h8/source_input.json').read_text()),named_histograms=json.loads((W.parent/'h9/named_histograms.json').read_text()),full18_states=json.loads((W/'full18_states.json').read_text()),upper5={name:dict(m=m,types=list(phi),phi=list(phi.values()),bound=bd)for name,(m,phi,bd)in (O.U5|H4.NEW).items()});break
 SAVE(report,'h10_single_'+sys.argv[1]+'.json');print('RESULT',report['claim'],reason,flush=True)
if __name__=='__main__':main()
