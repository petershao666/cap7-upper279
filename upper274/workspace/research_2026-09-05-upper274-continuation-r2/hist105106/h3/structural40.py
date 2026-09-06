import sys,json
from pathlib import Path
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W.parent))
import depth40 as D
from clashes import PATTERNS
np=D.np
HIST=json.loads((W/'hist19_20.json').read_text())
src=(D.O.B/'baseline277/research/nested108.py').read_text();code=src[src.index('@njit(cache=True)'):src.index('\ndef inner_data')].replace('@njit(cache=True)','@njit').replace('range(21)','range(10)').replace('<=20','<=9').replace('x>45 or y>45','x>20 or y>20')
code=code.replace('tt[0],tt[1],tt[2]))','tt[0],tt[1],tt[2],a[0],a[1],a[2],b[0],b[1],b[2],c[0],c[1],c[2]))').replace('(len(rows),19)','(len(rows),28)').replace('range(19)','range(28)')
scope={'njit':D.O.njit,'np':np,'e2':D.E.e2,'sorted3':D.E.sorted3};exec(code,scope);raw_enum=scope['inner_enum']
PS=np.full((len(PATTERNS),9),-1,np.int32)
for j,p in enumerate(PATTERNS):
 for ix,val in p:PS[j,ix]=val
@D.O.njit
def filter_clashes(ar,patterns):
 keep=np.ones(len(ar),np.bool_)
 for r in range(len(ar)):
  x=ar[r,19:28]
  flat=(x[0],x[3],x[6],x[1],x[4],x[7],x[2],x[5],x[8])
  for pat in patterns:
   match=True
   for j in range(9):
    if pat[j]>=0 and flat[j]!=pat[j]:match=False;break
   if match:keep[r]=False;break
 return keep
COUNTS=[]
def build(key,i):
 index=np.full((21,21),-1,np.int64)
 for t,j in D.IX40.items():index[t[:2]]=j
 top=D.E.make_top(20,40,np.array(D.SUP40[:i],np.int64).reshape(-1,3));ar=raw_enum(*key,D.A4,top,index);before=len(ar);ar=ar[filter_clashes(ar,PS)];COUNTS.append(dict(type=key,before=before,after=len(ar),removed=before-len(ar)))
 (W/'enumeration_counts.json').write_text(json.dumps(COUNTS,indent=2)+'\n')
 X=ar[:,:7].copy();F=list(D.E.force(key,5));extra=[]
 for j,N in enumerate(key):
  if str(N) not in HIST:continue
  h=HIST[str(N)]
  for t,n in zip(h['types'],h['histogram']):
   X=np.c_[X,np.all(ar[:,7+3*j:10+3*j]==t,axis=1).astype(np.int64)];F.append(n);extra.append((j,'exact4',t,n))
 F=np.array(F,np.int64)
 if not len(X):return dict(m=40,key=key,empty=True)
 sc=np.maximum(np.max(abs(X-F/40),axis=0),1);wv=(X-F/40)/sc
 return dict(m=40,key=key,X=X,F=F,W=wv,scale=sc,extra=extra,pos=[],tops=ar[:,16:19].copy(),anchor=D.IX40[key],empty=False)
if __name__=='__main__':
 for i,t in enumerate(D.SUP40):build(t,i)
 print('TOTAL',sum(x['before']for x in COUNTS),sum(x['after']for x in COUNTS),'REMOVED',sum(x['removed']for x in COUNTS),flush=True)
