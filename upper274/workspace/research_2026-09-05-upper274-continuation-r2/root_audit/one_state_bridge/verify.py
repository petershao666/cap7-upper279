"""Root direct profile/status arithmetic and bindings; no discovery imports."""
from pathlib import Path
from itertools import product
from math import comb
import json,hashlib,time
W=Path(__file__).resolve().parent;R=W.parents[1];M=R.parent
inputs={};start=time.monotonic()
def read(p):
    b=p.read_bytes();inputs[str(p.relative_to(M))]=hashlib.sha256(b).hexdigest();return json.loads(b)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def Q(t):a,b,c=t;return 9*a*b*c-899*(a*b+a*c+b*c)+15730000
def key(s):return tuple(map(int,s.split(',')))
def excludes(t,bs):return any(all(x>=y for x,y in zip(t,b)) for b in bs)
def gap(c):assert c['gap']==364*c['K']-c['forced']>0
A=M/'research_2026-09-05-capset-round1-r1'
c=read(A/'route_a/certificates.json')
assert c==read(A/'root_audit/audited_certificate_snapshot.json')
prior=read(A/'root_audit/integration_checks.json')
assert prior['status']=='PASS' and prior['a_exact_cases']==88 and prior['a_matrices']==153548040
bridge=read(R/'compatibility/global_bridge_audit/GLOBAL_BRIDGE_AUDIT.json')
assert bridge['status']=='PASS_CONDITIONAL_GLOBAL_BRIDGE_ONLY'
reg=read(R/'RESEARCH_OUTPUT_REGISTRY.json');reg={e['id']:e for e in reg['entries']}
seed=[(112,112,29),(112,111,35),(112,110,45),(111,111,45)]
assert list(map(tuple,c['seeds']))==seed and c['size']==275 and c['k']==67
ordinary=[]
assert list(map(len,c['stages']))==[12,0]
for stage in c['stages']:
    for s,z in stage.items():gap(z);ordinary.append(key(s))
delete=[(112,109,51),(111,110,51)]
bans=seed+ordinary+delete
assert len(bans)==18 and set(bans)==set(map(tuple,bridge['ordinary_bans']))
types=[];residual=set();nc=0
for a in range(113):
    for b in range(a+1):
        t=(a,b,275-a-b)
        if not 0<=t[2]<=b:continue
        types.append(t)
        states=set(product(*[((-1,) if n<103 else (0,1) if n<109 else (1,)) for n in t]))
        rec=c['extremal'].get(','.join(map(str,t)));done=set()
        if rec:
            if 'branches' in rec:
                assert {tuple(z['status']) for z in rec['branches']}==states
                assert len(rec['branches'])==len(states)
                for z in rec['branches']:
                    if z['certificate']:gap(z['certificate']);done.add(tuple(z['status']));nc+=1
            else:gap(rec);done=states;nc+=1
        if Q(t)<0 and not excludes(t,bans):residual.update((t,s) for s in states-done)
        x,y,z=t
        assert 4*Q(t)==(3*z-275)**2*(z-67)+(899-9*z)*(x-y)**2
assert len(types)==341 and sum(Q(t)<0 for t in types)==56 and nc==76
total=9*243*comb(275,3)-899*729*comb(275,2)+1093*15730000
assert total==-246950==c['root_sum']
assert residual=={(tuple(t),tuple(s)) for t,s in prior['remaining_minimum_states']}
assert residual=={(tuple(z['type']),tuple(z['state'])) for z in bridge['r1_residuals']}
# Bind every source previously checked by the independent two-state bridge.
for p,sha in bridge['input_sha256'].items():
    if p.endswith('/RESEARCH_OUTPUT_REGISTRY.json'):continue # This live registry gained the seventh accepted entry.
    assert digest(M/p)==sha,p
closed=[]
for z in bridge['accepted_new_minimum_closures']:
    e=reg[z['registry_id']];assert e['certificate_hash']==z['certificate_sha256']
    assert e['ordinary_exclusion'] is False and z['ordinary_exclusion'] is False and z['positive_gap']>0
    st=(tuple(z['type']),tuple(z['state']));assert st in residual
    closed.append(st)
remaining=residual-set(closed)
assert remaining=={((106,106,63),(0,0,-1)),((106,105,64),(0,0,-1))}
cp=R/'compatibility/complete41_support_10610564/RESULT.json'
cert=read(cp);vpath=R/'root_audit/complete41_min10610564/VERIFICATION.json';v=read(vpath)
e=reg['L-COMPLETE41-MIN10610564']
assert digest(cp)==e['certificate_hash']==v['certificate_sha256']
assert digest(vpath)==e['root_verification_hash']
assert v['status']=='EXACT_CONDITIONAL_MINIMUM_BRANCH_EXCLUSION_INDEPENDENTLY_VERIFIED'
assert not e['ordinary_exclusion'] and not v['ordinary_exclusion']
assert len(cert['outer'])==1 and cert['outer'][0]['type']==[106,105,64]
gap(cert['outer'][0]);assert cert['outer'][0]['gap']==v['positive_gap']==21576254250
for p,sha in v['evidence'].items():assert digest(R/p)==sha,p
remaining.remove(((106,105,64),(0,0,-1)))
assert remaining=={((106,106,63),(0,0,-1))}
result={'status':'PASS_REDUCED_TO_ONE_MINIMUM_STATE_NOT_274','sorted275_types':341,'negative_types':56,'root_total':total,'r1_exact_certificates':88,'accepted_continuation_minimum_closures':7,'remaining':[{'type':t,'state':s,'Q67':Q(t)} for t,s in remaining],'conditional_bridge':'If the remaining actual Q67-minimum NC/NC/* state is excluded by a complete independently checked certificate, no275cap exists; a larger cap would contain a275subset.','global_upper':275,'cap237_existence':'UNKNOWN','shared_dependencies':'Previously accepted exact-domain audits and explicit published classification/completion inputs; no source classification is re-proved here.','input_hashes':inputs,'elapsed':time.monotonic()-start}
(W/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='input_hashes'},indent=2))
