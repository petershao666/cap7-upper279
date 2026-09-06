#!/usr/bin/env python3
"""Regenerate the C++ header from the two adjacent JSON certificates. Standard library only."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
c=json.loads((D/'certificate.json').read_text());hill=json.loads((D/'hill_certificate.json').read_text())
ident=[]
for stage in c['six_stages']+c['completion_stages']:
 for key,rec in stage.items():
  t=list(map(int,key.split(',')))
  for e in rec.get('extra',[]):
   x=(t[e['column']],e['identity']['coeff'],e['identity']['sum'],e['identity'].get('bound','exact')=='upper')
   if x not in ident:ident.append(x)
def v(vals):return '{'+','.join(str(x)+'LL' for x in vals)+'}'
def tr(t):return '{'+','.join(map(str,t))+'}'
def rec(key,r):
 t=tuple(map(int,key.split(',')));status=r.get('status',[-1,-1,-1])
 if r.get('empty'):return '{'+tr(t)+',{},0,0,0,{},true,'+tr(status)+'}'
 ex=[]
 for e in r.get('extra',[]):
  x=(t[e['column']],e['identity']['coeff'],e['identity']['sum'],e['identity'].get('bound','exact')=='upper')
  ex.append('{'+str(e['column'])+','+str(ident.index(x))+'}')
 return '{'+tr(t)+','+v(r['coeff'])+','+str(r['K'])+'LL,'+str(r['forced'])+'LL,'+str(r['gap'])+'LL,{'+','.join(ex)+'},false,'+tr(status)+'}'
def records(st):
 return [rec(k,b) for k,r in sorted(st.items()) for b in (r['branches'] if 'branches' in r else [r])]
with (D/'certificate_data.hpp').open('w') as f:
 f.write('// Exact integer certificate data. Generated from the adjacent JSON files.\n')
 f.write('const int TARGET='+str(c['target_size'])+';\n')
 f.write('const std::vector<Spec> SPECS={\n'+',\n'.join('{'+str(size)+','+v(vals)+','+str(total)+'LL,'+('true' if bounded else 'false')+'}' for size,vals,total,bounded in ident)+'\n};\n')
 f.write('const std::map<int,std::vector<Triple>> TYPES={\n'+',\n'.join('{'+str(size)+',{'+','.join(tr(t) for t in c['spectrum5'][str(size)]['types'])+'}}' for size in (42,43,44,45))+'\n};\n')
 f.write('const std::map<int,std::set<std::vector<I>>> HISTOGRAMS={\n'+',\n'.join('{'+str(size)+',{'+','.join(v(t) for t in c['spectrum5'][str(size)]['spectra'])+'}}' for size in (42,43,44,45))+'\n};\n')
 for name,stages in [('SIX',c['six_stages']),('CONDITIONAL',c['completion_stages']),('SEVEN',c['seven_stages'])]:
  f.write('const std::vector<std::vector<Record>> '+name+'={\n'+',\n'.join('{\n'+',\n'.join(records(st))+'\n}' for st in stages)+'\n};\n')
 f.write('const std::vector<Triple> COMPLETION_SEEDS={'+','.join(tr(t) for t in c['completion_seeds'])+'};\n')
 f.write('const std::vector<Triple> COMPLETION_ROOT_USES={'+','.join(tr(t) for t in c['completion109_root_uses'])+'};\n')
 f.write('const std::vector<Triple> SEVEN_SEEDS={'+','.join(tr(t) for t in c['seven_seed_exclusions'])+'};\n')
 for name,r in [('ROOT',c['root']),('COMPLETION_ROOT',c['completion109_root'])]:
  f.write('const I '+name+'_Q2='+str(r['coeff'][0])+'LL, '+name+'_Q3='+str(r['coeff'][1])+'LL, '+name+'_K='+str(r['K'])+'LL, '+name+'_FORCED='+str(r['forced'])+'LL, '+name+'_GAP='+str(r['gap'])+'LL;\n')
 hr=[]
 for r in hill:
  bad=r.get('infeasible',False)
  vals=[r['h'],str(bad).lower(),v(r['coeff'] if bad else r['q']),r['K'] if bad else 0,0 if bad else r['L'],r['forced'] if bad else r['upper'],r['gap']]
  hr.append('{'+','.join(str(x) if i<3 else str(x)+'LL' for i,x in enumerate(vals))+'}')
 f.write('const std::vector<HillRecord> HILL={\n'+',\n'.join(hr)+'\n};\n')
