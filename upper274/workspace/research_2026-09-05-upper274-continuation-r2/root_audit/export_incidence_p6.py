from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;R=W.parent;B=R.parent/'audit_2026-09-05_upper275/cap7_upper275'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=R/'root_potential/incidence107_all5d_certificate_107_106_62.json';d=read(p);f=read(B/'baseline277/baseline278/certificate.json')
assert d['target']==[107,106,62] and d['state']==[0,0,-1] and d['root_parameter']==67 and len(d['dual'])==len(d['rows'])==587
old=[list(map(int,k.split(',')))for s in f['six_stages']for k in s];comp=f['completion_seeds']+[list(map(int,k.split(',')))for s in f['completion_stages']for k in s]
prev=read(R.parent/'research_2026-09-05-capset-round1-r1/route_a/certificates.json');ban=prev['seeds']+[[112,109,51],[111,110,51]]+[list(map(int,k.split(',')))for s in prev['stages']for k in s]
assert len(ban)==len(d['ordinary_bans'])==18 and set(map(tuple,ban))==set(map(tuple,d['ordinary_bans']))
known=read(B/'results/size276/proof.json')['new_histograms']+read(R/'root_potential/transfer_tables.json')['functions']+read(W/'h3_transport_tables.json')['functions']+read(W/'incidence_histograms_independent.json')['functions'];lu={h['id']:h for h in known}
for h in d['functions']:
 hh=lu[h['id']];assert all(h[k]==hh[k]for k in ['m','types','phi','bound']) and h['m']==d['target'][h['column']]
lowpath=R/'compatibility/l2_all5d_10610663/FUNCTIONS.json';low=read(lowpath)['functions'];assert d['source_functions_sha256']==sha(lowpath)
th=read(R/'hist105106/h3/h3_result.json')['histograms']['40'];out=[]
def line(*x):out.append(' '.join(map(str,x)))
line(*d['target'],len(old),len(comp),len(ban),len(th['types']),587,len(d['functions']),len(low),d['rhs'])
for t in old+comp+ban:line(*t)
for n in [42,43,44,45]:
 ts=f['spectrum5'][str(n)]['types'];line(n,len(ts))
 for t in ts:line(*t)
line(th['bound']+121*10**10)
for t,v in zip(th['types'],th['phi']):line(*t,v+10**10)
for h in d['functions']:
 line(h['column'],h['bound'],len(h['types']))
 for t,v in zip(h['types'],h['phi']):line(*t,v)
for h in low:
 line(h['size'],int(h['kind']=='exact'),h['bound'],len(h['types']))
 for t,v in zip(h['types'],h['values']):line(*t,v)
li={h['name']:i for i,h in enumerate(low)}
upper=[];fi={(h['column'],h['id']):i for i,h in enumerate(d['functions'])}
for i,(q,row)in enumerate(zip(d['dual'],d['rows'])):
 tag=row[0]
 if tag=='norm_outer':rr=[0,-1,0,0,0,-1]
 elif tag=='norm_inner':rr=[1,0,0,0,0,-1]
 elif tag=='outer_centered_moment':rr=[2,-1,0,0,0,row[1]]
 elif tag=='conditional':rr=[3,0,*row[1],row[2]]
 elif tag=='conditional_extra':
  k=li[row[2]];assert row[3]==low[k]['kind'];rr=[4,0,*row[1],k]
  if row[3]=='upper':upper.append(i);assert q<=0
 else:
  assert tag=='outer_centered_upper';rr=[5,-1,0,0,0,fi[(row[1],row[2])]];upper.append(i);assert q<=0
 line(q,*rr)
assert upper==d['upper_rows'];(W/'incidence_p6_input.txt').write_text('\n'.join(out)+'\n')
info=dict(status='INPUT_DEPENDENCIES_EXACT_PASS',source_sha256=sha(p),input_sha256=sha(W/'incidence_p6_input.txt'),target=d['target'],rows=587,upper_signs=len(upper),strict_rhs=d['rhs'],ordinary_bans='exactly18frozenordinarytypes; no minimum-onlytypeban',checker='verify_incidence_all5d.cpp; independentrawdomain usingrootpriorincidencekernel')
(W/'incidence_p6_manifest.json').write_text(json.dumps(info,indent=2)+'\n');print(info)
