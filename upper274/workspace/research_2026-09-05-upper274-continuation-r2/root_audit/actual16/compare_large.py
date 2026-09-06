from pathlib import Path
import json, hashlib, itertools, math
W=Path(__file__).resolve().parent; R=W.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=R/'compatibility/actual16/OVER_COVER.json'
assert sha(source)=='a4a815543db7a98d4b67d7606436c2a98dd2cf0e310992dd32ad7b878510b294'
d=json.loads(source.read_text()); raw=(W/'root_histograms.txt').read_text().splitlines()
codes=list(map(int,raw[0].split()));types=[(a//100,a//10%10,a%10)for a in codes]
rows=[list(map(int,line.split()))for line in raw[1:]];hs={tuple(r[:14])for r in rows};assert len(hs)==len(rows)==376
order=[list(map(tuple,d['types'])).index(t)for t in types]; other=set(); pairs=0
normals=[v for v in itertools.product(range(3),repeat=4)if any(v)and next(x for x in v if x)==1]; assert len(normals)==40
for rec in d['actual_large_histograms']:
 h=tuple(rec['counts'][i]for i in order);other.add(h)
 pts=list(map(tuple,rec['points']));assert len(pts)==len(set(pts))==16 and all(len(t)==4 and all(x in range(3)for x in t)for t in pts)
 ss=set(pts)
 for a,b in itertools.combinations(pts,2):assert tuple((-x-y)%3 for x,y in zip(a,b))not in ss;pairs+=1
 actual={t:0 for t in types}
 for v in normals:
  bins=[0,0,0]
  for p in pts:bins[sum(a*b for a,b in zip(v,p))%3]+=1
  actual[tuple(sorted(bins,reverse=True))]+=1
 assert tuple(actual[t]for t in types)==h
 assert sum(h)==40 and sum(n*(t[0]*t[1]+t[0]*t[2]+t[1]*t[2])for t,n in zip(types,h))==3240 and sum(n*math.prod(t)for t,n in zip(types,h))==5040
assert other==hs
report=dict(status='COMPLETE_LARGE_SECTION_ACTUAL16_HISTOGRAMS_INDEPENDENT_PASS',histograms=376,normalized_caps=553678,root_allpairchecks=66441360,producer_representative_pairchecks=pairs,source_sha256=sha(source),root_frozen_sha256=sha(W/'ROOT_FROZEN.json'),checker_sha256=sha(Path(__file__)),scope='Exactly all histograms of16caps with an8/9point3Dsection. Complete arbitrary16 family still depends on the independent small-only branch audit.',shared_dependencies='Accepted3D cap catalogue, affine8/9orbitcover; rootdifferentAreps andfullBcataloguefilter versusproducerrecursiveBkernel; no discoverycode imported.')
(W/'LARGE_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS376fullhistograms and45120representativepairs')
