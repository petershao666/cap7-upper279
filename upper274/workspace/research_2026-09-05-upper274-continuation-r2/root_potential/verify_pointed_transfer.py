from pathlib import Path
from fractions import Fraction
import json,hashlib
P=Path(__file__).resolve().parent;B=P.parents[1]/'audit_2026-09-05_upper275/cap7_upper275'
S={h['id']:h for h in json.loads((B/'results/size276/proof.json').read_text())['new_histograms']}
D=json.loads((P/'pointed_result.json').read_text());C={h['id']:h for h in D['conditional_bounds']}
old=json.loads((P/'transfer_tables.json').read_text())['functions']
tab=json.loads((P/'pointed_transfer_tables.json').read_text());count=0
for h in tab['functions']:
    b=C[h['source_id']];s=S[h['source_id']];phi=dict(zip(map(tuple,s['types']),s['phi']));g=h['positive_gcd']
    prior=next(x for x in old if x['source_id']==h['source_id']and x['m']==108)
    assert h['types']==prior['types']and h['phi']==prior['phi']and g==prior['positive_gcd']
    for t,v in zip(h['types'],h['phi']):
        vals=0
        for j in range(3):
            u=t.copy();u[j]-=1;vals+=t[j]*phi[tuple(sorted(u,reverse=True))]
        assert vals==g*v;count+=1
    bd=Fraction(b['numerator'],b['denominator']);assert h['conditional107_bound']==str(bd)
    f=bd.numerator//bd.denominator;assert f==h['integer_conditional107_bound']
    assert h['bound']==108*f//g<h['old_bound']==prior['bound']
out=dict(status='PASS_ROUTE_SIDE_ROOT_AUDIT_PENDING',functions=3,values=count,new_bounds=[(h['id'],h['bound'])for h in tab['functions']],table_sha256=hashlib.sha256((P/'pointed_transfer_tables.json').read_bytes()).hexdigest())
(P/'pointed_transfer_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
