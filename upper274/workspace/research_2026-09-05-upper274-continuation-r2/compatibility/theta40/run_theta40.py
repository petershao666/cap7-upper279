import sys,hashlib,math,resource
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import full_pricing as P
from full_pricing import M,np,njit,E,json,time,signal,KEY,OLD,COMP,itertools,allowed
from scipy import sparse
from scipy.optimize import linprog
SRC=HERE.parents[1]/'hist105106/h3/h3_result.json'
assert hashlib.sha256(SRC.read_bytes()).hexdigest()=='cbb4973544cf7e2388097bb333504dc0c53c943d1671605fa300996394dfd294'
H=json.loads(SRC.read_text());H40=H['histograms']['40'];BTH=H40['bound']+121*10**10
assert BTH==475918720
theta=np.zeros((21,21),np.int64)
for t,v in zip(H40['types'],H40['phi']):theta[t[0],t[1]]=v+10**10
@njit
def records(mats,theta):
    ans=np.empty((len(mats),40),np.int32);dirs=((1,0),(0,1),(1,1),(1,2))
    for ix in range(len(mats)):
        rec=np.zeros((4,10),np.int64)
        for di in range(4):
            ax,ay=dirs[di];bx=0 if ax else 1;by=1 if ax else 0
            R=np.zeros((3,3),np.int64)
            for x in range(3):
              for y in range(3):R[(ax*x+ay*y)%3,(bx*x+by*y)%3]=np.int64(mats[ix,3*x+y])
            su=np.zeros(3,np.int64)
            for x in range(3):
              for y in range(3):su[x]+=R[x,y]
            a,b,c=E.sorted3(su[0],su[1],su[2]);rec[di,0]=a;rec[di,1]=b
            for i in range(3):
              for j in range(3):rec[di,2]+=R[0,i]*R[1,j]*R[2,(-i-j)%3]
            vs=[]
            for v in (c,b,a):
                if len(vs)==0 or vs[-1]!=v:vs.append(v)
            for vi in range(len(vs)):
              for x in range(3):
                if su[x]==vs[vi]:
                    aa,bb,cc=R[x,0],R[x,1],R[x,2]
                    rec[di,3+2*vi]+=aa*bb+aa*cc+bb*cc;rec[di,4+2*vi]+=aa*bb*cc
                    if vs[vi]==40:
                        aa,bb,cc=E.sorted3(aa,bb,cc);rec[di,9]+=theta[aa,bb]
        for i in range(1,4):
          for j in range(i,0,-1):
            less=False
            for k in range(10):
                if rec[j,k]<rec[j-1,k]:less=True;break
                if rec[j,k]>rec[j-1,k]:break
            if not less:break
            temp=rec[j].copy();rec[j]=rec[j-1];rec[j-1]=temp
        for j in range(4):
          for k in range(10):ans[ix,10*j+k]=rec[j,k]
    return ans
def complete_inner(N):
    old=np.load(HERE.parent/f'inner_{N}.npz');adm=E.make_adm(5,np.empty((0,3),np.int64))
    bad=[(20,19,2),(20,18,3),(19,19,3),(19,18,4)]
    for t in itertools.product(range(21),repeat=3):
        if not allowed(t,bad):adm[t]=False
    top=E.make_top(45,N,np.array(OLD+COMP,np.int64));chunks=[];counts=[]
    for tt,nold in zip(old['types'],old['counts']):
        a,count=M.collect(*map(int,tt),adm,top,np.ones_like(adm),False,max(1,int(nold)))
        assert len(a)==count==nold
        chunks.append(a);counts.append(count)
    raw=np.concatenate(chunks);rec=records(raw,theta);unique,ix=np.unique(rec,axis=0,return_index=True)
    np.savez_compressed(HERE/f'inner_{N}.npz',records=unique,representatives=raw[ix],types=old['types'],counts=np.array(counts),full_count=len(raw))
    print('THETA_INNER',N,'full',len(raw),'quotient',len(unique),flush=True)
    return unique,old['types'],dict(size=N,full_count=len(raw),quotient_count=len(unique))
@njit
def assemble(O,I0,I1,lookup,forces,lengths,thid,thmult):
    cap=10*len(O)+37*(len(I0)+len(I1))
    rr=np.empty(cap,np.int32);cc=np.empty(cap,np.int32);vv=np.empty(cap,np.int64);p=0
    for i in range(len(O)):
        rr[p]=0;cc[p]=i;vv[p]=1;p+=1
        for k in range(7):
            v=364*np.int64(O[i,k])
            if v:rr[p]=3+k;cc[p]=i;vv[p]=v;p+=1
        for j in range(2):
            a,b=O[i,7+2*j],O[i,8+2*j];rr[p]=lookup[j,a,b,0];cc[p]=i;vv[p]=-4;p+=1
    offset=len(O)
    for j in range(2):
      I=I0 if j==0 else I1
      for i in range(len(I)):
        c=offset+i;rr[p]=1+j;cc[p]=c;vv[p]=1;p+=1
        for di in range(4):
            a,b=I[i,10*di],I[i,10*di+1]
            rr[p]=lookup[j,a,b,0];cc[p]=c;vv[p]=1;p+=1
            for k in range(lengths[j,a,b]):
                v=121*np.int64(I[i,10*di+2+k])-forces[j,a,b,k]
                if v:rr[p]=lookup[j,a,b,k+1];cc[p]=c;vv[p]=v;p+=1
            if thid[j,a,b]>=0:
                v=121*np.int64(I[i,10*di+9])-475918720*thmult[j,a,b]
                if v:rr[p]=thid[j,a,b];cc[p]=c;vv[p]=v;p+=1
      offset+=len(I)
    return rr[:p],cc[:p],vv[:p]
