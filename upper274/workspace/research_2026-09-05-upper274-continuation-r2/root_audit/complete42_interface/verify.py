import json, hashlib, math, time
from pathlib import Path
from fractions import Fraction as F

t0=time.monotonic()
ROOT=Path('/Users/hengshao/Desktop/math')
R=ROOT/'research_2026-09-05-upper274-continuation-r2'
D=R/'root_audit/complete42_interface'
H=R/'hist105106/h24_42_dominance'
paths=[]
def read(p):
    paths.append(p)
    return json.loads(p.read_text())
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def rank(rows):
    rows=[[F(x) for x in row] for row in rows]; r=0
    for c in range(len(rows[0])):
        p=next((i for i in range(r,len(rows)) if rows[i][c]),None)
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]
        f=rows[r][c]; rows[r]=[x/f for x in rows[r]]
        for i in range(len(rows)):
            if i!=r:
                f=rows[i][c]; rows[i]=[x-f*y for x,y in zip(rows[i],rows[r])]
        r+=1
        if r==len(rows):break
    return r
src=read(ROOT/'audit_2026-09-05_upper275/cap7_upper275/baseline277/baseline278/certificate.json')['spectrum5']['42']
a=read(H/'INPUT.json'); w=read(H/'RATIONAL_WITNESS.json'); hull=read(H/'COMPLETE_HULL.json')
old=read(R/'compatibility/complete41_support_10610564/RESULT.json')
types=src['types']; hs=src['spectra']
assert types==a['types']==w['types']==hull['types']
assert hs==a['histograms']==hull['histograms']
mom=[[1]*len(types),[x*y+x*z+y*z for x,y,z in types],[x*y*z for x,y,z in types]]
bounds=[121,81*math.comb(42,2),27*math.comb(42,3)]
assert mom==a['equalities'] and bounds==a['equality_bounds']
n=w['numerators']; den=w['denominator']; assert den>0 and min(n)>0
assert [dot(v,n) for v in mom]==[den*b for b in bounds]==w['old_equality_numerators']
slacks=[]
for row in a['upper_rows']:
    v=old['upper5'][row['id']]
    assert v['m']==42 and v['bound']==row['bound']
    bytype=dict(zip(map(tuple,v['types']),v['phi']))
    values=[bytype[tuple(t)] for t in types]
    assert values==row['values']
    assert max(dot(values,h) for h in hs)<=v['bound']
    s=v['bound']*den-dot(values,n);assert s>0
    slacks.append({'id':row['id'],'slack_numerator':s,'denominator':den})
assert len(slacks)==19 and slacks==w['old_upper_slack_numerators']
g=[3,1,-3]+[0]*10
assert [dot(g,h) for h in hs]==[72]*4
assert F(dot(g,n),den)-72==F(1,20)
assert rank([[x-y for x,y in zip(h,hs[0])] for h in hs[1:]])==3
eqs=hull['affine_equations'];assert len(eqs)==10 and rank([e['coeff'] for e in eqs])==10
for e in eqs: assert all(dot(e['coeff'],h)==e['bound'] for h in hs)
facets=hull['facets']; assert len(facets)==4
for j,fa in enumerate(facets):
    sl=[fa['bound']-dot(fa['coeff'],h) for h in hs]
    assert sl==fa['vertex_slacks'] and sl[j]>0 and all(sl[i]==0 for i in range(4) if i!=j)
    lc=F(fa['lambda_constant']);lv=list(map(F,fa['lambda_coeff']))
    assert [lc+dot(lv,h) for h in hs]==[int(i==j) for i in range(4)]
    assert lc==F(fa['bound'],sl[j]) and lv==[F(-x,sl[j]) for x in fa['coeff']]
# Four affine-basis values prove reconstruction and sum-to-one throughout the span.
nc=next(x for x in old['histograms'] if x['N']==106) if isinstance(old['histograms'],list) else old['histograms']['106']
anchors=[c['type'] for c in nc['inner']]
positions=[{'case':i,'anchor':an,'column':j} for i,an in enumerate(anchors) for j,x in enumerate(an) if x==42]
assert positions==a['physical42']
res={'status':'PASS_EXACT_MARGINAL_SEPARATION_AND_COMPLETE_HULL','old_upper_rows':19,'moments':bounds,'affine_rank':3,'affine_equations':10,'facets':4,'strict_gap':'1/20','physical42':positions,'shared_dependencies':'Accepted published complete42 spectra; accepted old upper functions; H24 pure witness data. No producer imports.','nonclaim':'No actual cap or parent relaxation realization; no new global bound or classification.','elapsed':time.monotonic()-t0,'inputs':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(D/'VERIFICATION.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
