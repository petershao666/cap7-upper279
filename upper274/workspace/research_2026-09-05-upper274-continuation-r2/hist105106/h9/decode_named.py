from pathlib import Path
import re,itertools,json,hashlib,collections,time
W=Path(__file__).resolve().parent;src=W/'Dim5_41_CapsFoundArguments.txt';lines=src.read_text().splitlines();sha=hashlib.sha256(src.read_bytes()).hexdigest()
SYM={'+':['*.*','.*.','*.*'],'x':['.*.','***','.*.'],'|':['*.*','***','*.*'],'-':['***','.*.','***'],'.':['***','*.*','***'],'o':['***','***','***']}
def compact(ln):
 raw=[lines[i-1]for i in ln];diag=[]
 for row in raw:
  syms=''.join(row.split());assert len(syms)==9
  for j in range(3):diag.append(''.join(SYM[c][j]for c in syms))
 return raw,diag

def expanded(ln,right=False):
 raw=[lines[i-1].split('\t')[-1]if right else lines[i-1]for i in ln];diag=[''.join(s.split())for s in raw];assert all(len(s)==27 and set(s)<=set('*.')for s in diag);return raw,diag
DOM={'41F':([66,67,68],False,True),'Delta686':([15,16,17],False,True),'41H':([142,143,144,146,147,148,150,151,152],False,False),'41I':([155,156,157,159,160,161,163,164,165],False,False),'41G':([284,285,286,288,289,290,292,293,294],True,False)}
DIRS=[u for u in itertools.product(range(3),repeat=5)if any(u)and next(x for x in u if x)==1];assert len(DIRS)==121

def hist(pts):
 out=collections.Counter()
 for u in DIRS:
  cc=[0,0,0]
  for p in pts:cc[sum(a*b for a,b in zip(u,p))%3]+=1
  out[tuple(sorted(cc,reverse=True))]+=1
 return out

def verify(pts):
 ss=set(pts);assert len(ss)==len(pts);blocked=set()
 for p,q in itertools.combinations(pts,2):
  z=tuple((-a-b)%3 for a,b in zip(p,q));assert z not in ss,(p,q,z);blocked.add(z)
 return {'pairs_checked':len(pts)*(len(pts)-1)//2,'complete':len(ss|blocked)==243,'unblocked_points':243-len(ss|blocked)}
NP={};NH={};expect={'41F':[0,8,3],'41G':[0,5,5],'41H':[0,4,5],'41I':[0,2,10]};types3=[(18,18,5),(18,17,6),(18,16,7)]
for name,(ln,right,small)in DOM.items():
 raw,diag=compact(ln)if small else expanded(ln,right)
 pts=sorted((r//3,r%3,c//9,(c//3)%3,c%3)for r,row in enumerate(diag)for c,ch in enumerate(row)if ch=='.');assert len(pts)==(42 if name=='Delta686'else 41)
 chk=verify(pts);hh=hist(pts)
 if name in expect:assert[hh[t]for t in types3]==expect[name],(name,hh)
 else:
  exp={(20,16,6):3,(18,18,6):4,(18,17,7):18,(18,12,12):6,(16,15,11):24,(16,14,12):36,(15,15,12):3,(14,14,14):27};assert hh==exp
 b=json.dumps(pts,separators=(',',':')).encode();NP[name]={'source_url':'https://arxiv.org/src/2206.09719v1/anc/Dim5_41_CapsFoundArguments.txt','source_sha256':sha,'source_lines_one_based':ln,'right_hand_diagram':right,'compact_symbols':small,'raw_diagram':raw,'expanded_rows':diag,'points':pts,'point_sha256':hashlib.sha256(b).hexdigest(),'verification':chk}
 NH[name]={'point_sha256':NP[name]['point_sha256'],'types':[list(t)for t in sorted(hh)],'histogram':[hh[t]for t in sorted(hh)],'directions':121,'size':len(pts)}
 print(name,len(pts),chk,'types',len(hh),NP[name]['point_sha256'])
pts=NP['Delta686']['points'];dels=collections.defaultdict(list)
for j in range(42):
 h=hist(pts[:j]+pts[j+1:]);dels[tuple(sorted(h.items()))].append(j)
NH['Delta686_minus1_family']=[{'types':[list(t)for t,n in h],'histogram':[n for t,n in h],'deleted_point_indices':js}for h,js in sorted(dels.items())]
(W/'named_points.json').write_text(json.dumps(NP,indent=2)+'\n');(W/'named_histograms.json').write_text(json.dumps(NH,indent=2)+'\n')
print('Delta_one_deletion_histogram_count',len(dels))
