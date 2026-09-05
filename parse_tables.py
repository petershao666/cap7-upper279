"""Parse user-visible Markdown, not the original generated C++ header."""
import ast, hashlib, json, re
from pathlib import Path
from math import comb
base=Path(__file__).resolve().parent
lines=(base/'user_CERTIFICATE_TABLES.md').read_text().splitlines()
hist={};spec={};rows=[];size=None;stage=None
for line in lines:
    if m:=re.fullmatch(r'### Size (\d+)',line):size=int(m[1]);hist[size]={};stage=None
    if m:=re.fullmatch(r'### Dimension (\d+), stage (\d+): (\d+) cases',line):stage=tuple(map(int,m.groups()));size=None
    if not line.startswith('| '):continue
    p=[s.strip().strip('`') for s in line.strip('|').split('|')]
    if size and re.match(r'^\(\d',p[0]):hist[size][ast.literal_eval(p[0])]=list(map(int,p[1:]))
    if re.fullmatch(r'G\d+',p[0]):
        gid=int(p[0][1:]);n=int(p[1]);v=ast.literal_eval(p[2]);kind=p[3];bound=int(p[4]);sums=ast.literal_eval(p[5])
        types=list(hist[n]);assert len(v)==len(types)
        actual=[sum(v[i]*hist[n][t][j] for i,t in enumerate(types)) for j in range(len(sums))]
        assert sums==actual and (all(x==bound for x in sums) if kind=='exact' else max(sums)==bound)
        spec[gid]=(n,dict(zip(types,v)),kind,bound)
    if stage and re.match(r'^\(\d',p[0]):
        key=ast.literal_eval(p[0]);q=ast.literal_eval(p[1]);extras=[tuple(map(int,m)) for m in re.findall(r'(-?\d+) G(\d+)\((\d+)\)',p[2])]
        assert p[2]=='None' or len(extras)==len(p[2].split(';'))
        K,U,gap,count,minimum=map(int,p[3:]);n,st,_=stage
        F=[(3**(n-2)-1)//2*key[0]*key[1]*key[2]]
        for x in key:F.extend([3**(n-2)*comb(x,2),3**(n-3)*comb(x,3)])
        computed=sum(a*b for a,b in zip(q,F));phi=[{} for _ in range(3)]
        for mult,gid,col in extras:
            N,vals,kind,bound=spec[gid];assert N==key[col] and (kind=='exact' or mult>=0)
            computed+=mult*bound
            for t,v in vals.items():phi[col][t]=phi[col].get(t,0)+mult*v
        assert computed==U and (3**(n-1)-1)//2*K-U==gap and gap>0
        rows.append(dict(n=n,stage=st,key=key,q=q,K=K,U=U,gap=gap,count=count,minimum=minimum,phi=phi))
assert len(rows)==155 and sum(r['n']==6 for r in rows)==97
assert sum(r['count'] for r in rows)==55253413
out=[]
for n,h in sorted(hist.items()):
    out.append(f'{n} {len(h)}')
    out.extend(' '.join(map(str,t)) for t in h)
out.append(str(len(rows)))
for r in rows:
    out.append(' '.join(map(str,[r['n'],r['stage'],*r['key'],*r['q'],r['K'],r['U'],r['gap'],r['count'],r['minimum']])))
    for phi in r['phi']:
        out.append(str(len(phi)))
        out.extend(' '.join(map(str,[*t,v])) for t,v in phi.items())
(base/'audit_data.txt').write_text('\n'.join(out)+'\n')
print('PASS: parsed 155 rows and 17 spectral functions from the supplied Markdown; all U values, positive gaps, histogram bounds, and multiplier signs agree.')
# Integrity checks of the original package; no original code is executed here.
pkg=base/'cap7_upper279'
for line in (pkg/'SHA256SUMS.txt').read_text().splitlines():
    digest,name=line.split();assert hashlib.sha256((pkg/name).read_bytes()).hexdigest()==digest,name
assert (pkg/'CERTIFICATE_TABLES.md').read_bytes()==(base/'user_CERTIFICATE_TABLES.md').read_bytes()
print('PASS: all 16 original file hashes; attached table equals package table.')
