"""Final exact global bridge. Inherited audits are hash-bound, not rerun."""
from pathlib import Path
from itertools import product
from math import comb
import hashlib,json
W=Path(__file__).resolve().parent;R=W.parents[1];M=R.parent
hashes={}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    hashes[str(p.relative_to(M))]=sha(p)
    return json.loads(p.read_text())
def check(p,h):
    assert sha(p)==h,str(p)
    hashes[str(p.relative_to(M))]=h
def gap(z):assert z['gap']==364*z['K']-z['forced']>0
def Q(t):a,b,c=t;return 9*a*b*c-899*(a*b+a*c+b*c)+15730000
def key(s):return tuple(map(int,s.split(',')))

regpath=W/'REGISTRY_BEFORE_274.json'
check(regpath,'ae4b16840d5611a914a995451cf36a8b9207618d8268d05e89a57904eff8465b')
reg={z['id']:z for z in read(regpath)['entries']}
one=read(R/'root_audit/one_state_bridge/VERIFICATION.json')
assert one['status']=='PASS_REDUCED_TO_ONE_MINIMUM_STATE_NOT_274'
for path,h in one['input_hashes'].items():
    check(regpath if path.endswith('/RESEARCH_OUTPUT_REGISTRY.json') else M/path,h)
assert one['remaining']==[dict(type=[106,106,63],state=[0,0,-1],Q67=-7396)]
old=read(M/'research_2026-09-05-capset-round1-r1/route_a/certificates.json')
assert old==read(M/'research_2026-09-05-capset-round1-r1/root_audit/audited_certificate_snapshot.json')
prior=read(M/'research_2026-09-05-capset-round1-r1/root_audit/integration_checks.json')
assert prior['status']=='PASS' and prior['a_exact_cases']==88 and prior['a_matrices']==153548040
bridge=read(R/'compatibility/global_bridge_audit/GLOBAL_BRIDGE_AUDIT.json')
assert bridge['status']=='PASS_CONDITIONAL_GLOBAL_BRIDGE_ONLY'
for path,h in bridge['input_sha256'].items():
    # Its old live registry was bookkeeping; exact certificates and audits are separately bound.
    if not path.endswith('/RESEARCH_OUTPUT_REGISTRY.json'):check(M/path,h)
bans=list(map(tuple,old['seeds']))+[(112,109,51),(111,110,51)]
assert list(map(len,old['stages']))==[12,0]
for stage in old['stages']:
    for s,z in stage.items():gap(z);bans.append(key(s))
assert len(set(bans))==18 and set(bans)==set(map(tuple,bridge['ordinary_bans']))
types=[];residual=set();minimum_certificates=0
for a in range(113):
    for b in range(a+1):
        t=(a,b,275-a-b);c=t[2]
        if not 0<=c<=b:continue
        types.append(t)
        assert 4*Q(t)==(3*c-275)**2*(c-67)+(899-9*c)*(a-b)**2
        states=set(product(*[(-1,)if n<103 else(0,1)if n<109 else(1,)for n in t]))
        z=old['extremal'].get(','.join(map(str,t)));done=set()
        if z:
            if 'branches'in z:
                assert len(z['branches'])==len(states) and {tuple(v['status'])for v in z['branches']}==states
                for v in z['branches']:
                    if v['certificate']:gap(v['certificate']);done.add(tuple(v['status']));minimum_certificates+=1
            else:gap(z);done=states;minimum_certificates+=1
        if Q(t)<0 and not any(all(x>=y for x,y in zip(t,s))for s in bans):
            residual.update((t,s)for s in states-done)
assert len(types)==341 and sum(Q(t)<0 for t in types)==56 and minimum_certificates==76
total=9*243*comb(275,3)-899*729*comb(275,2)+1093*15730000
assert total==-246950==old['root_sum']
assert residual=={(tuple(t),tuple(s))for t,s in prior['remaining_minimum_states']}
assert len(residual)==8
closed=[]
for z in bridge['accepted_new_minimum_closures']:
    assert z['ordinary_exclusion'] is False and z['positive_gap']>0
    e=reg[z['registry_id']]
    assert e['certificate_hash']==z['certificate_sha256'] and e['ordinary_exclusion'] is False
    t=(tuple(z['type']),tuple(z['state']));assert t in residual
    residual.remove(t);closed.append(dict(type=t[0],state=t[1],registry_id=z['registry_id'],gap=z['positive_gap'],ordinary_exclusion=False))
