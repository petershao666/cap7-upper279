from minimum import *
from scipy import sparse
from scipy.optimize import linprog
# Assemble all available lower-dimensional upper-bound functions; no optimization or proof of them here.
H107=next(h for h in H if h['id']=='nested107_size276');TY=list(map(tuple,H107['types']));IX={t:i for i,t in enumerate(TY)};RARE=[tuple(r['type']) for r in H107['inner']]
U5={}
for h in H:
 for r in h['inner']:
  for u in r.get('uppercuts',[]):U5[u['id']]=(41,dict(zip(map(tuple,u['data']['types']),u['data']['phi'])),u['data']['bound'])
  for u in r.get('spectra',[]):
   phi=dict(zip(map(tuple,u['types']),u['phi']));name='spec42_'+str(len(U5))
   if not any(m==42 and p==phi for m,p,b in U5.values()):U5[name]=(42,phi,u['bound'])
src=(B/'baseline277/research/nested108.py').read_text();code=src[src.index('@njit(cache=True)'):src.index('\ndef inner_data')].replace('@njit(cache=True)','@njit')
scope={'njit':njit,'np':np,'e2':E.e2,'sorted3':E.sorted3};exec(code,scope);ien=scope['inner_enum']
index=np.full((46,46),-1,np.int64)
for t,i in IX.items():index[t[:2]]=i

def inner(key,ri):
 adm=E.make_adm(5,np.empty((0,3),np.int64))
 for t in itertools.product(range(21),repeat=3):
  if not V.downwards_allowed(t,[(20,19,2),(20,18,3),(19,19,3),(19,18,4)]):adm[t]=False
 top=E.make_top(45,107,np.array(OLD+COMP+RARE[:ri],np.int64))
 ar=ien(*key,adm,top,index);X=ar[:,:7].copy();F=list(E.force(key,6));extra=[];pos=[]
 for j,N in enumerate(key):
  if N in (43,44,45):
   sp=C['spectrum5'][str(N)]
   for typ,bd in zip(sp['types'],sp['spectra'][0]):
    X=np.c_[X,np.all(ar[:,7+3*j:10+3*j]==typ,axis=1).astype(np.int64)];F.append(bd);extra.append((j,'exact',typ,bd))
  for name,(m,phi,bd) in U5.items():
   if m!=N:continue
   vals=np.array([phi[tuple(t)] for t in ar[:,7+3*j:10+3*j]],np.int64);X=np.c_[X,vals];pos.append(len(F));F.append(bd);extra.append((j,'upper',name,bd))
 F=np.array(F,np.int64);sc=np.maximum(np.max(abs(X-F/121),axis=0),1);wv=(X-F/121)/sc
 return dict(key=key,X=X,F=F,W=wv,scale=sc,extra=extra,pos=pos,tops=ar[:,16:19].copy(),anchor=IX[key])
def outer(key,ban):
 ar=en(key,ban+[t for t in T if Q(t)<Q(key)]);mask=np.ones(len(ar),bool)
 for j in (0,1):
  for t in COMP:mask&=~np.all(ar[:,7+3*j:10+3*j]>=t,axis=1)
 ar=ar[mask];X=ar[:,:7].astype(np.int64);F=list(E.force(key));extra=[];pos=[]
 for j in (0,1):
  for name,(m,phi,bd) in REG.items():
   if key[j]!=m or m==107:continue
   lu=np.zeros((46,46),np.int64)
   for t,val in phi.items():lu[t[:2]]=val
   tt=ar[:,7+3*j:10+3*j];X=np.c_[X,lu[tt[:,0],tt[:,1]]];pos.append(len(F));F.append(bd);extra.append((j,name))
 ids=[np.array([IX[tuple(t)] for t in ar[:,7+3*j:10+3*j]],np.int32) for j in (0,1) if key[j]==107]
 F=np.array(F,np.int64);sc=np.maximum(np.max(abs(X-F/364),axis=0),1);wv=(X-F/364)/sc
 return dict(key=key,X=X,F=F,W=wv,scale=sc,pos=pos,extra=extra,ids=ids)
