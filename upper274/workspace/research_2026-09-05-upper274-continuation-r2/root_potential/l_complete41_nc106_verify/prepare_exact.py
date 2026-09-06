"""Pure JSON source/sign/finite-support audit and exact integer row compiler."""
from pathlib import Path
from hashlib import sha256
from math import comb
from collections import Counter
import json,time

start=time.monotonic()
p=Path(__file__).resolve().parent;b=p.parent.parent;workspace=b.parent
dom=b/'root_potential/complete41_domain_audit'
digest=lambda f:sha256(f.read_bytes()).hexdigest()
source=b/'compatibility/complete41_support_10610564/RESULT.json'
assert digest(source)=='0fde44267b424bac9570b72813e8af4f0a44e0e7e87ba5ce9ae118af57881e97'
j=json.loads(source.read_text());di=json.loads((dom/'INPUTS.json').read_text());df=json.loads((dom/'FROZEN.json').read_text())
assert digest(dom/'INPUTS.json')==df['input']
baseline=workspace/'audit_2026-09-05_upper275/cap7_upper275/baseline277/baseline278/certificate.json'
base=json.loads(baseline.read_text());hpath=b/'root_audit/complete41/ACCEPTED_HISTOGRAMS.json'
h=json.loads(hpath.read_text());assert digest(hpath)=='38193858291a37b0b71cff568a11db481080125140771e41af57f6fd973374fa'
nc=j['histograms']['106'];child=j['histograms']['40'];assert nc['types']==di['support106']
assert nc['bound']==-359979101924637 and child['bound']==-95858610055698
assert nc['root']=={'coeff':[-39,1],'K':di['anchor_root']['cut'],'forced':di['anchor_root']['forced'],'gap':273}

def lookup(obj):
    assert len(obj['types'])==len(obj['phi']) and all(type(v) is int for v in obj['phi'])
    d=dict(zip(map(tuple,obj['types']),obj['phi']));assert len(d)==len(obj['types'])
    return d

phi106=lookup(nc);phi40=lookup(child)
upper=j['upper5'];functions={k:lookup(v) for k,v in upper.items()}
uses={k:[] for k in upper}
for ci,r in enumerate(nc['inner']):
    assert r['type']==di['anchors106'][ci]
    assert len(r['coeff'])==7+len(r['extra']) and all(type(q) is int for q in r['coeff'])
    for off,desc in enumerate(r['extra'],7):
        col,kind,tag,bound=desc;assert 0<=col<3
        if kind=='exact':
            spec=base['spectrum5'][str(r['type'][col])];assert len(spec['spectra'])==1
            assert spec['spectra'][0][spec['types'].index(tag)]==bound
        else:
            assert kind in ['upper','new_upper']
            assert upper[tag]['m']==r['type'][col] and upper[tag]['bound']==bound
            assert r['coeff'][off]>=0
            uses[tag].append({'case':ci,'column':col,'coefficient':r['coeff'][off],'kind':kind})

upper_audit={}
transport=json.loads((b/'hist105106/h4/transport_tables.json').read_text())
for name,obj in upper.items():
    m=obj['m'];fn=functions[name]
    if name.startswith('centered_theta'):
        original=transport[str(m)];shift=10**10*original['subcap_count']
        assert fn==dict(zip(map(tuple,original['types']),[v+shift for v in original['phi']]))
        assert obj['bound']==original['bound']+121*shift
    if m==41:
        support=[dict(zip(map(tuple,h['types']),row['counts'])) for row in h['histograms']]
    elif 42<=m<=45:
        spec=base['spectrum5'][str(m)]
        support=[dict(zip(map(tuple,spec['types']),row)) for row in spec['spectra']]
    else:
        assert m==40 and all(u['coefficient']==0 for u in uses[name])
        upper_audit[name]={'size':m,'status':'ZERO_MULTIPLIER_IN_EVERY_NC106_OCCURRENCE','declared_bound':obj['bound'],'actual_full_family_maximum':None,'uses':uses[name],'centered_transport_identity_checked':True}
        continue
    values=[]
    for spectrum in support:
        assert all(t in fn for t,n in spectrum.items() if n)
        values.append(sum(n*fn[t] for t,n in spectrum.items() if n))
    assert max(values)<=obj['bound'],name
    upper_audit[name]={'size':m,'status':'PASS_DIRECT_COMPLETE_SPECTRA_UPPER_BOUND','declared_bound':obj['bound'],'actual_full_family_maximum':max(values),'all_histogram_values':values,'maximizers':[i for i,v in enumerate(values) if v==max(values)],'uses':uses[name]}

local={name:obj for name,obj in j['local_supports'].items() if obj['m']==41}
assert len(local)==6
local_fn={k:lookup(v) for k,v in local.items()};support_audit={}
for name,obj in local.items():
    assert obj['types']==h['types'] and obj['case_dimension_size']==106
    values=[sum(a*c for a,c in zip(row['counts'],obj['phi'])) for row in h['histograms']]
    assert max(values)==obj['bound'],name
    support_audit[name]={'bound':max(values),'all44_values':values,'maximizers':[i for i,v in enumerate(values) if v==max(values)],'anchor':obj['anchor'],'column':obj['column']}

