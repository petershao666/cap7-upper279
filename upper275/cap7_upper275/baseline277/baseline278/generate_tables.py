#!/usr/bin/env python3
"""Print the complete certificate as Markdown, directly from the JSON data."""
from pathlib import Path
import json,re
D=Path(__file__).resolve().parent
c=json.loads((D/'certificate.json').read_text());hill=json.loads((D/'hill_certificate.json').read_text())
info={}
pattern=re.compile(r'^n=(\d) \((\d+), (\d+), (\d+)\)(?: status=([01-]{3}))?: matrices=(\d+), minimum=(-?\d+), certified_K=(-?\d+), gap=(\d+)')
for line in (D/'python_verification.txt').read_text().splitlines():
 m=pattern.match(line)
 if m:
  n,a,b,z,st,count,minimum,K,gap=m.groups();key=(int(n),(int(a),int(b),int(z)),st or '')
  assert key not in info
  info[key]=(int(count),int(minimum))
ident=[]
for stage in c['six_stages']+c['completion_stages']:
 for k,r in stage.items():
  t=list(map(int,k.split(',')))
  for e in r.get('extra',[]):
   item=(t[e['column']],e['identity'])
   if item not in ident:ident.append(item)
lines=['# Complete upper-278 certificate tables','',
'All coefficients below are exact integers. These tables are generated from `certificate.json` and `hill_certificate.json`; the verifier computes the counts and minima rather than trusting this text.','',
'The base feature order is `(T, E2(alpha), E3(alpha), E2(beta), E3(beta), E2(gamma), E3(gamma))`. A listed spectral function is appended in the order shown. An upper-bound multiplier must be nonnegative.','',
'For completion-status branches, `0` means the entire slice is not contained in a 112-cap, `1` means it is contained in one, and `-` means no split is made on that slice. After the seven base features, each `1` column in column order appends the functions `1[c<=22]` and `1[c<=22](22-c)`, with sums 56 and 11(112-N); if N>=108 it also appends `1[c>22](40-a)`, with sum 110(112-N). Here (a,b,c) is that column sorted decreasingly.','']

def row(n,k,r,state=''):
 t=tuple(map(int,k.split(',')))
 ct,mn=info.get((n,t,state),('not recorded','not recorded'))
 extra=[]
 for e in r.get('extra',[]):
  item=(t[e['column']],e['identity']);extra.append(f"column {e['column']}: H{ident.index(item)}")
 status=state or '—'
 return f"| {t} | {status} | `{tuple(r['coeff'])}` | {r['K']} | {r['forced']} | {r['gap']} | {ct} | {mn} | {'; '.join(extra) or '—'} |"
for heading,n,stages in [('Universal six-dimensional exclusions',6,c['six_stages']),('Conditional six-dimensional completions',6,c['completion_stages']),('Seven-dimensional exclusions at total 279',7,c['seven_stages'])]:
 lines+=['## '+heading,'']
 for i,stage in enumerate(stages):
  lines += [f'### Stage {i}','', '| Slice type | Status | Coefficients | K | Forced sum / upper bound U | Gap | Case-matrix count | Computed minimum | Spectral functions |', '|---|---|---|---:|---:|---:|---:|---:|---|']
  for k,r in sorted(stage.items(),key=lambda kv:tuple(map(int,kv[0].split(',')))):
   if 'branches' in r:
    for b in r['branches']:
     state=''.join('-' if x<0 else str(x) for x in b['status']);lines.append(row(n,k,b,state))
   else:lines.append(row(n,k,r))
  lines.append('')
lines+=['## Spectral type indices and complete histogram families','']
for size in (42,43,44,45):
 dd=c['spectrum5'][str(size)]
 lines += [f'### Size {size}','', '| Index | Sorted type | '+ ' | '.join('Histogram '+str(j) for j in range(len(dd['spectra'])))+' |', '|---:|---|'+'---:|'*len(dd['spectra'])]
 for i,t in enumerate(dd['types']):lines.append(f'| {i} | {tuple(t)} | '+' | '.join(str(h[i]) for h in dd['spectra'])+' |')
 lines.append('')
lines += ['## All additional five-dimensional spectral functions','', '| ID | Slice size | Coefficients in the above type order | Relation | Total / upper bound |', '|---|---:|---|---|---:|']
for i,(N,fn) in enumerate(ident):lines.append(f"| H{i} | {N} | `{tuple(fn['coeff'])}` | {'≤' if fn.get('bound')=='upper' else '='} | {fn['sum']} |")
lines += ['', '## The 109-completion root','', 'Only the four seed patterns, the original universal exclusions, and conditional type (44,43,22) are needed. Exactly 24 types remain.','',f"`{c['completion109_root']}`",'', '## Two-112-slice certificates','',
'The eight coefficients multiply `(1[u=0], 1[u=1], 1[u=2], p, C(p,2), C(p,3), u*p, u*C(p,2))`. For a zero-count case the local bound is `qX >= L*1[m=0]`, and the gap is `15L-qR > 0`. For an impossible-intersection case the bound is `qX >= K`, and the gap is `364K-qR > 0`. See `HILL_PROOF.md`.','',
'| h | Certificate type | Coefficients | K or L | qR | Positive gap | Number of states |','|---:|---|---|---:|---:|---:|---:|']
for r in hill:
 bad=r.get('infeasible',False);h=r['h'];ns=sum(p<=h and h-p<=45 for u in range(3) for p in range(21 if u==0 else 12))
 lines.append(f"| {h} | {'Impossible intersection' if bad else 'Zero-count bound'} | `{tuple(r['coeff'] if bad else r['q'])}` | {r['K'] if bad else r['L']} | {r['forced'] if bad else r['upper']} | {r['gap']} | {ns} |")
lines += ['', '## Final root','',f"`{c['root']}`",'', 'The 69 excluded types include all 42 types with smallest slice at most 66. On the 231 remaining types the factorization in README Section 8 proves the root inequality. Its forced nonnegative sum would be -38,502.','']
(D/'CERTIFICATE_TABLES.md').write_text('\n'.join(lines))
print('Wrote complete tables:',len(info),'local check records;',len(ident),'spectral functions.')
