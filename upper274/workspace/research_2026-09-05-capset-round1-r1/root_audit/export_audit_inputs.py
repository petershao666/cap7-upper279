"""Only data transcription; no discovery/verifier kernel imports."""
import json,math,itertools,hashlib
from pathlib import Path
W=Path(__file__).resolve().parent; ROUND=W.parent; BASE=ROUND.parent/'audit_2026-09-05_upper275/cap7_upper275'
newpath=ROUND/'route_a/certificates.json'
C=json.loads(newpath.read_text()); D=json.loads((BASE/'baseline277/baseline278/certificate.json').read_text())
old=[list(map(int,k.split(','))) for stage in D['six_stages'] for k in stage]
comp=D['completion_seeds']+[list(map(int,k.split(','))) for stage in D['completion_stages'] for k in stage]
hist=json.loads((BASE/'results/size276/proof.json').read_text())['new_histograms']
hist+=[dict(json.loads((BASE/'baseline277/certificate.json').read_text())['nested108'],id='psi108',m=108)]
reg={h['id']:i for i,h in enumerate(hist)}
cases=[];banned=[list(t) for t in C['seeds']]
for stage in C['stages']:
  for k,rec in stage.items():cases.append(dict(key=list(map(int,k.split(','))),rec=rec,ban=banned[:],minimum=0,state=[-1]*3,extras=[]))
  banned += [list(map(int,k.split(','))) for k in stage]
for k,r in C['extremal'].items():
  key=list(map(int,k.split(',')))
  for branch in r.get('branches',[dict(certificate=r,status=[-1]*3,extra_features=[])]):
    if branch['certificate'] is not None:
      cases.append(dict(key=key,rec=branch['certificate'],ban=banned[:],minimum=1,state=branch['status'],extras=branch['extra_features']))
def line(*x):return ' '.join(map(str,x))+'\n'
out=line(len(old),len(comp),len(hist),len(cases))
for t in old+comp:out+=line(*t)
for h in hist:
  out+=line(h['m'],h['bound'],len(h['types']))
  for t,v in zip(h['types'],h['phi']):out+=line(*t,v)
index=[]
for i,case in enumerate(cases):
  r=case['rec'];q=r.get('coeff',[])
  out+=line(*case['key'],case['minimum'],*case['state'],int(r.get('empty',False)),len(case['ban']),len(case['extras']),len(q))
  for t in case['ban']:out+=line(*t)
  for j,name in case['extras']:out+=line(j,{'fam':-1,'small':-2,'label40':-3}.get(name,reg.get(name,999)))
  out+=line(*q)+line(r.get('K',0),r.get('forced',0),r.get('gap',0))
  index.append(dict(index=i,key=case['key'],minimum=bool(case['minimum']),state=case['state']))
(W/'a_certificate_input.txt').write_text(out)
(W/'a_case_index.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(newpath.read_bytes()).hexdigest(),cases=index),indent=2)+'\n')
print('transcribed',len(cases),'cases; histograms',list(reg))
