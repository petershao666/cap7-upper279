"""New pure-data compiler for the activated three40/complete42 NC106 layer.

Only our own fail-closed reader is imported. No producer or root kernels.
"""
import sys
sys.dont_write_bytecode = True
from collections import Counter
from math import comb
from pathlib import Path
import json, time
from read_candidate import read_activated, integer_function, digest, HERE, ROUND, DOMAIN, TIERS

start=time.monotonic()
j,activation=read_activated()
P=HERE;R=ROUND;D=DOMAIN
di=json.loads((D/'INPUTS.json').read_text());df=json.loads((D/'FROZEN.json').read_text())
dc=json.loads((D/'COUNTS.json').read_text())
assert digest(D/'FROZEN.json')=='19b3e4c9e574e97eded83a851ffd61d6c66fb83f1b5d1076ca5e171cf85cb860'
assert digest(D/'INPUTS.json')==df['input']
baseline=R.parent/'audit_2026-09-05_upper275/cap7_upper275/baseline277/baseline278/certificate.json'
assert digest(baseline)=='2780fba39eff792892e7aac960675e1ffdf8b2cf99b0c3b9e29d1123a98435be'
base=json.loads(baseline.read_text())
hpath=R/'root_audit/complete41/ACCEPTED_HISTOGRAMS.json'
assert digest(hpath)=='38193858291a37b0b71cff568a11db481080125140771e41af57f6fd973374fa'
h=json.loads(hpath.read_text())
assert j['complete41']==h and j['complete42']==base['spectrum5']['42']
hist=j['histograms'];nc=hist['106']
assert nc['bound']==activation['expected_NC106_bound']
assert nc['root']=={'coeff':[-39,1],'K':di['anchor_root']['cut'],'forced':di['anchor_root']['forced'],'gap':273}
assert j['ordinary5D_pruning']['ordinary5D41_zero_types']==di['zero41']
fn106=integer_function(nc,106)
child={key:integer_function(hist[key],40) for key in TIERS}
for key in TIERS:
    assert hist[key]['bound']==activation['expected_child_bounds'][key]
    assert hist[key]['tier_parent']==TIERS[key]['parent']
upper=j['upper5'];functions={k:integer_function(v,v['m']) for k,v in upper.items()}
uses={k:[] for k in upper}
upper_signs=exact_features=0
for ci,row in enumerate(nc['inner']):
    for off,(col,kind,tag,bound) in enumerate(row['extra'],7):
        n=row['type'][col]
        if kind=='exact':
            sp=base['spectrum5'][str(n)];assert len(sp['spectra'])==1
            assert sp['spectra'][0][sp['types'].index(tag)]==bound
            exact_features+=1
        else:
            assert kind in ('upper','new_upper')
            assert upper[tag]['m']==n and upper[tag]['bound']==bound
            assert row['coeff'][off]>=0
            upper_signs+=1
            uses[tag].append(dict(case=ci,column=col,coefficient=row['coeff'][off],kind=kind))
h3path=R/'hist105106/h3/h3_result.json'
assert digest(h3path)=='cbb4973544cf7e2388097bb333504dc0c53c943d1671605fa300996394dfd294'
h3=json.loads(h3path.read_text())['histograms']['40']
h3fn=integer_function(h3,40)
h3auditpath=R/'root_audit/h3_independent.json'
h3audit=json.loads(h3auditpath.read_text())
assert h3audit['status']=='PASS' and h3audit['source_sha256']==digest(h3path)
transportpath=R/'hist105106/h4/transport_tables.json'
transport=json.loads(transportpath.read_text())
upper_audit={}
for name,obj in upper.items():
    n=obj['m'];fn=functions[name]
    if name.startswith('centered_theta'):
        original=transport[str(n)];shift=10**10*original['subcap_count']
        assert fn==dict(zip(map(tuple,original['types']),[v+shift for v in original['phi']]))
        assert obj['bound']==original['bound']+121*shift
    if n==40:
        assert name=='centered_theta40'
        assert fn=={t:v+10**10 for t,v in h3fn.items()}
        assert obj['bound']==h3['bound']+121*10**10==475918720
        upper_audit[name]=dict(size=40,status='PASS_EXACT_CENTERING_OF_ROOT_ACCEPTED_H3_THETA40',
            original_bound=h3['bound'],shift_per_direction=10**10,declared_bound=obj['bound'],
            accepted_h3_source_sha256=digest(h3path),accepted_root_audit_sha256=digest(h3auditpath),uses=uses[name])
        continue
    if n==41:
        spectra=[dict(zip(map(tuple,h['types']),s['counts'])) for s in h['histograms']]
    else:
        assert 42<=n<=45
        sp=base['spectrum5'][str(n)]
        spectra=[dict(zip(map(tuple,sp['types']),s)) for s in sp['spectra']]
    values=[]
    for spectrum in spectra:
        assert all(t in fn for t,c in spectrum.items() if c)
        values.append(sum(c*fn[t] for t,c in spectrum.items() if c))
    assert max(values)<=obj['bound'],name
    upper_audit[name]=dict(size=n,status='PASS_DIRECT_COMPLETE_SPECTRA_UPPER_BOUND',
        declared_bound=obj['bound'],actual_maximum=max(values),all_values=values,
        maximizers=[i for i,v in enumerate(values) if v==max(values)],uses=uses[name])
