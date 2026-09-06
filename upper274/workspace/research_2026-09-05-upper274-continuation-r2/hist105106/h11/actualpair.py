import importlib.util,json
from pathlib import Path
W=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('h10_readonly_full18',W.parent/'h10/full18model.py');B=importlib.util.module_from_spec(sp);sp.loader.exec_module(B)
IN=json.loads((W/'named_pair_input.json').read_text());ST=json.loads((W.parent/'h10/full18_states.json').read_text());ids={name:h['id']for h in ST for name in h['classes']};PAIR={cl:{tuple(ids[n]for n in ns)for ns in ps}for cl,ps in IN['named_pairs'].items()}
def all_branches():
 B.W=W
 allz=B.all_branches();out=[];removed=[]
 for z in allz:
  if z['key']==(18,18,5):
   cl='delta_minus1'if z['class41'].startswith('delta_hist_')else z['class41'];assert cl in PAIR
   pair=tuple(z['full18_state'][:2])
   if pair not in PAIR[cl]:removed.append({'type':z['key'],'class41':z['class41'],'full18_state':z['full18_state'],'reason':'PUBLISHED_NAMED_PAIR_MISMATCH'});continue
  out.append(z)
 assert len(out)==58,(len(allz),len(out),len(removed))
 (W/'state_coverage.json').write_text(json.dumps({'branches':[{'type':z['key'],'state18':z['state18'],'full18_state':z['full18_state'],'class41':z['class41'],'empty':z['empty'],'count':0 if z['empty']else len(z['X'])}for z in out],'literature_dominated_removed':removed,'allowed_histogram_pairs':{cl:[list(p)for p in sorted(ps)]for cl,ps in PAIR.items()}},indent=2)+'\n')
 return out
