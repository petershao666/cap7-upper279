#!/usr/bin/env python3
"""Generate the human-readable certificate tables from the exact data and log."""
import json,re,ast
from pathlib import Path
D=Path(__file__).resolve().parent
C=json.loads((D/'certificate.json').read_text())
functions=[]
for stage in C['six_stages']:
 for key,r in stage.items():
  key=tuple(map(int,key.split(',')))
  for ex in r.get('extra',[]):
   f=(key[ex['column']],ex['identity'])
   if f not in functions:functions.append(f)
counts={}
for line in (D/'cpp_verification.txt').read_text().splitlines():
 m=re.match(r'n=(\d) (\([^)]*\)): matrices=(\d+), minimum=(-?\d+), certified_K=(-?\d+), gap=(\d+)',line)
 if m:counts[int(m[1]),ast.literal_eval(m[2])]=(int(m[3]),int(m[4]))
lines=['# Complete integer certificate tables: f(7,3) <= 279','',
'This file is generated from `certificate.json` and the independently executed C++ log.',
'`README.md` supplies the mathematical reduction and the meaning of every condition.',
'The two full verifiers, not this display file, exhaustively check the inequalities.','',
'## Spectral histograms','',
'Each histogram gives the number of projective hyperplane directions of each sorted type.',
'For size 42 the first three columns are the possible three-point deletions of a 45-cap;',
'H4 is the published Delta686 histogram. Other sizes have a unique histogram.','']
for size,data in C['spectrum5'].items():
 size=int(size);H=data['spectra'];lines += [f'### Size {size}','', '| Sorted type | '+' | '.join(f'H{i+1}' for i in range(len(H)))+' |','|---|'+'---:|'*len(H)]
 for i,t in enumerate(data['types']):lines.append('| '+str(tuple(t))+' | '+' | '.join(str(h[i]) for h in H)+' |')
 lines.append('')
lines += ['## Verified spectral functions','',
'For G_i, its integer values are listed in the type order in the corresponding table above.',
'An **exact** entry means its sum over all 121 directions is the stated number.',
'An **upper** entry means its sum is at most that number, verified on every possible histogram.',
'Only nonnegative multipliers of upper-bound entries are used.','',
'| Function | Size | Values in type order | Kind | Sum or upper bound | Sums on all histograms |',
'|---|---:|---|---|---:|---|']
for i,(N,f) in enumerate(functions):
 hs=C['spectrum5'][str(N)]['spectra'];sums=[sum(x*y for x,y in zip(f['coeff'],h)) for h in hs]
 lines.append(f"| G{i+1} | {N} | `{f['coeff']}` | {f.get('bound','exact')} | {f['sum']} | `{sums}` |")
lines += ['','## Local certificates','',
'The ordinary feature order is `[T, E2(alpha), E3(alpha), E2(beta), E3(beta), E2(gamma), E3(gamma)]`.',
'`c G_i(j)` adds c times G_i evaluated on column j, numbered 0=alpha, 1=beta, 2=gamma.',
'K is the certified lower bound on the full polynomial. U is an exact upper bound on its sum',
'over D_n directions; it is an equality when only exact features occur.',
'The gap is D_n*K-U, where D_6=121 and D_7=364. Every gap is positive.',
'All stages use only completed earlier same-dimension stages for whole-cap consistency.','']
for n,name in [(6,'six_stages'),(7,'seven_stages')]:
 for st,stage in enumerate(C[name]):
  lines += [f'### Dimension {n}, stage {st}: {len(stage)} cases','',
  '| (A,B,C) | Ordinary coefficients | Extra terms | K | U | Gap | Matrices | Computed minimum |',
  '|---|---|---|---:|---:|---:|---:|---:|']
  for key,r in sorted(stage.items(),key=lambda kv:tuple(map(int,kv[0].split(',')))):
   t=tuple(map(int,key.split(',')));ex=[]
   for mul,x in zip(r['coeff'][7:],r.get('extra',[])):
    fi=functions.index((t[x['column']],x['identity']))+1
    ex.append(f'{mul} G{fi}({x["column"]})')
   count,minimum=counts[n,t]
   lines.append(f"| {t} | `{r['coeff'][:7]}` | {'; '.join(ex) or 'None'} | {r['K']} | {r['forced']} | {r['gap']} | {count} | {minimum} |")
  lines.append('')
lines += ['## Root certificate','',
'For every sorted triple of sum 280, entries at most 112, not excluded above:',
'','```text','6*abc - 613*(ab+ac+bc) >= -11141493','```','',
'There are 232 such allowed triples and 58 excluded triples.',
'The forced sum of the left side over 1093 directions is -12177697140.',
'Its lower bound would be 1093*(-11141493) = -12177651849.',
'The positive contradiction gap is 45291.','']
(D/'CERTIFICATE_TABLES.md').write_text('\n'.join(lines))