local={name:obj for name,obj in j['local_supports'].items() if obj['case_dimension_size']==106}
assert len(local)==12
local_fn={k:integer_function(v,v['m']) for k,v in local.items()}
support_audit={}
for name,obj in local.items():
    n=obj['m'];assert n in (41,42)
    types=h['types'] if n==41 else base['spectrum5']['42']['types']
    spectra=[row['counts'] for row in h['histograms']] if n==41 else base['spectrum5']['42']['spectra']
    assert obj['types']==types
    vals=[sum(a*b for a,b in zip(row,obj['phi'],strict=True)) for row in spectra]
    assert max(vals)==obj['bound'],name
    support_audit[name]=dict(size=n,bound=max(vals),all_values=vals,
        maximizers=[i for i,v in enumerate(vals) if v==max(vals)],anchor=obj['anchor'],column=obj['column'])

def allowed(t):
    n=sum(t)
    if n>=42 and list(t) not in di['large5_support'][str(n)]:return False
    return not any(all(a>=b for a,b in zip(t,z)) for z in di['old41']+di['zero41'])
def e2(t):
    a,b,c=t;return a*b+a*c+b*c
def e3(t):
    a,b,c=t;return a*b*c

text=[str(len(fn106))]+[' '.join(map(str,(*t,v))) for t,v in fn106.items()]+['14']
compiled=[];seen=[]
for ci,row in enumerate(nc['inner']):
    A=row['type'];q=row['coeff']
    assert row['type']==di['anchors106'][ci]
    assert all(row.get(k) is None for k in ['class41','state18','full18_state','state8'])
    F=[40*A[0]*A[1]*A[2]]
    for n in A:F.extend([81*comb(n,2),27*comb(n,3)])
    F.extend(d[3] for d in row['extra'])
    slots={d['column']:d for d in row['local_supports']}
    seen.extend(d['id'] for d in row['local_supports'])
    tiers={d['column']:str(d['m']) for d in row['dependencies']}
    childbound=sum(hist[key]['bound'] for key in tiers.values())+sum(local[d['id']]['bound'] for d in slots.values())
    text.append(' '.join(map(str,[ci,*A,q[0],row['K']])))
    tables=[]
    for col,n in enumerate(A):
        rows=[]
        for a in range(21):
            for b in range(a+1):
                c=n-a-b;t=(a,b,c)
                if not 0<=c<=b or not allowed(t):continue
                value=q[1+2*col]*e2(t)+q[2+2*col]*e3(t)
                for off,(jcol,kind,tag,bd) in enumerate(row['extra'],7):
                    if jcol==col:value+=q[off]*(int(t==tuple(tag)) if kind=='exact' else functions[tag][t])
                if col in tiers:value+=child[tiers[col]][t]
                if col in slots:value+=local_fn[slots[col]['id']][t]
                rows.append([*t,value])
        assert rows
        text.append(str(len(rows)));text.extend(' '.join(map(str,r)) for r in rows);tables.append(rows)
    raw=D/f'case{ci:02d}_new_raw.u8';assert digest(raw)==df['files'][raw.name]
    mode=next(m for m in dc['cases'][ci]['modes'] if m['mode']=='new')
    assert raw.stat().st_size==9*mode['raw'] and row['count']==mode['discovery_cover']
    coarse=abs(q[0])*9*20**3+sum(max(abs(t[-1]) for t in table) for table in tables)+3*max(map(abs,fn106.values()))
    assert coarse<2**126
    compiled.append(dict(case=ci,anchor=A,F=F,q_dot_F=sum(a*b for a,b in zip(q,F,strict=True)),
        sum_child_bounds=childbound,phi_at_anchor=fn106[tuple(A)],declared_K=row['K'],
        declared_case_bound=row['bound'],column_tables=tables,q_cross=q[0],
        raw_file=str(raw),raw_sha256=digest(raw),raw_count=mode['raw'],cover_count=mode['discovery_cover'],
        coarse_abs_value_bound=coarse,dependencies=row['dependencies'],local_supports=row['local_supports']))
assert Counter(seen)==Counter(local.keys())
assert sum(c['raw_count'] for c in compiled)==1106094
assert sum(c['cover_count'] for c in compiled)==94242
(P/'REPLAY_INPUT.txt').write_text('\n'.join(text)+'\n')
source=R/activation['candidate_path']
report=dict(status='PASS_NC106_DATA_SIGNS_AND_COMPLETE41_42_SUPPORTS_CHILD40_ROOT_AUDIT_PENDING',
    candidate_sha256=digest(source),upper_functions=upper_audit,local_supports=support_audit,
    upper_feature_signs_checked=upper_signs,exact_indicator_features_checked=exact_features,
    child40_bounds=activation['expected_child_bounds'],NC106_claim=nc['bound'],
    cases=compiled,phi106_types=nc['types'],phi106=nc['phi'],root_cover=di['anchor_root'],
    root_H3_fixed_function_audit=h3audit,source_hashes={str(f):digest(f) for f in
        [source,baseline,hpath,h3path,h3auditpath,transportpath,D/'INPUTS.json',D/'FROZEN.json',P/'ACTIVATION.json']},
    seconds=time.monotonic()-start,whole42_state_filters_used=False,
    own_code_sha256=digest(Path(__file__)))
(P/'SOURCE_AND_SUPPORT_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],upper_signs=upper_signs,exact_indicators=exact_features,
    physical41_supports=6,physical42_supports=6,centered_theta40_nonzero_uses=[u for u in uses['centered_theta40'] if u['coefficient']],seconds=report['seconds'])))
