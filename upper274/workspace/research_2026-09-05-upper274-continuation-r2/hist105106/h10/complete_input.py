from pathlib import Path
import json,hashlib,collections,itertools
W=Path(__file__).resolve().parent;z=json.loads((W/'coded18_points_histograms.json').read_text());rpath=W.parents[1]/'root_audit/882_points_independent.json';r=json.loads(rpath.read_text());dirs=[u for u in itertools.product(range(3),repeat=4)if any(u)and next(x for x in u if x)==1]
for name in ['882A1','882A2']:
 pts=sorted(map(tuple,r[name]['points']));assert len(pts)==len(set(pts))==18;ss=set(pts)
 for a,b in itertools.combinations(pts,2):assert tuple((-x-y)%3 for x,y in zip(a,b))not in ss
 hh=collections.Counter()
 for u in dirs:
  vals=[sum(a*b for a,b in zip(p,u))%3 for p in pts];hh[tuple(sorted([vals.count(i)for i in range(3)],reverse=True))]+=1
 assert hh=={(8,5,5):9,(6,6,6):4,(8,8,2):9,(7,7,4):18}
 z[name]={'points':pts,'point_sha256':hashlib.sha256(json.dumps(pts,separators=(',',':')).encode()).hexdigest(),'types':[list(t)for t in sorted(hh)],'histogram':[hh[t]for t in sorted(hh)],'three_counts':[0,0,9],'pair_checks':153,'directions':40,'source':'Root independent primaryFigure40/42 transcription; identity belongs to publishedfigures.','root_input_sha256':hashlib.sha256(rpath.read_bytes()).hexdigest(),'root_input_relative_path':'../../root_audit/882_points_independent.json'}
assert len(z)==20
(W/'all20_points_histograms.json').write_text(json.dumps(z,indent=2)+'\n')
groups={}
for name,h in z.items():
 sig=tuple(zip(map(tuple,h['types']),h['histogram']));groups.setdefault(sig,[]).append(name)
ST=[{'id':i,'classes':ns,'types':[list(t)for t,n in sig],'histogram':[n for t,n in sig],'partial':[dict(sig).get(t,0)for t in [(9,7,2),(9,6,3),(8,8,2)]]}for i,(sig,ns)in enumerate(sorted(groups.items()))]
(W/'full18_states.json').write_text(json.dumps(ST,indent=2)+'\n')
cov=json.loads((W.parent/'h9/state_coverage.json').read_text())['branches'];counts=[]
for b in cov:
 n=1
 for t in b['state18']:
  if t is not None:n*=sum(h['partial']==t for h in ST)
 counts.append(n)
print('PASS20classes',len(ST),'distincthistograms','full41plannedbranches',sum(counts),'perpartial',dict(collections.Counter(tuple(h['partial'])for h in ST)))
(W/'input_check.json').write_text(json.dumps({'classes':20,'distinct_histograms':len(ST),'pair_checks':20*153,'directions_per_cap':40,'planned_full41_branches':sum(counts),'source_cover':'Accepted publishedcomplete20class18classification; rootfigureidentity+ourpointchecks; remaining18staticcodesawaitrootindependentparse'},indent=2)+'\n')
