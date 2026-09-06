"""Standalone exact verification: stdlib Python JSON parsing + fresh C++ raw-table walk.
No discovery, engine, NumPy, quotient, generated table or LP imports.
"""
import json, hashlib, subprocess, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
D=HERE/'EXACT_DUAL.json'
assert hashlib.sha256(D.read_bytes()).hexdigest()=='c574f90aa862a7b94ed395cba567b4f4a2088fe96a515e7b55bde8ece140b4ec'
C=json.loads(D.read_text())
base=ROOT/'audit_2026-09-05_upper275/cap7_upper275/baseline277/baseline278/certificate.json'
r1=ROOT/'research_2026-09-05-capset-round1-r1/root_audit/audited_certificate_snapshot.json'
h3=HERE.parents[1]/'hist105106/h3/h3_result.json'
assert hashlib.sha256(h3.read_bytes()).hexdigest()=='cbb4973544cf7e2388097bb333504dc0c53c943d1671605fa300996394dfd294'
B=json.loads(base.read_text()); R=json.loads(r1.read_text());H=json.loads(h3.read_text())['histograms']['40']
parse=lambda k:list(map(int,k.split(',')))
old=[parse(k)for st in B['six_stages']for k in st]
comp=B['completion_seeds']+[parse(k)for st in B['completion_stages']for k in st]
ban=R['seeds']+[[112,109,51],[111,110,51]]+[parse(k)for st in R['stages']for k in st]
lines=[str(len(C['rows']))]
for row,q in zip(C['rows'],C['dual']):
    kind=row[0]
    if kind=='norm_outer':rec=[0,0,0,0,0,0,q]
    elif kind=='norm_inner':rec=[1,0,0,0,0,0,q]
    elif kind=='outer_symmetric_feature':rec=[2,0,0,0,0,row[1],q]
    elif kind=='conditional':rec=[3,0,*row[1],row[2],q]
    elif kind=='conditional_theta40':rec=[4,0,*row[1],0,q]
    else:raise ValueError(kind)
    lines.append(' '.join(map(str,rec)))
for arr in (old,comp,ban):
    lines.append(str(len(arr)));lines.extend(' '.join(map(str,t))for t in arr)
assert H['bound']+121*10**10==475918720
lines.append(str(len(H['types'])))
for t,phi in zip(H['types'],H['phi']):lines.append(' '.join(map(str,[*t,phi+10**10])))
(HERE/'own_input.txt').write_text('\n'.join(lines)+'\n')
exe=HERE/'own_verify_bin';start=time.monotonic()
subprocess.run(['clang++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(HERE/'own_verify.cpp'),'-o',str(exe)],check=True)
p=subprocess.run([str(exe),str(HERE/'own_input.txt')],check=True,capture_output=True,text=True,timeout=600)
(HERE/'OWN_VERIFY.log').write_text(p.stdout+p.stderr)
print(p.stdout,end='')
result=json.loads(p.stdout)
assert result['rhs']==9410019729 and result['counts']==[3772668,1407366] and result['maximum_columns']==[0,0]
result['status']='PASS_FRESH_COMPLETE_RAW_DOMAIN'
result['seconds_including_compile']=time.monotonic()-start
result['shared_dependencies']=['Named frozen mathematical certificates','JSON coefficient and row metadata input; no generated table input','This own checker reuses accepted theta40 own verifier helpers, adapted symmetric rows; root audit is separate']
result['sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [D,base,r1,h3,HERE/'own_verify.py',HERE/'own_verify.cpp',HERE/'own_input.txt']}
(HERE/'OWN_VERIFY.json').write_text(json.dumps(result,indent=2)+'\n')
