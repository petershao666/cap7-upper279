import sys
from pathlib import Path
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W.parent))
import joint as J
from joint import np,O,E,V,C,OLD,COMP,ANCH,SUP,ROOT,SEEDS,T,Q,en,signal,limit,math,json,itertools,time,sparse,linprog,R
SAVE=lambda x,n:(W/n).write_text(json.dumps(x,indent=2)+'\n')
TR=json.loads((W/'transport_tables.json').read_text())
# Subtract known constant for stable arithmetic. A constant contributes121times
# itself to a5-dimensional directional histogram; no strength is changed.
NEW={}
for sm,h in TR.items():
 shift=10**10*h['subcap_count'];NEW['centered_theta'+sm]=(int(sm),dict(zip(map(tuple,h['types']),[v+shift for v in h['phi']])),h['bound']+121*shift)
SAVE({k:dict(m=m,types=list(phi),phi=list(phi.values()),bound=bd)for k,(m,phi,bd)in NEW.items()},'centered_transport.json')

def inner(key,ri):
 z=J.inner(106,key,ri);ix={t:i for i,t in enumerate(SUP[106])};index=np.full((46,46),-1,np.int64)
 for t,i in ix.items():index[t[:2]]=i
 ar=O.ien(*key,J.ADM5,E.make_top(45,106,np.array(OLD+COMP+ANCH[106][:ri],np.int64)),index);assert len(ar)==len(z['X']);X=z['X'];F=list(z['F']);extra=z['extra'];pos=z['pos']
 for j,N in enumerate(key):
  for name,(m,phi,bd)in NEW.items():
   if N!=m:continue
   lu=np.zeros((21,21),np.int64)
   for t,v in phi.items():lu[t[:2]]=v
   tt=ar[:,7+3*j:10+3*j];X=np.c_[X,lu[tt[:,0],tt[:,1]]];pos.append(len(F));F.append(bd);extra.append((j,'new_upper',name,bd))
 F=np.array(F,np.int64);sc=np.maximum(np.max(abs(X-F/121),axis=0),1);z.update(X=X,F=F,W=(X-F/121)/sc,scale=sc,extra=extra,pos=pos);return z

def outer(key,ban):
 return J.outer(key,ban)

