from pathlib import Path
import json,hashlib,subprocess,time
R=Path('/Users/hengshao/Desktop/math/research_2026-09-05-upper274-continuation-r2')
O=Path('/private/tmp/cap274-review-20260906')
D=R/'root_potential/complete41_domain_audit'
fresh=O/'fresh_nc_domains';fresh.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
start=time.monotonic()
cmd=['c++','-O2','-std=c++17','-fsanitize=undefined','-fno-sanitize-recover=all',str(D/'enumerate_domains.cpp'),'-o',str(O/'enumerate_nc_domains.bin')]
cp=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
(O/'nc_domains.compile.log').write_text(cp.stdout+cp.stderr)
assert cp.returncode==0,cp.stderr
with (O/'nc_domains.stdout').open('wb') as so,(O/'nc_domains.stderr').open('wb') as se:
 cp=subprocess.run([str(O/'enumerate_nc_domains.bin'),str(D/'INPUTS.txt'),str(fresh)],stdout=so,stderr=se,timeout=190)
assert cp.returncode==0,cp.returncode
assert not (O/'nc_domains.stderr').read_bytes()
summary=json.loads((O/'nc_domains.stdout').read_text())
records=[]
for i in range(14):
 name=f'case{i:02d}_new_raw.u8'
 a,b=fresh/name,D/name
 assert sha(a)==sha(b),name
 assert a.stat().st_size%9==0
 records.append({'case':i,'sha256':sha(a),'rows':a.stat().st_size//9})
assert sum(v['rows'] for v in records)==1106094
out={'status':'PASS_FRESH_DOMAIN_RECONSTRUCTION','scope':'Fresh build and full regeneration of previously independent NC106 domain kernel; generated row files byte-identical to frozen inputs used by exact replay. No new independent implementation claim.',
 'compiler_command':cmd,'source_sha256':sha(D/'enumerate_domains.cpp'),'input_sha256':sha(D/'INPUTS.txt'),
 'rows':1106094,'cases':records,'elapsed_seconds':time.monotonic()-start}
(O/'nc_domains_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['compiler_command','cases']}))
