"""Independent exact finite root/profile/status arithmetic; no research imports."""
from pathlib import Path
from math import comb, prod
from itertools import product
from collections import Counter
import json, hashlib, time
W=Path(__file__).resolve().parent;R=W.parents[1];M=R.parent
INPUTS={}
def read(p):
    raw=p.read_bytes();INPUTS[str(p.relative_to(M))]=hashlib.sha256(raw).hexdigest();return json.loads(raw)
def key(s):return tuple(map(int,s.split(',')))
def q(t):a,b,c=t;return 9*a*b*c-899*(a*b+a*c+b*c)+15730000
def dominates(t,s):return all(x>=y for x,y in zip(t,s))
def states(t):return set(product(*[(0,1)if 103<=n<=108 else(1,)if n>=109 else(-1,)for n in t]))
def validate_integer_certificate(c):
    assert all(type(v)is int for v in c['coeff'])
    assert type(c['K'])is int and type(c['forced'])is int
    assert c['gap']==364*c['K']-c['forced']>0

def main():
    begin=time.monotonic();A=M/'research_2026-09-05-capset-round1-r1';cert=read(A/'route_a/certificates.json');ledger=read(A/'route_a/case_ledger.json');prior=read(A/'root_audit/integration_checks.json');reg=read(R/'RESEARCH_OUTPUT_REGISTRY.json')
    assert prior['status']=='PASS'and prior['a_exact_cases']==88 and prior['a_matrices']==153548040
    audited_snapshot=read(A/'root_audit/audited_certificate_snapshot.json');assert audited_snapshot==cert
    deletion_audit=read(A/'root_audit/deleted3_independent_result.json')
    read(A/'root_audit/deleted3_certificate.json')
    assert deletion_audit['status']=='PASS_EXACT_FINITE_CERTIFICATE'and deletion_audit['derived_third_layer_bound']==50
    assert deletion_audit['coefficient_sha256']==INPUTS[str((A/'root_audit/deleted3_certificate.json').relative_to(M))]
    assert ledger['certificate_sha256']==INPUTS[str((A/'route_a/certificates.json').relative_to(M))]
    inherited=[(112,112,29),(112,111,35),(112,110,45),(111,111,45)]
    deletion=[(112,109,51),(111,110,51)]
    assert cert['size']==275 and cert['k']==67 and cert['root_sum']==-246950
    assert list(map(tuple,cert['seeds']))==inherited
    ordinary=[]
    for stage in cert['stages']:
        for name,c in stage.items():ordinary.append(key(name));validate_integer_certificate(c)
    assert [len(z)for z in cert['stages']]==[12,0]and set(ordinary)==set(map(tuple,prior['ordinary_types']))
    bans=inherited+ordinary+deletion;assert len(bans)==len(set(bans))==18
    # Independent loop order: smallest section first, recover the largest.
    types=[]
    for c in range(113):
        for b in range(c,113):
            a=275-b-c
            if b<=a<=112:types.append((a,b,c))
    assert len(types)==len(set(types))==341
    for a,b,c in types:assert 4*q((a,b,c))==(3*c-275)**2*(c-67)+(899-9*c)*(a-b)**2
    total=9*3**5*comb(275,3)-899*3**6*comb(275,2)+((3**7-1)//2)*15730000
    assert total==-246950 and (3**7-1)//2==1093
    negatives={t for t in types if q(t)<0};assert len(negatives)==56
    oldbans=inherited+ordinary
    before=[t for t in negatives if not any(dominates(t,s)for s in oldbans)];assert len(before)==40
    ledger_by={tuple(z['type']):z for z in ledger['types']};assert set(ledger_by)==set(types)
    certs_used=set();residual_before_deletion=set();residual=set();rows=[]
    for t in types:
        st=states(t);ext=cert['extremal'].get(','.join(map(str,t)));covered=set()
        if ext:
            if 'branches'in ext:
                assert len(ext['branches'])==len(st)
                assert {tuple(b['status'])for b in ext['branches']}==st
                for i,b in enumerate(ext['branches']):
                    if b['certificate']:
                        validate_integer_certificate(b['certificate']);covered.add(tuple(b['status']));certs_used.add((t,i))
            else:validate_integer_certificate(ext);covered=st;certs_used.add((t,None))
        out=[]
        for s in sorted(st):
            if any(dominates(t,b)for b in oldbans):why='ORDINARY_OLD_AND_STAGE0'
            elif q(t)>=0:why='NONNEGATIVE_NOT_GLOBAL_MINIMUM'
            elif s in covered:why='ACCEPTED_R1_MINIMUM_CERTIFICATE'
            else:residual_before_deletion.add((t,s));why='OPEN_BEFORE_THREE_DELETION'
            if why=='OPEN_BEFORE_THREE_DELETION':
                if any(dominates(t,b)for b in deletion):why='RECOVERED_THREE_DELETION_ORDINARY'
                else:residual.add((t,s));why='R1_RESIDUAL'
            out.append(dict(state=s,reason=why))
        expected={tuple(c['status'])for c in ledger_by[t]['completion_cases']if c['conclusion']=='OPEN'}
        assert expected=={s for tt,s in residual if tt==t}
        rows.append(dict(type=t,Q67=q(t),completion_states=out))
    assert len(certs_used)==76 and len(residual_before_deletion)==10 and len(residual)==8
    assert residual_before_deletion=={(tuple(t),tuple(s))for t,s in prior['open_before_three_deletion']}
    assert residual=={(tuple(t),tuple(s))for t,s in prior['remaining_minimum_states']}
    entries={e['id']:e for e in reg['entries']}
    closure_specs=[
      ('H3-THETA40-PHI105-MIN10510565',(105,105,65),'hist105106/h3/h3_result.json','h3_independent.json',1926831607),
      ('L-THETA40-INCIDENCE-MIN10810760',(108,107,60),'compatibility/theta40/EXACT_DUAL.json','incidence_independent.json',21167272),
      ('P3B-POINTED107-TRANSFER108-MIN10810661',(108,106,61),'root_potential/pointed_joint_certificate.json','pointed_joint_outer_independent.json',1993186322),
      ('L-THETA40-INCIDENCE-MIN10710761',(107,107,61),'compatibility/theta40_10710761/EXACT_DUAL.json','incidence_sym_independent.json',9410019729),
      ('P5-SHARED107-MIN10710563',(107,105,63),'root_potential/incidence107_certificate_107_105_63.json','incidence_p5_independent.json',39396474454),
      ('P6-ALL5D-SHARED107-MIN10710662',(107,106,62),'root_potential/incidence107_all5d_certificate_107_106_62.json','incidence_p6_independent.json',456644586)]
    closed=[]
    for ident,t,cp,ap,gap in closure_specs:
        e=entries[ident];c=read(R/cp);audit=read(R/'root_audit'/ap)
        sha=INPUTS[str((R/cp).relative_to(M))];assert sha==e['certificate_hash']
        assert audit['status']in('PASS','EXACT_ROOT_INDEPENDENT_PASS')and e['ordinary_exclusion']is False
        ah=audit.get('source_sha256',audit.get('candidate_sha256'));assert ah==sha
        ag=next(audit[x]for x in ['gap','positive_rhs','positive_gap','claimed_positive_rhs','strict_rhs']if x in audit);assert ag==gap>0
        if ident.startswith('P3B'):
            local=read(R/'root_audit/pointed_joint_independent.json');assert local['status']=='PASS'and local['original_joint_sha256']==sha
        assert(t,(0,0,-1))in residual
        closed.append(dict(registry_id=ident,type=t,state=(0,0,-1),certificate_sha256=sha,audit_path='root_audit/'+ap,positive_gap=gap,ordinary_exclusion=False))
    current=residual-{(tuple(z['type']),tuple(z['state']))for z in closed}
    assert current=={((106,106,63),(0,0,-1)),((106,105,64),(0,0,-1))}
    result=dict(status='PASS_CONDITIONAL_GLOBAL_BRIDGE_ONLY',directions=1093,complete_type_count=341,negative_type_count=56,root_total=total,root_coefficients=[9,-899,15730000],ordinary_bans=bans,negative_after_four_plus12_ordinary=len(before),r1_ordinary_certificates=12,r1_minimum_certificates=len(certs_used),before_three_deletion=[dict(type=t,state=s)for t,s in sorted(residual_before_deletion)],r1_residuals=[dict(type=t,state=s)for t,s in sorted(residual)],accepted_new_minimum_closures=closed,remaining=[dict(type=t,state=s,Q67=q(t))for t,s in sorted(current)],conditional_statement='If both remaining minimum states are independently excluded, every275-point cap inF3^7 is impossible and C7<=274 follows by taking a275-subset of any larger cap.',candidate10610564_used=False,no_matrix_enumeration_or_optimizer=True,all_type_state_rows=rows,input_sha256=INPUTS,seconds=time.monotonic()-begin)
    assert result['seconds']<180
    (W/'GLOBAL_BRIDGE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ['status','complete_type_count','negative_type_count','root_total','r1_minimum_certificates','remaining','seconds']},indent=2))
if __name__=='__main__':main()
