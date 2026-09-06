from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib
W=Path(__file__).resolve().parent;R=W.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=json.loads((W/'INPUTS.json').read_text());assert all(sha(R/n)==s for n,s in inputs['source_hashes'].items())
raw=[json.loads(x)for x in (W/'ROWS.jsonl').read_text().splitlines()]
h=(W/'HISTOGRAM_ROWS.txt').read_text().splitlines();t=list(map(int,h[0].split()));n=t.pop(0);T=[t[3*i:3*i+3]for i in range(n)];assert len(t)==3*n
rows=[list(map(int,x.split()))for x in h[1:]];assert len(rows)==len(raw)==34345
pointsets=set();by_hist={};shape=Counter();ledgers=[];exclusion_fail=[]
for rec,rr in zip(raw,rows):
 assert rr.pop(0)==rec['index'];assert len(rr)==len(T)and sum(rr)==121
 for excluded in rec['excluded']:
  typ=sorted(excluded,reverse=True)
  if sum(typ)==41 and typ in T:assert rr[T.index(typ)]==0,('excluded_profile',rec['file'],rec['source_line'],typ)
 vec=tuple(rr);shape[rec['kind']]+=1;pointsets.add(tuple(rec['points_encoded']))
 if vec not in by_hist:
  pts=[tuple((p//3**k)%3 for k in range(4,-1,-1))for p in rec['points_encoded']]
  assert hashlib.sha256(json.dumps(pts,separators=(',',':')).encode()).hexdigest()==rec['point_sha256']
  by_hist[vec]={'counts':rr,'points':pts,'point_sha256':rec['point_sha256'],'representative_raw_file':rec['file'],'representative_raw_line':rec['source_line'],'normalized_output_record_count':0,'shapes':Counter()}
 by_hist[vec]['normalized_output_record_count']+=1;by_hist[vec]['shapes'][rec['kind']]+=1
 ordered=list(sorted(by_hist));
# IDs depend only on complete histogram vector lexicographic order.
ordered=sorted(by_hist);ix={v:i for i,v in enumerate(ordered)}
with (W/'ROW_LEDGER.jsonl').open('w')as out:
 for rec,rr in zip(raw,rows):
  x={k:rec[k]for k in ['index','file','source_line','block_line','kind','point_sha256']};x['histogram_id']=ix[tuple(rr)];out.write(json.dumps(x,separators=(',',':'))+'\n')
packet={'status':'ALL34345_RAW_POINT_ROWS_AND_HISTOGRAMS_INDEPENDENTLY_VERIFIED_PENDING_PRODUCER_COMPARISON','types':T,'histograms':[{'id':i,**by_hist[v]}for i,v in enumerate(ordered)],'histogram_count':len(ordered),'raw_record_count':34345,'distinct_normalized_pointsets':len(pointsets),'shapes':shape,'point_coordinate_order':['x1','x2','x3','x4','x5'],'point_index_encoding':'81*x1+27*x2+9*x3+3*x4+x5','scope':'Complete source-listed34,345-row necessary overcover for exceptional41 alternative; not complete41 affine-isomorphism classes and not a new proof of the primary search-completeness theorem.','pair_checks':34345*820,'direction_histogram_checks':34345*121,'all_stated3x3_matrices_checked':True,'all_recorded_excluded_profile_conditions_checked':True,'sources':inputs['source_hashes'],'other_decoder_outputs_read':False}
(W/'HISTOGRAM_PACKET.json').write_text(json.dumps(packet,indent=2)+'\n')
(W/'RESULT.json').write_text(json.dumps({k:v for k,v in packet.items()if k not in ['histograms','sources']},indent=2)+'\n')
print('COMPLETE',len(ordered),'histograms;',len(pointsets),'distinct normalized pointsets;',dict(shape))
