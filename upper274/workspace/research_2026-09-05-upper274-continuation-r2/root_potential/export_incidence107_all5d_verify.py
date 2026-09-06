"""P6 source/interface checks and integer input; no discovery records."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;B=P.parents[1]/'audit_2026-09-05_upper275/cap7_upper275'
cp=P/'incidence107_all5d_certificate_107_106_62.json';D=json.loads(cp.read_text());C=json.loads((B/'baseline277/baseline278/certificate.json').read_text())
funpath=P.parent/'compatibility/l2_all5d_10610663/FUNCTIONS.json';FUN=json.loads(funpath.read_text())['functions'];assert len(FUN)==33 and D['source_functions']==FUN and hashlib.sha256(funpath.read_bytes()).hexdigest()==D['source_functions_sha256']=='92a0104c9db8bf04b55e503e2e71f523178dd134ca25045480ea55093a6f5336'
source=json.loads((B/'results/size276/proof.json').read_text())['new_histograms']+[dict(json.loads((B/'baseline277/certificate.json').read_text())['nested108'],id='psi108',m=108)]
source+=json.loads((P/'transfer_tables.json').read_text())['functions']+json.loads((P.parent/'root_audit/h3_transport_tables.json').read_text())['functions']+json.loads((P.parent/'root_audit/incidence_histograms_independent.json').read_text())['functions'];sources={h['id']:h for h in source}
q=D['dual'];rows=D['rows'];assert len(q)==len(rows)and D['target']==[107,106,62]and D['state']==[0,0,-1]
assert rows[:2]==[['norm_outer'],['norm_inner']]and rows[2:9]==[['outer_centered_moment',i]for i in range(7)]
upper=[i for i,r in enumerate(rows)if r[0]=='outer_centered_upper'or(r[0]=='conditional_extra'and r[3]=='upper')];assert upper==D['upper_rows']and all(q[i]<=0 for i in upper)
assert q[0]+q[1]==D['rhs']>0
parse=lambda k:tuple(map(int,k.split(',')));old=[parse(k)for st in C['six_stages']for k in st];comp=list(map(tuple,C['completion_seeds']))+[parse(k)for st in C['completion_stages']for k in st]
sub=lambda t:t[2]<=22 or(t[0]<=40 and t[1]<=36);f6=old+[t for t in comp if not sub(t)]
seed=json.loads((P.parents[1]/'research_2026-09-05-capset-round1-r1/route_a/certificates.json').read_text());ban=list(map(tuple,seed['seeds']))+[parse(k)for st in seed['stages']for k in st]+[(112,109,51),(111,110,51)]
assert set(ban)==set(map(tuple,D['ordinary_bans']))
types=sorted(map(tuple,sources['nested107_size276']['types']));assert len(types)==47
def allows(t):return not any(all(a>=b for a,b in zip(t,u))for u in old+comp)
expected=sorted((a,b,107-a-b)for a in range(46)for b in range(a+1)if 0<=107-a-b<=b and allows((a,b,107-a-b)))
assert expected==types
parts=[' '.join(map(str,D['target'])),' '.join(map(str,q[:2])),' '.join(map(str,q[2:9]))]
for ts in [old,comp,f6,ban]:parts.append(str(len(ts)));parts+=[' '.join(map(str,t))for t in ts]
parts.append(str(len(FUN)))
for f in FUN:
    parts.append(' '.join(map(str,[f['size'],int(f['kind']=='upper'),f['bound'],len(f['types'])])))
    parts+=[' '.join(map(str,t+[v]))for t,v in zip(f['types'],f['values'])]
parts.append(str(len(types)))
for t in types:
    length=1+2*len(set(t));co=[q[rows.index(['conditional',list(t),k])]for k in range(length+1)]
    more=[]
    for f in FUN:
        r=['conditional_extra',list(t),f['name'],f['kind']]
        if f['size']in t:more.append(q[rows.index(r)])
        else:assert r not in rows;more.append(0)
    parts.append(' '.join(map(str,list(t)+[length]+co+more)))
funcs=D['functions'];assert len(funcs)==sum(r[0]=='outer_centered_upper'for r in rows);parts.append(str(len(funcs)))
for h in funcs:
    src=sources[h['id']];assert all(h[k]==src[k]for k in ['m','types','phi','bound'])and D['target'][h['column']]==h['m']
    i=rows.index(['outer_centered_upper',h['column'],h['id']]);parts.append(' '.join(map(str,[h['column'],q[i],h['bound'],len(h['types'])])))
    parts+=[' '.join(map(str,t+[v]))for t,v in zip(h['types'],h['phi'])]
(P/'incidence107_all5d_own_input.txt').write_text('\n'.join(parts)+'\n')
(P/'incidence107_all5d_interface_verification.json').write_text(json.dumps(dict(status='INTERFACE_AND_SIGNS_PASS_RAW_MATRICES_PENDING',certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),row_count=len(rows),upper_rows=len(upper),rhs=D['rhs'],source_functions=33),indent=2)+'\n');print('INTERFACE_PASS',len(rows),D['rhs'])
