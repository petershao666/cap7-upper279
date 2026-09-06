from pathlib import Path
from hashlib import sha256
from math import comb
import json

here=Path(__file__).resolve().parent
base=here.parent.parent
workspace=base.parent
rel='audit_2026-09-05_upper275/cap7_upper275/baseline277/baseline278/certificate.json'
source=workspace/rel
c=json.loads(source.read_text())
accepted=base/'root_audit/complete41/ACCEPTED_HISTOGRAMS.json'
h=json.loads(accepted.read_text())
assert sha256(accepted.read_bytes()).hexdigest()=='38193858291a37b0b71cff568a11db481080125140771e41af57f6fd973374fa'
old=[tuple(map(int,k.split(','))) for stage in c['six_stages'] for k in stage]
completion=list(map(tuple,c['completion_seeds']))+[tuple(map(int,k.split(','))) for stage in c['completion_stages'] for k in stage]
zero=[tuple(t) for j,t in enumerate(h['types']) if all(g['counts'][j]==0 for g in h['histograms'])]
old41=[(20,19,2),(20,18,3),(19,19,3),(19,18,4)]
assert len(zero)==14 and set(old41)<=set(zero)

def allowed(t,bans):
    t=sorted(t,reverse=True)
    return not any(all(x>=y for x,y in zip(t,b)) for b in bans)

def q(t):
    a,b,c=t
    return a*b*c-39*(a*b+a*c+b*c)

support=[(a,b,106-a-b) for a in range(46) for b in range(a+1)
         if 0<=106-a-b<=b and allowed((a,b,106-a-b),old+completion)]
forced=-39*243*comb(106,2)+81*comb(106,3)
cut=forced//364+1
anchors=[t for t in support if q(t)<cut]
assert len(support)==79 and len(anchors)==14 and 364*cut-forced==273
declared=json.loads((base/'hist105106/selected_anchor_covers.json').read_text())
assert list(map(tuple,declared['anchors']['106']))==anchors
large={int(n):[tuple(t) for j,t in enumerate(v['types']) if any(row[j]>0 for row in v['spectra'])] for n,v in c['spectrum5'].items()}
delta={(20,16,6),(18,18,6),(18,17,7),(18,12,12),(16,15,11),(16,14,12),(15,15,12),(14,14,14)}
for n in range(42,46):
    formula={(a,b,n-a-b) for a in range(21) for b in range(a+1) if 0<=n-a-b<=b
             and ((a<=18 and b<=18 and n-a-b<=9) or a<=15 or (n==42 and (a,b,n-a-b) in delta))}
    assert set(large[n])==formula

packet={'old6':old,'completion6':completion,'old41':old41,'zero41':zero,
        'support106':support,'anchors106':anchors,'large5_support':large,
        'anchor_root':{'coeff':[-39,1],'forced':forced,'cut':cut,'gap':364*cut-forced},
        'source_hashes':{str(p.relative_to(workspace)):sha256(p.read_bytes()).hexdigest() for p in [source,accepted,base/'hist105106/selected_anchor_covers.json']},
        'semantics':'All 12 grid lines are ordinary 5D profiles; three transverse profiles are directions of the same NC106 cap; earlier anchor types excluded only within their first-anchor case.'}
(here/'INPUTS.json').write_text(json.dumps(packet,indent=2)+'\n')
lines=[]
for items in [old,completion,old41,zero,support,anchors]:
    lines.append(str(len(items)));lines.extend(' '.join(map(str,t)) for t in items)
for n in range(42,46):
    lines.append(str(len(large[n])));lines.extend(' '.join(map(str,t)) for t in large[n])
(here/'INPUTS.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps({'support106':len(support),'anchors':anchors,'anchor_root':packet['anchor_root'],'old6_count':len(old),'completion6_count':len(completion),'input_sha256':sha256((here/'INPUTS.json').read_bytes()).hexdigest()}))