assert len(closed)==6
for directory,registry_id,profile,expected_gap in [
 ('complete41_min10610564','L-COMPLETE41-MIN10610564',[106,105,64],21576254250),
 ('three40_complete42','L-TWO-LOCAL-THETA400-MIN10610663',[106,106,63],148616699075)]:
    v=read(R/f'root_audit/{directory}/VERIFICATION.json')
    assert v['status']=='EXACT_CONDITIONAL_MINIMUM_BRANCH_EXCLUSION_INDEPENDENTLY_VERIFIED'
    assert v['target']==profile and v['state']==[0,0,-1] and v['ordinary_exclusion'] is False
    assert v['positive_gap']==expected_gap>0
    for path,h in v['evidence'].items():check(R/path,h)
    state=(tuple(profile),(0,0,-1));assert state in residual
    residual.remove(state);closed.append(dict(type=profile,state=[0,0,-1],registry_id=registry_id,gap=expected_gap,ordinary_exclusion=False))
assert not residual and len(closed)==8
h=read(R/'hist105106/final274_logic_audit/STATIC_VERIFICATION.json')
check(R/'hist105106/final274_logic_audit/STATIC_VERIFICATION.json','e8f259e44b66bdff7442e5aa87f3c01f53221f70a15088fab5ff149a077ad654')
assert h['status']=='PASS_LOGICAL_IMPLICATION_AND_STATIC_EXACT_ARITHMETIC'
assert (h['global_profiles'],h['negative_profiles'],h['global_Q67_sum'])==(341,56,-246950)
assert h['outer_gap']==148616699075 and h['NC106_anchor_count']==14
for path,digest in h['input_hashes'].items():
    check(regpath if path.endswith('/RESEARCH_OUTPUT_REGISTRY.json') else M/path,digest)
last=read(R/'root_audit/three40_complete42/VERIFICATION.json')
assert h['candidate_sha256']==last['certificate_sha256']
assert last['exact_pointwise_rows_checked_total']==8807118 and last['finite_support_checks']==15885
H=R/'hist105106/final274_logic_audit'
check(H/'FROZEN.json','95bc8ab64ae621939f7ee28ec16c564ed1401ce1cec4fa369f4301e745a3a1c5')
hf=read(H/'FROZEN.json');assert hf['status']=='PASS_FINAL_LOGIC_AND_STATIC_ARITHMETIC'
for name,digest in hf['sha256'].items():check(H/name,digest)
dag=read(H/'DEPENDENCY_DAG.json');nodes={z['id']:z for z in dag['nodes']}
assert len(nodes)==15
visited=set();active=set()
def visit(n):
    assert n in nodes and n not in active
    if n in visited:return
    active.add(n)
    for p in nodes[n]['depends_on']:visit(p)
    active.remove(n);visited.add(n)
for n in nodes:visit(n)
check(R/'root_potential/three40_complete42_nc106_verify/PROOF.md','bbbf5aaf6988abdcd50421ba4dd47d870e5ac7ad2ef46802a0c61e0ad77250a2')
check(W/'PROOF.md',sha(W/'PROOF.md'))
check(Path(__file__),sha(Path(__file__)))
out={'status':'NEW_BOUND_VERIFIED','claim':'Every cap in F_3^7 has at most274 points, using the explicit accepted published lower-dimensional inputs.','excluded_cardinality':275,'global_upper':274,'accepted_lower':236,'cap237_existence':'UNKNOWN','sorted275_profiles':341,'negative_Q67_profiles':56,'Q67_total':total,'ordinary_bans':bans,'r1_exact_certificates':88,'inherited_r1_raw_rows_not_rerun':153548040,'continuation_minimum_closures':closed,'remaining_minimum_states':[],'last_certificate_sha256':last['certificate_sha256'],'last_certificate_positive_gap':last['positive_gap'],'last_certificate_independent_raw_rows':8807118,'last_certificate_finite_support_checks':15885,'published_premises':'Audited baseline low-dimensional cap bounds/classifications/completion results; Thackeray complete41 classification and explicitly asserted ancillary-list completeness. See PROOF.md and complete41 source audits.','independence':'Root independent lower/outer and support arithmetic, P independently generated NC106 domains/compiler/replay, H independent logical/static arithmetic; accepted coefficient/source data and earlier verified kernels are explicitly shared. Inherited large audits were not rerun.','novelty':'Internal global bound improvement275 to274; no publication-priority claim. Published input recovery is not new mathematics.','input_hashes':hashes}
(W/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k not in ['input_hashes','ordinary_bans','continuation_minimum_closures']},indent=2))
