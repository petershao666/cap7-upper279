import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import sys,json,math,time,signal,resource
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import coupled_model as M
from coupled_model import np,E,njit,itertools,OLD,COMP,BAN,allowed,sparse,linprog
KEY=(107,107,61)
@njit
def outer_records(mats):
    out=np.zeros((len(mats),9),np.int32)
    for n in range(len(mats)):
        m=mats[n].astype(np.int64)
        for a in range(3):
          for b in range(3):out[n,0]+=m[a]*m[3+b]*m[6+(-a-b)%3]
        for j in range(3):
            a,b,c=m[3*j],m[3*j+1],m[3*j+2]
            k=1 if j<2 else 3
            out[n,k]+=a*b+a*c+b*c;out[n,k+1]+=a*b*c
        a,b,c=E.sorted3(m[0],m[1],m[2]);d,e,f=E.sorted3(m[3],m[4],m[5])
        if (a,b)>(d,e):a,b,d,e=d,e,a,b
        out[n,5]=a;out[n,6]=b;out[n,7]=d;out[n,8]=e
    return out
@njit
def assemble(O,I,lookup,forces,lengths,thid,thmult):
    cap=8*len(O)+37*len(I)
    rr=np.empty(cap,np.int32);cc=np.empty(cap,np.int32);vv=np.empty(cap,np.int64);p=0
    for c in range(len(O)):
        rr[p]=0;cc[p]=c;vv[p]=1;p+=1
        for k in range(5):
            v=364*np.int64(O[c,k])
            if v:rr[p]=2+k;cc[p]=c;vv[p]=v;p+=1
        for j in range(2):
            a,b=O[c,5+2*j],O[c,6+2*j];rr[p]=lookup[a,b,0];cc[p]=c;vv[p]=-2;p+=1
    for i in range(len(I)):
        c=len(O)+i;rr[p]=1;cc[p]=c;vv[p]=1;p+=1
        for di in range(4):
            a,b=I[i,10*di],I[i,10*di+1]
            rr[p]=lookup[a,b,0];cc[p]=c;vv[p]=1;p+=1
            for k in range(lengths[a,b]):
                v=121*np.int64(I[i,10*di+2+k])-forces[a,b,k]
                if v:rr[p]=lookup[a,b,k+1];cc[p]=c;vv[p]=v;p+=1
            if thid[a,b]>=0:
                v=121*np.int64(I[i,10*di+9])-475918720*thmult[a,b]
                if v:rr[p]=thid[a,b];cc[p]=c;vv[p]=v;p+=1
    return rr[:p],cc[:p],vv[:p]
