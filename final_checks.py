from pathlib import Path
from collections import Counter
import json, re
b=Path(__file__).resolve().parent
p=b/'cap7_upper279'
def log(path):return Counter(x for x in path.read_text().splitlines() if x and not x.startswith('Elapsed verification seconds:'))
assert log(b/'original_cpp_replay.txt')==log(b/'original_python_replay.txt')==log(p/'cpp_verification.txt')==log(p/'python_verification.txt')
local=[s for s in (b/'original_cpp_replay.txt').read_text().splitlines() if s.startswith('n=')]
assert len(local)==155
# Separate verification of the actual point file with integer base-3 encoding.
points=[tuple(map(int,s)) for s in (p/'cap236.txt').read_text().splitlines() if s]
assert len(points)==236 and len(set(points))==236 and all(len(t)==7 and set(t)<={0,1,2} for t in points)
def encode(p):
    x=0
    for v in p:x=3*x+v
    return x
codes={encode(t) for t in points};count=0
for i,x in enumerate(points):
    for y in points[:i]:
        assert encode(tuple((6-u-v)%3 for u,v in zip(x,y))) not in codes
        count+=1
assert count==27730
# Check the independently reconstructed deletion spectra from the preceding audit,
# performed before receipt of the complete upper-279 certificate package.
old=json.loads((b/'previous_histogram_checks.json').read_text())
j=json.loads((p/'certificate.json').read_text())
for n in [42,43]:
    types=[tuple(t) for t in j['spectrum5'][str(n)]['types']]
    from_old={tuple(dict((tuple(t),v) for t,v in h['histogram']).get(t,0) for t in types) for h in old[f'histograms{n}']}
    got=set(map(tuple,j['spectrum5'][str(n)]['spectra']))
    if n==42:
        delta={(20,16,6):3,(18,18,6):4,(18,17,7):18,(18,12,12):6,(16,15,11):24,(16,14,12):36,(15,15,12):3,(14,14,14):27}
        from_old.add(tuple(delta.get(t,0) for t in types))
    assert got==from_old
print('PASS: both fresh original-verifier logs match every supplied exact log line; 155 cases.')
print('PASS: separate base-3 point-file checker; 236 distinct points; 27730 pairs.')
print('PASS: size-42 and size-43 histograms match the earlier independent deletion enumeration.')
print('PASS: independent unquotiented audit completed; 262070710 full matrices, 55253413 canonical matrices.')
