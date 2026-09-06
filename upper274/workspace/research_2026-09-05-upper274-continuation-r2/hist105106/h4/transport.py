from pathlib import Path
import json,math,itertools,hashlib
W=Path(__file__).resolve().parent
r=json.loads((W.parent/'h3/h3_result.json').read_text());h=r['histograms']['40'];PHI=dict(zip(map(tuple,h['types']),h['phi']));B=h['bound'];res={}
for m in [40,41,42]:
 T=[(a,b,m-a-b)for a in range(21)for b in range(a+1)if 0<=m-a-b<=b]
 values=[];total_terms=0
 for t in T:
  val=0;count=0
  for a in range(t[0]+1):
   for b in range(t[1]+1):
    c=40-a-b
    if 0<=c<=t[2]:
     w=math.comb(t[0],a)*math.comb(t[1],b)*math.comb(t[2],c);val+=w*PHI[tuple(sorted((a,b,c),reverse=True))];count+=w;total_terms+=1
  assert count==math.comb(m,40)
  values.append(val)
 res[str(m)]=dict(m=m,types=T,phi=values,bound=math.comb(m,40)*B,terms=total_terms,subcap_count=math.comb(m,40))
print([(m,len(h['types']),h['bound'],h['terms'])for m,h in res.items()])
(W/'transport_tables.json').write_text(json.dumps(res,indent=2)+'\n')
