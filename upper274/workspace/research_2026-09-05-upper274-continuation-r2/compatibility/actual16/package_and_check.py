from pathlib import Path
from itertools import product,combinations
import json,hashlib,time
HERE=Path(__file__).resolve().parent;R=HERE.parents[1];st=time.monotonic();raw=json.loads((HERE/'LARGE_RAW.json').read_text());assert raw['status']=='COMPLETE_LARGE_ANCHOR_ACTUAL_HISTOGRAMS' and len(raw['cases'])==19
for name,sha in json.loads((HERE/'INPUTS.json').read_text())['source_hashes'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==sha
T=list(map(tuple,raw['types']));assert len(T)==14;ix={t:i for i,t in enumerate(T)}
D=[v for v in product(range(3),repeat=4)if any(v)and next(x for x in v if x)!=2];assert len(D)==40
actual=[]
for h in raw['histograms']:
 points=[]
 for layer,mask in enumerate(h['layer_masks']):
  points += [(layer,i%3,(i//3)%3,i//9)for i in range(27)if mask>>i&1]
 S=set(points);assert len(S)==16
 for a,b in combinations(points,2):assert tuple((-x-y)%3 for x,y in zip(a,b))not in S
 vec=[0]*14
 for d in D:
  counts=[0,0,0]
  for p in points:counts[sum(x*y for x,y in zip(d,p))%3]+=1
  t=tuple(sorted(counts,reverse=True));assert t in ix;vec[ix[t]]+=1
 assert vec==h['counts'] and sum(vec)==40
 actual.append(dict(counts=vec,points=points,layer_masks=h['layer_masks'],normalized_lift_multiplicity=h['multiplicity'],status='ACTUAL_POINT_REPRESENTATIVE_CHECKED'))
assert len({tuple(h['counts'])for h in actual})==len(actual)
assert sum(h['multiplicity']for h in raw['histograms'])==raw['total_lifts']==sum(c['lifted_caps']for c in raw['cases'])
small=[]
for a in range(14):
 v=[0]*14
 for t,n in [((7,7,2),a),((7,6,3),40-3*a),((7,5,4),2*a)]:v[ix[t]]=n
 small.append(dict(a=a,counts=v,status='NECESSARY_SMALL_ONLY_NOT_ASSERTED_REALIZABLE'))
assert not({tuple(x['counts'])for x in actual}&{tuple(x['counts'])for x in small})
packet=dict(status='COMPLETE_NECESSARY_4D16_HISTOGRAM_OVERCOVER',point_coordinate_order=['layer','x','y','z'],types=raw['types'],actual_large_histograms=actual,small_only_necessary_histograms=small,linear_small_only_endpoints=[small[0]['counts'],small[-1]['counts']],actual_large_histogram_count=len(actual),necessary_small_only_count=len(small),overcover_count=len(actual)+len(small),normalized_lift_count=raw['total_lifts'],cases=raw['cases'],scope='Actual16caps with a large8/9-section plus the proven necessary small-only14spectra; not a complete actual16classification',source_raw_sha256=hashlib.sha256((HERE/'LARGE_RAW.json').read_bytes()).hexdigest())
(HERE/'OVER_COVER.json').write_text(json.dumps(packet,indent=2)+'\n')
check=dict(status='ALL_REPRESENTATIVES_PAIR_AND_DIRECTION_PASS',representatives=len(actual),pairs_checked=120*len(actual),directions_per_representative=40,total_lifts=raw['total_lifts'],seconds=time.monotonic()-st,dependencies='Reads produced representative masks, independently computes4D point pairs and every dot-product direction; no C++ histogram reuse')
(HERE/'OWN_CHECK.json').write_text(json.dumps(check,indent=2)+'\n')
print(dict(actual=len(actual),small=len(small),total=len(actual)+len(small),lifts=raw['total_lifts'],seconds=raw['seconds']))
