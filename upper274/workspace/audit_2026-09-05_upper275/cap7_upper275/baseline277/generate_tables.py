#!/usr/bin/env python3
"""Render the full exact certificate in Markdown; no optimization."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
C=json.loads((D/'certificate.json').read_text())
lines=['# Complete new integer certificate tables\n',
'The inherited coefficients are preserved in `baseline278/CERTIFICATE_TABLES.md`. All tables below are generated from `certificate.json`. The full mathematical interpretation is in `README.md`.\n',
'## 1. Ordinary seven-dimensional exclusions\n',
'The feature order is `(T, E2(alpha), E3(alpha), E2(beta), E3(beta), E2(gamma), E3(gamma))`. Every row asserts `q*f >= K` on all matrices allowed by its earlier stages. `U` is the exact forced sum; the positive gap is `364*K-U`. A stage uses only completed earlier stages, plus the two-112 seed.\n']
for i,stage in enumerate(C['ordinary_stages']):
 lines += [f'### Stage {i}: {len(stage)} types\n','| Type | q | K | U | Gap |','|---|---|---:|---:|---:|']
 for k,r in sorted(stage.items()):lines.append(f'| ({k}) | `{r["coeff"]}` | {r["K"]} | {r["forced"]} | {r["gap"]} |')
lines+=['\n## 2. Extended pair-of-large-slices certificates\n',
'The eight features are `(1[u=0],1[u=1],1[u=2],p,C(p,2),C(p,3),u*p,u*C(p,2))`. The states and exact totals `R(h)` are defined in README Section 3.\n',
'For a low-multiplicity certificate, `q*X >= L*1[m<=1]`; its gap is `18*L-q*R(h)`. For an impossible-intersection certificate, `q*X >= K` and the gap is `364*K-q*R(h)`. The special cases h=0 and h=52,...,56 are handled by the stated mathematical arguments, not omitted.\n',
'| h | Form | q | L or K | q*R(h) | Gap |','|---:|---|---|---:|---:|---:|']
for r in C['near112']:
 imp=r.get('infeasible',False)
 lines.append(f'| {r["h"]} | {"Impossible intersection" if imp else "Low multiplicity"} | `{r["coeff"] if imp else r["q"]}` | {r["K"] if imp else r["L"]} | {r["forced"] if imp else r["upper"]} | {r["gap"]} |')
n=C['nested108'];lines+=['\n## 3. Non-completable 108-cap histogram lemma\n',
'Exactly the following thirty sorted types survive the inherited necessary conditions. The nonnegative function called `phi` in the machine-readable data is denoted **psi** in the proof. Its full-direction sum is at most **18,044,648**.\n',
'| Type | psi(type) |','|---|---:|']
for t,val in zip(n['types'],n['phi']):lines.append(f'| {tuple(t)} | {val} |')
lines+=['\n### Rare-direction existence certificate\n',
'Except for `(45,41,22)`, `(44,43,21)`, and `(43,43,22)`, every listed type satisfies `E3-39*E2 >= -105001`. The forced sum is -38221470 and `364*(-105001)-(-38221470)=1106 > 0`. Thus at least one rare direction exists.\n',
'### Inner inequalities\n',
'Every inner row asserts `q*g(M) - sum_{s=0}^2 psi(t_s(M)) >= K`. The first seven features of g are the universal ones. The subsequent features, in the displayed order, are indicators that the specified column has the specified sorted type. Column indices are 0,1,2. Their sums come from the exactly checked unique histograms at sizes 43,44,45. The induced bound is `psi(t)+q*G_t-121*K`.\n']
for r in n['inner']:
 lines += [f'#### Type {tuple(r["type"])}\n',f'`q = {r["coeff"]}`\n',f'`K = {r["K"]}; histogram upper bound = {r["bound"]}`\n','Extra features (column, sorted type), in order:\n','```text',*map(str,r['extras']),'```\n']
lines+=['## 4. Extremal seven-dimensional certificates\n',
'Each case assumes the chosen whole-cap direction **globally minimizes Q**. The additional necessary tests are `Q(t_s(M)) >= Q(key)` for each of its three transverse whole-cap directions. Conclusions here are NOT unconditional slice exclusions and are NEVER fed to another case.\n',
'An unsplit row uses seven universal features. In a completed-status row append three features for each completed column, in increasing column index: family indicator, deletions from the original 22-point section, labelled deletions from the original 40-point section. Their summed values are `(56,11*d,110*d)`, d=112-column_size. Status 0 means non-completable; status 1 means completable.\n',
'| Type | First/second status | q | K | Summed upper bound U | Gap |','|---|---|---|---:|---:|---:|']
for k,r in sorted(C['extremal'].items()):
 for b in r.get('branches',[r]):
  if b.get('nested108'):
   z=n['outer'];lines.append(f'| ({k}) | 00, nested histogram | See below | {z["K"]} | {z["forced"]} | {z["gap"]} |')
  else:
   status='Unsplit' if 'status' not in b else ''.join(str(v) for v in b['status'][:2])
   lines.append(f'| ({k}) | {status} | `{b["coeff"]}` | {b["K"]} | {b["forced"]} | {b["gap"]} |')
r=n['outer']
lines+=['\n### Nested outer row: (108,108,62), status 00\n',
'The five ordinary feature groups are `(T, E2(alpha)+E2(beta), E3(alpha)+E3(beta), E2(gamma), E3(gamma))`.\n',
 f'`q = {r["coeff"]}`\n',
'Append `psi(sort(alpha)) + psi(sort(beta))`, with coefficient +1 on each. Each summed psi is at most 18,044,648.\n',
 f'`K = {r["K"]}; U = {r["forced"]}; 364*K-U = {r["gap"]}`\n',
'## 5. Final direction-minimum contradiction\n',
'`Q = 9*abc - 911*(ab+ac+bc) + 16306924`. There are 310 basic sorted triples of total 278 with entries at most 112. After the ordinary exclusions and the two seeds, nine Q-negative types remain, exactly those listed in Section 4. Every one is impossible for a globally minimizing direction. The forced sum over all 1093 directions is -148313, so a negative global minimum must exist. This is the contradiction.\n']
(D/'CERTIFICATE_TABLES.md').write_text('\n'.join(lines)+'\n')
print('Generated CERTIFICATE_TABLES.md')
