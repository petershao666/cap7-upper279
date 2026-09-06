import json,hashlib,time
from pathlib import Path
from itertools import permutations
W=Path(__file__).resolve().parent;R=W.parents[1];M=R.parent
t0=time.monotonic()
bp=M/'audit_2026-09-05_upper275/cap7_upper275/baseline277/baseline278/certificate.json'
hp=R/'root_audit/complete41/ACCEPTED_HISTOGRAMS.json'
source=json.loads(bp.read_text())['spectrum5'];h41=json.loads(hp.read_text())
hs=[h['counts'] for h in h41['histograms']]
zero=[tuple(t)for i,t in enumerate(h41['types'])if all(h[i]==0 for h in hs)]
assert len(zero)==14
oldzero=[(20,19,2),(20,18,3),(19,19,3),(19,18,4)]
types={n:set(map(tuple,source[str(n)]['types']))for n in [42,43,44,45]}
def permitted(t,zs):
    t=tuple(sorted(t,reverse=True));n=sum(t)
    return max(t)<=20 and n<=45 and not any(all(x>=y for x,y in zip(t,z))for z in zs) and (n<42 or t in types[n])
results={}
for label,zs in [('old',oldzero),('complete41',zero)]:
    U={(a,b):max([c for c in range(21)if permitted((a,b,c),zs)],default=-1)for a in range(21)for b in range(21)}
    details={}
    for n in [43,44,45]:
        rows=[]
        for t in sorted(types[n]):
            for a in sorted(set(permutations(t))):
                b=(20,16,6)
                # For each k, all three lines i+j+k=0 are necessary5D profiles.
                bounds=[min(U[a[i],b[(-i-k)%3]]for i in range(3))for k in range(3)]
                rows.append({'first_column':a,'third_entry_bounds':bounds,'sum_bound':sum(bounds)})
        details[n]={'maximum_third_total':max(r['sum_bound']for r in rows),'all_type_permutations':rows}
    results[label]=details
assert [results['old'][n]['maximum_third_total']for n in [43,44,45]]==[20,19,18]
assert [results['complete41'][n]['maximum_third_total']for n in [43,44,45]]==[19,18,18]
out={'status':'PASS_KNOWN_ROW_DOMAIN_IMPLICATION_NOT_NEW_GLOBAL_EXCLUSION','bound_by_first_size':{'old':{n:results['old'][n]['maximum_third_total']for n in [43,44,45]},'complete41':{n:results['complete41'][n]['maximum_third_total']for n in [43,44,45]}},'conditional_empty_NC106_anchors':[[43,42,21],[44,42,20],[45,42,19]],'condition':'Physical42 section is Delta686, equivalently the fourth accepted42 histogram.','already_implied_by_old_rows_and_full42_support':True,'all_cases':results,'source_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [bp,hp]},'elapsed':time.monotonic()-t0}
(W/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k!='all_cases'},indent=2))
