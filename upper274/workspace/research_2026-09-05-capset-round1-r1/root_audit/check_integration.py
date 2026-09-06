import json,re,hashlib,itertools,math
from pathlib import Path
from collections import Counter
W=Path(__file__).resolve().parent;R=W.parent
C=json.loads((W/'audited_certificate_snapshot.json').read_text())
rows=json.loads((W/'a_case_index.json').read_text())['cases']
own=[]
for line in (W/'a_independent.log').read_text().splitlines():
    m=re.match(r'(\d+) (\d+,\d+,\d+) mincase=(\d) state=([-\d,]+) count=(\d+) minimum=(-?\d+) gap=(\d+)',line)
    if m:
        i=int(m[1]); key=list(map(int,m[2].split(',')));state=list(map(int,m[4].split(',')))
        assert rows[i]==dict(index=i,key=key,minimum=bool(int(m[3])),state=state)
        own.append(tuple(map(int,(m[5],m[6],m[7]))))
other=[]
for line in (R/'route_a/verification.log').read_text().splitlines():
    m=re.search(r' count=(\d+) minimum=(-?\d+) K=-?\d+ gap=(\d+)',line)
    if m:other.append(tuple(map(int,m.groups())))
assert len(own)==88 and own==other
def dominates(t,ds):return any(all(a>=b for a,b in zip(t,d)) for d in ds)
def q(t):a,b,c=t;return 9*a*b*c-899*(a*b+a*c+b*c)+15730000
types=[(a,b,275-a-b) for a in range(113) for b in range(a+1) if 0<=275-a-b<=b]
assert len(types)==341
assert all(4*q((a,b,c))==(3*c-275)**2*(c-67)+(899-9*c)*(a-b)**2 for a,b,c in types)
total=9*243*math.comb(275,3)-899*729*math.comb(275,2)+1093*15730000
assert total==C['root_sum']==-246950
ban=[tuple(x) for x in C['seeds']];ordinary=[]
for stage in C['stages']:
    stage_types=[tuple(map(int,k.split(','))) for k in stage]
    assert all(sum(t)==275 and not dominates(t,ban) for t in stage_types)
    ban+=stage_types;ordinary+=stage_types
want={t for t in types if q(t)<0 and not dominates(t,ban)}
have={tuple(map(int,k.split(','))) for k in C['extremal']}
assert want==have and len(have)==40
open_states=[]
for key,record in C['extremal'].items():
    t=tuple(map(int,key.split(',')))
    if 'branches' not in record:continue
    variable=[j for j,n in enumerate(t) if 103<=n<=108]
    expected={tuple(b[variable.index(j)] if j in variable else 1 if n>=109 else -1 for j,n in enumerate(t)) for b in itertools.product((0,1),repeat=len(variable))}
    assert len(record['branches'])==len(expected) and {tuple(b['status']) for b in record['branches']}==expected
    for b in record['branches']:
        if b['certificate'] is None:open_states.append((t,tuple(b['status'])))
recovered=[(112,109,51),(111,110,51)]
remaining=[(t,s) for t,s in open_states if not dominates(t,recovered)]
assert len(open_states)==10 and len(remaining)==8
ledger=json.loads((R/'route_a/case_ledger.json').read_text())
assert ledger['target_size_to_exclude']==275 and ledger['proved_upper_bound']==275
assert [tuple(row['type']) for row in ledger['types']]==types
assert {(tuple(r['type']),tuple(r['status'])) for r in ledger['open_states']}==set(remaining)
status_counts=Counter()
for row in ledger['types']:
    t=tuple(row['type']);assert row['Q']==q(t)
    os=row['ordinary_status'];status_counts[os]+=1
    if os=='EXCLUDED_INHERITED_SEED':assert dominates(t,C['seeds'])
    elif os=='EXCLUDED_RECOVERED_THREE_DELETION_SEED':assert dominates(t,recovered)
    elif os!='OPEN':assert t in ordinary
    assert (row['minimum_status']=='OPEN')==(t in {v[0] for v in remaining})
    for case in row['completion_cases']:
        if case['conclusion']=='OPEN':assert (t,tuple(case['status'])) in remaining
# Independent diagnostic: construct all affine lines through unordered pairs,
# rather than grouping centers as the discovery checker did.
points=list(itertools.product(range(3),repeat=5))
def f(x):return (-x[4]**2*(x[0]**2+x[1]**2)%3,-x[4]**2*(x[2]**2+x[3]**2)%3)
bad=set();directions=Counter()
for a,b in itertools.combinations(points,2):
    c=tuple((-x-y)%3 for x,y in zip(a,b));line=tuple(sorted((a,b,c)))
    if line in bad:continue
    if all((x+y+z)%3==0 for x,y,z in zip(f(a),f(b),f(c))):bad.add(line)
for line in bad:
    a,b,_=line;d=tuple((y-x)%3 for x,y in zip(a,b));first=next(x for x in d if x)
    if first==2:d=tuple(2*x%3 for x in d)
    directions[d]+=1
assert len(directions)==121 and dict(Counter(directions.values()))=={1:1,4:16,16:64,27:40}
out=dict(status='PASS',a_exact_cases=len(own),a_matrices=sum(x[0] for x in own),
         a_linewise_count_minimum_gap_match=True,root_sum=total,basic_types=len(types),
         negative_types=sum(q(t)<0 for t in types),ordinary_types=ordinary,
         final_ledger_verified=True,ledger_ordinary_status_counts=dict(status_counts),
         open_before_three_deletion=open_states,remaining_minimum_states=remaining,
         b_diagnostic_bad_lines=len(bad),b_direction_histogram=dict(Counter(directions.values())),
         b_status='DIAGNOSTIC_ONLY_NO_NEW_MATH')
(W/'integration_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