def main():
    signal.alarm(1200);start=time.monotonic()
    path=HERE/'outer.npz'
    if not path.exists():
        f6=OLD+[t for t in COMP if not (t[2]<=22 or(t[0]<=40 and t[1]<=36))]
        adm=E.make_adm(6,np.array(f6,np.int64));nc=adm.copy()
        for t in itertools.product(range(46),repeat=3):
            if not allowed(t,COMP):nc[t]=False
        worse=[(a,b,275-a-b)for a in range(113)for b in range(a+1)if 0<=275-a-b<=b and M.q((a,b,275-a-b))<M.q(KEY)]
        top=E.make_top(112,275,np.array(BAN+worse,np.int64))
        _,count=M.collect(*KEY,adm,top,nc,True,1)
        raw,count2=M.collect(*KEY,adm,top,nc,True,int(count));assert count==count2==len(raw)
        records=outer_records(raw);unique,ix=np.unique(records,axis=0,return_index=True)
        np.savez_compressed(path,records=unique,representatives=raw[ix],full_count=count)
        print('OUTER_FULL',count,'QUOTIENT',len(unique),flush=True)
        del raw,records,unique,ix
    d=np.load(path);O=d['records'];outercount=int(d['full_count'])
    d=np.load(HERE.parent/'theta40/inner_107.npz');I=d['records'];types=d['types'];innercount=int(d['full_count'])
    lookup=np.full((46,46,8),-1,np.int32);forces=np.zeros((46,46,7),np.int64);lengths=np.zeros((46,46),np.int32);thid=np.full((46,46),-1,np.int32);thmult=np.zeros((46,46),np.int64)
    rows=[('norm_outer',),('norm_inner',)]+[('outer_symmetric_feature',k)for k in range(5)]
    for tt in types:
        t=tuple(map(int,tt));a,b,c=t;F=M.grouped_force(t);forces[a,b,:len(F)]=F;lengths[a,b]=len(F)
        for k in range(len(F)+1):lookup[a,b,k]=len(rows);rows.append(('conditional',t,k))
    upper=[]
    for tt in types:
        t=tuple(map(int,tt));a,b,c=t
        if 40 in t:thid[a,b]=len(rows);thmult[a,b]=t.count(40);upper.append(len(rows));rows.append(('conditional_theta40',t))
    (HERE/'ROWS.json').write_text(json.dumps(rows,indent=2)+'\n')
    nt=len(O)+len(I);nr=len(rows)
    planned=(8*len(O)+37*len(I))*95+(nt+len(upper))*90+220000000
    assert planned<2*1024**3
    rr,cc,vv=assemble(O,I,lookup,forces,lengths,thid,thmult);assert np.all(rr>=0)
    A=sparse.coo_matrix((vv,(rr,cc)),shape=(nr,nt),dtype=np.int64).tocsr();del rr,cc,vv
    sl=sparse.coo_matrix((np.ones(len(upper),np.int64),(upper,np.arange(len(upper)))),shape=(nr,len(upper))).tocsr();A=sparse.hstack([A,sl],format='csr');A.eliminate_zeros();del sl
    b=np.array([1,1,121*107*107*61,2*243*math.comb(107,2),2*81*math.comb(107,3),243*math.comb(61,2),81*math.comb(61,3)]+[0]*(nr-7),np.int64)
    scale=np.maximum(np.asarray(abs(A).max(axis=1).toarray()).ravel(),abs(b));scale[scale==0]=1
    As=(sparse.diags(1/scale)@A).tocsr();At=As.T.tocsr();bb=b/scale
    active=set(range(nt,A.shape[1]))
    for r in range(nr):
        lo,hi=As.indptr[r:r+2]
        if hi>lo:
            v=As.data[lo:hi];ids=As.indices[lo:hi];active.add(int(ids[np.argmin(v)]));active.add(int(ids[np.argmax(v)]))
    print('MODEL',dict(rows=nr,columns=A.shape[1],nnz=A.nnz,outer_full=outercount,inner_full=innercount,outer_quotient=len(O),inner_quotient=len(I),seconds=time.monotonic()-start,planned=planned),flush=True)
    bounds=[(-1,0)if r in upper else(-1,1)for r in range(nr)];hist=[];ds=time.monotonic();result=dict(target=KEY,status='UNRESOLVED_BOUNDED_SEARCH',exact_result=False,outer_count=outercount,inner_count=innercount,rows=nr,columns=A.shape[1])
    for it in range(80):
        remain=420-(time.monotonic()-ds)
        if remain<=0:break
        ids=np.array(sorted(active),np.int64)
        lp=linprog(-bb,A_ub=At[ids],b_ub=np.zeros(len(ids)),bounds=bounds,method='highs',options={'time_limit':min(30,remain),'presolve':True})
        if not lp.success:hist.append(dict(iteration=it,status=lp.status,message=lp.message));break
        u=lp.x;v=np.asarray(At@u).ravel();mx=float(v.max());gap=float(bb@u);h=dict(iteration=it,active=len(ids),gap=gap,maximum=mx,seconds=time.monotonic()-ds);hist.append(h);print('DUAL',json.dumps(h),flush=True)
        (HERE/'HISTORY.json').write_text(json.dumps(hist,indent=2)+'\n')
        if mx<=1e-9:
            dual=u/scale;(HERE/'FLOAT_DUAL.json').write_text(json.dumps(dict(dual=dual.tolist(),rows=rows),indent=2)+'\n')
            attempts=[]
            for mul in (10**6,10**8,10**10,10**12,10**14):
                q=np.rint(dual*mul).astype(np.int64);q[upper]=np.minimum(q[upper],0);div=math.gcd(*map(int,q))
                if div:q//=div
                ab=sum(int(abs(q[r]))*int(abs(A.getrow(r)).max())for r in range(nr))
                if ab>=2**62:continue
                cost=np.asarray(A.T@q).ravel();repairs=[int(cost[:len(O)].max()),int(cost[len(O):nt].max())]
                for j,r in enumerate(repairs):q[j]-=r
                ab+=sum(abs(r)for r in repairs);assert ab<2**62
                cost=np.asarray(A.T@q).ravel();rhs=sum(int(x)*int(y)for x,y in zip(q,b));maxcol=int(cost.max())
                attempts.append(dict(scale=mul,rhs=rhs,maximum_column=maxcol,repairs=repairs,absolute_bound=ab))
                if rhs>0 and maxcol<=0:
                    cert=dict(target=KEY,symmetric_equal_slice_model=True,dual=list(map(int,q)),rows=rows,upper_rows=upper,rhs=rhs,maximum_column=maxcol,normalization_repairs=repairs,absolute_integer_bound=ab)
                    (HERE/'EXACT_DUAL.json').write_text(json.dumps(cert,indent=2)+'\n');result.update(status='CANDIDATE_EXACT_DUAL',exact_result=True,rhs=rhs);break
            result['attempts']=attempts;result['numerical_gap']=gap
            if gap<=1e-9:
                weight=np.zeros(A.shape[1]);weight[ids]=-lp.ineqlin.marginals;support=np.flatnonzero(weight>1e-10);sparse.save_npz(HERE/'FEASIBLE_BASIS.npz',A[:,support]);np.savez_compressed(HERE/'FEASIBLE_NUMERICAL.npz',support=support,weights=weight[support],rhs=b);result['status']='NUMERICAL_FEASIBLE_NEEDS_EXACT_RECOVERY'
            break
        added=0
        for lo,hi in ((0,len(O)),(len(O),nt)):
            vv=v[lo:hi];k=min(128,len(vv));ii=np.argpartition(-vv,k-1)[:k]+lo
            for j in ii:
                if v[j]>1e-10 and int(j)not in active:active.add(int(j));added+=1
        if not added:break
    result.update(history=hist,seconds=time.monotonic()-start,maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print('RESULT',json.dumps(result),flush=True)
if __name__=='__main__':main()