def main():
 signal.signal(signal.SIGALRM,limit);signal.alarm(1150);start=time.monotonic();old=json.loads((R/'certificates.json').read_text());ban=SEEDS+[(112,109,51),(111,110,51)]+[V.parse_key(k)for s in old['stages']for k in s]
 INS=[inner(t,i)for i,t in enumerate(ANCH[106])];OUT=[outer((106,106,63),ban)];print('DOMAINS',sum(len(z['X'])for z in INS),len(OUT[0]['X']),flush=True)
 pof=0;bof=len(SUP[106]);off=bof+1;bounds=[(-1,1)]*bof+[(None,None)]
 for z in INS+OUT:z['offset']=off;off+=z['X'].shape[1];bounds += [(0,1)if j in z['pos']else(-1,1)for j in range(z['X'].shape[1])]
 nv=off+1;dof=off;bounds.append((None,None));obj=np.zeros(nv);obj[-1]=-1
 for z in INS+OUT:z['inds']=np.unique(np.r_[np.argmin(z['W'],axis=0),np.argmax(z['W'],axis=0)])
 sol=None;reason='ITERATION_LIMIT';history=[]
 for it in range(180):
  chunks=[]
  for z in INS:
   ii=z['inds'];rr=np.zeros((len(ii),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W'][ii]
   for j in range(3):rr[np.arange(len(ii)),z['tops'][ii,j]]+=1
   rr[:,z['anchor']]+=1/121;rr[:,bof]=-364/121;chunks.append(sparse.csr_matrix(rr))
  for z in OUT:
   ii=z['inds'];rr=np.zeros((len(ii),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W'][ii]
   for m,ids in z['ids']:assert m==106;rr[np.arange(len(ii)),ids[ii]]-=1;rr[:,bof]+=1
   rr[:,dof]=1;chunks.append(sparse.csr_matrix(rr))
  A=sparse.vstack(chunks,format='csr');res=linprog(obj,A_ub=A,b_ub=np.zeros(A.shape[0]),bounds=bounds,method='highs',options={'time_limit':120})
  if not res.success:reason=res.message;break
  x=res.x;gap=x[-1];done=True;inmin=0;mins=[]
  for z in INS:
   vals=z['W']@x[z['offset']:z['offset']+z['X'].shape[1]]+364*x[bof]/121-x[z['anchor']]/121
   for j in range(3):vals-=x[z['tops'][:,j]]
   inmin=min(inmin,float(vals.min()))
   if vals.min()<-1e-8:done=False;add=np.argpartition(vals,min(19,len(vals)-1))[:20];z['inds']=np.unique(np.r_[z['inds'],add])
  for z in OUT:
   vals=z['W']@x[z['offset']:z['offset']+z['X'].shape[1]]
   for m,ids in z['ids']:vals+=x[ids]-x[bof]
   mins.append(float(vals.min()))
   if vals.min()<gap-1e-8:done=False;add=np.argpartition(vals,min(29,len(vals)-1))[:30];z['inds']=np.unique(np.r_[z['inds'],add])
  print('ITER',it,'rows',A.shape[0],'delta',gap,'inner_min',inmin,'outer_min',mins,'elapsed',round(time.monotonic()-start,2),flush=True);history.append(dict(iteration=it,rows=A.shape[0],delta=gap,inner_min=inmin,outer_min=mins))
  if gap<1e-8:reason='THETA41_TRANSPORT_NO_POSITIVE_DUAL';break
  if done:sol=x;reason='POSITIVE_FLOAT_CANDIDATE';break
 report=dict(targets=[z['key']for z in OUT],inner_counts=[len(z['X'])for z in INS],outer_counts=[len(z['X'])for z in OUT],iterations=it+1,numerical_status=reason,claim='NO_NEW_MATH',elapsed=time.monotonic()-start,history=history)
 if sol is not None:
  floats=sol.copy()
  for z in INS+OUT:floats[z['offset']:z['offset']+z['X'].shape[1]]/=z['scale']
  for mul in [10**i for i in range(4,17)]:
   qi=np.rint(floats*mul).astype(np.int64);ph=qi[:bof];ic=[];bs=[];safe=True
   for z in INS:
    q=qi[z['offset']:z['offset']+z['X'].shape[1]]
    if sum(int(a)*int(b)for a,b in zip(np.max(abs(z['X']),axis=0),abs(q)))+3*max(map(abs,ph))>8*10**18:safe=False;break
    K=int((z['X']@q-ph[z['tops']].sum(axis=1)).min());bd=int(ph[z['anchor']])+sum(int(a)*int(b)for a,b in zip(q,z['F']))-121*K;bs.append(bd);ic.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,bound=bd,extra=z['extra'],count=len(z['X'])))
   if not safe:continue
   B=max(bs);oc=[]
   for z in OUT:
    q=qi[z['offset']:z['offset']+z['X'].shape[1]];vv=z['X']@q
    for m,ids in z['ids']:vv+=ph[ids]
    K=int(vv.min());U=sum(int(a)*int(b)for a,b in zip(q,z['F']))+len(z['ids'])*B;g=364*K-U;oc.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,forced=U,gap=g,count=len(z['X'])))
   print('INTEGER',mul,[z['gap']for z in oc],flush=True)
   if all(z['gap']>0 for z in oc):report.update(claim='CANDIDATE_EXACT_CERTIFICATE',histogram=dict(m=106,types=SUP[106],root=ROOT[106],phi=list(map(int,ph)),bound=B,inner=ic),outer=oc,upper5={name:dict(m=m,types=list(phi),phi=list(phi.values()),bound=bd)for name,(m,phi,bd)in (O.U5|NEW).items()});break
 SAVE(report,'h4_result.json');print('RESULT',report['claim'],reason,flush=True)
if __name__=='__main__':main()
