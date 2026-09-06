import importlib.util,json,copy
from pathlib import Path
W=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('h8_readonly_class',W.parent/'h8/class41.py');P=importlib.util.module_from_spec(sp);sp.loader.exec_module(P)
np=P.np;H=P.H;NH=json.loads((W/'named_histograms.json').read_text())
def strengthen(z,h,name):
 z=copy.deepcopy(z);z['class41']=name
 if z['empty']:return z
 hh={tuple(t):n for t,n in zip(h['types'],h['histogram'])if n};z['whole_histogram']=hh
 if z['key']not in hh:z['empty']=True;return z
 ids=[H.IX41[t]for t in hh];mask=np.isin(z['tops'],ids).all(axis=1);z['X']=z['X'][mask];z['tops']=z['tops'][mask]
 if not len(z['X']):z['empty']=True;return z
 for t,n in hh.items():
  vv=(z['tops']==H.IX41[t]).sum(axis=1);bd=n-int(z['key']==t);z['X']=np.c_[z['X'],vv];z['F']=np.r_[z['F'],bd];z['extra'].append((-1,'whole41_group',[list(t)],bd))
 z['scale']=np.maximum(np.max(abs(z['X']-z['F']/40),axis=0),1);z['W']=(z['X']-z['F']/40)/z['scale'];return z

def all_branches():
 out=[]
 for ai,key in enumerate(H.A41[:8]):
  bs=list(P.B.branches(key,ai))
  pairs=[]
  if key==(18,18,5):
   for c in P.IN['cover18185']:
    found=[b for b in bs if b['state18']==c['state18']];assert len(found)==1;pairs.append((found[0],c['class']))
  elif ','.join(map(str,key))in P.IN['other_class_cover']:
   assert len(bs)==1
   pairs=[(bs[0],cl)for cl in P.IN['other_class_cover'][','.join(map(str,key))]]
  else:pairs=[(b,'general')for b in bs]
  for base,cl in pairs:
   z=P.addclass(base,cl)
   if cl=='delta_minus1':
    for i,h in enumerate(NH['Delta686_minus1_family']):out.append(strengthen(z,h,'delta_hist_'+str(i)))
   elif cl=='41F':out.append(strengthen(z,NH['41F'],'41F_full'))
   else:out.append(z)
 assert len(out)==49
 (W/'state_coverage.json').write_text(json.dumps({'branches':[{'type':z['key'],'state18':z['state18'],'class41':z['class41'],'empty':z['empty'],'count':0 if z['empty']else len(z['X'])}for z in out]},indent=2)+'\n')
 return out
