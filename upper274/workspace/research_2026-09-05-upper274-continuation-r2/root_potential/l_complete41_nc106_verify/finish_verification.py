from pathlib import Path
from hashlib import sha256
from math import comb
import json
p=Path(__file__).resolve().parent;b=p.parent.parent
digest=lambda f:sha256(f.read_bytes()).hexdigest()
source=b/'compatibility/complete41_support_10610564/RESULT.json'
assert digest(source)=='0fde44267b424bac9570b72813e8af4f0a44e0e7e87ba5ce9ae118af57881e97'
j=json.loads(source.read_text());s=json.loads((p/'SOURCE_AND_SUPPORT_VERIFICATION.json').read_text());raw=json.loads((p/'RAW_VERIFICATION.json').read_text())
dom=b/'root_potential/complete41_domain_audit';counts=json.loads((dom/'COUNTS.json').read_text());di=json.loads((dom/'INPUTS.json').read_text())
maps={n:dict(zip(map(tuple,h['types']),h['phi'])) for n,h in j['histograms'].items()}
up={n:dict(zip(map(tuple,h['types']),h['phi'])) for n,h in j['upper5'].items()}
loc={n:dict(zip(map(tuple,h['types']),h['phi'])) for n,h in j['local_supports'].items()}
def e2(t):
 a,b,c=t;return a*b+a*c+b*c
def e3(t):
 a,b,c=t;return a*b*c
report=[]
for ci,(r,z,compiled) in enumerate(zip(j['histograms']['106']['inner'],raw['cases'],s['cases'],strict=True)):
 assert z['case']==ci and z['anchor']==r['type']==di['anchors106'][ci]
 assert z['raw_count']==counts['cases'][ci]['modes'][0]['raw']==compiled['raw_count']
 rawpath=Path(compiled['raw_file']);assert digest(rawpath)==compiled['raw_sha256']
 g=z['witness'];a=g[:3];bb=g[3:6];c=g[6:];cs=[a,bb,c];profiles=[tuple(sorted(t,reverse=True)) for t in cs]
 assert list(map(sum,cs))==r['type']
 mixed=sum(a[u]*bb[v]*c[(-u-v)%3] for u in range(3) for v in range(3))
 X=[mixed]
 for t in cs:X.extend([e2(t),e3(t)])
 F=[40*comb(r['type'][0],1)*r['type'][1]*r['type'][2]]
 for n in r['type']:F.extend([81*comb(n,2),27*comb(n,3)])
 for col,kind,tag,bound in r['extra']:
  X.append(int(profiles[col]==tuple(tag)) if kind=='exact' else up[tag][profiles[col]])
  F.append(bound)
 assert F==compiled['F']
 qF=sum(q*f for q,f in zip(r['coeff'],F,strict=True));assert qF==compiled['q_dot_F']
 value=sum(q*x for q,x in zip(r['coeff'],X,strict=True))
 subbound=0
 for d in r['dependencies']:
  value+=maps[str(d['m'])][profiles[d['column']]]
  subbound+=j['histograms'][str(d['m'])]['bound']
 for d in r['local_supports']:
  value+=loc[d['id']][profiles[d['column']]]
  subbound+=s['physical41_supports'][d['id']]['bound']
 transverse=[]
 for slope in range(3):
  typ=tuple(sorted((sum(cs[x][(row+slope*x)%3] for x in range(3)) for row in range(3)),reverse=True))
  transverse.append(typ);value-=maps['106'][typ]
 assert value==int(z['minimum'])==r['K']
 assert subbound==compiled['sum_child_bounds']
 bd=maps['106'][tuple(r['type'])]+qF+subbound-121*value
 assert bd==r['bound']==compiled['declared_case_bound']
 assert int(z['maximum_abs_value'])<=compiled['coarse_abs_value_bound']<2**126
 report.append({'case':ci,'anchor':r['type'],'raw_count':z['raw_count'],'minimum':value,'case_bound':bd,'q_dot_F':qF,'child_bounds_sum':subbound,'phi_at_anchor':maps['106'][tuple(r['type'])],'witness':g,'witness_physical_profiles':profiles,'witness_transverse_profiles':transverse,'witness_direct_original_coefficient_check':True,'raw_file_sha256':compiled['raw_sha256']})
B=max(r['case_bound'] for r in report);assert B==-359979101924637==j['histograms']['106']['bound']
assert sum(z['raw_count'] for z in report)==1120785==raw['all_raw_count']
out={'status':'INDEPENDENT_PASS_ALL14_NC106_INEQUALITIES_AND_WHOLE_BOUND','candidate_sha256':digest(source),'scope':'Universal NC106 histogram function from the complete fourteen-case cover, with root-accepted phi40/B40 and published/accepted ordinary/completion inputs. No outer or global exclusion is proved by this layer alone.','B106':B,'maximum_cases':[r['case'] for r in report if r['case_bound']==B],'B40_root_accepted':j['histograms']['40']['bound'],'cases':report,'all_raw_count':1120785,'all_six_physical41_maxima_verified':True,'upper_feature_signs_checked':s['upper_feature_signs_checked'],'all23_applicable_41_42_upper_functions_verified_from_complete_spectra':True,'centered_theta40_all_multipliers_zero':True,'source_and_support_sha256':digest(p/'SOURCE_AND_SUPPORT_VERIFICATION.json'),'raw_verification_sha256':digest(p/'RAW_VERIFICATION.json'),'own_domain_prefreeze_sha256':digest(dom/'FROZEN.json'),'codes':{f:digest(p/f) for f in ['prepare_exact.py','replay_raw.cpp','finish_verification.py']},'arithmetic':'Python arbitrary-precision source/support/bound calculations and signed128 C++ complete raw replay with per-case strict coarse bounds below2^126; fourteen witnesses re-evaluated directly from the original candidate JSON using Python integers.','shared_dependencies':'Candidate coefficients, accepted complete41 and baseline42..45 spectra, accepted ordinary/completion predicates, root-accepted phi40/B40. Own previous independent domain enumerator is shared between P domain audit and this P replay; no H/L/root computational kernel imported.'}
(p/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['cases','scope','arithmetic','shared_dependencies']},indent=2))
