from pathlib import Path
import json,hashlib,itertools,math
W=Path(__file__).resolve().parent;R=W.parents[1];read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=R/'root_potential/small3d_0_7_families.json';assert sha(p)=='fa6d3915c54fa8a4ca9601531fc497c19a3961599fd6fe08e1ac01b83e8cb635';d=read(p)
lines=iter((W/'histograms.txt').read_text().splitlines());out=[];checks=0;norms=[v for v in itertools.product(range(3),repeat=3)if any(v)and next(x for x in v if x)==1]
for f in d['families']:
 n,nc,nt,nh=map(int,next(lines).split());assert n==f['size'] and nc==f['actual_cap_count'] and nh==f['histogram_count'];codes=list(map(int,next(lines).split()));ts=[(c//100,c//10%10,c%10)for c in codes];raw=[list(map(int,next(lines).split()))for _ in range(nh)];want={tuple(x[:nt])for x in raw};tsp=list(map(tuple,f['types']));order=[tsp.index(t)for t in ts];actual=set()
 for h in f['histograms']:
  hh=tuple(h['counts'][i]for i in order);actual.add(hh);pts=list(map(tuple,h['points']));assert len(pts)==len(set(pts))==n and all(all(x in range(3)for x in v)for v in pts);ss=set(pts)
  for a,b in itertools.combinations(pts,2):assert tuple((-x-y)%3 for x,y in zip(a,b))not in ss;checks+=1
  hist={t:0 for t in ts}
  for v in norms:
   cnt=[0,0,0]
   for x in pts:cnt[sum(a*b for a,b in zip(v,x))%3]+=1
   hist[tuple(sorted(cnt,reverse=True))]+=1
  assert tuple(hist[t]for t in ts)==hh
 assert actual==want
 out.append(dict(size=n,types=ts,histograms=[list(x)for x in sorted(want)],actual_cap_count=nc))
# N8/9 actual finite families already independently established in H16/H17; no rerun.
for n in [8,9]:
 ts=[(a,b,n-a-b)for a in range(4,-1,-1)for b in range(a,-1,-1)if 0<=n-a-b<=b]
 if n==8:
  lu=[{(4,4,0):a,(4,3,1):12-4*a,(4,2,2):3*a-3,(3,3,2):4}for a in [1,2,3]];hs=[[h[t]for t in ts]for h in lu];nc=63180
 else:hs=[[{(4,4,1):9,(4,3,2):0,(3,3,3):4}[t]for t in ts]];nc=2106
 out.append(dict(size=n,types=ts,histograms=hs,actual_cap_count=nc))
report=dict(status='EXACT_ROOT_INDEPENDENT_SMALL3D_FAMILY_PASS',sizes=list(range(8)),actual_cap_counts=[f['actual_cap_count']for f in out[:8]],histogram_counts=[len(f['histograms'])for f in out[:8]],root_method='recursive canonical-increasing cap augmentation; allpartialcaps emitted; separate fromPallsubsets scan',producer_sha256=sha(p),checker_sha256=sha(W/'verify.cpp'),representative_pairchecks=checks,scope='Complete histogram sets and totalcapcounts; per-histogram frequencies inPsource are notused')
(W/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
family=dict(status='ACCEPTED_COMPLETE_3D_HISTOGRAMS_0_TO_9',families=out,new_0_7_verification_sha256=sha(W/'VERIFICATION.json'),old_8_9_sources=['../../root_potential/h16_input_independent_verification.json','../../root_potential/h17_complete3d_orbits.json'])
(W/'ACCEPTED_0_9.json').write_text(json.dumps(family,indent=2)+'\n');print('PASS complete0..7plusfrozen8/9; acceptedsha',sha(W/'ACCEPTED_0_9.json'))
