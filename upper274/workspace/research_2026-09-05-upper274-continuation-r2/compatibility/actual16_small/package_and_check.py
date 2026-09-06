from pathlib import Path
from itertools import combinations,product
import json,hashlib,time
HERE=Path(__file__).resolve().parent;R=HERE.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((HERE/'SMALL_RAW.json').read_text());inp=json.loads((HERE/'INPUTS.json').read_text())
assert r['status']=='COMPLETE_SMALL_ONLY_ACTUAL_HISTOGRAMS'
assert sha(R/inp['extension_source'])==inp['extension_sha256']
large_path=HERE.parent/'actual16/OVER_COVER.json'
assert sha(large_path)==inp['large_packet_sha256']
large=json.loads(large_path.read_text());T=list(map(tuple,r['types']));assert T==list(map(tuple,large['types']))
cover=inp['A7_cover'];assert len(cover)==24
for x in cover:
 assert x['parent8'] in (13851,13853,13902)
 assert x['parent8']>>x['deleted']&1
 assert x['A7']==x['parent8']^(1<<x['deleted']) and x['A7'].bit_count()==7
assert [(tuple(x['anchor']),x['A_mask'])for x in r['cases']]==[(t,x['A7'])for t in [(7,7,2),(7,6,3)]for x in cover]
assert sum(x['constructed_caps']for x in r['cases'])==r['total_constructed']==1084572
assert sum(x['lifted_caps']for x in r['cases'])==r['total_lifts']==0
for x in r['cases']:
 assert sum(x['free_size_counts'])==x['B_caps']
 assert x['B_with_C']==0 and x['lifted_caps']==0
assert r['histograms']==[]
small_types=[(7,7,2),(7,6,3),(7,5,4),(6,6,4),(6,5,5)]
f=lambda t:7*(t[0]*t[1]+t[0]*t[2]+t[1]*t[2])-t[0]*t[1]*t[2]
assert list(map(f,small_types))==[441,441,441,444,445]
assert 7*(27*120)-9*560==441*40
# Independently recompute all point-pair and directional tests of the final packet.
D=[v for v in product(range(3),repeat=4)if any(v)and next(x for x in v if x)==1];assert len(D)==40
ix={t:i for i,t in enumerate(T)}
actual=large['actual_large_histograms']
for h in actual:
 points=list(map(tuple,h['points']));S=set(points);assert len(points)==len(S)==16
 for a,b in combinations(points,2):assert tuple((-x-y)%3 for x,y in zip(a,b))not in S
 vec=[0]*len(T)
 for d in D:
  c=[sum(sum(x*y for x,y in zip(d,p))%3==j for p in points)for j in range(3)]
  vec[ix[tuple(sorted(c,reverse=True))]]+=1
 assert vec==h['counts'] and any(n and T[j][0]>=8 for j,n in enumerate(vec))
assert len({tuple(h['counts'])for h in actual})==len(actual)==376
packet=dict(status='COMPLETE_ACTUAL_4D16_HISTOGRAM_FAMILY_PENDING_INDEPENDENT_COMPARISON',types=r['types'],point_coordinate_order=['layer','x','y','z'],histograms=actual,histogram_count=376,actual_small_only_histogram_count=0,scope='Every affine cap of size16 in F3^4 has exactly one of these376 direction histograms; every histogram has a checked explicit cap representative. This is a complete histogram family, not an affine-isomorphism classification.',large_normalized_lifts=553678,small_normalized_lifts_constructed=1084572,small_lifts_retained=0,source_large_sha256=sha(large_path),source_small_raw_sha256=sha(HERE/'SMALL_RAW.json'))
(HERE/'COMPLETE_ACTUAL16.json').write_text(json.dumps(packet,indent=2)+'\n')
check=dict(status='PACKET_AND_REPRESENTATIVES_CHECKED_PENDING_ROOT_ENUMERATION_COMPARISON',cases=48,constructed=1084572,retained_small=0,small_histograms=0,complete_histograms=376,representatives_checked=376,pairs_checked=45120,directions_per_representative=40,root_small_results_read=False,dependencies='Same producer small recursive enumeration kernel as frozen large enumeration; independent Python direct point-pair/dot-product check of final witnesses. Root uses a separate catalogue-filter/subset kernel and alternative affine representatives. Shared accepted complete3D8 orbit cover and independently accepted7-extension bridge.')
(HERE/'OWN_CHECK.json').write_text(json.dumps(check,indent=2)+'\n')
print(check)
