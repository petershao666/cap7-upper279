"""Export formal deletions of accepted affine 8-cap representatives; no catalogue search."""
import hashlib
import itertools
import json
from pathlib import Path

here = Path(__file__).resolve().parent
base = here.parent
sources = {
    'small3d_actual_caps7.txt': '488211429dc1c2a6795859395914135e83990952ee2c109fcdd20956c8758db1',
    'h17_actual_caps8.txt': '01dcd9448bb1c4ad1232c97ec09e8d395c1167d630e0a31edbcdf68dfd4dfa4b',
    'h17_representatives_explicit.json': '940af30e07e4371103496a757551388a1dd94142d7646dbca4d7eed34fed4a9d',
}
for name, digest in sources.items():
    assert hashlib.sha256((base/name).read_bytes()).hexdigest() == digest
packet = json.loads((base/'h17_representatives_explicit.json').read_text())
actual7 = set(map(int, (base/'small3d_actual_caps7.txt').read_text().split()))
assert len(actual7) == 126360
entries = []
for rep in packet['representatives']:
    if rep['size'] != 8:
        continue
    mask = rep['canonical_mask']
    for removed in rep['point_indices']:
        reduced = mask ^ (1 << removed)
        indices = [i for i in range(27) if reduced >> i & 1]
        points = [[i%3, i//3%3, i//9] for i in indices]
        assert len(points) == 7 and reduced in actual7
        assert all(any(sum(p[k] for p in triple) % 3 for k in range(3))
                   for triple in itertools.combinations(points, 3))
        entries.append({'source8_mask': mask, 'removed_point_index': removed,
                        'mask7': reduced, 'point_indices': indices, 'points': points})
assert len(entries) == 24
result = {
    'status': 'COMPLETE_AFFINE7CAP_COVER_BY_DELETIONS',
    'encoding': 'Point i=x+3*y+9*z; bit i encodes that point; coordinates in F3.',
    'formal_entry_count': 24,
    'affine_orbit_classification_claimed': False,
    'duplicates_retained': True,
    'dependency_sha256': sources,
    'extension_result': 'SEVEN_EXTENSION_RESULT.json',
    'proof': 'SEVEN_EXTENSION_PROOF.md',
    'entries': entries,
}
(here/'SEVEN_DELETION_COVER.json').write_text(json.dumps(result, indent=2)+'\n')
print('PASS: 24 explicit deletion entries; every entry is a frozen actual 7-cap.')
