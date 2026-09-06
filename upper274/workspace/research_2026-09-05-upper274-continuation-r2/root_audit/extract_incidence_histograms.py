from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;R=W.parent
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
want=read(R/'compatibility/ACCEPTED_SHARED_HISTOGRAMS.json')['histograms'];hs=[]
for file,blocks in [('theta40',[(0,108),(1,107)]),('theta40_10710761',[(0,107)])]:
 p=R/f'compatibility/{file}/EXACT_DUAL.json';d=read(p);sym=file!='theta40'
 for j,n in blocks:
  values={};norm=None
  for q,row in zip(d['dual'],d['rows']):
   if row[0]=='norm_inner' and (sym or row[1]==j):norm=q
   if row[0]=='conditional' and (sym or row[1]==j):
    t,k=row[1:] if sym else row[2:]
    if k==0:values[tuple(t)]=q
   if row[0]=='conditional_theta40':assert q<=0
  assert norm is not None
  matches=[h for h in want if h['source_sha256']==sha(p) and h['size']==n];assert len(matches)==1;h=matches[0]
  assert dict(zip(map(tuple,h['types']),h['phi']))==values and h['bound']==-91*norm and h['inner_normalization']==norm
  hs.append(dict(id=h['name'],m=n,types=h['types'],phi=h['phi'],bound=h['bound'],source_sha256=sha(p),source_inner_block=j))
  if sym:
   div=10000
   hs.append(dict(id=h['name']+'_floor10000',m=n,types=h['types'],phi=[v//div for v in h['phi']],bound=h['bound']//div,positive_divisor=div,derivation='sum floor(phi/d)<=sum phi/d<=B/d and integer sum; conservative exact corollary',source_sha256=sha(p),source_inner_block=j))
out=dict(status='ROOT_EXACT_EXTRACTION_AND_ANALYTIC_PROJECTION_PASS',functions=hs,universal_scope='ArbitraryNCsix-dimensional caps of the specified cardinality; not conditional on any seven-dimensional minimum',producer_table_sha256=sha(R/'compatibility/ACCEPTED_SHARED_HISTOGRAMS.json'),proof='INCIDENCE_EXTRACTION_GATE.md')
(W/'incidence_histograms_independent.json').write_text(json.dumps(out,indent=2)+'\n');print([(h['id'],h['bound'])for h in hs])
