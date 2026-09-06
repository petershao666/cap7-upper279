from pathlib import Path
import json, hashlib, itertools
W=Path(__file__).resolve().parent;R=W.parents[1];P=R/'root_potential/complete20200';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=P/'HISTOGRAMS.json';assert sha(p)=='f3278815900918e48c0af51b7d88c8907c006b5451cd35fe52ee4b6ce198013d';d=json.loads(p.read_text())
lines=(W/'root_histograms.txt').read_text().splitlines();types=[tuple(map(int,t.split(',')))for t in lines[0].split()];assert [list(t)for t in types]==d['types'];rows=[line.split()for line in lines[1:]];root={tuple(map(int,r[:44])):int(r[44])for r in rows}
assert len(root)==8 and sum(root.values())==682344;other={tuple(h['counts']):h['normalized_B_frequency']for h in d['histograms']};assert root==other
norms=[v for v in itertools.product(range(3),repeat=5)if any(v)and next(x for x in v if x)==1];assert len(norms)==121;pairs=0
for rec in d['histograms']:
 pts=list(map(tuple,rec['points']));ss=set(pts);assert len(ss)==len(pts)==40 and all(len(t)==5 and all(x in range(3)for x in t)for t in pts)
 for a,b in itertools.combinations(pts,2):assert tuple((-x-y)%3 for x,y in zip(a,b))not in ss;pairs+=1
 hist={}
 for v in norms:
  bins=[0,0,0]
  for x in pts:bins[sum(a*b for a,b in zip(v,x))%3]+=1
  t=tuple(sorted(bins,reverse=True));hist[t]=hist.get(t,0)+1
 assert [hist.get(t,0)for t in types]==rec['counts']
 k=hist.get((18,18,4),0);assert k in [0,1,2,3,4,5,6,10]
 expected={(20,20,0):1,(18,18,4):k,(18,11,11):2*k,(16,12,12):20+k,(14,14,12):40+2*k,(15,15,10):20-2*k,(17,15,8):40-4*k}
 assert hist=={t:n for t,n in expected.items()if n}
report={'status':'EXACT_COMPLETE20200_CENSUS_PASS_BUT_LINEAR_SUPPORT_ALREADY_DOMINATED','histograms':8,'parameters':[0,1,2,3,4,5,6,10],'normalized_caps':682344,'root_all_pairchecks':532228320,'producer_all_pairchecks':532228320,'root_producer_representative_pairchecks':pairs,'source_sha256':sha(p),'root_frozen_sha256':sha(W/'ROOT_FROZEN.json'),'producer_frozen_sha256':sha(P/'FROZEN.json'),'scope':'Complete40cap20200directionfamily, notall40caps. DifferentcanonicalA anddirectionkernels, sharedaccepted20catalogue.','linear_status':'STOP_LINEAR_DUPLICATE: explicitold20-indicator dual alreadyproves bothendpointsupport; k7..9gap gives no linearTheta40strengthening. Seecompatibility/complete20200_dominance/PROOF.md.','novelty':'No publication-priority or newglobalbound claim.'}
(W/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS8exacthistograms/frequencies,6240producerpairs;STOP_LINEAR_DUPLICATE')
