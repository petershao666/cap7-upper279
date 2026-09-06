from pathlib import Path
import json,hashlib
w=Path(__file__).resolve().parent;r=w.parents[1]
f=json.loads((w/'TERMINAL_FROZEN.json').read_text());z=json.loads((w/'RESULT.json').read_text());inp=json.loads((w/'INPUTS.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(w/'RESULT.json')==f['result_sha256']
for n,s in f['source_hashes'].items():assert sha(w/n)==s,(n,s)
for n,s in inp['source_hashes'].items():assert sha(r/n)==s,(n,s)
assert z['claim']=='NO_NEW_MATH'and z['optimizer_calls']==0
assert [v['scale']for v in z['repairs']]==[10**i for i in range(10,15)]
assert z['outer_count']==2460769
assert sum(c['count']for c in z['counts'])==109365+94242
for v in z['repairs']:
 assert v['status']=='EXACT_COMPLETE_SIGNED_GAP'
 assert v['integer_product_ceiling']<8*10**18
 assert len(v['outer'])==1
 o=v['outer'][0];assert o['gap']==364*o['K']-o['forced']<0
 assert v['gaps']==[o['gap']]
assert z['elapsed']<600
print('PASS_FROZEN_SUMMARY_ARITHMETIC_AND_INPUT_HASHES; not an independent domain replay')
