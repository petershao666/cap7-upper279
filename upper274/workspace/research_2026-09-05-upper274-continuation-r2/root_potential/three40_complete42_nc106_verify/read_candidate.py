"""Fail-closed pure-JSON reader. No feature compiler or grid kernel imports.

No candidate is opened without an explicit local root-activation record.
This module only checks binding/schema. Its output is not a replay PASS.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROUND = HERE.parents[1]
DOMAIN = HERE.parent / 'complete41_domain_audit'
TIERS = {
    '400': {'mathematical_size': 40, 'parent': [43, 40, 23], 'physical_column': 1},
    '401': {'mathematical_size': 40, 'parent': [44, 40, 22], 'physical_column': 1},
    '402': {'mathematical_size': 40, 'parent': [45, 40, 21], 'physical_column': 1},
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def integer_function(node, size):
    types, values = node['types'], node['phi']
    assert len(types) == len(values) and all(type(v) is int for v in values)
    assert type(node['bound']) is int
    keys = [tuple(t) for t in types]
    assert len(set(keys)) == len(keys)
    assert all(len(t) == 3 and all(type(a) is int and a >= 0 for a in t)
               and sum(t) == size and list(t) == sorted(t, reverse=True) for t in types)
    return dict(zip(keys, values))

def read_activated():
    activation_path = HERE / 'ACTIVATION.json'
    assert activation_path.exists(), 'WAITING_FOR_ROOT_HASH_BINDING_AND_REPLAY_ACTIVATION'
    activation = json.loads(activation_path.read_text())
    assert activation['root_authorized_exact_replay'] is True
    assert activation['target'] == [106, 106, 63]
    source = (ROUND / activation['candidate_path']).resolve()
    assert source == (ROUND / 'compatibility/two_local_theta400_certificates/RESULT.json').resolve()
    assert activation['candidate_sha256'] == '78238a2e3f389f9c7a4f93e049ad56e678c09103151fb3bfed0adc6e1dcf14bf'
    assert digest(source) == activation['candidate_sha256']
    candidate = json.loads(source.read_text())
    assert candidate['target'] == [106, 106, 63]
    assert candidate['tier_mapping'] == TIERS
    hist = candidate['histograms']
    assert set(hist) == {'400', '401', '402', '106'}
    for key, size in [('400', 40), ('401', 40), ('402', 40), ('106', 106)]:
        integer_function(hist[key], size)
        assert hist[key]['mathematical_size'] == size
    inputs = json.loads((DOMAIN / 'INPUTS.json').read_text())
    assert hist['106']['types'] == inputs['support106']
    cases = hist['106']['inner']
    assert len(cases) == 14
    support = candidate['local_supports']
    seen = []
    for ci, row in enumerate(cases):
        anchor = inputs['anchors106'][ci]
        assert row['type'] == anchor
        assert len(row['coeff']) == 7 + len(row['extra'])
        assert all(type(q) is int for q in row['coeff'])
        assert type(row['K']) is int and type(row['bound']) is int
        expected = [{'m': int(k), 'column': 1, 'coefficient': 1}
                    for k, value in TIERS.items() if value['parent'] == anchor]
        assert row['dependencies'] == expected
        slots = row['local_supports']
        assert len({s['column'] for s in slots}) == len(slots)
        assert {s['column'] for s in slots} == {c for c, n in enumerate(anchor) if n in (41, 42)}
        for slot in slots:
            assert slot['coefficient'] == 1
            obj = support[slot['id']]
            assert obj['case_dimension_size'] == 106
            assert obj['anchor'] == anchor and obj['column'] == slot['column']
            assert obj['m'] == anchor[slot['column']]
            integer_function(obj, obj['m'])
            seen.append(slot['id'])
        assert not row['conditional_dependencies'] and row['conditional_bound'] is None
    expected_names = {k for k, obj in support.items() if obj['case_dimension_size'] == 106}
    assert len(seen) == len(set(seen)) == 12 and set(seen) == expected_names
    assert sum(support[k]['m'] == 41 for k in seen) == 6
    assert sum(support[k]['m'] == 42 for k in seen) == 6
    return candidate, activation

if __name__ == '__main__':
    data, activation = read_activated()
    print(json.dumps({'status': 'HASH_AND_SCHEMA_ONLY_NOT_A_REPLAY_PASS',
                      'candidate_sha256': activation['candidate_sha256']}))