def e2(t):
    a,b,c=t;return a*b+a*c+b*c
def e3(t):
    a,b,c=t;return a*b*c
def oldok(t):
    if sum(t)>=42 and t not in map(tuple,di['large5_support'][str(sum(t))]):return False
    return not any(all(a>=b for a,b in zip(t,z)) for z in di['old41'])

compiled=[];text=[str(len(phi106))]
for t,val in phi106.items():text.append(' '.join(map(str,(*t,val))))
text.append('14');seen_local=[];upper_sign_count=0
for ci,r in enumerate(nc['inner']):
    A=r['type'];q=r['coeff'];F=[40*A[0]*A[1]*A[2]]
    for n in A:F.extend([81*comb(n,2),27*comb(n,3)])
    assert not r['conditional_dependencies'] and r['conditional_bound'] is None
    assert r['class41'] is None and r['state18'] is None and r['full18_state'] is None
    expected_children=[{'m':40,'column':col,'coefficient':1} for col,n in enumerate(A) if n==40]
    assert r['dependencies']==expected_children
    slots={s['column']:s for s in r['local_supports']}
    assert set(slots)=={col for col,n in enumerate(A) if n==41}
    for col,s in slots.items():
        assert s['coefficient']==1 and s['id'] in local
        obj=local[s['id']];assert obj['anchor']==A and obj['column']==col
        seen_local.append(s['id'])
    for off,desc in enumerate(r['extra'],7):
        F.append(desc[3]);upper_sign_count+=desc[1] in ['upper','new_upper']
    constant=sum(a*c for a,c in zip(q,F))
    bound_children=sum(child['bound'] for d in expected_children)+sum(local[s['id']]['bound'] for s in slots.values())
    text.append(' '.join(map(str,[ci,*A,q[0],r['K']])))
    tables=[]
    for col,n in enumerate(A):
        rows=[]
        for a in range(21):
            for bb in range(a+1):
                c=n-a-bb;t=(a,bb,c)
                if not 0<=c<=bb or not oldok(t):continue
                val=q[1+2*col]*e2(t)+q[2+2*col]*e3(t)
                for off,(jcol,kind,tag,bd) in enumerate(r['extra'],7):
                    if col!=jcol:continue
                    val+=q[off]*(int(t==tuple(tag)) if kind=='exact' else functions[tag][t])
                if n==40:val+=phi40[t]
                if n==41:val+=local_fn[slots[col]['id']][t]
                rows.append([*t,val])
        text.append(str(len(rows)));text.extend(' '.join(map(str,row)) for row in rows);tables.append(rows)
    raw=dom/f'case{ci:02d}_old_raw.u8';assert digest(raw)==df['files'][raw.name]
    crude=abs(q[0])*9*20**3+sum(max(abs(v[-1]) for v in tbl) for tbl in tables)+3*max(map(abs,phi106.values()))
    assert crude<2**126
    compiled.append({'case':ci,'anchor':A,'q_cross':q[0],'column_tables':tables,'F':F,'q_dot_F':constant,'sum_child_bounds':bound_children,'phi_at_anchor':phi106[tuple(A)],'declared_K':r['K'],'declared_case_bound':r['bound'],'raw_file':str(raw),'raw_sha256':digest(raw),'raw_count':raw.stat().st_size//9,'coarse_abs_value_bound':crude,'dependencies':expected_children,'local_supports':r['local_supports']})
assert Counter(seen_local)==Counter(local.keys())
(p/'REPLAY_INPUT.txt').write_text('\n'.join(text)+'\n')
report={'status':'PASS_INPUT_SCOPE_SIGNS_AND_ALL_RELEVANT_FINITE_SUPPORTS','candidate_sha256':digest(source),'accepted41_sha256':digest(hpath),'baseline_sha256':digest(baseline),'own_domain_prefreeze_sha256':digest(dom/'FROZEN.json'),'upper_functions':upper_audit,'physical41_supports':support_audit,'upper_feature_signs_checked':upper_sign_count,'cases':compiled,'phi106_types':nc['types'],'phi106':nc['phi'],'B40_accepted_from_root':child['bound'],'B106_claim':nc['bound'],'root_cover':di['anchor_root'],'source_hashes':{str(f.relative_to(workspace)):digest(f) for f in [source,hpath,baseline,b/'hist105106/h4/transport_tables.json',dom/'INPUTS.json']},'prepare_code_sha256':digest(Path(__file__)),'seconds':time.monotonic()-start}
(p/'SOURCE_AND_SUPPORT_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'upper_signs':upper_sign_count,'support41':len(local),'size41_or42_upper_functions_verified':sum(v['status']=='PASS_DIRECT_COMPLETE_SPECTRA_UPPER_BOUND' for v in upper_audit.values()),'unused40_upper_functions':sum(v['status'].startswith('ZERO') for v in upper_audit.values()),'seconds':report['seconds']}))
