from pathlib import Path
import json,math,hashlib
W=Path(__file__).resolve().parent;R=W.parent;read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();C=math.comb
src=W/'r105_incidence/NC105_INNER_CANDIDATE.json';d=read(src);assert 'PASS universal NC105 bound=9070787191178440' in (W/'r105_inner_independent.log').read_text();lu=dict(zip(map(tuple,d['types']),d['phi']))
b=read(R.parent/'audit_2026-09-05_upper275/cap7_upper275/baseline277/baseline278/certificate.json');bad=[list(map(int,k.split(',')))for st in b['six_stages']for k in st]+b['completion_seeds']+[list(map(int,k.split(',')))for st in b['completion_stages']for k in st]
fs=[];prev=lu;prevB=d['bound'];checks=0
for n in range(105,109):
 k=n-105;ts=[(a,b,n-a-b)for a in range(46)for b in range(a+1)if 0<=n-a-b<=b and not any(all(x>=y for x,y in zip((a,b,n-a-b),z))for z in bad)]
 vv=[]
 for t in ts:
  value=0
  for a in range(k+1):
   for b0 in range(k+1-a):
    ds=(a,b0,k-a-b0)
    if any(x>y for x,y in zip(ds,t)):continue
    tt=tuple(sorted([x-y for x,y in zip(t,ds)],reverse=True));value+=math.prod(C(x,y)for x,y in zip(t,ds))*lu[tt];checks+=1
  if k:
   rec=sum(t[i]*prev[tuple(sorted([t[j]-int(i==j)for j in range(3)],reverse=True))]for i in range(3)if t[i])
   assert rec==k*value
  else:assert value==lu[t]
  vv.append(value)
 B=C(n,k)*d['bound'];assert not k or n*prevB==k*B
 h=dict(id='R105_inner'+('_to'+str(n)if k else''),m=n,types=ts,phi=vv,bound=B,source_sha256=sha(src),deletions=k,derivation='sum over unorderedkpointdeletions;NC preservation by accepted103extensionrigidity')
 fs.append(h);div=10**(4+2*k);fs.append(dict(h,id=h['id']+'_floor'+str(div),phi=[v//div for v in vv],bound=B//div,positive_divisor=div))
 prev=dict(zip(ts,vv));prevB=B
out=dict(status='ROOT_RAW_PASS_CANDIDATE_AWAIT_AGENT_RAW_AUDIT',functions=fs,finite_formula_checks=checks,root_checker_sha256=sha(W/'verify_r105_inner.cpp'),scope='Universal NC105 and unordereddeletiontransfers NC106..108; independent agentraw pass pending')
(W/'r105_functions.json').write_text(json.dumps(out,indent=2)+'\n');print([(h['id'],h['m'],h['bound'])for h in fs])
