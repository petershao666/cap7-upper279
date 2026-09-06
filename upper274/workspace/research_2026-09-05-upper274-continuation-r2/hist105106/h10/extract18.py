from pathlib import Path
import re,json,hashlib,itertools,collections
W=Path(__file__).resolve().parent;src=W.parent/'h9/SetDim5Cap43_9General_ExclPtCounts.java';raw=src.read_bytes();s=raw.decode();SHA=hashlib.sha256(raw).hexdigest()
NAMES=['990A1','990A2','990A3','990B']+['981'+c for c in 'ABCDEFGHIJ']+['972A','963A','963B','954A'];assert len(NAMES)==18
pat=r'if\(code\.equals\("([^"\n]+)"\)\)\s*return\s*("[^"\n]*(?:\n[^"\n]*)*"(?:\s*\+\s*"[^"]*")*)\s*;'
# Parse only literal concatenations; never evaluate Java or source expressions.
pat=r'if\(code\.equals\("([^"\n]+)"\)\)\s*return\s*("[^"]*"(?:\s*\+\s*"[^"]*")*)\s*;'
DIRS=[u for u in itertools.product(range(3),repeat=4)if any(u)and next(x for x in u if x)==1];assert len(DIRS)==40
H18=json.loads((W.parents[1]/'root_audit/h18_input.json').read_text());EXP={r['type']:r['counts']for r in H18['rows']}
OUT={}
for mt in re.finditer(pat,s):
 name,expr=mt.groups()
 if name not in NAMES or name in OUT:continue
 st=''.join(re.findall(r'"([^"]*)"',expr));pts=sorted(tuple(map(int,p.split(',')))for p in re.split('[;:]',st)if p)
 assert len(pts)==18 and len(set(pts))==18 and all(len(p)==4 and set(p)<={0,1,2}for p in pts)
 ss=set(pts)
 for a,b in itertools.combinations(pts,2):assert tuple((-x-y)%3 for x,y in zip(a,b))not in ss
 hh=collections.Counter()
 for u in DIRS:
  ct=collections.Counter(sum(x*y for x,y in zip(p,u))%3 for p in pts);hh[tuple(sorted((ct[i]for i in range(3)),reverse=True))]+=1
 vals=[hh[tuple(t)]for t in H18['statistics']];assert vals==EXP[name],(name,vals,EXP[name])
 OUT[name]={'source_url':'https://arxiv.org/src/2206.09719v1/anc/JavaPrograms/SetDim5Cap43Flats3/src/setDim5Cap43_9General/SetDim5Cap43_9General_ExclPtCounts.java','source_sha256':SHA,'source_lines_one_based':[s.count('\n',0,mt.start())+1,s.count('\n',0,mt.end())+1],'raw_literal_concatenation':expr,'joined_coordinate_string':st,'points':pts,'point_sha256':hashlib.sha256(json.dumps(pts,separators=(',',':')).encode()).hexdigest(),'types':[list(t)for t in sorted(hh)],'histogram':[hh[t]for t in sorted(hh)],'three_counts':vals,'pair_checks':153,'directions':40}
assert set(OUT)==set(NAMES),(set(NAMES)-set(OUT))
(W/'coded18_points_histograms.json').write_text(json.dumps(OUT,indent=2)+'\n')
print('PASS',len(OUT),'classes;',len({tuple(zip(map(tuple,h['types']),h['histogram']))for h in OUT.values()}),'distincthistograms;',sum(h['pair_checks']for h in OUT.values()),'pairs')
for name,h in OUT.items():print(name,h['source_lines_one_based'],len(h['types']),h['three_counts'],h['point_sha256'])
