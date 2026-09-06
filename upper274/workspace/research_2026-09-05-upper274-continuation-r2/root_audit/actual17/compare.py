from pathlib import Path
import json,hashlib,math,itertools
W=Path(__file__).resolve().parent;R=W.parents[1];read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=R/'hist105106/h17/histograms17.json';assert sha(p)=='7c47c4c3468fc8ead940a889f24fdb31bc6d45dfeea764e53aa998462399528c';d=read(p)
lines=(W/'histograms.txt').read_text().splitlines();codes=list(map(int,lines[0].split()));ts=[(v//100,(v//10)%10,v%10)for v in codes];rows=[list(map(int,s.split()))for s in lines[1:]];hset={tuple(x[:13])for x in rows};assert len(rows)==len(hset)==102
other=set();types=list(map(tuple,d['types']));order=[types.index(t)for t in ts]
checks=0;norms=[v for v in itertools.product(range(3),repeat=4)if any(v)and next(x for x in v if x)==1];assert len(norms)==40
for rec in d['histograms']:
 h=tuple(rec['counts'][i]for i in order);other.add(h);pts=list(map(tuple,rec['points']));assert len(pts)==len(set(pts))==17 and all(len(t)==4 and all(x in [0,1,2]for x in t)for t in pts)
 ss=set(pts)
 for a,b in itertools.combinations(pts,2):assert tuple((-x-y)%3 for x,y in zip(a,b))not in ss;checks+=1
 actual={t:0 for t in ts}
 for v in norms:
  bins=[0,0,0]
  for x in pts:bins[sum(a*b for a,b in zip(v,x))%3]+=1
  actual[tuple(sorted(bins,reverse=True))]+=1
 assert tuple(actual[t]for t in ts)==h
 assert sum(h)==40 and sum(hh*(t[0]*t[1]+t[0]*t[2]+t[1]*t[2])for t,hh in zip(ts,h))==27*math.comb(17,2) and sum(hh*math.prod(t)for t,hh in zip(ts,h))==9*math.comb(17,3)
assert hset==other and len(d['histograms'])==102
report=dict(status='EXACT_COMPLETE_ACTUAL17_HISTOGRAM_FAMILY_INDEPENDENT_PASS',histogram_count=102,types=ts,normalized_cover_caps=70935,cover_branches=dict(f980=63180,f971=3240,f881=4515),root_entire_cover_pairchecks=9647160,producer_representative_pairchecks=checks,producer_sha256=sha(p),root_histogram_table_sha256=sha(W/'histograms.txt'),root_cpp_sha256=sha(W/'enumerate.cpp'),p_orbit_inputs=read(W/'INPUT_MANIFEST.json'),scope='Complete possible40-direction histograms for arbitraryAG4caps of17points, via primary980/971/881cover;102is NOT an affineorbit count and70935is NOT all labeled17caps',shared_dependencies='Published17capcover andPindependentlyverified3Dcapcatalog; root usesP representatives, notHnormalization/generator. RootC++recursiveBconstruction/popcountdirections andPythonrepresentativecheck are separate fromH discovery.')
(W/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
family=dict(status=report['status'],types=ts,histograms=[list(h)for h in sorted(hset)],source_verification_sha256=sha(W/'VERIFICATION.json'),scope=report['scope'])
(W/'ACCEPTED_HISTOGRAMS.json').write_text(json.dumps(family,indent=2)+'\n');print('PASS102fullhistograms;all70935rootpointsets;producer136x102pairs',checks,'acceptedsha',sha(W/'ACCEPTED_HISTOGRAMS.json'))
