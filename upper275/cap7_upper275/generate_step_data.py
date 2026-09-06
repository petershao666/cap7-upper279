#!/usr/bin/env python3
"""Transcribe a step's candidate JSON into integer C++ data, without doing discovery."""
from pathlib import Path
import json,sys
W=Path(__file__).resolve().parent
S=int(sys.argv[1]);folder=W/'results'/f'size{S}';C=json.loads((folder/'proof.json').read_text())
def cpp(x):
 if isinstance(x,bool):return str(x).lower()
 if isinstance(x,str):return json.dumps(x)
 if isinstance(x,(list,tuple)):return '{'+','.join(cpp(v) for v in x)+'}'
 return str(x)+'LL' if abs(x)>2**31-1 else str(x)
def rec(t,r):
 return cpp([list(map(int,t.split(','))),r.get('coeff',[]),r.get('K',0),r.get('forced',0),r.get('gap',0),r.get('status',[-1,-1,-1]),r.get('extra_features',[]),r.get('empty',False)])
lines=[f'const int STEP_SIZE={S}, STEP_K={C["k"]};',f'const std::vector<Triple> STEP_INITIAL_SEEDS={cpp(C["initial_seeds"])};',f'const std::vector<Triple> STEP_SEEDS={cpp(C["seeds"])};']
stages=['{'+','.join(rec(t,r) for t,r in sorted(st.items()))+'}' for st in C['stages']]
lines.append('const std::vector<std::vector<StepRecord>> STEP_ORDINARY={'+','.join(stages)+'};')
lines.append('const std::vector<StepRecord> STEP_EXTREMAL={'+','.join(rec(t,b) for t,r in sorted(C['extremal'].items()) for b in (r['branches'] if 'branches' in r else [r]))+'};')
near=json.loads((W/'results/near_deleted2.json').read_text())
rr=[]
for r in near:rr.append(cpp([r['h'],r.get('infeasible',False),r.get('coeff',r.get('q')),r.get('K',0),r.get('L',0),r.get('forced',r.get('upper')),r['gap']]))
lines.append('const std::vector<HillRecord> DELETED2={'+','.join(rr)+'};')
AUX={}
HH=[]
for h in C['new_histograms']:
 inn=[]
 for r in h['inner']:
  for use in r.get('uppercuts',[]):
   assert not use['data'].get('hist4'), '4D histogram enumeration still needs independent verification'
   if use['id'] in AUX:assert AUX[use['id']]==use['data']
   AUX[use['id']]=use['data']
  spec=[[s['column'],s['types'],s['phi'],s['bound']] for s in r['spectra']]
  inn.append([r['type'],r['coeff'],r['K'],r['bound'],r['extras'],spec,r.get('absent_types',[]),[[u['column'],u['id']] for u in r.get('uppercuts',[])]])
 root=h['root'];HH.append([h['id'],h['m'],h['types'],h['phi'],h['bound'],root['coeff'],root['K'],root['forced'],root['gap'],inn,h.get('admissibility5_extra',[])])
lines.append('const std::vector<GeneralHistogram> STEP_HISTOGRAMS='+cpp(HH)+';')
AA=[]
for name,h in AUX.items():
 inner=[[r['type'],r['coeff'],r['K'],r['bound'],r['matrices'],r.get('absent_types',[])] for r in h['inner']]
 AA.append([name,h['types'],h['phi'],h['bound'],inner])
lines.append('const std::vector<Aux41Cut> STEP_AUX41='+cpp(AA)+';')
(folder/'step_data.hpp').write_text('\n'.join(lines)+'\n')
print('Generated',folder/'step_data.hpp')