def main(mode='primal'):
    signal.alarm(600 if mode=='dual' else 260);start=time.monotonic()
    INNER=[complete_inner(N)for N in KEY[:2]];I0,I1=[d[0]for d in INNER]
    O=np.load(HERE.parent/'quotient_outer.npz')['records'];lookup=np.full((2,46,46,8),-1,np.int32);forces=np.zeros((2,46,46,7),np.int64);lengths=np.zeros((2,46,46),np.int32)
    thid=np.full((2,46,46),-1,np.int32);thmult=np.zeros((2,46,46),np.int64)
    rows=[('norm_outer',),('norm_inner',0),('norm_inner',1)]+[('outer_feature',i)for i in range(7)]
    for j,d in enumerate(INNER):
      for tt in d[1]:
        t=tuple(map(int,tt));a,b,c=t;F=M.grouped_force(t);lengths[j,a,b]=len(F);forces[j,a,b,:len(F)]=F
        for k in range(len(F)+1):lookup[j,a,b,k]=len(rows);rows.append(('conditional',j,t,k))
    neq=len(rows);upper=[]
    for j,d in enumerate(INNER):
      for tt in d[1]:
        t=tuple(map(int,tt));a,b,c=t
        if 40 in t:thid[j,a,b]=len(rows);thmult[j,a,b]=t.count(40);upper.append(len(rows));rows.append(('conditional_theta40',j,t))
    ntables=len(O)+len(I0)+len(I1);nv=ntables+len(upper);nrows=len(rows)
    nnz_bound=10*len(O)+37*(len(I0)+len(I1))
    planned_bytes=nnz_bound*100+nv*100+300_000_000
    print('THETA_MEMORY',planned_bytes,flush=True);assert planned_bytes<2*1024**3
    rr,cc,vv=assemble(O,I0,I1,lookup,forces,lengths,thid,thmult)
    assert np.all(rr>=0)
    A=sparse.coo_matrix((vv,(rr,cc)),shape=(nrows,ntables),dtype=np.int64).tocsr();del rr,cc,vv
    sl=sparse.coo_matrix((np.ones(len(upper),np.int64),(upper,np.arange(len(upper)))),shape=(nrows,len(upper))).tocsr()
    A=sparse.hstack([A,sl],format='csr');A.eliminate_zeros();del sl
    b=np.array([1,1,1]+M.force(KEY,7)+[0]*(nrows-10),np.int64)
    scale=np.maximum(np.asarray(abs(A).max(axis=1).toarray()).ravel(),abs(b));scale[scale==0]=1
    As=sparse.diags(1/scale)@A;eye=sparse.eye(nrows,format='csr');AA=sparse.hstack([As,eye,-eye],format='csr');del As,eye
    print('THETA_FULL_LP',dict(shape=A.shape,nnz=A.nnz,build_seconds=time.monotonic()-start,ru_maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),flush=True)
    lp=linprog(np.r_[np.zeros(nv),np.ones(2*nrows)],A_eq=AA,b_eq=b/scale,bounds=(0,None),method='highs',options={'time_limit':120,'presolve':True})
    result=dict(target=KEY,complete_declared_cone=True,inner_counts=[d[2]for d in INNER],rows=nrows,columns=nv,status=int(lp.status),message=lp.message,elapsed=time.monotonic()-start,exact_result=False,ru_maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if lp.success:
        result['objective']=float(lp.fun);dual=np.asarray(lp.eqlin.marginals)/scale
        (HERE/'FLOAT_DUAL.json').write_text(json.dumps(dict(dual=dual.tolist(),rows=rows),indent=2)+'\n')
        if lp.fun<1e-8:
            support=np.flatnonzero(lp.x[:nv]>1e-11);sparse.save_npz(HERE/'feasible_basis.npz',A[:,support]);np.savez_compressed(HERE/'feasible_solution.npz',support=support,weights=lp.x[support],rhs=b)
            result.update(status_label='NUMERICAL_FEASIBLE_NEEDS_EXACT_RECOVERY',support=len(support))
        else:
            attempts=[]
            for mul in(10**6,10**8,10**10,10**12,10**14):
                q=np.rint(dual*mul).astype(np.int64);q[upper]=np.minimum(q[upper],0)
                div=math.gcd(*map(int,q))
                if div:q//=div
                ab=sum(int(abs(q[r]))*int(abs(A.getrow(r)).max())for r in range(nrows))
                if ab>=2**62:continue
                val=np.asarray(A.T@q).ravel();bounds=[int(val[:len(O)].max()),int(val[len(O):len(O)+len(I0)].max()),int(val[len(O)+len(I0):ntables].max())]
                for j,v in enumerate(bounds):q[j]-=v
                ab+=sum(abs(v)for v in bounds);assert ab<2**62
                val=np.asarray(A.T@q).ravel();rhs=sum(int(a)*int(bb)for a,bb in zip(q,b));mx=int(val.max())
                attempts.append(dict(scale=mul,maximum_column=mx,rhs=rhs,normalization_repairs=bounds,absolute_integer_bound=ab))
                if mx<=0 and rhs>0:
                    result['exact_result']=True;result['status_label']='CANDIDATE_EXACT_COUPLED_THETA40_DUAL'
                    (HERE/'EXACT_DUAL.json').write_text(json.dumps(dict(target=KEY,dual=list(map(int,q)),rows=rows,maximum_column=mx,rhs=rhs,upper_rows=upper,normalization_repairs=bounds,absolute_integer_bound=ab),indent=2)+'\n');break
            result['integer_attempts']=attempts
    (HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print('THETA_RESULT',json.dumps(result),flush=True)
if __name__=='__main__':main()
