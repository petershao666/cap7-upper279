"""P3b independent local replay plus plain integer C++ outer input export."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from itertools import product
import json,time,hashlib
import verify_pointed as V
P=V.P;J=json.loads((P/'pointed_joint_certificate.json').read_text());ph=dict(zip(map(tuple,J['types']),J['phi']))
for h in json.loads((P/'pointed_transfer_tables.json').read_text())['functions']:V.sources[h['id']]=h;V.look[h['id']]=dict(zip(map(tuple,h['types']),h['phi']))
start=time.monotonic();checks=[]
assert set(ph)==V.T107
for z in J['inner']:
    A=tuple(z['anchor']);j=z['marked_column'];ri=V.D['anchors'].index(list(A));prefix=list(map(tuple,V.D['anchors'][:ri]))
    assert V.forced(A,j,z['features'])==z['forced'] and all(z['coeff'][i]>=0 for i in z['positive'])
    cols=[[t for t in V.allowed if sum(t)==n]for n in A];count=0;mini=None
    for mat in product(*cols):
        if not V.cross(mat):continue
        ts=V.top(mat)
        if any(t not in V.T107 or any(V.dom(t,u)for u in prefix)for t in ts):continue
        for r in range(3):
            upd=[list(t)for t in mat];upd[j][r]+=1
            if tuple(upd[j])not in V.allowed or not V.cross(upd)or any(t not in V.T108 for t in V.top(upd)):continue
            f=V.features(mat,j,r,z['features']);val=sum(a*b for a,b in zip(f,z['coeff']))-sum(ph[t]for t in ts)
            assert val>=z['K'];mini=val if mini is None else min(mini,val);count+=1
    assert mini==z['K']and count>=z['count']
    assert z['bound']==ph[A]+sum(a*b for a,b in zip(z['coeff'],z['forced']))-121*z['K']
    checks.append(dict(anchor=A,marked_column=j,count=count,minimum=mini));print('LOCAL',A,j,count,'PASS',flush=True)
assert J['conditional_bound']==max(z['bound']for z in J['inner'])
tr=J['transferred108'];assert set(map(tuple,tr['types']))==V.T108 and tr['bound']==108*J['conditional_bound']
for t,v in zip(tr['types'],tr['phi']):
    ans=0
    for i in range(3):u=t.copy();u[i]-=1;ans+=t[i]*ph[V.sort(u)]
    assert ans==v
o=J['outer'];assert o['features'][2]==[1,'joint106_107_106_63_size276']
assert all(q==0 for i,q in enumerate(o['coeff'])if i>=7 and i!=9)
assert sum(a*b for a,b in zip(o['coeff'],o['totals']))+tr['bound']==o['forced']
assert 364*o['K']-o['forced']==o['gap']>0
out=dict(status='LOCAL_AND_TRANSFER_PASS_OUTER_PENDING',full_marked_count=sum(x['count']for x in checks),branches=checks,transfer_values=30,certificate_sha256=hashlib.sha256((P/'pointed_joint_certificate.json').read_bytes()).hexdigest(),elapsed=time.monotonic()-start)
(P/'pointed_joint_local_verification.json').write_text(json.dumps(out,indent=2)+'\n')
f6=V.old+[x for x in V.comp if not(x[2]<=22 or x[0]<=40 and x[1]<=36)]
src=V.sources['joint106_107_106_63_size276'];parts=[]
parts.append(' '.join(map(str,J['base']+o['coeff'][:7]+[o['coeff'][9],o['K'],o['forced'],o['gap']])))
for tt in [f6,V.comp,J['ordinary_bans']]:
    parts.append(str(len(tt)));parts +=[' '.join(map(str,t))for t in tt]
for h in [tr,src]:
    parts.append(str(len(h['types'])));parts +=[' '.join(map(str,t+[v]))for t,v in zip(h['types'],h['phi'])]
(P/'pointed_joint_outer_input.txt').write_text('\n'.join(parts)+'\n')
print('LOCAL_TRANSFER_PASS',out['full_marked_count'],flush=True)
