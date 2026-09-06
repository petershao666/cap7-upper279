from pathlib import Path
import json
W=Path(__file__).resolve().parent;ROOT=W.parents[2];BASE=ROOT/'audit_2026-09-05_upper275/cap7_upper275';r=json.loads((W/'h3_result.json').read_text());C=json.loads((BASE/'baseline277/baseline278/certificate.json').read_text());a=json.loads((ROOT/'research_2026-09-05-capset-round1-r1/route_a/certificates.json').read_text())
parse=lambda s:tuple(map(int,s.split(',')))
OLD=[parse(k)for s in C['six_stages']for k in s];COMP=list(map(tuple,C['completion_seeds']))+[parse(k)for s in C['completion_stages']for k in s]
sub=lambda t:t[2]<=22 or(t[0]<=40 and t[1]<=36)
F6=OLD+[t for t in COMP if not sub(t)]
cl=json.loads((W/'clash_data.json').read_text());records=[]
SUP40=[(a,b,40-a-b)for a in range(21)for b in range(a+1)if 0<=40-a-b<=b]
H=r['histograms']
for m in (40,105):
 h=H[str(m)];phi=dict(zip(map(tuple,h['types']),h['phi']));refs={tuple(z['type']):z for z in h['inner']};anchors=SUP40 if m==40 else list(refs)
 for i,key in enumerate(anchors):
  z=refs.get(key);empty=z is None;extra=[]
  if z:
   for j,(col,kind,data,bd)in enumerate(z['extra']):
    if kind.startswith('exact'):p={tuple(data):1};sg=0
    else:u=r['upper5'][data];p=dict(zip(map(tuple,u['types']),u['phi']));sg=1
    extra.append((col,z['coeff'][7+j],bd,sg,p))
   for col in z.get('theta40_columns',[]):extra.append((col,1,H['40']['bound'],1,dict(zip(map(tuple,H['40']['types']),H['40']['phi']))))
  ban=anchors[:i]if m==40 else OLD+COMP+anchors[:i];coeff=z['coeff'][:7]if z else[0]*7;U=0
  if z:
   keyF=[((3**((5 if m==40 else 6)-2)-1)//2)*key[0]*key[1]*key[2]]
   from math import comb
   n=5 if m==40 else 6
   for v in key:keyF.extend([3**(n-2)*comb(v,2),3**(n-3)*comb(v,3)])
   U=sum(x*y for x,y in zip(coeff,keyF))+sum(q*bd for col,q,bd,sg,p in extra)
  records.append((f'hist{m}_{key[0]}_{key[1]}_{key[2]}',5 if m==40 else 6,key,0,empty,z['K']if z else 0,U,z['bound']if z else 0,ban,coeff,extra,phi))
seeds=[(112,112,29),(112,111,35),(112,110,45),(111,111,45),(112,109,51),(111,110,51)]
ban=seeds+[parse(k)for st in a['stages']for k in st]
for z in r['outer']:
 key=tuple(z['type']);extra=[(j,1,H[str(key[j])]['bound'],1,dict(zip(map(tuple,H[str(key[j])]['types']),H[str(key[j])]['phi'])))for j in (0,1)]
 records.append(('outer105_105_65',7,key,1,False,z['K'],z['forced'],z['gap'],ban,z['coeff'],extra,None))
with(W/'verify_input.txt').open('w')as f:
 def line(*x):f.write(' '.join(map(str,x))+'\n')
 line(len(F6));[line(*t)for t in F6];line(len(COMP));[line(*t)for t in COMP];line(len(cl['patterns']))
 for p in cl['patterns']:
  x=[-1]*9
  for j,v in p:x[j]=v
  line(*x)
 line(len(records))
 for name,n,key,ism,empty,K,U,bd,ban,q,ex,phi in records:
  line(name,n,*key,ism,int(empty),K,U,bd,len(ban));[line(*t)for t in ban];line(*q);line(len(ex))
  for col,qq,bb,sg,ph in ex:
   line(col,qq,bb,sg);lookup={(t[0],t[1]):v for t,v in ph.items()};line(*(lookup.get((a,b),0)for a in range(46)for b in range(46)))
  line(int(phi is not None))
  if phi is not None:
   lookup={(t[0],t[1]):v for t,v in phi.items()};line(*(lookup.get((a,b),0)for a in range(113)for b in range(113)))
print('records',len(records))
