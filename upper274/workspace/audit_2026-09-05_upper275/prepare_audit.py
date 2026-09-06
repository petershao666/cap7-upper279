from pathlib import Path
import hashlib,json,subprocess,shutil
from math import comb
D=Path(__file__).resolve().parent; P=D/'cap7_upper275'
checked=0
for line in (P/'SHA256SUMS.txt').read_text().splitlines():
    sha,name=line.split(maxsplit=1);assert hashlib.sha256((P/name).read_bytes()).hexdigest()==sha,name;checked+=1
print('Source manifest PASS:',checked,'files')
subprocess.run(['python3',str(P/'check_integrity.py')],check=True)
C=json.loads((P/'results/size276/proof.json').read_text());aux={}
for h in C['new_histograms']:
    for r in h['inner']:
        for u in r.get('uppercuts',[]):
            if u['id'] in aux:assert aux[u['id']]==u['data']
            aux[u['id']]=u['data']
lines=[str(len(aux))]
for name,h in aux.items():
    types=[(a,b,41-a-b) for a in range(21) for b in range(a+1) if 0<=41-a-b<=b and (a,b,41-a-b) not in ((20,19,2),(20,18,3),(19,19,3),(19,18,4))]
    assert types==list(map(tuple,h['types']))
    anchors=[tuple(r['type']) for r in h['inner']]
    assert len(anchors)==len(set(anchors))==10
    assert set(anchors)=={t for t in types if t in ((20,20,1),(18,18,5)) or 20>=t[0]>=17>=t[1]>=16>=t[2]}
    lines.append(f"{name} {len(types)} {len(anchors)} {h['bound']}")
    lines.extend(' '.join(map(str,(*t,v))) for t,v in zip(types,h['phi']))
    for i,r in enumerate(h['inner']):
        absent=list(map(tuple,r.get('absent_types',[])))
        assert not absent or absent==anchors[:i]
        lines.append(' '.join(map(str,(*r['type'],*r['coeff'],r['K'],r['bound'],r['matrices'],len(absent)))))
        lines.extend(' '.join(map(str,t)) for t in absent)
(D/'aux41_input.txt').write_text('\n'.join(lines)+'\n')
print('Independent 41-cap support/anchor/prefix checks PASS:',len(aux),'functions')
N=276;k=C['k'];assert k==67
q=lambda a,b,c:9*a*b*c-903*(a*b+a*c+b*c)+15920784
types=[(a,b,N-a-b) for a in range(113) for b in range(a+1) if 0<=N-a-b<=b]
assert len(types)==331
for a,b,c in types:assert 4*q(a,b,c)==(3*c-N)**2*(c-k)+(4*N-3*k-9*c)*(a-b)**2
root=9*243*comb(N,3)-903*729*comb(N,2)+15920784*1093
assert root==-214038
print('Independent root identity PASS:',len(types),'types; root sum',root)
# Run the supplied transcription in a separate directory; preserve all source bytes.
G=D/'regenerate';(G/'results/size276').mkdir(parents=True,exist_ok=True)
for rel in ['generate_step_data.py','results/near_deleted2.json','results/size276/proof.json']:
    shutil.copy2(P/rel,G/rel)
subprocess.run(['python3',str(G/'generate_step_data.py'),'276'],check=True,capture_output=True)
assert (G/'results/size276/step_data.hpp').read_bytes()==(P/'results/size276/step_data.hpp').read_bytes()
print('JSON to C++ data regeneration PASS')
print('Source ZIP SHA256:',hashlib.sha256((D/'source.zip').read_bytes()).hexdigest())
