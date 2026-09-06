"""P6 full33 conditional five-dimensional functions, sole10710662 target."""
import os,sys
sys.dont_write_bytecode=True
for n in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[n]='1'
from pathlib import Path
from math import comb,prod,gcd
import json,time,signal,hashlib
import numpy as np
from numba import njit
from scipy import sparse
from scipy.optimize import linprog
P=Path(__file__).resolve().parent;R=P.parents[1]/'research_2026-09-05-capset-round1-r1/route_a'
sys.path.insert(0,str(R));import minimum as M
start=time.monotonic();signal.alarm(590)
import importlib.util
funpath=P.parent/'compatibility/l2_all5d_10610663/FUNCTIONS.json'
assert hashlib.sha256(funpath.read_bytes()).hexdigest()=='92a0104c9db8bf04b55e503e2e71f523178dd134ca25045480ea55093a6f5336'
FUN=json.loads(funpath.read_text())['functions'];NF=len(FUN);assert NF==33
spec=importlib.util.spec_from_file_location('p6_shared_l2',funpath.parent/'search.py');L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
old=np.load(P.parent/'compatibility/theta40/inner_107.npz');types=list(map(tuple,old['types'].tolist()));assert len(types)==47
adm=M.E.make_adm(5,np.empty((0,3),np.int64))
for t in M.itertools.product(range(21),repeat=3):
    if not M.V.downwards_allowed(t,[(20,19,2),(20,18,3),(19,19,3),(19,18,4)]):adm[t]=False
for f in FUN:
    supp=set(map(tuple,f['types']))
    for a in range(21):
        for b in range(a+1):
            c=f['size']-a-b
            if 0<=c<=b and adm[a,b,c]:assert(a,b,c)in supp
stop=M.E.make_top(45,107,np.array(M.OLD+M.COMP,np.int64));chunks=[];counts=[]
for t,n in zip(types,old['counts']):
    raw,count=L.M.collect(*t,adm,stop,np.ones_like(adm),False,int(n));assert count==len(raw)==n
    rec=L.new_records(raw);chunks.append(np.unique(rec,axis=0));counts.append(count)
I=np.unique(np.concatenate(chunks),axis=0).astype(np.int64);del chunks,raw,rec
np.savez_compressed(P/'incidence107_all5d_inner.npz',records=I,types=np.array(types),counts=np.array(counts),full_count=sum(counts))
print('FRESH_INNER',sum(counts),len(I),'elapsed',round(time.monotonic()-start,2),flush=True)
rows=[('norm_outer',),('norm_inner',)]+[('outer_centered_moment',i)for i in range(7)]
lookup=np.full((46,46,8),-1,np.int32);forces=np.zeros((46,46,7),np.int64);lengths=np.zeros((46,46),np.int32)
for t in types:
    a,b,c=t;ff=[40*prod(t)]+[z for v in sorted(set(t))for z in (t.count(v)*81*comb(v,2),t.count(v)*27*comb(v,3))]
    lengths[a,b]=len(ff);forces[a,b,:len(ff)]=ff
    for k in range(len(ff)+1):lookup[a,b,k]=len(rows);rows.append(('conditional',t,k))
xid=np.full((46,46,NF),-1,np.int32);mult=np.zeros((46,46,NF),np.int64);upper=[]
fnsize=np.array([f['size']for f in FUN],np.int64);fb=np.array([f['bound']for f in FUN],np.int64);phi=np.zeros((NF,21,21),np.int64)
for fi,f in enumerate(FUN):
    for t,v in zip(f['types'],f['values']):phi[fi,t[0],t[1]]=v
for t in types:
    for fi,f in enumerate(FUN):
        if f['size']not in t:continue
        xid[t[0],t[1],fi]=len(rows);mult[t[0],t[1],fi]=t.count(f['size'])
        if f['kind']=='upper':upper.append(len(rows))
        rows.append(('conditional_extra',t,f['name'],f['kind']))
