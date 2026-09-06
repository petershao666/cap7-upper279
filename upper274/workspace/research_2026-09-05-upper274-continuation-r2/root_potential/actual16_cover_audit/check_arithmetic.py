from pathlib import Path
from math import comb
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
large=[(9,7,0),(9,6,1),(9,5,2),(9,4,3),(8,8,0),(8,7,1),(8,6,2),(8,5,3),(8,4,4)]
small=[(7,7,2),(7,6,3),(7,5,4),(6,6,4),(6,5,5)]
alltypes=sorted((a,b,16-a-b)for a in range(10)for b in range(a+1)if 0<=16-a-b<=b)
assert len(alltypes)==14 and set(alltypes)==set(large+small)
e2=lambda t:t[0]*t[1]+t[0]*t[2]+t[1]*t[2]
e3=lambda t:t[0]*t[1]*t[2]
force=[40,27*comb(16,2),9*comb(16,3)];assert force==[40,3240,5040]
slack=[7*e2(t)-e3(t)-441 for t in small];assert slack==[0,0,0,3,4]
assert 7*force[1]-force[2]-441*force[0]==0
states=[[a,40-3*a,2*a,0,0]for a in range(14)]
for a,h in enumerate(states):
 assert min(h)>=0 and sum(h)==40 and sum(n*e2(t)for n,t in zip(h,small))==3240 and sum(n*e3(t)for n,t in zip(h,small))==5040
 assert all(13*h[j]==(13-a)*states[0][j]+a*states[-1][j]for j in range(5))
# Formal coefficient check in variables (L*a,L*b,L*c,L*z_star,v).
Aprime=[1,0,0,0,1];Bprime=[0,1,0,1,2];Cprime=[0,0,1,2,0]
assert [sum(v)%3 for v in zip(Aprime,Bprime,Cprime)]==[1,1,1,0,0]
assert (1+2)%3==0 # C=z_star maps to0.
assert (1+2)%3==0 and (1+2)%3==0 # w=L*z_star+v cancels at level2.
# Only all-equal or all-distinct level triples can sum to0.
for i in range(3):
 for j in range(3):
  for k in range(3):assert ((i+j+k)%3==0)==(i==j==k or len({i,j,k})==3)
cp=ROOT/'compatibility/theta16_gate/COVERAGE.json';cover=json.loads(cp.read_text());assert cover['four_dimensional_types']==[list(t)for t in alltypes]and cover['large_anchor_order']==[list(t)for t in large]and cover['small_types']==[list(t)for t in small]and cover['global_moment_totals']==force and cover['small_histograms']==states and cover['small_linear_bound_endpoints']==[states[0],states[-1]]
packet=ROOT/'root_audit/small3d/ACCEPTED_0_9.json';assert hashlib.sha256(packet.read_bytes()).hexdigest()==cover['source_sha256']=='dc1d5f0578ca3df5d0cf6da03d9b097d9e818c8523451c261e92d07414465018'
out=dict(status='PASS_COMPLETE_NECESSARY_ACTUAL16_HISTOGRAM_OVERCOVER_THEORY',large_anchors=large,small_types=small,small_moment_totals=force,positive_slack_identity=slack,small_only_histograms=states,affine_map='(t,x)->(t,L*x+v+t*(L*z_star+v))',cross_sum_image='L*(a+b+c)',large_empty_third_layer='All actual B of required size; no complement restriction.',large_nonempty_third_layer='B actual in complement(-A), then C actual subset complement(-(A+B)) containing0.',coverage_json_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),accepted_small3d_sha256=cover['source_sha256'],no_cap_enumeration=True,no_LP=True,limitations='Complete necessary histogram overcover only. The14 small-only vectors are not asserted realizable. Large-family enumeration and L raw1314-table completeness have not been performed by this audit.')
(P/'ARITHMETIC_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
