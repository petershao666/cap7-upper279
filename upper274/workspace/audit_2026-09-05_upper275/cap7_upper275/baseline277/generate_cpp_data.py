#!/usr/bin/env python3
"""Transcribe new exact JSON certificate into C++ data; no search or optimization."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
c=json.loads((D/'certificate.json').read_text())
def tr(t):return '{'+','.join(map(str,t))+'}'
def vec(q):return '{'+','.join(str(x)+'LL' for x in q)+'}'
def key(k):return list(map(int,k.split(',')))
def rec(t,r):return '{'+tr(t)+','+vec(r['coeff'])+','+','.join(str(r[k])+'LL' for k in ('K','forced','gap'))+',{},false,{-1,-1,-1}}'
out=['// Exact new certificate, generated from certificate.json.\n']
out.append('const std::vector<std::vector<Record>> NEW_ORDINARY={\n')
for stage in c['ordinary_stages']:
 out.append('{\n'+',\n'.join(rec(key(k),r) for k,r in sorted(stage.items()))+'\n},\n')
out.append('};\nconst std::vector<HillRecord> NEAR112={\n')
for r in c['near112']:
 impossible=r.get('infeasible',False);q=r['coeff'] if impossible else r['q']
 out.append('{'+str(r['h'])+','+str(impossible).lower()+','+vec(q)+','+','.join(str(x)+'LL' for x in (r.get('K',0),r.get('L',0),r['forced'] if impossible else r['upper'],r['gap']))+'},\n')
out.append('};\nconst std::map<Triple,I> PSI108={\n')
n=c['nested108']
for t,z in zip(n['types'],n['phi']):out.append('{'+tr(t)+','+str(z)+'LL},\n')
out.append('};\nconst I SPECTRAL108_BOUND='+str(n['bound'])+'LL;\n')
out.append('const std::vector<InnerRecord> INNER108={\n')
for r in n['inner']:
 ex='{'+','.join('{'+str(j)+','+tr(t)+'}' for j,t in r['extras'])+'}'
 out.append('{'+tr(r['type'])+','+vec(r['coeff'])+','+str(r['K'])+'LL,'+str(r['bound'])+'LL,'+ex+'},\n')
out.append('};\n')
r=n['outer'];out.append('const std::vector<I> OUTER108_Q='+vec(r['coeff'])+';\n')
for k in ('K','forced','gap'):out.append('const I OUTER108_'+k.upper()+'='+str(r[k])+'LL;\n')
out.append('const std::vector<ExtremalRecord> EXTREMAL={\n')
for k,r in sorted(c['extremal'].items()):
 for br in r.get('branches',[r]):
  nested=br.get('nested108',False);rr=n['outer'] if nested else br
  state=br.get('status',[-1,-1,-1])
  out.append('{'+tr(key(k))+','+vec(rr['coeff'])+','+','.join(str(rr[z])+'LL' for z in ('K','forced','gap'))+','+tr(state)+','+str(nested).lower()+'},\n')
out.append('};\n')
(D/'certificate_data.hpp').write_text(''.join(out))
print('Generated certificate_data.hpp from certificate.json')