@njit
def buildinner(I,lookup,forces,lengths,xid,mult,fnsize,fb,phi):
    nn=(1+4*(8+len(fnsize)))*len(I);rr=np.empty(nn,np.int32);cc=np.empty(nn,np.int32);vv=np.empty(nn,np.int64);p=0
    for i in range(len(I)):
        rr[p]=i;cc[p]=1;vv[p]=1;p+=1
        for di in range(4):
            off=15*di;a,b=I[i,off],I[i,off+1];c=107-a-b;sz=(c,b,a)
            rr[p]=i;cc[p]=lookup[a,b,0];vv[p]=1;p+=1
            for k in range(lengths[a,b]):
                v=121*I[i,off+2+k]-forces[a,b,k]
                if v:rr[p]=i;cc[p]=lookup[a,b,k+1];vv[p]=v;p+=1
            for fi in range(len(fnsize)):
                if xid[a,b,fi]<0:continue
                g=0
                for j in range(3):
                    if sz[j]==fnsize[fi]:g+=phi[fi,I[i,off+9+2*j],I[i,off+10+2*j]]
                v=121*g-mult[a,b,fi]*fb[fi]
                if v:rr[p]=i;cc[p]=xid[a,b,fi];vv[p]=v;p+=1
    return rr[:p],cc[:p],vv[:p]
