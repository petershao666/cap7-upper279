"""Root source-point union, independent of H merging and normal kernels."""
import sys
sys.dont_write_bytecode=True
import hashlib,itertools,json,time
from collections import Counter,defaultdict
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parent.parent;H=R/'hist105106/complete41_candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads((R/p).read_text())
types=sorted({tuple(sorted(t,reverse=True))for t in itertools.product(range(21),repeat=3)if sum(t)==41})
assert len(types)==40
ns=list(itertools.product(range(3),repeat=5))[1:]
started=time.monotonic();checks=0;fam=defaultdict(set);reps={}
def add(label,points):
    global checks
    S=set(map(tuple,points));assert len(S)==len(points)==41
    assert all(len(p)==5 and all(v in range(3)for v in p)for p in S)
    for a,b in itertools.combinations(S,2):
        assert tuple((6-x-y)%3 for x,y in zip(a,b))not in S;checks+=1
    counts=Counter()
    for n in ns:
        c=[0,0,0]
        for p in S:c[sum(x*y for x,y in zip(n,p))%3]+=1
        counts[tuple(sorted(c,reverse=True))]+=1
    assert set(counts)<=set(types)and all(v%2==0 for v in counts.values())
    hist=tuple(counts[t]//2 for t in types)
    assert sum(hist)==121
    fam[label].add(hist);reps.setdefault(hist,sorted(S))
    assert time.monotonic()-started<180

for z in read('root_audit/exceptional41_raw/ACCEPTED_RAW_HISTOGRAMS.json')['histograms']:add('raw_exceptional_overcover',z['points'])
for z in read('root_audit/fortyfive/ACCEPTED_FOUR_DELETE_HISTOGRAMS.json')['histograms']:add('45_minus4',z['points'])
for z in read('root_audit/named41_pdf/ACCEPTED_POINTS.json')['caps']:
    if z['name']!='45':add(z['name'],z['points'])
old=read('hist105106/h9/named_points.json')
for label in ['41F','41G','41H','41I']:add(label,old[label]['points'])
delta=old['Delta686']['points']
assert len(set(map(tuple,delta)))==len(delta)==42
for i in range(42):add('Delta686_minus1',delta[:i]+delta[i+1:])
c20201=read('root_audit/complete20201/ACCEPTED_HISTOGRAM.json')
point_path=Path(c20201['point_representative'])
point_lines=point_path.read_text().splitlines()
assert point_lines[0].split()==['point_id','t','x0','x1','x2','x3']
add('all_20201_41_caps',[list(map(int,line.split()))[1:]for line in point_lines[1:]])
assert len(fam)==13 and len(reps)==44
candidate=json.loads((H/'CANDIDATE_UNION.json').read_text())
for f,s in candidate['source_hashes'].items():assert sha(R/f)==s
assert types==list(map(tuple,candidate['types']))
assert set(reps)=={tuple(z['counts'])for z in candidate['histograms']}
producer_family=defaultdict(set)
for z in candidate['histograms']:
    h=tuple(z['counts'])
    for s in z['sources']:producer_family[s['family']].add(h)
assert dict(fam)==dict(producer_family)
supp=[i for i in range(40)if any(h[i]for h in reps)]
data={'status':'ROOT_NUMERIC_UNION_PASS_PENDING_INDEPENDENT_SOURCE_AUDIT',
 'types':types,'histograms':[{'counts':h,'points':reps[h],
 'source_families':sorted(k for k,v in fam.items()if h in v)}for h in sorted(reps)],
 'histogram_count':44,'ordinary5D41_present_types':[types[i]for i in supp],
 'ordinary5D41_absent_types':[t for i,t in enumerate(types)if i not in supp],
 'family_counts':{k:len(v)for k,v in fam.items()},'root_source_point_instances':checks//820,
 'root_pair_checks':checks,'source_hashes':candidate['source_hashes'],
 'candidate_union_sha256':sha(H/'CANDIDATE_UNION.json'),
 'root_code_sha256':sha(Path(__file__)),'seconds':time.monotonic()-started,
 'independence':'Root directly assembles all accepted source pointsets, all42Delta deletions and242normalvectors; no H merger or generated input kernel imported. H candidate used only for final comparison. Accepted component data and published source classifications are shared.',
 'scope':'All arbitrary5D41caps conditional on published Theorem6.3 and supplementary-list coverage; finite numeric union verified here, source proof recorded separately. No7D upper improvement follows alone.'}
(D/'ROOT_UNION.json').write_text(json.dumps(data,indent=2)+'\n')
print(data['status'],'histograms',len(reps),'pairchecks',checks,'hash',sha(D/'ROOT_UNION.json'))
