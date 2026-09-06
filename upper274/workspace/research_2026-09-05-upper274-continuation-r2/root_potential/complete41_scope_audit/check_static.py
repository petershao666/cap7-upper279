"""Independent static-source union audit; no geometric enumerator is imported."""
from pathlib import Path
from collections import Counter, defaultdict
from hashlib import sha256
import json
import time

start = time.monotonic()
here = Path(__file__).resolve().parent
base = here.parent.parent
packet = base / 'hist105106/complete41_candidate'

def read(rel):
    return json.loads((base / rel).read_text())

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

frozen = json.loads((packet / 'FROZEN.json').read_text())
for name, expected in frozen['files'].items():
    assert digest(packet / name) == expected, name
snapshot = json.loads((packet / 'INPUT_SNAPSHOT.json').read_text())
for name, expected in snapshot['source_hashes'].items():
    assert digest(base / name) == expected, name

u = json.loads((packet / 'CANDIDATE_UNION.json').read_text())
types = sorted((a, b, 41-a-b) for a in range(21) for b in range(a+1)
               if 0 <= 41-a-b <= b)
assert len(types) == 40
assert list(map(tuple, u['types'])) == types

def vector(ty, co):
    assert len(ty) == len(co)
    mapping = {tuple(t): n for t, n in zip(ty, co)}
    assert len(mapping) == len(ty) and set(mapping) <= set(types)
    assert all(isinstance(n, int) and n >= 0 for n in co)
    v = tuple(mapping.get(t, 0) for t in types)
    assert sum(v) == 121
    assert sum(n*(a*b+a*c+b*c) for (a,b,c),n in zip(types,v)) == 66420
    assert sum(n*a*b*c for (a,b,c),n in zip(types,v)) == 287820
    return v

expected = defaultdict(list)
raw = read('root_audit/exceptional41_raw/ACCEPTED_RAW_HISTOGRAMS.json')
for h in raw['histograms']:
    expected['raw_exceptional_overcover'].append(vector(raw['types'], h['counts']))
four = read('root_audit/fortyfive/ACCEPTED_FOUR_DELETE_HISTOGRAMS.json')
assert sum(h['four_deletion_frequency'] for h in four['histograms']) == 148995
for h in four['histograms']:
    expected['45_minus4'].append(vector(four['types'], h['counts']))
all20201 = read('root_audit/complete20201/ACCEPTED_HISTOGRAM.json')
for h in all20201['histograms']:
    expected['all_20201_41_caps'].append(vector(all20201['types'], h))
named = read('hist105106/h9/named_histograms.json')
for letter in 'FGHI':
    h = named['41'+letter]
    expected['41'+letter].append(vector(h['types'], h['histogram']))
deleted = []
for h in named['Delta686_minus1_family']:
    expected['Delta686_minus1'].append(vector(h['types'], h['histogram']))
    deleted.extend(h['deleted_point_indices'])
assert sorted(deleted) == list(range(42))
ae = read('root_audit/named41_pdf/ACCEPTED_POINTS.json')
for cap in ae['caps']:
    if cap['name'] == '45':
        continue
    assert cap['name'] in ['41'+s for s in 'ABCDE']
    h = cap['histogram']
    expected[cap['name']].append(vector([e['type'] for e in h], [e['count'] for e in h]))

source_table = [(4,0,4),(2,7,2),(2,4,6),(1,1,8),(1,1,6),
                (0,8,3),(0,5,5),(0,4,5),(0,2,10)]
for letter, published in zip('ABCDEFGHI', source_table):
    v, = expected['41'+letter]
    assert tuple(v[types.index(t)] for t in [(18,18,5),(18,17,6),(18,16,7)]) == published

actual = defaultdict(list)
union = set()
alternatives = set()
for h in u['histograms']:
    v = vector(u['types'], h['counts'])
    assert v not in union
    union.add(v)
    for source in h['sources']:
        actual[source['family']].append(v)
        alternatives.add(source['alternative'])
        assert source['family_verification_status'] == 'ROOT_ACCEPTED'
assert alternatives == set(range(1,14))
assert set(actual) == set(expected)
assert {k: Counter(v) for k,v in actual.items()} == {k: Counter(v) for k,v in expected.items()}
assert union == set(v for vv in expected.values() for v in vv)
assert len(union) == 44 and sum(map(len, expected.values())) == 80
absent = [list(t) for j,t in enumerate(types) if all(v[j] == 0 for v in union)]
assert len(absent) == 14

source_files = dict(snapshot['source_hashes'])
extra = ['root_potential/named41_45_source/CapSetProblem5S41.tex',
         'compatibility/exceptional41_source/COVERAGE_MAP.md',
         'compatibility/exceptional41_source/RAW_AMENDMENT.md',
         'compatibility/exceptional41_source/RAW_SUMMARY_MATCH.json',
         'compatibility/exceptional41_decode/PROOF_AND_VERIFICATION.md',
         'root_audit/exceptional41_raw/SOURCE_MANIFEST.json',
         'root_audit/exceptional41_raw/ROOT_VERIFICATION.json']
for rel in extra:
    source_files[rel] = digest(base / rel)
rawmanifest = read('root_audit/exceptional41_raw/SOURCE_MANIFEST.json')
for name, meta in rawmanifest.items():
    p = base / 'root_audit/exceptional41_raw' / name
    assert digest(p) == meta['sha256']
    assert len(p.read_bytes()) == meta['bytes']
    assert len(p.read_bytes().splitlines()) == meta['lines']
    source_files[str(p.relative_to(base))] = meta['sha256']

result = {
    'status': 'PASS_STATIC_SOURCE_UNION_AND_SOURCE_IDENTITIES',
    'logical_status': 'PASS_WITH_EXPLICIT_PUBLISHED_PREMISES',
    'candidate_sha256': digest(packet/'CANDIDATE_UNION.json'),
    'candidate_frozen_sha256': digest(packet/'FROZEN.json'),
    'frozen_packet_files_checked': len(frozen['files']),
    'snapshot_source_hashes_checked': len(snapshot['source_hashes']),
    'family_occurrences': {k:len(v) for k,v in sorted(expected.items())},
    'all_13_alternatives_present': True,
    'family_multisets_preserved': True,
    'source_occurrences': 80,
    'distinct_histograms': 44,
    'formal_types': 40,
    'absent_types': absent,
    'all_nine_named_table2_checks': True,
    'delta_deletion_indices_partition_42': True,
    'four_deletion_total': 148995,
    'source_files': source_files,
    'code_sha256': digest(Path(__file__)),
    'seconds': time.monotonic()-start,
    'LP_runs': 0,
    'geometric_enumerations': 0,
    'independence': 'New static set/multiset and source-hash implementation; no H/L/root kernel imported. Accepted histogram tables and published classification/list completeness are shared premises. Not an independent point replay or reproduction of the author search.'
}
(here/'STATIC_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['source_files','absent_types','independence']},indent=2))