def main():
 signal.alarm(570);start=time.monotonic();base=json.loads((W/'certificates.json').read_text());ban=SEEDS+[(112,109,51),(111,110,51)]+[V.parse_key(k) for s in base['stages'] for k in s]
 INS=[inner(t,j) for j,t in enumerate(RARE)];print('INNER_COUNTS',[(z['key'],len(z['X']),z['X'].shape[1])for z in INS],flush=True)
 OUT=[outer(t,ban) for t in [(108,107,60),(107,107,61),(107,106,62)]];print('OUTER_COUNTS',[(z['key'],len(z['X']),z['X'].shape[1])for z in OUT],flush=True)
 # phi + beta + each local q vector + common delta
 pof=0;bof=len(TY);offset=bof+1;bounds=[(-1,1)]*bof+[(None,None)]
 for z in INS+OUT:
  z['offset']=offset;offset+=z['X'].shape[1];bounds += [(0,1) if j in z['pos'] else (-1,1) for j in range(z['X'].shape[1])]
 nv=offset+1;dof=offset;bounds.append((None,None));obj=np.zeros(nv);obj[-1]=-1
 fixed=[]
 for z in INS:
  rr=np.zeros((len(z['X']),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W']
  for j in range(3):rr[np.arange(len(rr)),z['tops'][:,j]]+=1
  rr[:,z['anchor']]+=1/121;rr[:,bof]=-364/121;fixed.append(sparse.csr_matrix(rr))
 fixed=sparse.vstack(fixed,format='csr')
 for z in OUT:z['inds']=np.unique(np.r_[np.argmin(z['W'],axis=0),np.argmax(z['W'],axis=0)])
 sol=None;reason='ITERATION_LIMIT'
 for it in range(120):
  chunks=[fixed]
  for z in OUT:
   ii=z['inds'];rr=np.zeros((len(ii),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W'][ii]
   for ids in z['ids']:rr[np.arange(len(ii)),ids[ii]]-=1
   rr[:,bof]=len(z['ids']);rr[:,dof]=1;chunks.append(sparse.csr_matrix(rr))
  A=sparse.vstack(chunks,format='csr');r=linprog(obj,A_ub=A,b_ub=np.zeros(A.shape[0]),bounds=bounds,method='highs',options={'time_limit':60})
  if not r.success:reason=r.message;break
  x=r.x;gap=x[-1];mins=[];done=True
  for z in OUT:
   vals=z['W']@x[z['offset']:z['offset']+z['X'].shape[1]]-len(z['ids'])*x[bof]
   for ids in z['ids']:vals+=x[ids]
   mins.append(float(vals.min()))
   if vals.min()<gap-1e-9:
    done=False;add=np.argpartition(vals,min(49,len(vals)-1))[:50];z['inds']=np.unique(np.r_[z['inds'],add])
  print('ITER',it,'delta',gap,'min',mins,'elapsed',round(time.monotonic()-start,2),flush=True)
  if gap<1e-9:reason='JOINT_RELAXATION_NO_POSITIVE_DUAL';break
  if done:sol=x;break
 report=dict(targets=[z['key']for z in OUT],inner_counts=[len(z['X'])for z in INS],outer_counts=[len(z['X'])for z in OUT],iterations=it+1,numerical_status=reason,claim='NO_NEW_MATH',elapsed=time.monotonic()-start)
 if sol is not None:
  floats=sol.copy()
  for z in INS+OUT:floats[z['offset']:z['offset']+z['X'].shape[1]]/=z['scale']
  for mul in [10**i for i in range(4,12)]:
   qi=np.rint(floats*mul).astype(np.int64);ph=qi[:bof];innercert=[];bs=[]
   for z in INS:
    q=qi[z['offset']:z['offset']+z['X'].shape[1]];K=int((z['X']@q-ph[z['tops']].sum(axis=1)).min());bd=int(ph[z['anchor']])+sum(int(a)*int(b)for a,b in zip(q,z['F']))-121*K;bs.append(bd);innercert.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,bound=bd,extra=z['extra']))
   bd=max(bs);outercert=[]
   for z in OUT:
    q=qi[z['offset']:z['offset']+z['X'].shape[1]];vv=z['X']@q
    for ids in z['ids']:vv+=ph[ids]
    K=int(vv.min());U=sum(int(a)*int(b)for a,b in zip(q,z['F']))+len(z['ids'])*bd;g=364*K-U;outercert.append(dict(type=z['key'],coeff=list(map(int,q)),K=K,forced=U,gap=g,extra=z['extra']))
   print('INTEGER',mul,[r['gap']for r in outercert],flush=True)
   if all(r['gap']>0 for r in outercert):
    report.update(claim='CANDIDATE_EXACT_CERTIFICATE',types=TY,phi=list(map(int,ph)),bound=bd,inner=innercert,outer=outercert,root=H107['root']);break
 save(report,'common107_result.json');print('RESULT',report['claim'],reason,flush=True)
if __name__=='__main__':main()
