"""P3b: unknown conditional107 function enters outer only after108 deletions."""
import sys,os
sys.dont_write_bytecode=True
for n in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[n]='1'
from pathlib import Path
import json,time,signal,itertools
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
import pointed as P3
P=P3.P;G=P3.G;M=sys.modules['minimum'];E=G.E
fixedP3=json.loads((P/'pointed_transfer_tables.json').read_text())['functions']
P3.H108 +=fixedP3;P3.LOOK108 +=[dict(zip(map(tuple,h['types']),h['phi']))for h in fixedP3]
prior=json.loads((P/'pointed_result.json').read_text())
signal.alarm(590);start=time.monotonic()
INS=[]
for ri,key in enumerate(G.RARE):
    eligible=[x for x in prior['ledger']if tuple(x['anchor107'])==key and x['status']=='ENUMERATED']
    if not eligible:continue
    z=G.inner(key,ri);adm=E.make_adm(5,np.empty((0,3),np.int64))
    for t in itertools.product(range(21),repeat=3):
        if not G.V.downwards_allowed(t,[(20,19,2),(20,18,3),(19,19,3),(19,18,4)]):adm[t]=False
    top=E.make_top(45,107,np.array(G.OLD+G.COMP+G.RARE[:ri],np.int64));ar=P3.rawenum(*key,adm,top,G.index)
    for rec in eligible:
        j=rec['marked_column'];zz=P3.marked(z,ar,j,adm);assert zz['status']=='ENUMERATED';zz.update(key=key,j=j)
        zz['scale']=np.maximum(np.max(abs(zz['X']-zz['F']/121),axis=0),1);zz['W']=(zz['X']-zz['F']/121)/zz['scale'];INS.append(zz)
print('INNER_COUNTS',[(z['key'],z['j'],len(z['X']))for z in INS],flush=True)
ordinary=list(map(tuple,json.loads((P/'arrangement.json').read_text())['ordinary_bans']))
funcs=json.loads((P/'transfer_tables.json').read_text())['functions']+json.loads((P.parent/'root_audit/h3_transport_tables.json').read_text())['functions']+fixedP3
targets=[(108,106,61)] if '--first-only'in sys.argv else[(108,106,61),(108,107,60)]
results=[]
for base in targets:
    ar=M.en(base,ordinary+[t for t in M.T if M.Q(t)<M.Q(base)])
    mask=np.ones(len(ar),bool)
    for j in (0,1):
        for t in M.COMP:mask &=~np.all(ar[:,7+3*j:10+3*j]>=t,axis=1)
    ar=ar[mask];X,F,meta,pos=M.prepare(ar,base,(0,0,-1))
    for j in (0,1):
        for h in funcs:
            if h['m']!=base[j]:continue
            lu=np.zeros((46,46),np.int64)
            for t,v in zip(h['types'],h['phi']):lu[tuple(t[:2])]=v
            X=np.c_[X,lu[ar[:,7+3*j],ar[:,8+3*j]]];pos.append(len(F));F=np.r_[F,h['bound']];meta.append((j,h['id']))
    scale=np.maximum(np.max(abs(X-F/364),axis=0),1);W=(X-F/364)/scale
    ty108=list(map(tuple,fixedP3[0]['types']));ix108={t:i for i,t in enumerate(ty108)}
    parentid=np.array([ix108[tuple(t)]for t in ar[:,7:10]],np.int32)
    # Transfer matrix has exactly108 weighted source profiles per parent.
    TR=np.zeros((len(ty108),len(G.TY)),np.int64)
    for ii,t in enumerate(ty108):
        for j in range(3):
            u=list(t);u[j]-=1;TR[ii,G.IX[tuple(sorted(u,reverse=True))]]+=t[j]
    assert np.all(TR.sum(axis=1)==108)
    no=len(G.TY);beta=no;offset=no+1;bounds=[(-1,1)]*no+[(None,None)]
    for z in INS:
        z['offset']=offset;offset+=z['X'].shape[1];bounds +=[(0,1)if i in z['pos']else(-1,1)for i in range(z['X'].shape[1])]
    outeroffset=offset;offset+=X.shape[1];bounds +=[(0,1)if i in pos else(-1,1)for i in range(X.shape[1])]
    delta=offset;nv=offset+1;bounds.append((None,None))
    chunks=[]
    for z in INS:
        rr=np.zeros((len(z['X']),nv));rr[:,z['offset']:z['offset']+z['X'].shape[1]]=-z['W']
        for j in range(3):rr[np.arange(len(rr)),z['tops'][:,j]]+=1
        rr[:,z['anchor']]+=1/121;rr[:,beta]=-364/121;chunks.append(sparse.csr_matrix(rr))
    fixed=sparse.vstack(chunks,format='csr');inds=np.unique(np.r_[np.argmin(W,axis=0),np.argmax(W,axis=0)])
    result=dict(base=base,count=len(X),inner_counts=[len(z['X'])for z in INS],status='NO_NEW_CERTIFICATE_NO_INFERENCE',outer_features=meta,positive=pos,forced=list(map(int,F)))
    print('MODEL',base,len(X),'variables',nv,flush=True)
    for it in range(120):
        rr=np.zeros((len(inds),nv));rr[:,:no]=-TR[parentid[inds]]/108;rr[:,beta]=1;rr[:,outeroffset:delta]=-W[inds];rr[:,delta]=1
        A=sparse.vstack([fixed,sparse.csr_matrix(rr)],format='csr')
        lp=linprog(np.r_[np.zeros(nv-1),-1.],A_ub=A,b_ub=np.zeros(A.shape[0]),bounds=bounds,method='highs',options={'time_limit':120})
        if not lp.success:result['numerical_status']=lp.message;break
        q=lp.x;gap=q[-1];values=W@q[outeroffset:delta]+(TR@q[:no])[parentid]/108-q[beta];mini=float(values.min())
        print('ITER',base,it,'gap',gap,'min',mini,'elapsed',round(time.monotonic()-start,2),flush=True)
        result.update(last_gap=float(gap),last_min=mini,iterations=it+1)
        if gap<1e-9:break
        if mini>=gap-1e-9:
            result.update(status='POSITIVE_FLOAT_CANDIDATE_REQUIRES_EXACT_RECOVERY',solution=list(map(float,q)),outeroffset=outeroffset,outer_scale=list(map(float,scale)),inner_offsets=[z['offset']for z in INS],inner_scales=[list(map(float,z['scale']))for z in INS]);break
        add=np.argpartition(values,min(49,len(values)-1))[:50];inds=np.unique(np.r_[inds,add])
    results.append(result);(P/'pointed_joint_result.json').write_text(json.dumps(dict(cases=results,elapsed=time.monotonic()-start,domain=G.TY,status='BOUNDED_DISCOVERY_COMPLETE'if len(results)==len(targets)else'DISCOVERY_RUNNING'),indent=2)+'\n')
    print('RESULT',base,result['status'],flush=True)
    del ar,X,W