rr,cc,vv=buildinner(I,lookup,forces,lengths,xid,mult,fnsize,fb,phi);AIN=sparse.coo_matrix((vv,(rr,cc)),shape=(len(I),len(rows)),dtype=np.int64).tocsr();del rr,cc,vv
core_rows=rows.copy();core_upper=upper.copy();ordinary=list(map(tuple,json.loads((P/'arrangement.json').read_text())['ordinary_bans']))
extra=json.loads((P/'transfer_tables.json').read_text())['functions']+json.loads((P.parent/'root_audit/h3_transport_tables.json').read_text())['functions']
extra +=[h for h in json.loads((P.parent/'root_audit/incidence_histograms_independent.json').read_text())['functions']if h['id']in['NC107_theta40_j1','NC107_theta40_10710761_j0_floor10000']]
reports=[]
for base in [(107,106,62)]:
    ar=M.en(base,ordinary+[t for t in M.T if M.Q(t)<M.Q(base)]);mask=np.ones(len(ar),bool)
    for j in (0,1):
        for t in M.COMP:mask &=~np.all(ar[:,7+3*j:10+3*j]>=t,axis=1)
    ar=ar[mask];X=364*ar[:,:7].astype(np.int64)-M.E.force(base);rowmeta=core_rows.copy();up=core_upper.copy();featureids=list(range(2,9));functions=[]
    for j in (0,1):
        for h in M.H+extra:
            if h['m']!=base[j]:continue
            lu=np.zeros((46,46),np.int64)
            for t,v in zip(h['types'],h['phi']):lu[tuple(t[:2])]=v
            X=np.c_[X,364*lu[ar[:,7+3*j],ar[:,8+3*j]]-h['bound']]
            featureids.append(len(rowmeta));up.append(len(rowmeta));rowmeta.append(('outer_centered_upper',j,h['id']));functions.append(dict(column=j,id=h['id'],m=h['m'],types=h['types'],phi=h['phi'],bound=h['bound']))
    margids=lookup[ar[:,7],ar[:,8],0];assert np.all(margids>=0);del ar
    nr=len(rowmeta);AI=sparse.hstack([AIN,sparse.csr_matrix((len(I),nr-AIN.shape[1]),dtype=np.int64)],format='csr')
    sc=np.maximum(np.asarray(abs(AI).max(axis=0).toarray()).ravel(),1).astype(float)
    sc[0]=1;sc[1]=1;sc[lookup[:,:,0][lookup[:,:,0]>=0]]=np.maximum(sc[lookup[:,:,0][lookup[:,:,0]>=0]],4)
    sc[featureids]=np.maximum(np.max(abs(X),axis=0),1)
    AS=AI@sparse.diags(1/sc);Y=X/sc[featureids]
    # Complete row extrema seed finite constraint generation.
    ii=set();Ac=AS.tocsc()
    for r in range(nr):
        lo,hi=Ac.indptr[r:r+2]
        if hi>lo:
            vv=Ac.data[lo:hi];inds=Ac.indices[lo:hi];ii.add(int(inds[np.argmin(vv)]));ii.add(int(inds[np.argmax(vv)]))
    oi=set(map(int,np.r_[np.argmin(Y,axis=0),np.argmax(Y,axis=0)]));b=np.zeros(nr);b[:2]=1
    rep=dict(base=base,outer_count=len(X),inner_full_count=1407366,inner_feature_count=len(I),status='NO_NEW_CERTIFICATE_NO_INFERENCE',history=[])
    print('MODEL',base,len(X),nr,'inner_nnz',AI.nnz,'elapsed',round(time.monotonic()-start,2),flush=True);solution=None
    for it in range(150):
        ia=np.array(sorted(ii));oa=np.array(sorted(oi));AO=np.zeros((len(oa),nr));AO[:,0]=1;AO[:,featureids]=Y[oa];AO[np.arange(len(oa)),margids[oa]]=-4/sc[margids[oa]]
        AT=sparse.vstack([AS[ia],sparse.csr_matrix(AO)],format='csr')
        lp=linprog(-b,A_ub=AT,b_ub=np.zeros(AT.shape[0]),bounds=[(-1,0)if r in up else(-1,1)for r in range(nr)],method='highs',options={'time_limit':120})
        if not lp.success:rep['numerical_status']=lp.message;break
        u=lp.x;gap=float(b@u);vi=np.asarray(AS@u).ravel();vo=u[0]+Y@u[featureids]-4*u[margids]/sc[margids];mx=max(float(vi.max()),float(vo.max()))
        rec=dict(iteration=it,objective=gap,maximum_inner=float(vi.max()),maximum_outer=float(vo.max()),inner_active=len(ia),outer_active=len(oa),elapsed=time.monotonic()-start);rep['history'].append(rec);print('ITER',base,it,'gap',gap,'max',mx,'elapsed',round(time.monotonic()-start,2),flush=True)
        if gap<1e-9:break
        if mx<=1e-9:solution=u/sc;break
        for vv,inds in [(vi,ii),(vo,oi)]:
            k=min(127,len(vv)-1);add=np.argpartition(-vv,k)[:k+1]
            inds.update(int(j)for j in add if vv[j]>1e-10)
    if solution is not None:
        rep['status']='FLOAT_POSITIVE_REQUIRES_INTEGER_RECOVERY'
        for mul in [10**i for i in range(6,15,2)]:
            q=np.rint(solution*mul).astype(np.int64);q[up]=np.minimum(q[up],0)
            # Row-wise absolute bounds certify every signed64 dot product.
            rowmax=np.asarray(abs(AI).max(axis=0).toarray()).ravel();limin=sum(int(a)*abs(int(v))for a,v in zip(rowmax,q));limout=abs(int(q[0]))+sum(int(a)*abs(int(v))for a,v in zip(np.max(abs(X),axis=0),q[featureids]))+4*max(abs(int(q[r]))for r in margids)
            if max(limin,limout)>8*10**18:continue
            vi=np.asarray(AI@q).ravel();vo=q[0]+X@q[featureids]-4*q[margids];mi=int(vi.max());mo=int(vo.max());q[1]-=mi;q[0]-=mo;rhs=int(q[0])+int(q[1]);mx=max(int((AI@q).max()),int((q[0]+X@q[featureids]-4*q[margids]).max()))
            print('RECOVER',base,mul,rhs,mx,flush=True)
            if rhs>0 and mx<=0:
                cert=dict(status='EXACT_INTEGER_CANDIDATE_REQUIRES_INDEPENDENT_REPLAY',target=base,state=[0,0,-1],rows=rowmeta,dual=list(map(int,q)),upper_rows=up,rhs=rhs,maximum_column=mx,normalization_repairs=[mo,mi],absolute_bounds=[limout,limin],outer_count=len(X),inner_feature_count=len(I),inner_full_count=1407366,ordinary_bans=ordinary,root_parameter=67,functions=functions,source_functions=FUN,source_functions_sha256='92a0104c9db8bf04b55e503e2e71f523178dd134ca25045480ea55093a6f5336',inner_record_sha256=hashlib.sha256((P/'incidence107_all5d_inner.npz').read_bytes()).hexdigest())
                name='incidence107_all5d_certificate_'+'_'.join(map(str,base))+'.json';(P/name).write_text(json.dumps(cert,indent=2)+'\n');rep.update(status=cert['status'],certificate_file=name,rhs=rhs);break
    reports.append(rep);(P/'incidence107_all5d_result.json').write_text(json.dumps(dict(cases=reports,status='COMPLETE'if len(reports)==1 else'RUNNING',elapsed=time.monotonic()-start),indent=2)+'\n');print('RESULT',base,rep['status'],flush=True)
    del X,Y,AI,AS,Ac
