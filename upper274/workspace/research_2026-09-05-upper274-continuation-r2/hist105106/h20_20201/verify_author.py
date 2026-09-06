"""Author stdlib coordinate replay. Independent external audit is P/root."""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
import hashlib,json,time

W=Path(__file__).resolve().parent
start=time.monotonic()
coord=[tuple((p//(3**j))%3 for j in range(4)) for p in range(81)]
def pid(p):return sum(x*3**i for i,x in enumerate(p))
addition=[[pid(tuple((x+y)%3 for x,y in zip(a,b))) for b in coord]for a in coord]
negaddition=[[pid(tuple((-x-y)%3 for x,y in zip(a,b))) for b in coord]for a in coord]
def mask(ps):return sum(1<<p for p in ps)
def verifycap(ps,table):
    ss=set(ps)
    assert all(table[a][b] not in ss for a,b in combinations(ps,2))

frozen=json.loads((W/'FROZEN.json').read_text())
for name,digest in frozen['artifacts'].items():assert hashlib.sha256((W/name).read_bytes()).hexdigest()==digest
base=json.loads((W/'centered20.json').read_text())
canonical=base['canonical_points'];assert len(canonical)==20
verifycap(canonical,negaddition)
assert mask(canonical)==int(base['canonical_mask'],16)
assert all((sum(x*x for x in coord[p][:3])+2*coord[p][3]**2)%3==0 for p in canonical)
centered=base['centered'];last=-1
for i,z in enumerate(centered):
    assert z['id']==i and len(z['point_ids'])==20
    m=int(z['mask'],16);assert m>last;last=m
    assert mask(z['point_ids'])==m
    q=z['matrix_code'];coef=[]
    for _ in range(10):coef.append(q%3);q//=3
    zeros=[]
    for p,x in enumerate(coord[1:],1):
        k=0;v=0
        for a in range(4):
            for b in range(a,4):
                v+=coef[k]*(1 if a==b else 2)*x[a]*x[b];k+=1
        if v%3==0:zeros.append(p)
    assert zeros==z['point_ids']
    assert all(sum(coord[p][j]for p in zeros)%3==0 for j in range(4))
    verifycap(zeros,negaddition)

seen_centers=[0]*len(centered);last=-1;n=0;elig={}
am=mask(canonical)
with (W/'all20_catalogue.tsv').open() as f,(W/'all20_masks.txt').open() as masks:
    for line in f:
        h,t,i=line.rstrip().split('\t');t=int(t);i=int(i);m=int(h,16)
        assert h==masks.readline().strip() and m>last;last=m;n+=1
        ps=[addition[p][t]for p in centered[i]['point_ids']]
        assert mask(ps)==m
        assert pid(tuple(-sum(coord[p][j]for p in ps)%3 for j in range(4)))==t
        assert not ((seen_centers[i]>>t)&1);seen_centers[i]|=1<<t
        if not (m&am):elig[h]=(t,i,ps)
    assert masks.readline()==''
assert all(x==(1<<81)-1 for x in seen_centers)
assert n==81*len(centered)

data=json.loads((W/'histograms41.json').read_text())
types=[tuple(x)for x in data['types']]
sup={tuple(z['counts']) for z in data['histograms']}
coord5=[tuple((p//(3**j))%3 for j in range(5)) for p in range(243)]
ng5=[[pid(tuple((-x-y)%3 for x,y in zip(a,b)))for b in coord5]for a in coord5]
dirs=[v for v in coord5[1:]if next(x for x in v if x)==1]
dot=[[sum(x*y for x,y in zip(v,p))%3 for p in coord5]for v in dirs]
def histogram(ps):
    counts=Counter()
    for row in dot:
        ns=[0,0,0]
        for p in ps:ns[row[p]]+=1
        counts[tuple(sorted(ns,reverse=True))]+=1
    assert set(counts)<=set(types)
    return tuple(counts[t]for t in types)
seen=set();hh=set()
for line in (W/'eligible41_ledger.tsv').read_text().splitlines():
    h,t,i,k=line.split('\t');t=int(t);i=int(i);k=int(k)
    assert h not in seen;seen.add(h)
    et,ei,B=elig[h];assert(et,ei)==(t,i)
    ps=sorted([3*p for p in canonical]+[1+3*p for p in B]+[2])
    verifycap(ps,ng5)
    hist=histogram(ps);hh.add(hist)
    assert hist==tuple(data['histograms'][k]['counts'])
assert seen==set(elig) and hh==sup
for z in data['histograms']:
    ps=z['point_ids'];assert len(ps)==41 and z['points']==[list(coord5[p])for p in ps]
    verifycap(ps,ng5);assert histogram(ps)==tuple(z['counts'])
st=json.loads((W/'enumeration_statistics.json').read_text())
assert st['centered_caps']==len(centered) and st['translated_caps']==n and st['eligible_B_caps']==len(elig) and st['distinct_histograms41']==len(hh)
res={'status':'PASS_AUTHOR_REPLAY_NOT_EXTERNAL_INDEPENDENCE','centered_matrices_and_caps_verified':len(centered),'translated_witnesses_verified':n,'eligible_lifts_verified':len(elig),'complete_histogram_set_size':len(hh),'pair_checks':190*(len(centered)+1)+820*(len(elig)+len(data['histograms'])),'direction_histograms_checked':121*(len(elig)+len(data['histograms'])),'seconds':time.monotonic()-start,'shared_inputs':'H generated catalogues and metadata; geometry/reconstruction code is separately written. P/root perform external independent complete enumeration.'}
(W/'author_verification.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res))
