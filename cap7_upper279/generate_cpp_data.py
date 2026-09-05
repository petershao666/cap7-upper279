#!/usr/bin/env python3
"""Regenerate certificate_data.hpp from the adjacent certificate.json (standard library only)."""
import json,sys
from pathlib import Path
D=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
c=json.load(open(D/'certificate.json'))
ident=[]
for stage in c['six_stages']:
 for key,rec in stage.items():
  t=list(map(int,key.split(',')))
  for e in rec.get('extra',[]):
   x=(t[e['column']],e['identity']['coeff'],e['identity']['sum'],e['identity'].get('bound','exact')=='upper')
   if x not in ident:ident.append(x)

def v(vals):return '{'+','.join(str(x)+'LL' for x in vals)+'}'
def tr(t):return '{'+','.join(map(str,t))+'}'
def rec(key,r):
 t=tuple(map(int,key.split(',')))
 if r.get('empty'):return '{'+tr(t)+',{},0,0,0,{},true}'
 ex=[]
 for e in r.get('extra',[]):
  x=(t[e['column']],e['identity']['coeff'],e['identity']['sum'],e['identity'].get('bound','exact')=='upper');ex.append('{'+str(e['column'])+','+str(ident.index(x))+'}')
 return '{'+tr(t)+','+v(r['coeff'])+','+str(r['K'])+'LL,'+str(r['forced'])+'LL,'+str(r['gap'])+'LL,{'+','.join(ex)+'},false}'
f=open(D/'certificate_data.hpp','w')
f.write('// Exact integer certificate data. Generated from certificate.json.\n')
f.write('const int TARGET='+str(c['target_size'])+';\n')
f.write('const std::vector<Spec> SPECS={\n'+',\n'.join('{'+str(size)+','+v(vals)+','+str(total)+'LL,'+('true' if bounded else 'false')+'}' for size,vals,total,bounded in ident)+'\n};\n')
f.write('const std::map<int,std::vector<Triple>> TYPES={\n'+',\n'.join('{'+str(size)+',{'+','.join(tr(t) for t in c['spectrum5'][str(size)]['types'])+'}}' for size in [42,43,44,45])+'\n};\n')
f.write('const std::map<int,std::set<std::vector<I>>> HISTOGRAMS={\n'+',\n'.join('{'+str(size)+',{'+','.join(v(t) for t in c['spectrum5'][str(size)]['spectra'])+'}}' for size in [42,43,44,45])+'\n};\n')
for name,stages in [('SIX',c['six_stages']),('SEVEN',c['seven_stages'])]:
 f.write('const std::vector<std::vector<Record>> '+name+'={\n'+',\n'.join('{\n'+',\n'.join(rec(k,r) for k,r in sorted(st.items()))+'\n}' for st in stages)+'\n};\n')
f.write('const I ROOT_Q2='+str(c['root']['coeff'][0])+'LL, ROOT_Q3='+str(c['root']['coeff'][1])+'LL, ROOT_K='+str(c['root']['K'])+'LL, ROOT_FORCED='+str(c['root']['forced'])+'LL, ROOT_GAP='+str(c['root']['gap'])+'LL;\n')
f.close()
