from pathlib import Path
import json, hashlib, itertools, math
W=Path(__file__).resolve().parent;R=W.parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
H=R/'hist105106/h20_20201';P=R/'root_potential/complete20201'
assert sha(H/'histograms41.json')=='74c4e1c900b519edc1124dbb2bc49c04dddd1845bbbfd6de74baacf1e19b4011'
assert sha(P/'HISTOGRAMS.json')=='bd60eb3207e5ad3df90c551378be0e960ce96772297f0dc247ab713610c23484'
assert (H/'all20_masks.txt').read_bytes()==(P/'ALL20_MASKS.txt').read_bytes()
h=json.loads((H/'histograms41.json').read_text());p=json.loads((P/'HISTOGRAMS.json').read_text())
assert h['types']==p['types'];types=list(map(tuple,h['types']));assert len(types)==40
assert len(h['histograms'])==len(p['histograms'])==1 and h['histograms'][0]['counts']==p['histograms'][0]['counts']
expected={(14,14,13):40,(15,15,11):20,(17,12,12):20,(17,16,8):40,(20,20,1):1}
normals=[v for v in itertools.product(range(3),repeat=5)if any(v)and next(x for x in v if x)==1];assert len(normals)==121
pairs=0
for d in [h,p]:
 rec=d['histograms'][0];pts=list(map(tuple,rec['points']));ss=set(pts);assert len(pts)==len(ss)==41 and all(len(t)==5 and all(x in range(3)for x in t)for t in pts)
 for a,b in itertools.combinations(pts,2):assert tuple((-x-y)%3 for x,y in zip(a,b))not in ss;pairs+=1
 hist={}
 for v in normals:
  bins=[0,0,0]
  for x in pts:bins[sum(a*b for a,b in zip(v,x))%3]+=1
  t=tuple(sorted(bins,reverse=True));hist[t]=hist.get(t,0)+1
 assert hist==expected and [hist.get(t,0)for t in types]==rec['counts']
assert sum(expected.values())==121 and sum(n*(t[0]*t[1]+t[0]*t[2]+t[1]*t[2])for t,n in expected.items())==81*math.comb(41,2) and sum(n*math.prod(t)for t,n in expected.items())==27*math.comb(41,3)
report={'status':'COMPLETE_20201_FAMILY_EXACT_HISTOGRAM_INDEPENDENTLY_ACCEPTED','scope':'Every41cap inF3^5 admitting a20/20/1 direction, whether complete or not. Not the full41cap family.','centered20_caps':8424,'all20_caps':682344,'normalized41_caps_per_canonicalA':198,'histograms':1,'root_representative_pairs':pairs,'root_source_check':'../COMPLETE20201_SOURCE_CHECK.md','code_audit':'Root read both complete enumeration kernels: all59049 ten-variable coefficient vectors, cap-checked zero masks, all81 translations, no presumedcount filter, exactdisjointness and all121directions. Mathematicalcoverage uses publishedaffine20capuniqueness and the proved singletonshear.','input_hashes':{str(f.relative_to(R)):sha(f)for f in [H/'FROZEN.json',P/'FROZEN.json',P/'H_COMPARISON.json',H/'all20_masks.txt',H/'histograms41.json',P/'HISTOGRAMS.json',H/'enumerate.cpp',P/'enumerate_polynomials.cpp']},'shared_dependencies':'Publishedaffine20cap uniqueness; finitefieldmath. Different canonicalquadraticcaps, monomial/matrix order and kernels; no generatedinputsharing. H saw P summarycounts after codecompletion but before execution; this is not a blindtwo-runcomparison. P froze before H outputs, root directpointscheck uses neither kernel.','novelty':'No literaturepriority or7Dglobalbound claim.'}
(W/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
accepted={'status':report['status'],'types':h['types'],'histograms':[h['histograms'][0]['counts']],'scope':report['scope'],'source_verification_sha256':sha(W/'VERIFICATION.json'),'point_representative':str((H/'REPRESENTATIVE_POINTS.tsv').resolve())}
(W/'ACCEPTED_HISTOGRAM.json').write_text(json.dumps(accepted,indent=2)+'\n')
print('PASS all20cataloguematch;1640rootrepresentativepairs;unique20201histogram',sha(W/'ACCEPTED_HISTOGRAM.json'))
