import importlib.util,json,itertools
from pathlib import Path
W=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('h9_readonly_full',W.parent/'h9/fullclass41.py');Q=importlib.util.module_from_spec(sp);sp.loader.exec_module(Q)
P=Q.P;H=P.H;np=H.np
ST=json.loads((W/'full18_states.json').read_text());assert len(ST)==17

def basebranches(key,ai):
 ix=np.full((21,21),-1,np.int64)
 for t,j in H.IX41.items():ix[t[:2]]=j
 top=H.E.make_top(20,41,np.array(H.BAD41+H.A41[:ai],np.int64).reshape(-1,3));ar=H.S40.raw_enum(*key,H.S40.D.A4,top,ix);ar=ar[H.S40.filter_clashes(ar,H.S40.PS)]
 cols=[j for j,N in enumerate(key)if N==18]
 for combo in itertools.product(ST,repeat=len(cols)):
  if key==(18,18,5)and tuple(tuple(h['partial'])for h in combo)not in P.B.ALLOWED_PAIRS:continue
  chosen=dict(zip(cols,combo));state18=[chosen[j]['partial']if j in chosen else None for j in range(3)];fullstate=[chosen[j]['id']if j in chosen else None for j in range(3)]
  mask=np.ones(len(ar),bool)
  for j,h in chosen.items():
   tt=ar[:,7+3*j:10+3*j];ok=np.zeros(len(ar),bool)
   for t,n in zip(h['types'],h['histogram']):
    if n:ok|=np.all(tt==t,axis=1)
   mask&=ok
  aa=ar[mask];z={'m':41,'key':key,'state18':state18,'full18_state':fullstate,'empty':not len(aa)}
  if not len(aa):yield z;continue
  X=aa[:,:7].copy();F=list(H.E.force(key,5));extra=[];pos=[]
  for j,N in enumerate(key):
   tt=aa[:,7+3*j:10+3*j]
   hh=H.H1920.get(str(N))if N!=18 else chosen[j]
   if hh is not None:
    for t,n in zip(hh['types'],hh['histogram']):
     X=np.c_[X,np.all(tt==t,axis=1).astype(np.int64)];F.append(n);extra.append((j,'full18'if N==18 else'exact4',t,n))
   if N==17:
    cover=[(9,8,0),(9,7,1),(8,8,1)];vals=-sum(np.all(tt==t,axis=1).astype(np.int64)for t in cover);X=np.c_[X,vals];pos.append(len(F));F.append(-1);extra.append((j,'direction_cover',cover,-1))
  F=np.array(F,np.int64);sc=np.maximum(np.max(abs(X-F/40),axis=0),1);z.update(X=X,F=F,W=(X-F/40)/sc,scale=sc,extra=extra,pos=pos,tops=aa[:,16:19].copy(),anchor=H.IX41[key]);yield z

def all_branches():
 out=[]
 for ai,key in enumerate(H.A41[:8]):
  bs=list(basebranches(key,ai));pairs=[]
  if key==(18,18,5):
   for c in P.IN['cover18185']:
    found=[b for b in bs if b['state18']==c['state18']];assert found;pairs +=[(b,c['class'])for b in found]
  elif ','.join(map(str,key))in P.IN['other_class_cover']:
   assert len(bs)==1;pairs=[(bs[0],cl)for cl in P.IN['other_class_cover'][','.join(map(str,key))]]
  else:pairs=[(b,'general')for b in bs]
  for base,cl in pairs:
   z=P.addclass(base,cl)
   if cl=='delta_minus1':
    for i,h in enumerate(Q.NH['Delta686_minus1_family']):out.append(Q.strengthen(z,h,'delta_hist_'+str(i)))
   elif cl=='41F':out.append(Q.strengthen(z,Q.NH['41F'],'41F_full'))
   else:out.append(z)
 assert len(out)==136
 (W/'state_coverage.json').write_text(json.dumps({'branches':[{'type':z['key'],'state18':z['state18'],'full18_state':z['full18_state'],'class41':z['class41'],'empty':z['empty'],'count':0 if z['empty']else len(z['X'])}for z in out]},indent=2)+'\n')
 return out
