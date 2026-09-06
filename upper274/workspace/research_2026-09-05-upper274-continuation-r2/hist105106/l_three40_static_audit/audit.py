from pathlib import Path
import json,hashlib,ast,time
from collections import Counter
W=Path(__file__).resolve().parent;R=W.parents[1];L=R/'compatibility/physical40_complete42_10610663';H=R/'hist105106/h25_complete42';start=time.monotonic()
read=lambda p:json.loads(p.read_text())
inputs=read(L/'INPUTS.json');frozen=read(L/'STATIC_FROZEN.json');planned=read(L/'PLANNED_COPY_LAYOUT.json');realized=read(L/'REALIZED_COPY_LAYOUT.json');base=read(H/'local_support_layout.json');signs=read(L/'SIGNS_AND_FEATURES.json');oldsigns=read(H/'SIGNS_AND_FEATURES.json');cov=read(L/'all_case_coverage.json');oldcov=read(H/'all_case_coverage.json')
for p,h in inputs['source_hashes'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
assert hashlib.sha256((L/'run.py').read_bytes()).hexdigest()==inputs['new_run_sha256']
assert hashlib.sha256((L/'verify.py').read_bytes()).hexdigest()==inputs['author_verifier_sha256']
assert planned['leaf_functions']==realized['leaf_functions']
leaves=planned['leaf_functions'];assert len(leaves)==96 and Counter(v['m']for v in leaves.values())=={16:30,17:30,18:24,41:6,42:6}
base40={(tuple(z['anchor']),z['column'],z['m'])for z in base.values()if z['case_dimension_size']==40};basehigh={(tuple(z['anchor']),z['column'],z['m'])for z in base.values()if z['case_dimension_size']==106};assert len(base40)==28 and len(basehigh)==12
for t in [400,401,402]:assert {(tuple(z['anchor']),z['column'],z['m'])for z in leaves.values()if z['case_dimension_size']==t}==base40
assert {(tuple(z['anchor']),z['column'],z['m'])for z in leaves.values()if z['case_dimension_size']==106}==basehigh
old40=[z for z in oldcov['lower']if z['m']==40];oldnc=[z for z in oldcov['lower']if z['m']==106]
for t in [400,401,402]:assert [dict(z,m=40)for z in cov['lower']if z['m']==t]==old40
assert [z for z in cov['lower']if z['m']==106]==oldnc
assert signs['outer_fixed_instances']==oldsigns['outer_fixed_instances']and signs['outer_extra']==oldsigns['outer_extra']and signs['outer_upper_indices']==oldsigns['outer_upper_indices']
for t in [400,401,402]:assert [dict(z,m=40)for z in signs['inner']if z['m']==t]==[z for z in oldsigns['inner']if z['m']==40]
assert [z for z in signs['inner']if z['m']==106]==[z for z in oldsigns['inner']if z['m']==106]
expected=[dict(parent_anchor=a,function=t,column=1)for t,a in [(400,[43,40,23]),(401,[44,40,22]),(402,[45,40,21])]];assert realized['parent_occurrences']==expected
widths={16:14,17:13,18:12,41:40,42:13};support_sizes={16:376,17:102,18:17,41:44,42:4}
finite=sum(support_sizes[z['m']]for z in leaves.values())+3*(267+16);assert finite==15885
main=3*(44+1)+(79+1);conditional=9*12+6;leafvars=sum(widths[z['m']]+1 for z in leaves.values());qvars=sum(z['feature_count']for z in signs['inner'])+signs['outer_feature_count'];variables=main+conditional+leafvars+qvars+1;assert variables==3291
assert realized['variables']==variables and realized['finite_support_rows']==finite
blocks=[]
for n,(a,b)in realized['main_offsets'].items():blocks.append((a,b+1,'main'+n))
for n,a in realized['conditional_function_offsets'].items():blocks.append((a,a+12,n))
for n,a in realized['conditional_bound_offsets'].items():blocks.append((a,a+1,n))
for z in realized['case_coefficients']:blocks.append((z['offset'],z['offset']+z['width'],str((z['function'],z['anchor']))))
for i,(a,b,n)in enumerate(blocks):
 for c,d,m in blocks[:i]:assert b<=c or d<=a,(n,m)
# Compare unchanged mathematical functions structurally, allowing only the owned path alias.
def functions(path):
 txt=path.read_text().replace("H/","W.parent/")
 return {n.name:ast.dump(n,include_attributes=False)for n in ast.parse(txt).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
a=functions(H/'run.py');b=functions(L/'run.py')
for n in ['attach16_17','low40','localize_supports','outer_new']:assert a[n]==b[n],n
out=dict(status='STATIC_COPY_MATHEMATICS_PASS_WITH_METADATA_DISPLAY_NOTE',no_producer_import=True,no_domain_enumeration=True,no_LP=True,source_hashes_verified=len(inputs['source_hashes']),run_sha256=inputs['new_run_sha256'],verify_sha256=inputs['author_verifier_sha256'],leaf_counts=dict(Counter(z['m']for z in leaves.values())),finite_support_rows=finite,variable_breakdown=dict(main=main,conditional=conditional,leaf=leafvars,case_and_outer_coefficients=qvars,gap=1,total=variables),all_physical_parent_mappings_exact=True,all_old_feature_signs_and_domains_unchanged=True,independent_offsets_checked=True,unchanged_mathematical_function_ASTs=['attach16_17','low40','localize_supports','outer_new'],note='400/401/402 are internal function IDs. Main histogram objects record mathematical_size40; ancillary counts/empty/leaf case_dimension_size retain IDs and need explicit function_id/mathematical_size display mapping. This is not a solver or proof-row bug.',shared_dependency_boundary='Both producer and its author verifier reuse frozen H25 domain generators. This audit checks copying and static connections, not independent raw certificate truth.',elapsed_seconds=time.monotonic()-start,wall_seconds_since_gate=time.time()-(W/'SCOPE.md').stat().st_mtime)
(W/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
