import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from joint import *
import importlib.util
spec=importlib.util.spec_from_file_location('aux41_readonly',O.B/'auxiliary41.py');aux=importlib.util.module_from_spec(spec);spec.loader.exec_module(aux)
SUP40=[(a,b,40-a-b)for a in range(21)for b in range(a+1)if 0<=40-a-b<=b];IX40={t:i for i,t in enumerate(SUP40)}
src=(O.B/'baseline277/research/nested108.py').read_text();code=src[src.index('@njit(cache=True)'):src.index('\ndef inner_data')].replace('@njit(cache=True)','@njit').replace('range(21)','range(10)').replace('<=20','<=9').replace('x>45 or y>45','x>20 or y>20')
scope={'njit':O.njit,'np':np,'e2':E.e2,'sorted3':E.sorted3};exec(code,scope);ien40=scope['inner_enum']
A4=np.zeros((10,10,10),bool)
for t in itertools.product(range(10),repeat=3):A4[t]=aux.adm4(t)

def unused_old_lower40(key,i):
 index=np.full((21,21),-1,np.int64)
 for t,j in IX40.items():index[t[:2]]=j
 top=E.make_top(20,40,np.array(SUP40[:i],np.int64).reshape(-1,3));ar=ien40(*key,A4,top,index)
 X=ar[:,:7].copy();F=E.force(key,5)
 if not len(X):return dict(m=40,key=key,empty=True)
 sc=np.maximum(np.max(abs(X-F/40),axis=0),1);wv=(X-F/40)/sc
 return dict(m=40,key=key,X=X,F=F,W=wv,scale=sc,extra=[],pos=[],tops=ar[:,16:19].copy(),anchor=IX40[key],empty=False)

def six_inner(m,key,ri):
 z=inner(m,key,ri);cols=[]
 if 40 in key:
  IX={t:i for i,t in enumerate(SUP[m])};index=np.full((46,46),-1,np.int64)
  for t,i in IX.items():index[t[:2]]=i
  top=E.make_top(45,m,np.array(OLD+COMP+ANCH[m][:ri],np.int64));ar=O.ien(*key,ADM5,top,index)
  assert len(ar)==len(z['X'])
  for j,N in enumerate(key):
   if N==40:cols.append(np.array([IX40[tuple(t)]for t in ar[:,7+3*j:10+3*j]],np.int32))
 z['ids40']=cols;return z

from structural40 import build as lower40
W=Path(__file__).resolve().parent
SAVE=lambda x,n:(W/n).write_text(json.dumps(x,indent=2)+"\n")

