import run_theta40 as T
from run_theta40 import np,sparse,time,json,HERE
from scipy.optimize import linprog as scipy_lp
from types import SimpleNamespace
def compact_dual(c,A_eq,b_eq,**kwargs):
    start=time.monotonic();nr=A_eq.shape[0];nv=len(c)-2*nr
    A=A_eq[:,:nv].tocsr();At=A.T.tocsr();Ac=A.tocsc()
    degrees=np.diff(Ac.indptr);single=np.flatnonzero(degrees==1)
    upperrows={int(Ac.indices[Ac.indptr[j]])for j in single if Ac.data[Ac.indptr[j]]>0}
    bounds=[(-1,0)if r in upperrows else(-1,1)for r in range(nr)]
    active=set(map(int,single))
    for r in range(nr):
        lo,hi=A.indptr[r:r+2]
        if hi>lo:
            v=A.data[lo:hi];ids=A.indices[lo:hi]
            active.add(int(ids[np.argmin(v)]));active.add(int(ids[np.argmax(v)]))
    qcounts=json.loads((HERE.parent/'QUOTIENT_COUNTS.json').read_text())
    ends=[0,qcounts['outer']['quotient_count']]
    ends+=[ends[-1]+qcounts[str(T.KEY[0])]['quotient_count']]
    ends+=[ends[-1]+qcounts[str(T.KEY[1])]['quotient_count'],nv]
    history=[]
    for it in range(80):
        remain=420-(time.monotonic()-start)
        if remain<=0:break
        ids=np.array(sorted(active),np.int64)
        r=scipy_lp(-b_eq,A_ub=At[ids],b_ub=np.zeros(len(ids)),bounds=bounds,method='highs',options={'time_limit':min(30,remain),'presolve':True})
        if not r.success:
            history.append(dict(iteration=it,status=int(r.status),message=r.message));break
        u=r.x;v=np.asarray(At@u).ravel();mx=float(v.max());gap=float(b_eq@u)
        rec=dict(iteration=it,constraints=len(ids),dual_objective=gap,full_maximum_column=mx,elapsed=time.monotonic()-start)
        history.append(rec);print('DIRECT_DUAL',json.dumps(rec),flush=True)
        (HERE/'DIRECT_DUAL_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n')
        if mx<=1e-9:
            z=np.zeros(nv);z[ids]=-np.asarray(r.ineqlin.marginals)
            residual=b_eq-A@z
            for j in single:
                rr=int(Ac.indices[Ac.indptr[j]]);a=float(Ac.data[Ac.indptr[j]])
                if a>0 and residual[rr]>0:
                    z[j]+=residual[rr]/a;residual[rr]=0
            x=np.r_[z,np.maximum(residual,0),np.maximum(-residual,0)]
            (HERE/'DIRECT_DUAL_CHECKPOINT.json').write_text(json.dumps(dict(dual_objective=gap,maximum_column=mx,normalized_dual=u.tolist(),active_columns=ids.tolist(),reconstructed_phase1_residual_l1=float(abs(residual).sum())),indent=2)+'\n')
            return SimpleNamespace(status=0,message='Optimal compact dual; every complete column priced',success=True,fun=gap,x=x,eqlin=SimpleNamespace(marginals=u))
        added=0
        for lo,hi in zip(ends,ends[1:]):
            if hi<=lo:continue
            vv=v[lo:hi];k=min(128,len(vv));ii=np.argpartition(-vv,k-1)[:k]+lo
            for j in ii:
                if v[j]>1e-10 and int(j)not in active:active.add(int(j));added+=1
        if not added:
            history.append(dict(status='FULL_PRICING_NUMERICAL_STAGNATION'));break
    (HERE/'DIRECT_DUAL_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n')
    return SimpleNamespace(status=1,message='Bounded compact-dual pricing ended without a verified terminal dual',success=False)
if __name__=='__main__':
    T.linprog=compact_dual
    T.main(mode='dual')
