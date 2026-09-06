"""Exact small rational arithmetic only. No optimizer, cap or grid enumeration."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,hashlib,time
W=Path(__file__).resolve().parent;R=W.parents[1]
start=time.monotonic();inputs={}
def read(p):
    b=p.read_bytes();inputs[str(p.relative_to(R))]=hashlib.sha256(b).hexdigest();return json.loads(b)
h=read(R/'hist105106/h3/h3_result.json')['histograms']['40'];ts=list(map(tuple,h['types']));theta=dict(zip(ts,h['phi']));assert len(ts)==44
ends=read(R/'compatibility/complete20200_dominance/RESULT.json')['endpoint_count_models']
end=[{tuple(map(int,k.split(','))):v for k,v in x['histogram'].items()}for x in ends]
p=R/'root_audit/complete20200/root_histograms.txt';b=p.read_bytes();inputs[str(p.relative_to(R))]=hashlib.sha256(b).hexdigest();lines=b.decode().splitlines();rt=[tuple(map(int,s.split(',')))for s in lines[0].split()];actual={tuple(map(int,line.split()[:len(rt)]))for line in lines[1:]if line.strip()}
assert len(actual)==8
for e in end:assert tuple(e.get(t,0)for t in rt)in actual
types=[(20,20,0),(18,18,4),(18,11,11),(16,12,12),(14,14,12),(15,15,10),(17,15,8)]
bar=[F(end[0].get(t,0)+end[1].get(t,0),2)for t in types];assert bar==[1,5,10,25,50,10,20]
den=59136241;num=[59136241,-154544760,151290368,-46118673,-9763176,0,0];v=[F(n,den)for n in num]
rows=[[1 for t in types],[a*b+a*c+b*c for a,b,c in types],[a*b*c for a,b,c in types],[theta[t]for t in types]]
assert all(sum(x*y for x,y in zip(v,row))==0 for row in rows)
plus=[x+y for x,y in zip(bar,v)];minus=[x-y for x,y in zip(bar,v)]
assert min(plus+minus)>=0 and plus[0]==2 and minus[0]==0
expected=[121,81*comb(40,2),27*comb(40,3)]
for z in [bar,plus,minus]:
    assert [sum(x*y for x,y in zip(z,row))for row in rows[:3]]==expected
    assert sum(x*y for x,y in zip(z,rows[3]))<=h['bound']
assert all((a+b+c)/3==m for a,b,c,m in zip(plus,minus,bar,bar))
old_interface=read(R/'compatibility/complete41_support_10610564/INTERFACE_CHECK.json')
qsum=sum(c['feature_count']for c in old_interface['case_features']if c['m']==40);assert qsum==379
baseline=read(R/'hist105106/h23_run/h23_result.json')
assert sum(c['count']for c in baseline['counts']if c['m']==40)==36455
assert sum(c['count']for c in baseline['counts']if c['m']==106)==94242 and baseline['outer_count']==2460769
read(R/'hist105106/h23_run/FROZEN.json')
tier=45+qsum+(10*14+10*13+8*12+28)+(3*12+2);assert tier==856
parent=[dict(NC106_case_index=i,anchor=t,physical_column=1)for i,t in [(3,(43,40,23)),(7,(44,40,22)),(11,(45,40,21))]]
out=dict(status='EXACT_STRICT_HISTOGRAM_INTERFACE_WITNESS_NOT_FULL_PARENT_FEASIBILITY',types=types,hbar=list(map(str,bar)),v_numerator=num,v_denominator=den,z_plus=list(map(str,plus)),z_minus=list(map(str,minus)),third_marginal=list(map(str,bar)),exact_moment_rows=rows[:3],exact_moment_totals=expected,H3_values=rows[3],H3_bound=h['bound'],H3_sum_at_all_three=int(sum(x*y for x,y in zip(bar,rows[3]))),H3_slack=int(h['bound']-sum(x*y for x,y in zip(bar,rows[3]))),known_valid_profile_upper={'type':[20,20,0],'bound':1},strict_violation_at_z_plus=1,mean_in_old40_polytope='hbar=(acceptedactualh0+acceptedactualh10)/2',parent_sections=parent,copies=3,one_complete40_tier_variables=tier,additional_variables=2*tier,finite_support_rows=3*5199+264,lower40_table_evaluations=3*36455,input_sha256=inputs,no_parent_grid_lift_claimed=True,no_optimizer_or_new_enumeration=True,seconds=time.monotonic()-start)
assert out['seconds']<120
(W/'WITNESS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['status','H3_slack','additional_variables','finite_support_rows','seconds']},indent=2))
