"""Independent data transcription and dependency checks, no research imports."""
from pathlib import Path
import json,math,hashlib
W=Path(__file__).resolve().parent;R=W.parent;B=R.parent/'audit_2026-09-05_upper275/cap7_upper275'
def read(p):return json.loads(p.read_text())
d=read(R/'hist105106/h3/h3_result.json')
assert hashlib.sha256((R/'hist105106/h3/h3_result.json').read_bytes()).hexdigest()=='cbb4973544cf7e2388097bb333504dc0c53c943d1671605fa300996394dfd294'
f=read(B/'baseline277/baseline278/certificate.json')
old=[list(map(int,k.split(','))) for s in f['six_stages'] for k in s]
comp=f['completion_seeds']+[list(map(int,k.split(','))) for s in f['completion_stages'] for k in s]
orig=read(B/'results/size276/proof.json')['new_histograms']+[read(B/'baseline277/certificate.json')['nested108']]
known=[]
for h in orig:
 for r in h['inner']:
  for u in r.get('uppercuts',[]):
   z=u['data'];known.append((41,z['types'],z['phi'],z['bound']))
  for u in r.get('spectra',[]):known.append((42,u['types'],u['phi'],u['bound']))
upper=list(d['upper5'].items());ui={name:i for i,(name,h) in enumerate(upper)}
for name,h in upper:assert (h['m'],h['types'],h['phi'],h['bound']) in known
hist4=read(R/'hist105106/h3/hist19_20.json')
clashes=read(R/'hist105106/h3/clash_data.json')['patterns']
r1=read(R.parent/'research_2026-09-05-capset-round1-r1/route_a/certificates.json')
ban=r1['seeds']+[[112,109,51],[111,110,51]]+[list(map(int,k.split(','))) for s in r1['stages'] for k in s]
def dominated(t,bads):return any(all(a>=b for a,b in zip(t,u)) for u in bads)
def support(n,u):return [[a,b,n-a-b] for a in range(u+1) for b in range(a+1) if 0<=n-a-b<=b]
support40=support(40,20);support105=[t for t in support(105,45) if not dominated(t,old+comp)]
assert d['histograms']['40']['types']==support40 and d['histograms']['105']['types']==support105
g=d['histograms']['105']['root'];q=g['coeff'];U=q[0]*243*math.comb(105,2)+q[1]*81*math.comb(105,3)
assert U==g['forced'] and 364*g['K']-U==g['gap']>0
anchors105=[t for t in support105 if q[0]*sum(t[i]*t[j] for i in range(3) for j in range(i))+q[1]*math.prod(t)<g['K']]
assert [r['type'] for r in d['histograms']['105']['inner']]==anchors105
cases=[]
for n,types in [(40,support40),(105,anchors105)]:
 h=d['histograms'][str(n)];records={tuple(r['type']):r for r in h['inner']}
 assert h['bound']==max(r['bound'] for r in records.values())
 for i,key in enumerate(types):
  r=records.get(tuple(key));empty=r is None
  if empty:assert n==40 and key in d['lower40_empty']
  extras=[]
  if r:
   assert len(r['coeff'])==7+len(r['extra'])
   for j,kind,arg,bd in r['extra']:
    if kind=='exact4':
     z=hist4[str(key[j])];assert n==40 and bd==z['histogram'][z['types'].index(arg)]
     extras.append([j,0,*arg,-1,bd])
    elif kind=='exact':
     z=f['spectrum5'][str(key[j])];assert len(z['spectra'])==1 and bd==z['spectra'][0][z['types'].index(arg)]
     extras.append([j,0,*arg,-1,bd])
    else:
     assert kind=='upper';u=d['upper5'][arg];assert u['m']==key[j] and bd==u['bound']
     extras.append([j,1,0,0,0,ui[arg],bd])
   assert r['theta40_columns']==([j for j,N in enumerate(key) if N==40] if n==105 else [])
  cases.append(dict(n=n,key=key,empty=empty,ban=(old+comp if n==105 else [])+types[:i],extra=extras,rec=r))
for r in d['outer']:
 assert r['type']==[105,105,65] and len(r['coeff'])==7
 cases.append(dict(n=275,key=r['type'],empty=False,ban=ban,extra=[],rec=r))
out=[]
def line(*args):out.append(' '.join(map(str,args)))
line(len(old),len(comp),len(upper),len(clashes),len(cases))
for t in old+comp:line(*t)
for n in [42,43,44,45]:
 ts=f['spectrum5'][str(n)]['types'];line(n,len(ts))
 for t in ts:line(*t)
for _,h in upper:
 line(h['m'],h['bound'],len(h['types']))
 for t,p in zip(h['types'],h['phi']):line(*t,p)
for n in [40,105]:
 h=d['histograms'][str(n)];line(n,h['bound'],len(h['types']))
 for t,p in zip(h['types'],h['phi']):line(*t,p)
for p in clashes:
 row=[-1]*9
 for i,v in p:row[i]=v
 line(*row)
for z in cases:
 r=z['rec'] or {};q=r.get('coeff',[])
 line(z['n'],*z['key'],int(z['empty']),len(z['ban']),len(z['extra']),len(q),r.get('count',0))
 for t in z['ban']:line(*t)
 for e in z['extra']:line(*e)
 line(*q);line(r.get('K',0),r.get('bound',r.get('forced',0)),r.get('gap',0))
(W/'h3_input.txt').write_text('\n'.join(out)+'\n')
info={'status':'DEPENDENCY_TRANSCRIPTION_PASS','case_count':len(cases),'theta40_anchors':44,'phi105_anchors':17,'outer_targets':[[105,105,65]],'certificate_sha256':hashlib.sha256((R/'hist105106/h3/h3_result.json').read_bytes()).hexdigest(),'input_sha256':hashlib.sha256((W/'h3_input.txt').read_bytes()).hexdigest()}
(W/'h3_input_manifest.json').write_text(json.dumps(info,indent=2)+'\n');print(info)
