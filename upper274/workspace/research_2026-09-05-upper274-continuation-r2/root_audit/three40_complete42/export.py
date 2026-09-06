"""Pure-data transcription and mathematical support checks, no research imports."""
from pathlib import Path
from collections import Counter
import hashlib,json,math
W=Path(__file__).resolve().parent;R=W.parent.parent;B=R.parent/'audit_2026-09-05_upper275/cap7_upper275'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
activation=read(W/'ACTIVATION.json')
cp=R/activation['certificate_path']
assert sha(cp)==activation['certificate_sha256']
d=read(cp);f=read(B/'baseline277/baseline278/certificate.json')
old=[list(map(int,k.split(',')))for stage in f['six_stages']for k in stage]
comp=f['completion_seeds']+[list(map(int,k.split(',')))for stage in f['completion_stages']for k in stage]
base=read(R.parent/'research_2026-09-05-capset-round1-r1/route_a/certificates.json')
ban=base['seeds']+[[112,109,51],[111,110,51]]+[list(map(int,k.split(',')))for stage in base['stages']for k in stage]
assert len(set(map(tuple,ban)))==18 and d['claim']=='CANDIDATE_EXACT_CERTIFICATE' and d['target']==[106,106,63]
tab=read(R/'hist105106/h13/table1_input_v2.json');assert d['table1']==tab
states=read(R/'hist105106/h10/full18_states.json');assert states==d['full18_states']
labels=tab['label_order'];cap=tab['symmetric_capacity_matrix'];idx={s:i for i,s in enumerate(labels)}
pair=[(i,j)for i,s in enumerate(states)for j,t in enumerate(states)
      if max(cap[idx[a]][idx[b]]for a in s['classes']for b in t['classes'])>=4]
cond=[i for i,s in enumerate(states)if max(cap[idx[a]][21]for a in s['classes'])>=2]
assert len(pair)==267 and len(cond)==16
assert pair==list(map(tuple,d['histogram_pair_capacity']['allowed_18184_ordered_pairs']))
assert cond==d['histogram_pair_capacity']['allowed_20182_full18_states']
T18=list(map(tuple,d['conditional_types']))
hist18=[dict(zip(map(tuple,s['types']),s['histogram']))for s in states]
families={18:hist18}
for n,file in [(16,'root_audit/actual16/ACCEPTED_HISTOGRAMS.json'),(17,'root_audit/actual17/ACCEPTED_HISTOGRAMS.json'),(41,'root_audit/complete41/ACCEPTED_HISTOGRAMS.json')]:
    p=read(R/file); hs=p['histograms']
    families[n]=[dict(zip(map(tuple,p['types']),z['counts']if isinstance(z,dict)else z))for z in hs]
families[42]=[dict(zip(map(tuple,f['spectrum5']['42']['types']),h)) for h in f['spectrum5']['42']['spectra']]
TIERS=[400,401,402]
PARENTS={400:[43,40,23],401:[44,40,22],402:[45,40,21]}
for m in TIERS:
    assert d['tier_mapping'][str(m)]==dict(mathematical_size=40,parent=PARENTS[m],physical_column=1)
funcs=[];names={}
def function(name,n,types,phi,bound):
    assert name not in names and len(types)==len(phi)
    assert all(type(v)is int for v in phi)and type(bound)is int
    assert len(set(map(tuple,types)))==len(types)
    names[name]=len(funcs);funcs.append((n,bound,types,phi));return names[name]
def dot(h,types,phi):
    p=dict(zip(map(tuple,types),phi));assert set(h)<=set(p)
    return sum(v*p[t]for t,v in h.items())
max_checks=0
for name,z in d['local_supports'].items():
    vals=[dot(h,z['types'],z['phi'])for h in families[z['m']]]
    assert max(vals)==z['bound'];max_checks+=len(vals)
    function(name,z['m'],z['types'],z['phi'],z['bound'])
for name,phi in d['conditional_functions'].items():
    function(name,18,d['conditional_types'],phi,0)
values={name:[dot(h,T18,phi)for h in hist18]for name,phi in d['conditional_functions'].items()}
for m in TIERS:
    left,right,conditional=(f't{m}_left18',f't{m}_right18',f't{m}_cond18')
    assert max(values[left][i]+values[right][j]for i,j in pair)==d['conditional_bounds'][f't{m}_pair18']
    assert max(values[conditional][i]for i in cond)==d['conditional_bounds'][conditional]
    max_checks+=len(pair)+len(cond)
