"""Data-only exporter for a fresh mathematical-domain incidence audit."""
from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;R=W.parent;B=R.parent/'audit_2026-09-05_upper275/cap7_upper275'
def read(p):return json.loads(p.read_text())
f=read(B/'baseline277/baseline278/certificate.json')
old=[list(map(int,k.split(','))) for s in f['six_stages'] for k in s]
comp=f['completion_seeds']+[list(map(int,k.split(','))) for s in f['completion_stages'] for k in s]
prior=read(R.parent/'research_2026-09-05-capset-round1-r1/route_a/certificates.json')
ban=prior['seeds']+[[112,109,51],[111,110,51]]+[list(map(int,k.split(','))) for s in prior['stages'] for k in s]
path=R/'compatibility/theta40_10710761/EXACT_DUAL.json';d=read(path)
assert d['target']==[107,107,61] and len(d['rows'])==len(d['dual'])==375
h=read(R/'hist105106/h3/h3_result.json')['histograms']['40']
out=[]
def line(*x):out.append(' '.join(map(str,x)))
line(len(old),len(comp),len(ban),len(h['types']),len(d['dual']),d['rhs'])
for t in old+comp+ban:line(*t)
for n in [42,43,44,45]:
 ts=f['spectrum5'][str(n)]['types'];line(n,len(ts))
 for t in ts:line(*t)
line(h['bound']+121*10**10)
for t,v in zip(h['types'],h['phi']):line(*t,v+10**10)
upper=[]
for i,(q,r) in enumerate(zip(d['dual'],d['rows'])):
 tag=r[0]
 if tag=='norm_outer':row=[0,-1,0,0,0,-1]
 elif tag=='norm_inner':row=[1,0,0,0,0,-1]
 elif tag=='outer_symmetric_feature':row=[2,-1,0,0,0,r[1]]
 elif tag=='conditional':row=[3,0,*r[1],r[2]]
 else:
  assert tag=='conditional_theta40';row=[4,0,*r[1],-1];upper.append(i);assert q<=0
 line(q,*row)
assert upper==d['upper_rows']
(W/'incidence_sym_input.txt').write_text('\n'.join(out)+'\n')
info={'candidate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'input_sha256':hashlib.sha256((W/'incidence_sym_input.txt').read_bytes()).hexdigest(),'target':d['target'],'dual_rows':375,'claimed_positive_rhs':d['rhs'],'upper_signs_verified':len(upper)}
(W/'incidence_sym_input_manifest.json').write_text(json.dumps(info,indent=2)+'\n');print(info)
