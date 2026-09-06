from pathlib import Path
import itertools,json,hashlib,math
W=Path(__file__).resolve().parent
z=json.loads((W/'histograms17.json').read_text());types=list(map(tuple,z['types']));normals=[v for v in itertools.product(range(3),repeat=4)if any(v)and next(x for x in v if x)==1]
assert len(normals)==40 and len(types)==13 and len(z['histograms'])==102
rows=[];seen=set();paircount=0
for h in z['histograms']:
 ps=list(map(tuple,h['points']));S=set(ps);assert len(S)==17
 assert sorted(p[0]+3*p[1]+9*p[2]+27*p[3]for p in ps)==h['point_ids']
 for p,q in itertools.combinations(ps,2):assert tuple((-a-b)%3 for a,b in zip(p,q))not in S;paircount+=1
 hist={t:0 for t in types}
 for v in normals:
  c=[0,0,0]
  for p in ps:c[sum(a*b for a,b in zip(p,v))%3]+=1
  hist[tuple(sorted(c,reverse=True))]+=1
 counts=[hist[t]for t in types];assert counts==h['counts']
 assert sum(counts)==40
 assert sum(n*(a*b+a*c+b*c)for(a,b,c),n in zip(types,counts))==27*math.comb(17,2)
 assert sum(n*a*b*c for(a,b,c),n in zip(types,counts))==9*math.comb(17,3)
 key=tuple(counts);assert key not in seen;seen.add(key);rows.append({'histogram_id':h['id'],'point_count':17,'directions_checked':40,'pairs_checked':136})
parent=W.parents[1]/'root_potential'
compare=[]
for n in[8,9]:
 mine=(W/f'actual{n}_masks.txt').read_bytes();other=(parent/f'h17_actual_caps{n}.txt').read_bytes();assert mine==other
 compare.append({'size':n,'count':len(mine.splitlines()),'sha256':hashlib.sha256(mine).hexdigest(),'independent_inventory_exact_byte_match':True})
r={'status':'AUTHOR_REPRESENTATIVE_CHECK_PASS','independent_inventory_comparison':compare,'histogram_representatives':len(rows),'pair_checks':paircount,'histogram_checks':rows,'scope':'Separate Python point and histogram arithmetic checks for all102 representatives; complete generated-family coverage still requires independent root/P review.','histograms17_sha256':hashlib.sha256((W/'histograms17.json').read_bytes()).hexdigest()}
(W/'author_check.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k!='histogram_checks'},indent=2))
