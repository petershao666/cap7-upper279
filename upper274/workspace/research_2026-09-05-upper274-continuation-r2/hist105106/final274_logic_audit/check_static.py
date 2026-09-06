"""Independent stdlib-only logical/finite-data audit. No domain or solver imports."""
from pathlib import Path
from math import comb
from itertools import product
import json,hashlib,time
START=time.monotonic();W=Path(__file__).resolve().parent;R=W.parents[1];M=R.parent
HASHES={}
def read(p):
 b=p.read_bytes();HASHES[str(p.relative_to(M))]=hashlib.sha256(b).hexdigest();return json.loads(b)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def e2(t):a,b,c=t;return a*b+a*c+b*c
def e3(t):return t[0]*t[1]*t[2]
def Q(t):return 9*e3(t)-899*e2(t)+15730000
def parse(s):return tuple(map(int,s.split(',')))
def avoided(t,forbidden):return not any(all(a>=b for a,b in zip(t,f))for f in forbidden)
def gap(z):assert 364*z['K']-z['forced']==z['gap']>0
def profiles(n,upper):
 out=[]
 for c in range(n//3+1):
  for b in range(c,upper+1):
   a=n-b-c
   if b<=a<=upper:out.append((a,b,c))
 return sorted(out)
def force(t,n):
 out=[((3**(n-2)-1)//2)*e3(t)]
 for a in t:out.extend([3**(n-2)*comb(a,2),3**(n-3)*comb(a,3)])
 return out
P=R/'compatibility/two_local_theta400_certificates'
cert=read(P/'RESULT.json');spec=read(P/'RAW_AUDIT_SPEC.json')
assert sha(P/'RESULT.json')=='78238a2e3f389f9c7a4f93e049ad56e678c09103151fb3bfed0adc6e1dcf14bf'==spec['candidate_sha256']
assert cert['claim']=='CANDIDATE_EXACT_CERTIFICATE'and spec['whole42_disjunction_used']is False
source_packet=read(R/'hist105106/whole42_fixed_evaluation/INTEGER_PACKET.json')
assert sha(R/'hist105106/whole42_fixed_evaluation/INTEGER_PACKET.json')==spec['source_integer_packet_sha256']==cert['integer_packet_sha256']
for m,h in cert['histograms'].items():
 assert h['types']==source_packet['main_functions'][m]['types']and h['phi']==source_packet['main_functions'][m]['phi']
assert cert['conditional_functions']==source_packet['conditional_functions']
for name,l in cert['local_supports'].items():
 for key in ['types','phi','bound']:assert l[key]==source_packet['local_supports'][name][key]
changed=[]
for s,old_s in zip(spec['cases'],source_packet['cases']):
 assert s['index']==old_s['index']and s['function_id']==old_s['function_id']and s['anchor']==old_s['anchor']
 assert s['forced']==old_s['forced']and s['X_sha256']==old_s['X_sha256']and s['tops_sha256']==old_s['tops_sha256']
 if s['coeff']!=old_s['coeff']:changed.append((s['function_id'],tuple(s['anchor'])))
assert changed==[(400,(20,17,3)),(400,(20,15,5))]
base=read(M/'audit_2026-09-05_upper275/cap7_upper275/baseline277/baseline278/certificate.json')
old=[parse(k)for stage in base['six_stages']for k in stage]
comp=list(map(tuple,base['completion_seeds']))+[parse(k)for stage in base['completion_stages']for k in stage]
assert all(sum(t)>=103 for t in comp[4:])
support106=[t for t in profiles(106,45)if avoided(t,old+comp)]
rf=-39*243*comb(106,2)+81*comb(106,3);threshold=rf//364+1
anchor106=[t for t in support106 if e3(t)-39*e2(t)<threshold]
assert len(support106)==79 and len(anchor106)==14
assert list(map(tuple,cert['histograms']['106']['types']))==support106
assert list(map(tuple,spec['first_anchor_order106']))==anchor106
assert cert['histograms']['106']['root']==dict(coeff=[-39,1],K=threshold,forced=rf,gap=364*threshold-rf)
order40=list(reversed(profiles(40,20)));assert len(order40)==44
assert list(map(tuple,spec['first_anchor_order40']))==order40
coverage=read(P/'all_case_coverage.json')
for m in [400,401,402]:
 rows=[z for z in coverage['lower']if z['m']==m]
 assert list(map(lambda z:tuple(z['type']),rows))==order40
 assert [z['type']for z in rows if z['empty']]==[[14,13,13]]
 assert list(map(tuple,cert['histograms'][str(m)]['types']))==list(reversed(order40))
assert [tuple(z['type'])for z in coverage['lower']if z['m']==106]==anchor106
assert not any(z['empty']for z in coverage['lower']if z['m']==106)

# Reconstruct all275 profile/status cases and bind inherited accepted closures.
r1dir=M/'research_2026-09-05-capset-round1-r1'
r1=read(r1dir/'route_a/certificates.json');snapshot=read(r1dir/'root_audit/audited_certificate_snapshot.json')
assert r1==snapshot and r1['size']==275 and r1['k']==67
inherited=read(r1dir/'root_audit/integration_checks.json')
assert inherited['status']=='PASS'and inherited['a_exact_cases']==88
assert inherited['a_matrices']==153548040
seed=list(map(tuple,r1['seeds']));assert seed==[(112,112,29),(112,111,35),(112,110,45),(111,111,45)]
ordinary=[]
for stage in r1['stages']:
 for k,z in stage.items():gap(z);ordinary.append(parse(k))
assert list(map(len,r1['stages']))==[12,0]
bans=seed+ordinary+[(112,109,51),(111,110,51)]
types=profiles(275,112);assert len(types)==341
total=9*243*comb(275,3)-899*729*comb(275,2)+1093*15730000
assert total==-246950==r1['root_sum']
unclosed=set();checked_r1_minimum=0;negative=0
for t in types:
 a,b,c=t;assert 4*Q(t)==(3*c-275)**2*(c-67)+(899-9*c)*(a-b)**2
 states=set(product(*[(-1,)if n<103 else(0,1)if n<109 else(1,)for n in t]))
 rec=r1['extremal'].get(','.join(map(str,t)));done=set()
 if rec:
  if 'branches'in rec:
   assert len(rec['branches'])==len(states)and {tuple(z['status'])for z in rec['branches']}==states
   for z in rec['branches']:
    if z['certificate']:gap(z['certificate']);done.add(tuple(z['status']));checked_r1_minimum+=1
  else:gap(rec);done=states;checked_r1_minimum+=1
 if Q(t)<0:
  negative+=1
  if avoided(t,bans):unclosed.update((t,s)for s in states-done)
assert negative==56 and checked_r1_minimum==76 and len(unclosed)==8
assert unclosed=={(tuple(t),tuple(s))for t,s in inherited['remaining_minimum_states']}
bridge=read(R/'compatibility/global_bridge_audit/GLOBAL_BRIDGE_AUDIT.json')
assert set(bans)==set(map(tuple,bridge['ordinary_bans']))
registry=read(R/'RESEARCH_OUTPUT_REGISTRY.json');reg={z['id']:z for z in registry['entries']}
for name,h in bridge['input_sha256'].items():
 if not name.endswith('/RESEARCH_OUTPUT_REGISTRY.json'):assert sha(M/name)==h,name
for z in bridge['accepted_new_minimum_closures']:
 assert not z['ordinary_exclusion']and z['positive_gap']>0
 assert reg[z['registry_id']]['certificate_hash']==z['certificate_sha256']
 unclosed.remove((tuple(z['type']),tuple(z['state'])))
seventh=read(R/'compatibility/complete41_support_10610564/RESULT.json')
seventh_v=read(R/'root_audit/complete41_min10610564/VERIFICATION.json')
assert sha(R/'compatibility/complete41_support_10610564/RESULT.json')==seventh_v['certificate_sha256']
assert seventh_v['status']=='EXACT_CONDITIONAL_MINIMUM_BRANCH_EXCLUSION_INDEPENDENTLY_VERIFIED'
assert not seventh_v['ordinary_exclusion']
gap(seventh['outer'][0]);assert seventh['outer'][0]['gap']==21576254250==seventh_v['positive_gap']
for name,h in seventh_v['evidence'].items():assert sha(R/name)==h,name
unclosed.remove(((106,105,64),(0,0,-1)))
assert unclosed=={((106,106,63),(0,0,-1))}
one=read(R/'root_audit/one_state_bridge/VERIFICATION.json')
assert one['status']=='PASS_REDUCED_TO_ONE_MINIMUM_STATE_NOT_274'
assert one['remaining']==[dict(type=[106,106,63],state=[0,0,-1],Q67=-7396)]

# Check finite data and exact support maxima independently, without grid enumeration.
hh=spec['finite_histograms'];local=cert['local_supports'];cf=cert['conditional_functions'];cb=cert['conditional_bounds']
assert cert['histogram_pair_capacity']==read(R/'hist105106/h13/histogram_pair_capacity_v2.json')
for n,path in [('16','root_audit/actual16/ACCEPTED_HISTOGRAMS.json'),('17','root_audit/actual17/ACCEPTED_HISTOGRAMS.json')]:
 a=read(R/path);assert set(map(tuple,hh[n]['types']))==set(map(tuple,a['types']))
 ix={tuple(t):i for i,t in enumerate(a['types'])}
 aligned={tuple(h[ix[tuple(t)]]for t in hh[n]['types'])for h in a['histograms']}
 assert {tuple(h)for h in hh[n]['histograms']}==aligned
a=read(R/'root_audit/complete41/ACCEPTED_HISTOGRAMS.json')
assert hh['41']['types']==a['types']and hh['41']['histograms']==[z['counts']for z in a['histograms']]
assert hh['42']['types']==base['spectrum5']['42']['types']and hh['42']['histograms']==base['spectrum5']['42']['spectra']
a=read(R/'hist105106/h10/full18_states.json')
assert hh['18']['histograms']==[[dict(zip(map(tuple,z['types']),z['histogram'])).get(tuple(t),0)for t in hh['18']['types']]for z in a]
support_checks=0
for name,z in local.items():
 n=str(z['m']);assert z['types']==hh[n]['types'];assert all(type(v)is int for v in z['phi'])
 assert z['anchor'][z['column']]==z['m']
 H=hh[n]['histograms'];assert all(sum(h)==(40 if z['m']<=18 else 121)for h in H)
 assert all(all(type(v)is int and v>=0 for v in h)for h in H)
 assert max(dot(h,z['phi'])for h in H)==z['bound'];support_checks+=len(H)
for tier in [400,401,402]:
 l=f't{tier}_left18';r=f't{tier}_right18';pair=f't{tier}_pair18';c=f't{tier}_cond18'
 pairs=cert['histogram_pair_capacity']['allowed_18184_ordered_pairs'];cond=cert['histogram_pair_capacity']['allowed_20182_full18_states'];H=hh['18']['histograms']
 assert len(pairs)==267 and len(cond)==16
 assert cb[pair]==max(dot(H[a],cf[l])+dot(H[b],cf[r])for a,b in pairs)
 assert cb[c]==max(dot(H[a],cf[c])for a in cond);support_checks+=len(pairs)+len(cond)
assert support_checks==15885

# Static exact layer arithmetic and all physical dependency/sign/feature totals.
hist=cert['histograms'];H1920=read(R/'hist105106/h3/hist19_20.json');upper=cert['upper5']
histrows={(int(m),tuple(c['type'])):c for m,h in hist.items()for c in h['inner']}
assert len(histrows)==143 and len(spec['cases'])==144
bound_results=[];seen=set();tiermap={400:(43,40,23),401:(44,40,22),402:(45,40,21)}
for s in spec['cases']:
 m=s['function_id'];t=tuple(s['anchor']);n=7 if m=='outer'else 6 if m==106 else 5
 assert s['forced'][:7]==force(t,n)
 assert len(s['coeff'])==len(s['forced'])==7+len(s['extra'])
 assert all(type(v)is int for v in s['coeff'])
 expected_positive=[]
 for i,e in enumerate(s['extra'],7):
  col,kind,name,bd=e;assert s['forced'][i]==bd
  if kind in('upper','new_upper'):
   assert upper[name]['m']==t[col]and upper[name]['bound']==bd;expected_positive.append(i)
  elif kind=='exact':
   h=base['spectrum5'][str(t[col])];assert len(h['spectra'])==1
   assert dict(zip(map(tuple,h['types']),h['spectra'][0]))[tuple(name)]==bd
  elif kind=='exact4':
   h=H1920[str(t[col])];assert dict(zip(map(tuple,h['types']),h['histogram']))[tuple(name)]==bd
  elif kind=='direction_cover':
   assert t[col]==17 and name==[[9,8,0],[9,7,1],[8,8,1]]and bd==-1;expected_positive.append(i)
  elif kind=='fixed6_upper':
   h=next(h for h in cert['fixed6']['functions']if h['id']==name);assert h['size']==t[col]and h['bound']==bd;expected_positive.append(i)
  else:raise AssertionError(kind)
 assert s['upper_indices']==expected_positive
 assert all(s['coeff'][j]>=0 for j in expected_positive)
 if m=='outer':
  assert t==(106,106,63)and len(cert['outer'])==1
  c=cert['outer'][0];assert c['coeff']==s['coeff']and c['K']==s['K']
  assert all(v==0 for v in s['coeff'][7:])
  forced=dot(s['coeff'],s['forced'])+2*hist['106']['bound']
  assert forced==c['forced']==s['exact_forced_with_children']
  gap(c);assert c['gap']==148616699075==s['outer_gap'];continue
 c=histrows[(m,t)];seen.add((m,t))
 assert c['coeff']==s['coeff']and c['K']==s['K']and c['count']==s['count']
 terms=0
 for dep in s['dependencies']:
  p=dep['function_id'];j=dep['column'];assert m==106 and t==tiermap[p]and j==1 and t[j]==40
  assert dict(m=p,column=j,coefficient=1)in c['dependencies'];terms+=hist[str(p)]['bound']
 for dep in s['local_supports']:
  z=local[dep['id']];assert tuple(z['anchor'])==t and z['column']==dep['column']and z['case_dimension_size']==m
  assert dict(id=dep['id'],column=dep['column'],coefficient=1)in c['local_supports'];terms+=z['bound']
 if s['conditional_dependencies']:
  assert m in tiermap and t in [(20,18,2),(18,18,4)]
  want=[(f't{m}_cond18',1)]if t==(20,18,2)else[(f't{m}_left18',0),(f't{m}_right18',1)]
  assert [(z['id'],z['column'])for z in s['conditional_dependencies']]==want
  assert s['conditional_bound']==(f't{m}_cond18'if t==(20,18,2)else f't{m}_pair18');terms+=cb[s['conditional_bound']]
 H=hist[str(m)];phi=dict(zip(map(tuple,H['types']),H['phi']))
 B=phi[t]+dot(s['coeff'],s['forced'])+terms-(121 if m==106 else 40)*s['K']
 assert B==c['bound']==s['exact_bound'];bound_results.append(dict(function_id=m,type=t,bound=B))
assert seen==set(histrows)
for m in [400,401,402,106]:assert max(r['bound']for r in bound_results if r['function_id']==m)==hist[str(m)]['bound']
assert [hist[str(m)]['bound']for m in [400,401,402,106]]==[-9829345995830952,-9618859046048364,-10564264755104425,-35039780423844643]
rootraw=read(R/'root_audit/three40_complete42/ROOT_RAW_VERIFICATION.json')
assert rootraw['status']=='INDEPENDENT_ROOT_RAW40_AND_OUTER_PASS'and rootraw['certificate_sha256']==sha(P/'RESULT.json')
assert rootraw['outer']['gap']==148616699075 and rootraw['raw']==7701024
for name,h in rootraw['input_hashes'].items():assert sha(R/name)==h,name
pvdir=R/'root_potential/three40_complete42_nc106_verify';pv=read(pvdir/'VERIFICATION.json')
assert sha(pvdir/'VERIFICATION.json')=='bb9a437a66965e478951c9dccbea60b23c9d889fcf19ba04f27218b24a9e2232'
assert pv['status']=='INDEPENDENT_PASS_ALL14_NC106_FULL_RAW_AND_UNIVERSAL_BOUND'
assert pv['candidate_sha256']==sha(P/'RESULT.json')and pv['B106']==hist['106']['bound']
assert pv['root_child40_acceptance_sha256']==sha(R/'root_audit/three40_complete42/ROOT_RAW_VERIFICATION.json')
assert pv['raw_verification_sha256']==sha(pvdir/'RAW_VERIFICATION.json')and pv['source_and_support_sha256']==sha(pvdir/'SOURCE_AND_SUPPORT_VERIFICATION.json')
out=dict(status='PASS_LOGICAL_IMPLICATION_AND_STATIC_EXACT_ARITHMETIC',candidate_sha256=sha(P/'RESULT.json'),global_promotion_by_this_audit=False,final_raw_NC106_verification_sha256=sha(pvdir/'VERIFICATION.json'),global_profiles=341,negative_profiles=56,global_Q67_sum=total,remaining_before_candidate=[dict(type=[106,106,63],state=[0,0,-1])],NC106_support_size=79,NC106_anchor_count=14,NC106_anchor_root=dict(forced=rf,K=threshold,gap=364*threshold-rf),universal40_formal_anchors=44,universal40_empty_anchor=[14,13,13],finite_support_scores_checked=support_checks,local_case_forced_bound_identities_checked=len(bound_results),main_bounds={m:hist[str(m)]['bound']for m in [400,401,402,106]},outer_gap=cert['outer'][0]['gap'],outer_forced=cert['outer'][0]['forced'],inherited_r1_replays_not_rerun=dict(certificates=88,matrices=153548040),root_new_raw_replay_dependency=dict(cases=133,raw=7701024),P_new_raw_replay_dependency=dict(cases=14,raw=pv['all_ordered_raw_count']),large_domain_enumerations_by_this_audit=0,optimizer_calls=0,input_hashes=HASHES,elapsed=time.monotonic()-START)
(W/'STATIC_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k!='input_hashes'},indent=2))