def main():
 signal.signal(signal.SIGALRM,limit);signal.alarm(1150);start=time.monotonic()
 old=json.loads((R/'certificates.json').read_text());ban=SEEDS+[(112,109,51),(111,110,51)]+[V.parse_key(k)for s in old['stages']for k in s]
 L40=[];empty40=[]
 for i,t in enumerate(SUP40):
  z=lower40(t,i)
  if z['empty']:empty40.append(t)
  else:L40.append(z)
 print('LOWER40',len(SUP40),'anchors',len(L40),'nonempty','matrices',sum(len(z['X'])for z in L40),'elapsed',time.monotonic()-start,flush=True)
 INS=[]
 for m in [105]:
  for ri,t in enumerate(ANCH[m]):
   z=six_inner(m,t,ri);INS.append(z)
 print('INNER6',len(INS),'matrices',sum(len(z['X'])for z in INS),'elapsed',time.monotonic()-start,flush=True)
 OUT=[outer(t,ban)for t in [(105,105,65)]]
 print('OUTER',[(z['key'],len(z['X']))for z in OUT],'elapsed',time.monotonic()-start,flush=True)
 pofs={};bofs={};off=0;bounds=[]
 for m,ts in [(40,SUP40),(105,SUP[105])]:pofs[m]=off;off+=len(ts);bounds += [(-1,1)]*len(ts);bofs[m]=off;off+=1;bounds.append((None,None))
 for z in L40+INS+OUT:
  z['offset']=off;off+=z['X'].shape[1];bounds += [(0,1)if j in z['pos']else(-1,1)for j in range(z['X'].shape[1])]
 nv=off+1;dof=off;bounds.append((None,None));obj=np.zeros(nv);obj[-1]=-1
 for z in L40+INS+OUT:z['inds']=np.unique(np.r_[np.argmin(z['W'],axis=0),np.argmax(z['W'],axis=0)])
 sol=None;reason='ITERATION_LIMIT';history=[]
 for it in range(160):
  chunks=[]
  for z in L40+INS:
   ii=z['inds'];rr=np.zeros((len(ii),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W'][ii]
   for j in range(3):rr[np.arange(len(ii)),pofs[z['m']]+z['tops'][ii,j]]+=1
   D,DD=(40,121)if z['m']==40 else(121,364)
   rr[:,pofs[z['m']]+z['anchor']]+=1/D;rr[:,bofs[z['m']]]=-DD/D
   for ids in z.get('ids40',[]):rr[np.arange(len(ii)),pofs[40]+ids[ii]]-=1;rr[:,bofs[40]]+=1
   chunks.append(sparse.csr_matrix(rr))
  for z in OUT:
   ii=z['inds'];rr=np.zeros((len(ii),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W'][ii]
   for m,ids in z['ids']:rr[np.arange(len(ii)),pofs[m]+ids[ii]]-=1;rr[:,bofs[m]]+=1
   rr[:,dof]=1;chunks.append(sparse.csr_matrix(rr))
  A=sparse.vstack(chunks,format='csr');res=linprog(obj,A_ub=A,b_ub=np.zeros(A.shape[0]),bounds=bounds,method='highs',options={'time_limit':120})
  if not res.success:reason=res.message;break
  x=res.x;gap=x[-1];mins=[];done=True;inmin=0
  for z in L40+INS:
   D,DD=(40,121)if z['m']==40 else(121,364)
   vals=z['W']@x[z['offset']:z['offset']+z['X'].shape[1]]+DD*x[bofs[z['m']]]/D-x[pofs[z['m']]+z['anchor']]/D
   for j in range(3):vals-=x[pofs[z['m']]+z['tops'][:,j]]
   for ids in z.get('ids40',[]):vals+=x[pofs[40]+ids]-x[bofs[40]]
   inmin=min(inmin,float(vals.min()))
   if vals.min()<-1e-8:
    done=False;add=np.argpartition(vals,min(19,len(vals)-1))[:20];z['inds']=np.unique(np.r_[z['inds'],add])
  for z in OUT:
   vals=z['W']@x[z['offset']:z['offset']+z['X'].shape[1]]
   for m,ids in z['ids']:vals+=x[pofs[m]+ids]-x[bofs[m]]
   mins.append(float(vals.min()))
   if vals.min()<gap-1e-8:
    done=False;add=np.argpartition(vals,min(29,len(vals)-1))[:30];z['inds']=np.unique(np.r_[z['inds'],add])
  print('ITER',it,'rows',A.shape[0],'delta',gap,'inner_min',inmin,'outer_min',mins,'elapsed',round(time.monotonic()-start,2),flush=True)
  history.append(dict(iteration=it,rows=A.shape[0],delta=gap,inner_min=inmin,outer_min=mins))
  if gap<1e-8:reason='STRUCTURAL40_NO_POSITIVE_DUAL';break
  if done:sol=x;reason='POSITIVE_FLOAT_CANDIDATE';break
 report=dict(targets=[z['key']for z in OUT],lower40_counts=[len(z['X'])for z in L40],lower40_empty=empty40,inner_counts=[len(z['X'])for z in INS],outer_counts=[len(z['X'])for z in OUT],iterations=it+1,numerical_status=reason,claim='NO_NEW_MATH',elapsed=time.monotonic()-start,history=history)
 if sol is not None:
  floats=sol.copy()
  for z in L40+INS+OUT:floats[z['offset']:z['offset']+z['X'].shape[1]]/=z['scale']
  for mul in [10**i for i in range(4,12)]:
   qi=np.rint(floats*mul).astype(np.int64);hist={};safe=True
   for m,ls,D in [(40,L40,40),(105,[z for z in INS if z['m']==105],121)]:
    ph=qi[pofs[m]:bofs[m]];ic=[];bs=[]
    for z in ls:
     q=qi[z['offset']:z['offset']+z['X'].shape[1]]
     if sum(int(a)*int(b)for a,b in zip(np.max(abs(z['X']),axis=0),abs(q)))+3*max(map(abs,ph))>8*10**18:safe=False;break
     val=z['X']@q-ph[z['tops']].sum(axis=1)
     for ids in z.get('ids40',[]):val+=np.array(hist[40]['phi'],np.int64)[ids]
     K=int(val.min());bd=int(ph[z['anchor']])+sum(int(a)*int(b)for a,b in zip(q,z['F']))-D*K
     bd+=len(z.get('ids40',[]))*hist.get(40,{}).get('bound',0);bs.append(bd);ic.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,bound=bd,extra=z['extra'],count=len(z['X']),theta40_columns=[j for j,N in enumerate(z['key'])if N==40]if m!=40 else[]))
    if not safe:break
    hist[m]=dict(types=SUP40 if m==40 else SUP[m],root='ALL_PROFILE_COVER'if m==40 else ROOT[m],phi=list(map(int,ph)),bound=max(bs),inner=ic)
   if not safe:continue
   oc=[]
   for z in OUT:
    q=qi[z['offset']:z['offset']+z['X'].shape[1]];vv=z['X']@q
    for m,ids in z['ids']:vv+=np.array(hist[m]['phi'],np.int64)[ids]
    K=int(vv.min());U=sum(int(a)*int(b)for a,b in zip(q,z['F']))+sum(hist[m]['bound']for m,ids in z['ids']);g=364*K-U;oc.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,forced=U,gap=g,count=len(z['X'])))
   print('INTEGER',mul,[r['gap']for r in oc],flush=True)
   if all(r['gap']>0 for r in oc):report.update(claim='CANDIDATE_EXACT_CERTIFICATE',histograms=hist,outer=oc,upper5={name:dict(m=m,types=list(phi),phi=list(phi.values()),bound=bd)for name,(m,phi,bd)in O.U5.items()});break
 SAVE(report,'h3_result.json');print('RESULT',report['claim'],reason,flush=True)
if __name__=='__main__':main()
