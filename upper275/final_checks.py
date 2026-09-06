from pathlib import Path
from collections import Counter
from math import comb
from itertools import product
import hashlib,json,re,platform,subprocess
D=Path(__file__).resolve().parent;P=D/'cap7_upper275'
C=json.loads((P/'results/size276/proof.json').read_text())
q=lambda t:9*t[0]*t[1]*t[2]-903*(t[0]*t[1]+t[0]*t[2]+t[1]*t[2])+15920784
covers=lambda t,ban:any(all(x>=y for x,y in zip(t,b)) for b in ban)
assert list(map(len,C['stages']))==[52,9,5]
ban=list(map(tuple,C['initial_seeds']))
assert ban==[(112,112,29),(112,111,35)]
for stage in C['stages']:
    keys=[tuple(map(int,k.split(','))) for k in stage]
    assert len(keys)==len(set(keys)) and all(sum(t)==276 and not covers(t,ban) for t in keys)
    for r in stage.values():assert r.get('status',[-1,-1,-1])==[-1,-1,-1] and not r.get('extra_features')
    ban.extend(keys)
ban.extend([(112,110,45),(111,111,45)])
expected={(a,b,276-a-b) for a in range(113) for b in range(a+1) if 0<=276-a-b<=b and q((a,b,276-a-b))<0 and not covers((a,b,276-a-b),ban)}
assert expected=={tuple(map(int,k.split(','))) for k in C['extremal']} and len(expected)==17
nr=0;gaps=[]
for key,r in C['extremal'].items():
    t=tuple(map(int,key.split(',')));rs=r.get('branches',[r]);nr+=len(rs)
    if len(rs)==1 and rs[0].get('status',[-1,-1,-1])==[-1,-1,-1]:pass
    else:
        choices=[[0,1] if 103<=n<=108 else [1] if n>=109 else [-1] for n in t]
        assert set(product(*choices))=={tuple(b['status']) for b in rs}
        assert len(rs)==len(set(product(*choices)))
    for b in rs:
        assert not b.get('empty',False)
        assert 364*b['K']-b['forced']==b['gap']>0;gaps.append(b['gap'])
assert nr==50 and min(gaps)==1259
print('Independent final coverage PASS: 331 basic types, 66 ordinary exclusions, 17 minimum alternatives, 50 complete branches; minimum gap=1259.')
clean=lambda p:[s for s in p.read_text().splitlines() if s and not s.startswith(('Elapsed seconds:','BASELINE INTEGRITY PASS:'))]
cpp=clean(D/'cpp_replay.txt');py=clean(D/'python_replay.txt')
assert any(s.startswith('STEP FULL PASS: no 276-point cap;') for s in py),'Python still running or did not pass'
assert len(cpp)==448 and Counter(cpp)==Counter(py),'Full implementation output disagreement'
for name in ['cpp_verification.txt','fresh_cpp_verification.txt']:assert cpp==clean(P/name)
print('Full Python/C++ comparison PASS: 448 matching non-timing computation lines; fresh C++ also matches both supplied full logs.')
bykey={}
for s in cpp:
    m=re.match(r'AUX41 INNER (\S+) \((\d+), (\d+), (\d+)\): matrices=(\d+), minimum=(-?\d+), K=(-?\d+), bound=(-?\d+)',s)
    if m:bykey[tuple(m.group(i) for i in range(1,5))]=tuple(map(int,m.groups()[4:]))
count=0
for s in (D/'independent_aux41.txt').read_text().splitlines():
    m=re.match(r'(\S+) \((\d+),(\d+),(\d+)\) ordered=(\d+) sorted=(\d+) min=(-?\d+) K=(-?\d+) bound=(-?\d+)',s)
    if m:
        assert bykey[tuple(m.group(i) for i in range(1,5))]==tuple(map(int,m.groups()[5:]));count+=1
assert count==30
print('Third implementation comparison PASS: all 30 auxiliary minima and canonical counts match; all 599436 ordered matrices verified.')
print('Python:',platform.python_version());print(subprocess.check_output(['c++','--version'],text=True).splitlines()[0])
result={'status':'PASS_WITH_STATED_PUBLISHED_INPUTS','excluded_size':276,'interval':[236,275],'fresh_cpp_complete':True,'fresh_python_complete':True,'matching_nontiming_lines':448,'independent_aux41_ordered_matrices':599436,'independent_aux41_sorted_matrices':138621,'source_zip_sha256':hashlib.sha256((D/'source.zip').read_bytes()).hexdigest(),'global_237_cap_existence':'UNKNOWN','priority_or_peer_review_claim':False}
(D/'AUDIT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
