from discover import *
from minimum import REG
out=json.loads((W/'certificates.json').read_text());records=[];ban=SEEDS[:]
for si,stage in enumerate(out['stages']):
 for k,r in stage.items():records.append((f'ordinary_s{si}_{k}',V.parse_key(k),[-1]*3,False,ban[:],[],r))
 ban.extend(V.parse_key(k) for k in stage)
for k,r in out['extremal'].items():
 if 'branches' not in r:records.append(('minimum_'+k,V.parse_key(k),[-1]*3,True,ban[:],[],r))
 else:
  for j,rr in enumerate(r['branches']):
   if rr['certificate']:records.append((f'minimum_{k}_state'+''.join(map(str,rr['status'])),V.parse_key(k),rr['status'],True,ban[:],rr['extra_features'],rr['certificate']))
with (W/'verification_input.txt').open('w') as f:
 def line(*x):f.write(' '.join(map(str,x))+'\n')
 line(len(F6));[line(*t) for t in F6];line(len(COMP));[line(*t) for t in COMP];line(len(records))
 for name,key,state,ism,banned,extra,r in records:
  line(name,*key,*state,int(ism),int(bool(r.get('empty'))),r.get('K',0),r.get('forced',0),r.get('gap',0),len(banned));[line(*t) for t in banned];line(len(extra))
  for j,ex in extra:
   if ex in ('fam','small','label40'):
    kind=('fam','small','label40').index(ex);bound=(56,11*(112-key[j]),110*(112-key[j]))[kind];line(j,kind,bound)
   else:
    m,phi,bound=REG[ex];assert m==key[j];line(j,3,bound);line(*(phi.get((a,b,m-a-b),0) for a in range(46) for b in range(46)))
  line(len(r.get('coeff',[])),*r.get('coeff',[]))
print('records',len(records))
