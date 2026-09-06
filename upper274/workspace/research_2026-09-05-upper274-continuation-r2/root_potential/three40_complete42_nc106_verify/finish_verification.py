"""Second exact calculation directly from original JSON at every raw minimizer.

No compiled physical-column table or producer computational module is used.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from hashlib import sha256
from math import comb
import json

P=Path(__file__).resolve().parent;R=P.parents[1];D=P.parent/'complete41_domain_audit'
digest=lambda p:sha256(p.read_bytes()).hexdigest()
activation=json.loads((P/'ACTIVATION.json').read_text())
source=R/activation['candidate_path']
assert digest(source)==activation['candidate_sha256']=='78238a2e3f389f9c7a4f93e049ad56e678c09103151fb3bfed0adc6e1dcf14bf'
j=json.loads(source.read_text())
s=json.loads((P/'SOURCE_AND_SUPPORT_VERIFICATION.json').read_text())
raw=json.loads((P/'RAW_VERIFICATION.json').read_text())
counts=json.loads((D/'COUNTS.json').read_text());di=json.loads((D/'INPUTS.json').read_text())
rootpath=R/'root_audit/three40_complete42/ROOT_RAW_VERIFICATION.json'
rootsupportpath=R/'root_audit/three40_complete42/SUPPORT_VERIFICATION.json'
root=json.loads(rootpath.read_text());rootsupport=json.loads(rootsupportpath.read_text())
assert root['status']=='INDEPENDENT_ROOT_RAW40_AND_OUTER_PASS'
assert rootsupport['status']=='INDEPENDENT_DATA_AND_SUPPORT_MAXIMA_PASS'
assert root['certificate_sha256']==rootsupport['certificate_sha256']==digest(source)
accepted={k:v['bound'] for k,v in root['tiers'].items()}
assert accepted==activation['expected_child_bounds']
for k in accepted:
    assert j['histograms'][k]['bound']==accepted[k] and root['tiers'][k]['mathematical_size']==40
assert raw['status']=='PASS_ALL14_EXACT_ALL_ORDERED_PRUNED_GRIDS'
assert len(raw['cases'])==len(s['cases'])==len(j['histograms']['106']['inner'])==14
maps={n:dict(zip(map(tuple,h['types']),h['phi'])) for n,h in j['histograms'].items()}
up={n:dict(zip(map(tuple,h['types']),h['phi'])) for n,h in j['upper5'].items()}
loc={n:dict(zip(map(tuple,h['types']),h['phi'])) for n,h in j['local_supports'].items()}
def e2(t):
    a,b,c=t;return a*b+a*c+b*c
def e3(t):
    a,b,c=t;return a*b*c
report=[]
for ci,(row,z,compiled) in enumerate(zip(j['histograms']['106']['inner'],raw['cases'],s['cases'],strict=True)):
    assert z['case']==ci and z['anchor']==row['type']==di['anchors106'][ci]
    mode=next(m for m in counts['cases'][ci]['modes'] if m['mode']=='new')
    assert z['raw_count']==mode['raw']==compiled['raw_count']
    assert row['count']==mode['discovery_cover']==compiled['cover_count']
    rawpath=Path(compiled['raw_file']);assert digest(rawpath)==compiled['raw_sha256']
    assert rawpath.name==f'case{ci:02d}_new_raw.u8'
    g=z['witness'];cols=[g[:3],g[3:6],g[6:]]
    assert len(g)==9 and all(type(c) is int and 0<=c<=20 for c in g)
    assert list(map(sum,cols))==row['type']
    profiles=[tuple(sorted(t,reverse=True)) for t in cols]
    # In F3 a nonvertical line satisfies u+v+w=0 for its three row positions.
    mixed=sum(cols[0][u]*cols[1][v]*cols[2][(-u-v)%3] for u in range(3) for v in range(3))
    X=[mixed]
    for t in cols:X.extend([e2(t),e3(t)])
    F=[40*row['type'][0]*row['type'][1]*row['type'][2]]
    for n in row['type']:F.extend([81*comb(n,2),27*comb(n,3)])
    for col,kind,tag,bound in row['extra']:
        X.append(int(profiles[col]==tuple(tag)) if kind=='exact' else up[tag][profiles[col]])
        F.append(bound)
    assert F==compiled['F']
    qF=sum(q*f for q,f in zip(row['coeff'],F,strict=True))
    assert qF==compiled['q_dot_F']
    value=sum(q*x for q,x in zip(row['coeff'],X,strict=True))
    subbound=0;subterms=[]
    for d in row['dependencies']:
        key=str(d['m']);assert d['coefficient']==1
        value+=maps[key][profiles[d['column']]]
        subbound+=accepted[key]
        subterms.append(dict(function_id=key,mathematical_size=40,column=d['column'],bound=accepted[key]))
    for d in row['local_supports']:
        assert d['coefficient']==1
        value+=loc[d['id']][profiles[d['column']]]
        local=s['local_supports'][d['id']]
        subbound+=local['bound']
        subterms.append(dict(function_id=d['id'],mathematical_size=local['size'],column=d['column'],bound=local['bound']))
    transverse=[]
    for slope in range(3):
        t=tuple(sorted((sum(cols[x][(r+slope*x)%3] for x in range(3)) for r in range(3)),reverse=True))
        transverse.append(t);value-=maps['106'][t]
    assert value==int(z['minimum'])==row['K']
    assert subbound==compiled['sum_child_bounds']
    bd=maps['106'][tuple(row['type'])]+qF+subbound-121*value
    assert bd==row['bound']==compiled['declared_case_bound']
    assert int(z['maximum_abs_value'])<=compiled['coarse_abs_value_bound']<2**126
    report.append(dict(case=ci,anchor=row['type'],raw_count=z['raw_count'],cover_count=row['count'],
        exact_minimum=value,declared_K=row['K'],case_bound=bd,q_dot_F=qF,
        child_bounds_sum=subbound,child_bound_terms=subterms,phi_at_anchor=maps['106'][tuple(row['type'])],
        forced_vector=F,raw_witness=g,witness_physical_profiles=profiles,
        witness_transverse_profiles=transverse,original_JSON_witness_replay_pass=True,
        raw_sha256=compiled['raw_sha256']))
B=max(r['case_bound'] for r in report)
assert B==activation['expected_NC106_bound']==j['histograms']['106']['bound']==-35039780423844643
assert sum(r['raw_count'] for r in report)==raw['all_raw_count']==1106094
assert sum(r['cover_count'] for r in report)==94242
out=dict(status='INDEPENDENT_PASS_ALL14_NC106_FULL_RAW_AND_UNIVERSAL_BOUND',
    candidate_sha256=digest(source),B106=B,maximum_cases=[r['case'] for r in report if r['case_bound']==B],
    accepted_child40_bounds=accepted,root_child40_acceptance_sha256=digest(rootpath),
    root_lower_support_acceptance_sha256=digest(rootsupportpath),cases=report,
    all_ordered_raw_count=1106094,discovery_cover_count=94242,
    upper_feature_signs_checked=s['upper_feature_signs_checked'],
    exact_indicator_features_checked=s['exact_indicator_features_checked'],
    full_physical41_supports_checked=6,full_physical42_supports_checked=6,
    complete41_support_dot_products=264,complete42_support_dot_products=24,
    nonzero_fixed_centered_theta40=dict(case=7,coefficient=1159,bound=475918720,
        justification='Exact +10^10-per-direction centering of root-accepted H3 theta40, source and audit SHA checked'),
    whole42_state_disjunction_used=False,domain_pruning='Only the original accepted14 ordinary5D41 zero types',
    source_and_support_sha256=digest(P/'SOURCE_AND_SUPPORT_VERIFICATION.json'),
    raw_verification_sha256=digest(P/'RAW_VERIFICATION.json'),
    raw_input_sha256=digest(P/'REPLAY_INPUT.txt'),
    own_domain_prefreeze_sha256=digest(D/'FROZEN.json'),
    codes={f:digest(P/f) for f in ['read_candidate.py','prepare_exact.py','replay_raw.cpp','finish_verification.py']},
    arithmetic='Python arbitrary integers for pure-data source/support compiler and independent original-JSON witness/bound replay; signed128 C++ on every ordered grid, with explicit coarse bound below2^126 for each case.',
    scope='Universal NC106 histogram inequality from all14 first-anchor cases. Root-accepted three40 child bounds and accepted complete41/42/baseline/theorem inputs. This P layer does not independently audit the outer inequality or assert a global274 bound.',
    shared_dependencies='Candidate coefficients, accepted finite spectra/ordinary/completion theorems and root-accepted three40/H3 bounds. P own independent raw catalogue and own prior raw arithmetic reused; no H/L/root feature or enumeration kernels imported.')
(P/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','candidate_sha256','B106','maximum_cases','all_ordered_raw_count','discovery_cover_count','accepted_child40_bounds']},indent=2))
