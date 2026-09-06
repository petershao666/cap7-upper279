"""Exact standard-library check of transfer tables and old-model comparisons."""
from pathlib import Path
from fractions import Fraction as F
from math import comb,gcd
from itertools import combinations
import json,hashlib
P=Path(__file__).resolve().parent;B=P.parents[1]/'audit_2026-09-05_upper275/cap7_upper275'
low=json.loads((B/'baseline277/baseline278/certificate.json').read_text())
src=json.loads((B/'results/size276/proof.json').read_text())['new_histograms']
src+=[dict(json.loads((B/'baseline277/certificate.json').read_text())['nested108'],id='psi108',m=108)]
sources={h['id']:h for h in src}
def key(x):return tuple(map(int,x.split(',')))
def e2(x):return sum(a*b for a,b in combinations(x,2))
def e3(x):a,b,c=x;return a*b*c
def sub(x):a,b,c=sorted(x,reverse=True);return c<=22 or a<=40 and b<=36
def dominates(x,y):return all(a>=b for a,b in zip(sorted(x,reverse=True),y))
comp=[tuple(x) for x in low['completion_seeds']]+[key(x) for st in low['completion_stages'] for x in st]
f6=[key(x) for st in low['six_stages'] for x in st]+[x for x in comp if not sub(x)]
def nc(x):return all(0<=a<=45 for a in x) and sum(x)<=112 and not any(dominates(x,y) for y in f6+comp)
trans=json.loads((P/'transfer_tables.json').read_text())['functions'];byid={h['id']:h for h in trans}
assert len(trans)==7
checked_values=0
for h in trans:
    source=sources[h['source_id']];N=h['m'];m=h['source_m'];d=N-m
    assert h['source_phi']==source['phi'] and h['source_types']==source['types'] and h['source_bound']==source['bound']
    expected=[(a,b,N-a-b) for a in range(46) for b in range(a+1) if 0<=N-a-b<=b and nc((a,b,N-a-b))]
    assert h['all_parent_types']==list(map(list,expected)) and h['types']==h['all_parent_types'] and not h['missing']
    phi=dict(zip(map(tuple,source['types']),source['phi']));values=[]
    for t in expected:
        ans=0;count=0
        for i in range(d+1):
            for j in range(d-i+1):
                r=(i,j,d-i-j)
                if any(a<b for a,b in zip(t,r)):continue
                u=tuple(sorted([a-b for a,b in zip(t,r)],reverse=True));assert u in phi
                mult=comb(t[0],i)*comb(t[1],j)*comb(t[2],d-i-j)
                count+=mult;ans+=mult*phi[u]
        assert count==comb(N,m)
        values.append(ans);checked_values+=1
    bd=comb(N,m)*source['bound'];g=gcd(*values,bd)
    assert h['positive_gcd']==g>0 and h['phi']==[x//g for x in values] and h['bound']==bd//g
comparisons=json.loads((P/'transfer_redundancy.json').read_text())
majorants=nonredundant=0
for rec in comparisons:
    h=byid[rec['id']];N=h['m'];types=list(map(tuple,h['types']))
    direct=[sources[x] for x in rec['direct_ids']];phi=[dict(zip(map(tuple,g['types']),g['phi'])) for g in direct]
    features=[[e2(t),e3(t)]+[f[t] for f in phi] for t in types]
    totals=[243*comb(N,2),81*comb(N,3)]+[g['bound'] for g in direct]
    if rec['status']=='EXACT_OLD_MODEL_DOMINATES':
        majorants+=1;co=list(map(F,rec['coefficients']));assert len(co)==len(totals)+1 and all(x>=0 for x in co[3:])
        for f,y in zip(features,h['phi']):assert co[0]+sum(a*b for a,b in zip(co[1:],f))>=y
        upper=364*co[0]+sum(a*b for a,b in zip(co[1:],totals))
        assert upper==F(rec['exact_upper'])<=h['bound'] and F(rec['exact_margin'])==h['bound']-upper
    elif rec['status']=='EXACT_NONREDUNDANCY_IN_OLD_HISTOGRAM_RELAXATION':
        nonredundant+=1;mass=F(0);sums=[F(0)]*len(totals);value=F(0)
        for v in rec['witness']:
            t=tuple(v['profile']);idx=types.index(t);w=F(v['weight']);assert w>=0;mass+=w
            for j,x in enumerate(features[idx]):sums[j]+=w*x
            value+=w*h['phi'][idx]
        assert mass==1 and all(sums[j]==F(totals[j],364) for j in (0,1))
        assert all(sums[j]<=F(totals[j],364) for j in range(2,len(totals)))
        assert value==F(rec['new_feature_sum']) and value>F(h['bound'],364)
        assert 364*value-h['bound']==F(rec['violation_after364'])
    else:raise AssertionError('comparison not certified')
assert majorants==4 and nonredundant==3
out={'status':'PASS_ROUTE_SIDE_ROOT_AUDIT_PENDING','transfer_functions':7,'table_values_checked':checked_values,'missing_source_subprofiles':0,'exact_old_model_dominance_certificates':majorants,'exact_nonredundancy_witnesses':nonredundant,'outer_cases_with_new_certificate':0,'transfer_sha256':hashlib.sha256((P/'transfer_tables.json').read_bytes()).hexdigest(),'comparison_sha256':hashlib.sha256((P/'transfer_redundancy.json').read_bytes()).hexdigest(),'scope':'puncturing-transfer inequalities and exact relation to old rational histogram model; no outer exclusion'}
(P/'transfer_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
