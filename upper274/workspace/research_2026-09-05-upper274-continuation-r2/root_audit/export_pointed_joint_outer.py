from pathlib import Path
import json,hashlib,math
W=Path(__file__).resolve().parent;R=W.parent;B=R.parent/'audit_2026-09-05_upper275/cap7_upper275'
def read(p):return json.loads(p.read_text())
d=read(R/'root_potential/pointed_joint_certificate.json');c=read(B/'baseline277/baseline278/certificate.json')
assert d['base']==[108,106,61] and d['state']==[0,0,-1] and d['root_parameter']==67
old=[list(map(int,k.split(','))) for s in c['six_stages'] for k in s]
comp=c['completion_seeds']+[list(map(int,k.split(','))) for s in c['completion_stages'] for k in s]
prior=read(R.parent/'research_2026-09-05-capset-round1-r1/route_a/certificates.json')
ban=prior['seeds']+[[112,109,51],[111,110,51]]+[list(map(int,k.split(','))) for s in prior['stages'] for k in s]
assert len(ban)==len(set(map(tuple,ban)))==len(d['ordinary_bans'])
assert set(map(tuple,d['ordinary_bans']))==set(map(tuple,ban))
oldh=read(B/'results/size276/proof.json')['new_histograms']+[dict(read(B/'baseline277/certificate.json')['nested108'],id='psi108',m=108)]
hs=oldh+read(R/'root_potential/transfer_tables.json')['functions']+read(W/'h3_transport_tables.json')['functions']+read(R/'root_potential/pointed_transfer_tables.json')['functions']
lookup={h['id']:h for h in hs}
new=d['transferred108'];phi=dict(zip(map(tuple,d['types']),d['phi']))
assert new['types']==lookup['psi108']['types'] and new['bound']==108*d['conditional_bound']
for t,v in zip(new['types'],new['phi']):
 value=0
 for j in range(3):
  u=t[:];u[j]-=1;value+=t[j]*phi[tuple(sorted(u,reverse=True))]
 assert value==v
hh=[];extras=[]
for j,name in d['outer']['features']:
 h=lookup[name];assert h['m']==d['base'][j];extras.append((j,len(hh)));hh.append(h)
extras.append((0,len(hh)));hh.append(dict(new,m=108))
q=d['outer']['coeff']+[1];assert all(v>=0 for v in q[7:])
key=d['base'];forced=[121*math.prod(key)]+[x for n in key for x in (243*math.comb(n,2),81*math.comb(n,3))]
assert d['outer']['totals']==forced+[h['bound'] for h in hh[:-1]]
U=sum(a*b for a,b in zip(q,forced+[h['bound'] for h in hh]));assert U==d['outer']['forced'] and 364*d['outer']['K']-U==d['outer']['gap']>0
out=[]
def line(*a):out.append(' '.join(map(str,a)))
line(len(old),len(comp),len(hh),1)
for t in old+comp:line(*t)
for h in hh:
 line(h['m'],h['bound'],len(h['types']))
 for t,v in zip(h['types'],h['phi']):line(*t,v)
line(*key,1,0,0,-1,0,len(ban),len(extras),len(q))
for t in ban:line(*t)
for j,i in extras:line(j,i)
line(*q);line(d['outer']['K'],U,d['outer']['gap'])
(W/'pointed_joint_outer_input.txt').write_text('\n'.join(out)+'\n')
info={'status':'EXACT_TRANSFER_AND_OUTER_DEPENDENCY_PASS','transfer_values':30,'target':key,'positive_gap':d['outer']['gap'],'source_sha256':hashlib.sha256((R/'root_potential/pointed_joint_certificate.json').read_bytes()).hexdigest(),'input_sha256':hashlib.sha256((W/'pointed_joint_outer_input.txt').read_bytes()).hexdigest(),'local_conditional_proof_required':'pointed_joint_independent.json','checker_dependency':'Frozen round1 root independent_a.cpp, mathematical domain rebuilt with new coefficients and checked source data'}
(W/'pointed_joint_outer_manifest.json').write_text(json.dumps(info,indent=2)+'\n');print(info)
