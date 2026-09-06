"""Independent output arithmetic and post-freeze full root comparison."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

here=Path(__file__).resolve().parent
rootdir=here.parents[1]/'root_audit'/'fortyfive'
frozen=json.loads((here/'FROZEN.json').read_text())
for name,digest in frozen['files'].items():
    assert hashlib.sha256((here/name).read_bytes()).hexdigest()==digest,name
meta=json.loads((here/'INPUT.json').read_text())
source=rootdir/'ACCEPTED_POINTS.json'
assert hashlib.sha256(source.read_bytes()).hexdigest()==meta['source_sha256']
original=[tuple(p) for p in json.loads(source.read_text())['points']]
ordered=sorted(original)
p=json.loads((here/'HISTOGRAMS.json').read_text())
r=json.loads((rootdir/'FOUR_DELETE_HISTOGRAMS.json').read_text())
assert r['point_input_sha256']==meta['source_sha256']
frequency=Counter()
subsets=0
with (here/'SUBSET_HISTOGRAM_IDS.txt').open() as f:
    for expected in itertools.combinations(range(45),4):
        row=tuple(map(int,f.readline().split()))
        assert len(row)==5 and row[:4]==expected and 0<=row[4]<len(p['histograms'])
        frequency[row[4]]+=1
        subsets+=1
    assert f.read()==''
assert subsets==148995
normals=[d for d in itertools.product(range(3),repeat=5) if any(d) and next(x for x in reversed(d) if x)==1]
assert len(normals)==121
def canonical(packet,freqfield):
    result={}
    for row in packet['histograms']:
        key=tuple(sorted((tuple(t),n) for t,n in zip(packet['types'],row['counts']) if n))
        assert key not in result
        result[key]=row[freqfield]
    assert sum(result.values())==148995
    return result
assert canonical(p,'frequency')==canonical(r,'four_deletion_frequency')
pair_checks={'P':0,'root':0}
normal_checks={'P':0,'root':0}
for owner,packet,input_order,freqfield in [('P',p,ordered,'frequency'),('root',r,original,'four_deletion_frequency')]:
    for row in packet['histograms']:
        cap=[tuple(x) for x in row['points']]
        lookup=set(cap)
        deleted=row['deleted_input_indices']
        assert len(deleted)==len(set(deleted))==4 and all(0<=i<45 for i in deleted)
        assert lookup=={x for i,x in enumerate(input_order) if i not in deleted}
        assert len(cap)==len(lookup)==41
        if owner=='P':
            assert frequency[row['id']]==row['frequency']
            assert [sum(x*3**k for k,x in enumerate(q)) for q in cap]==row['point_indices']
            assert [input_order[i] for i in row['retained_input_indices']]==cap
        for a,b in itertools.combinations(cap,2):
            assert tuple((-x-y)%3 for x,y in zip(a,b)) not in lookup
            pair_checks[owner]+=1
        counts=Counter()
        for d in normals:
            residues=Counter(sum(x*y for x,y in zip(d,q))%3 for q in cap)
            counts[tuple(sorted((residues[j] for j in range(3)),reverse=True))]+=1
            normal_checks[owner]+=1
        assert [counts[tuple(t)] for t in packet['types']]==row['counts']
        assert set(counts).issubset({tuple(t) for t in packet['types']})
        assert sum(counts.values())==121
        assert sum(n*(a*b+a*c+b*c) for (a,b,c),n in counts.items())==66420
        assert sum(n*a*b*c for (a,b,c),n in counts.items())==287820
report={
    'status':'FULL_INDEPENDENT_FAMILY_FREQUENCY_AND_REPRESENTATIVE_COMPARISON_PASS',
    'complete_histogram_vectors':len(p['histograms']),
    'frequencies_match_for_every_vector':True,
    'total_subsets':subsets,
    'P_assignment_file_full_subset_order_checked':True,
    'representative_pair_checks':pair_checks,
    'representative_normal_checks':normal_checks,
    'P_frozen_before_root_output_read':True,
    'P_generator_method':'explicitly assemble retained 41 points; count every retained point under all 242 nonzero normals; divide scalar duplicates by two',
    'root_generator_method_from_declared_gate':'subtract deleted occupancies from full45 point directional counts',
    'root_generator_source_read_or_imported':False,
    'independent_checker_method':'direct tuple point and pair arithmetic, normals normalized by last nonzero coordinate one',
    'shared_dependencies':['accepted 45-point coordinates','published affine uniqueness of the 45-cap'],
    'P_histograms_sha256':hashlib.sha256((here/'HISTOGRAMS.json').read_bytes()).hexdigest(),
    'root_histograms_sha256':hashlib.sha256((rootdir/'FOUR_DELETE_HISTOGRAMS.json').read_bytes()).hexdigest(),
    'P_enumeration_cpp_sha256':hashlib.sha256((here/'enumerate_retained.cpp').read_bytes()).hexdigest(),
    'root_declared_enumeration_cpp_sha256':r['enumeration_cpp_sha256'],
    'new_global_bound_claimed':False,
}
(here/'INDEPENDENT_COMPARISON.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
