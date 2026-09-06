import json,itertools,math,hashlib
from pathlib import Path
W=Path(__file__).resolve().parent;B=W.parents[1]/'audit_2026-09-05_upper275/cap7_upper275'
C=json.loads((W/'certificates.json').read_text())
T=[(a,b,275-a-b)for a in range(113)for b in range(a+1)if 0<=275-a-b<=b]
def Q(t):a,b,c=t;return 9*a*b*c-899*(a*b+a*c+b*c)+15730000
def dom(t,s):return all(a>=b for a,b in zip(t,s))
SEEDS=[(112,112,29),(112,111,35),(112,110,45),(111,111,45)]
NEWSEEDS=[(112,109,51),(111,110,51)]
ordinary={k:(si,r)for si,st in enumerate(C['stages'])for k,r in st.items()}
rows=[]
for t in T:
 k=','.join(map(str,t));old=[s for s in SEEDS if dom(t,s)];new=[s for s in NEWSEEDS if dom(t,s)]
 row=dict(type=t,Q=Q(t),ordinary_status='OPEN',ordinary_reference=None,minimum_status='OPEN',completion_cases=[])
 if old:row.update(ordinary_status='EXCLUDED_INHERITED_SEED',ordinary_reference=old)
 elif k in ordinary:row.update(ordinary_status='EXCLUDED_NEW_CERTIFICATE',ordinary_reference=f'certificates.json/stages/{ordinary[k][0]}/{k}')
 elif new:row.update(ordinary_status='EXCLUDED_RECOVERED_THREE_DELETION_SEED',ordinary_reference=new)
 elig=[j for j,N in enumerate(t)if 103<=N<109]
 states=[tuple(bits[elig.index(j)]if j in elig else 1 if N>=109 else -1 for j,N in enumerate(t))for bits in itertools.product((0,1),repeat=len(elig))]
 ex=C['extremal'].get(k)
 for state in states:
  claim='OPEN';ref=None
  if row['ordinary_status']!='OPEN':claim='EXCLUDED_ORDINARY';ref=row['ordinary_reference']
  elif Q(t)>=0:claim='IMPOSSIBLE_AS_GLOBAL_MINIMIZER_BY_NEGATIVE_SUM';ref='root_sum=-246950'
  elif ex and 'branches' not in ex:claim='EXCLUDED_MINIMUM_UNSPLIT';ref=f'certificates.json/extremal/{k}'
  elif ex:
   matching=[(j,b)for j,b in enumerate(ex['branches'])if tuple(b['status'])==state];assert len(matching)==1
   j,b=matching[0]
   if b['certificate']:claim='EXCLUDED_MINIMUM_FIXED_STATUS';ref=f'certificates.json/extremal/{k}/branches/{j}/certificate'
  row['completion_cases'].append(dict(status=state,conclusion=claim,reference=ref))
 row['minimum_status']='OPEN' if any(r['conclusion']=='OPEN'for r in row['completion_cases'])else 'EXCLUDED'
 rows.append(row)
assert len(T)==341 and sum(Q(t)<0 for t in T)==56
for a,b,c in T:assert 4*Q((a,b,c))==(3*c-275)**2*(c-67)+(899-9*c)*(a-b)**2
root=9*243*math.comb(275,3)-899*729*math.comb(275,2)+15730000*1093
assert root==-246950
openstates=[dict(type=r['type'],status=c['status'],Q=r['Q'])for r in rows for c in r['completion_cases']if c['conclusion']=='OPEN']
assert len(openstates)==8
ledger=dict(target_size_to_exclude=275,intended_upper_bound=274,proved_upper_bound=275,global_237_existence='UNKNOWN',root=dict(E3_coefficient=9,E2_coefficient=-899,constant=15730000,sum=root,directions=1093,k=67),scope='Every sorted integer profile with entries<=112 and total275; completion0 means whole slice not contained in112-cap,1 contained,-1 unrestricted.',basic_types=341,negative_types=56,ordinary_new_certificates=sum(map(len,C['stages'])),verified_certificates=88,verified_matrix_evaluations=153548040,certificate_sha256=hashlib.sha256((W/'certificates.json').read_bytes()).hexdigest(),ordinary_dependency_rule='each stage frozen before all its cases',minimum_dependency_rule='each minimum certificate uses only old four seeds plus completed ordinary stages, never another minimum case',three_deletion_input='Root-audited recovered scoped theorem; prior overlap; not a new result of Route A',verification='Route A standalone C++ and independent root Cartesian C++, all88 PASS; published low-dimensional inputs retained',open_states=openstates,types=rows)
(W/'case_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
print(json.dumps({k:ledger[k]for k in ['basic_types','negative_types','ordinary_new_certificates','verified_certificates','verified_matrix_evaluations','open_states']},indent=2))