assert max_checks==15885
cover={(9,8,0),(9,7,1),(8,8,1)}
assert all(sum(h.get(t,0)for t in cover)>=1 for h in families[17])
hist19_20=read(R/'hist105106/h3/hist19_20.json')
fixed_packet=read(R/'hist105106/h23_r105_transfer/FIXED_INPUTS.json')
assert d['fixed6']==fixed_packet
fixed=fixed_packet['functions'];assert len(fixed)==6 and all(z['size']==106 for z in fixed)
for z in fixed:function('fixed_'+z['id'],z['size'],z['types'],z['values'],z['bound'])
for m in TIERS+[106]:
    z=d['histograms'][str(m)];n=106 if m==106 else 40
    assert z['mathematical_size']==n
    function('main_'+str(m),n,z['types'],z['phi'],z['bound'])
patterns=read(R/'hist105106/h3/clash_data.json')['patterns']
types40=sorted(((a,b,40-a-b)for a in range(21)for b in range(a+1)if 0<=40-a-b<=b),reverse=True)
cases=[]
for m in TIERS:
    hz=d['histograms'][str(m)]
    assert list(map(tuple,hz['types']))==list(reversed(types40))
    assert hz['tier_parent']==PARENTS[m]
    records={tuple(z['type']):z for z in hz['inner']}
    assert set(records)==set(types40[:-1]) and len(hz['inner'])==43
    for i,key in enumerate(types40):
        rec=records.get(key);ex=[];terms=[];tb=0
        if rec:
            for col,kind,arg,bd in rec['extra']:
                if kind=='exact4':
                    src=hist19_20[str(key[col])];assert bd==src['histogram'][src['types'].index(arg)]
                    ex.append((col,0,arg,-1,bd))
                else:
                    assert kind=='direction_cover' and key[col]==17 and set(map(tuple,arg))==cover and bd==-1
                    ex.append((col,2,[0,0,0],-1,bd))
            assert not rec['dependencies']
            for term in rec['local_supports']:
                z=d['local_supports'][term['id']];j=term['column']
                assert term['coefficient']==1 and z['column']==j and z['anchor']==list(key) and z['m']==key[j]
                assert z['case_dimension_size']==m
                terms.append((j,names[term['id']]));tb+=z['bound']
            for term in rec['conditional_dependencies']:
                assert term['coefficient']==1 and term['function'].startswith(f't{m}_')
                terms.append((term['column'],names[term['function']]))
            cb=rec['conditional_bound']
            if cb:
                assert (key,cb) in [((18,18,4),f't{m}_pair18'),((20,18,2),f't{m}_cond18')]
                tb+=d['conditional_bounds'][cb]
        cases.append((40,names['main_'+str(m)],key,types40[:i],rec,ex,terms,tb))
assert types40[-1]==(14,13,13)
for rec in d['outer']:
    assert rec['type']==[106,106,63] and len(rec['coeff'])==19
    assert rec['fixed_functions']==[dict(z,column=j) for j in [0,1] for z in fixed]
    ex=[]
    for col in [0,1]:
        for z in fixed:ex.append((col,1,[0,0,0],names['fixed_'+z['id']],z['bound']))
    assert len(ex)==12
    terms=[(j,names['main_106']) for j in [0,1]]
    cases.append((275,-1,tuple(rec['type']),ban,rec,ex,terms,2*d['histograms']['106']['bound']))
assert len(cases)==133
lines=[]
def line(*v):lines.append(' '.join(map(str,v)))
line(len(old),len(comp),len(funcs),len(patterns),len(cases),names['main_400'])
for t in old+comp:line(*t)
for n in [42,43,44,45]:
    ts=f['spectrum5'][str(n)]['types'];line(n,len(ts))
    for t in ts:line(*t)
for n,b,ts,p in funcs:
    line(n,b,len(ts))
    for t,v in zip(ts,p):line(*t,v)
line(len(T18))
for t in T18:line(*t)
for p in patterns:
    row=[-1]*9
    for i,v in p:row[i]=v
    line(*row)
for n,primary,key,bad,rec,ex,terms,tb in cases:
    rec=rec or {};q=rec.get('coeff',[])
    assert len(q)==0 or len(q)==7+len(ex)
    line(n,primary,*key,int(not rec),len(bad),len(ex),len(terms),len(q),rec.get('count',0),tb)
    for t in bad:line(*t)
    for j,k,t,i,b in ex:line(j,k,*t,i,b)
    for j,i in terms:line(j,i)
    line(*q);line(rec.get('K',0),rec.get('bound',rec.get('forced',0)),rec.get('gap',0))
(W/'input.txt').write_text('\n'.join(lines)+'\n')
result={'status':'INDEPENDENT_DATA_AND_SUPPORT_MAXIMA_PASS','certificate_sha256':sha(cp),'finite_support_checks':max_checks,'pair18_states':267,'conditional18_states':16,'case_count':len(cases),'ordinary_bans':18,'input_sha256':sha(W/'input.txt'),'root_code_sha256':sha(Path(__file__)),'independence':'stdlib-only pure certificate/input reads; no producer domain imports'}
(W/'SUPPORT_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
