"""Root integration of the independent lower, NC106, and outer checks."""
from pathlib import Path
from math import comb
import hashlib,json
W=Path(__file__).resolve().parent;R=W.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
cp=R/'compatibility/two_local_theta400_certificates/RESULT.json';c=read(cp)
assert sha(cp)=='78238a2e3f389f9c7a4f93e049ad56e678c09103151fb3bfed0adc6e1dcf14bf'
rp=W/'ROOT_RAW_VERIFICATION.json';raw=read(rp)
sp=W/'SUPPORT_VERIFICATION.json';support=read(sp)
P=R/'root_potential/three40_complete42_nc106_verify';pp=P/'VERIFICATION.json';p=read(pp)
assert sha(pp)=='bb9a437a66965e478951c9dccbea60b23c9d889fcf19ba04f27218b24a9e2232'
assert raw['status']=='INDEPENDENT_ROOT_RAW40_AND_OUTER_PASS'
assert support['status']=='INDEPENDENT_DATA_AND_SUPPORT_MAXIMA_PASS'
assert p['status']=='INDEPENDENT_PASS_ALL14_NC106_FULL_RAW_AND_UNIVERSAL_BOUND'
assert raw['certificate_sha256']==support['certificate_sha256']==p['candidate_sha256']==sha(cp)
assert p['root_child40_acceptance_sha256']==sha(rp)
assert p['root_lower_support_acceptance_sha256']==sha(sp)
for path,h in raw['input_hashes'].items():assert sha(R/path)==h,path
for path,h in raw['accepted_input_hashes'].items():assert sha(R/path)==h,path
for path,h in p['codes'].items():assert sha(P/path)==h,path
for file,field in [('SOURCE_AND_SUPPORT_VERIFICATION.json','source_and_support_sha256'),('RAW_VERIFICATION.json','raw_verification_sha256'),('REPLAY_INPUT.txt','raw_input_sha256')]:
    assert sha(P/file)==p[field]
source=read(P/'SOURCE_AND_SUPPORT_VERIFICATION.json')
for path,h in source['source_hashes'].items():assert sha(Path(path))==h,path
domain=P.parent/'complete41_domain_audit'
assert sha(domain/'FROZEN.json')==p['own_domain_prefreeze_sha256']
assert p['whole42_state_disjunction_used'] is False
assert p['accepted_child40_bounds']=={k:z['bound']for k,z in raw['tiers'].items()}
by={tuple(z['type']):z for z in c['histograms']['106']['inner']}
assert len(by)==len(p['cases'])==14
for i,z in enumerate(p['cases']):
    a=z['anchor'];rec=by[tuple(a)]
    assert sha(domain/f'case{i:02}_new_raw.u8')==z['raw_sha256']
    F=[40*a[0]*a[1]*a[2]]
    for n in a:F.extend([81*comb(n,2),27*comb(n,3)])
    F.extend(t[3]for t in rec['extra'])
    assert F==z['forced_vector']
    qF=sum(q*f for q,f in zip(rec['coeff'],F,strict=True))
    assert qF==z['q_dot_F']
    child=sum(c['histograms'][str(t['m'])]['bound']for t in rec['dependencies'])
    child+=sum(c['local_supports'][t['id']]['bound']for t in rec['local_supports'])
    assert child==z['child_bounds_sum']
    assert z['exact_minimum']==z['declared_K']==rec['K']
    value=z['phi_at_anchor']+qF+child-121*rec['K']
    assert value==z['case_bound']==rec['bound']
assert max(z['case_bound']for z in p['cases'])==p['B106']==c['histograms']['106']['bound']==-35039780423844643
assert p['all_ordered_raw_count']==1106094 and p['discovery_cover_count']==94242
assert raw['raw']==7701024 and support['finite_support_checks']==15885
o=c['outer'][0];a=o['type'];F=[121*a[0]*a[1]*a[2]]
for n in a:F.extend([243*comb(n,2),81*comb(n,3)])
assert len(c['outer'])==1 and a==[106,106,63]
assert len(o['coeff'])==19 and all(x==0 for x in o['coeff'][7:])
U=sum(q*f for q,f in zip(o['coeff'][:7],F,strict=True))+2*p['B106']
gap=364*o['K']-U
assert U==o['forced']==15823509458918317
assert gap==o['gap']==raw['outer']['gap']==148616699075>0
evidence=[cp,rp,sp,pp,P/'SOURCE_AND_SUPPORT_VERIFICATION.json',P/'RAW_VERIFICATION.json',R/'root_audit/complete41/VERIFICATION.json',Path(__file__)]
out={'status':'EXACT_CONDITIONAL_MINIMUM_BRANCH_EXCLUSION_INDEPENDENTLY_VERIFIED','target':[106,106,63],'state':[0,0,-1],'ordinary_exclusion':False,'condition':'An actual Q67-global-minimum direction of an arbitrary275cap with both106-point whole6DsectionsNC','certificate_sha256':sha(cp),'positive_gap':gap,'outer_K':o['K'],'outer_forced':U,'B40':p['accepted_child40_bounds'],'B106':p['B106'],'root_lower40_raw':318717,'P_NC106_all_ordered_raw':1106094,'root_outer_raw':7382307,'finite_support_checks':15885,'exact_pointwise_rows_checked_total':8807118,'all12_fixed_outer_upper_coefficients_zero':True,'whole42_state_disjunction_used':False,'root_read_independent_code_and_proofs':True,'shared_dependencies':['Published lower-dimensional classifications and completion/NC theorems','Complete5D41 family with explicit published ancillary-list completeness premise','Accepted actual4D16/17/18 histograms, primary Table1 and previously independently checked clash patterns','Certificate coefficient data','Root own prior lower/outer kernel reused; P own prior independent raw-domain generator and arithmetic reused'],'independent_kernels':['Root stdlib input/support checker and direct forced-sum integration','Root standalone C++ raw40/outer checker','P fully ordered NC106 generator, separate pure-data row compiler and C++ replay, original-JSON witness arithmetic'],'evidence':{str(t.relative_to(R)):sha(t)for t in evidence},'remaining_minimum_states':[],'global_promotion':'Requires separate completed global274 bridge audit','cap237_existence':'UNKNOWN'}
(W/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k not in ['evidence','shared_dependencies','independent_kernels']},indent=2))
