#!/usr/bin/env python3
"""Full integer verification of 236 <= f(7,3) <= 278.

Python 3.10+, standard library only. Run `python3 verify.py` in any directory.
Published classification and rigidity inputs are listed precisely in README.md.
No optimizer, floating-point proof arithmetic, or failed cap search is trusted.
"""
from __future__ import annotations
import itertools,json,time
from pathlib import Path
from collections import Counter
from math import comb
import core as v
import verify_hill as hill
D=Path(__file__).resolve().parent

def sub112(t):
    a,b,c=sorted(t,reverse=True)
    return 0<=c and a<=45 and (c<=22 or (a<=40 and b<=36))

def extra_representative_checks():
    """Verify facts used by completion and by completed-column identities."""
    space=list(itertools.product(range(3),repeat=6));B=v.blocks()
    S=[p for p in space if (all(p) and p.count(2)%2==0) or
       frozenset(i for i,x in enumerate(p) if x) in B]
    dirs=[d for d in space if next((x for x in d if x),0)==1]
    fam1=[];fam2=[];cap45=None
    for d in dirs:
        buckets=[[p for p in S if hill.dot(p,d)==j] for j in range(3)]
        h=tuple(map(len,buckets))
        v.require(h in ((22,45,45),(40,36,36)), 'Centered representative spectrum')
        (fam1 if h[0]==22 else fam2).append(d)
        if cap45 is None and h[1]==45:
            pivot=next(i for i,x in enumerate(d) if x)
            cap45=[p[:pivot]+p[pivot+1:] for p in buckets[1]]
    v.require(len(fam1)==56 and len(fam2)==308,'Centered family sizes')
    for p in S:
        v.require(sum(hill.dot(p,d)==0 for d in fam1)==11,'Small-center point incidence')
        v.require(sum(hill.dot(p,d)==0 for d in fam2)==110,'Large-center point incidence')
    v.require(cap45 is not None and len(cap45)==45,'Missing 45-cap')
    v.check_cap(cap45,5)
    V5=list(itertools.product(range(3),repeat=5))
    diff=Counter(tuple((x-y)%3 for x,y in zip(p,q)) for p in cap45 for q in cap45)
    v.require(Counter(diff[z] for z in V5)==Counter({9:220,0:22,45:1}), '45-cap difference distribution')
    Z=[z for z in V5 if diff[z]==0]
    completed=[(0,)+p for p in cap45]+[(1,)+hill.neg(p) for p in cap45]+[(2,)+z for z in Z]
    v.require(len(completed)==112,'Reflected completion size');v.check_cap(completed,6)
    print('Completion representative: reflected 45-pair has 22 allowed points; positive multiplicities >=9; union is a 112-cap.',flush=True)
    print('Completed-slice identities: all 112 points have incidence 11 in the 56 small-center directions and 110 in the 308 large-center directions.',flush=True)

def completed_identities(N):
    """Type functions with known sums, justified by the representative checks
    and the deletion argument in README.md. Only used on completed columns."""
    v.require(103<=N<=112,'Unsupported completed size')
    types=[(a,b,N-a-b) for a in range(46) for b in range(a+1)
           if 0<=N-a-b<=b and sub112((a,b,N-a-b))]
    d=112-N
    funcs=[{'coeff':[int(t[2]<=22) for t in types],'sum':56},
           {'coeff':[22-t[2] if t[2]<=22 else 0 for t in types],'sum':11*d}]
    if N>=108:
        funcs.append({'coeff':[40-t[0] if t[2]>22 else 0 for t in types],'sum':110*d})
    v.SPECTRAL_TYPES[N]=types;v.SPECTRAL_IDENTITIES[N]=funcs
    return funcs

def completion_root(certificate,old_forbidden):
    rec=certificate['completion109_root'];q=rec['coeff'];K=rec['K']
    v.require(q==[-39,1],'Unexpected completion-root polynomial')
    uses=[tuple(t) for t in certificate['completion109_root_uses']]
    proved={v.parse_key(k) for stage in certificate['completion_stages'] for k in stage}
    v.require(all(t in proved for t in uses),'Unproved completion-root dependency')
    banned=old_forbidden+[tuple(t) for t in certificate['completion_seeds']]+uses
    allowed=[]
    for a in range(46):
        for b in range(a+1):
            t=(a,b,109-a-b)
            if 0<=t[2]<=b and v.original6(t) and v.downwards_allowed(t,banned):
                v.require(q[0]*v.e2(t)+q[1]*v.e3(t)>=K,'Completion-root inequality')
                allowed.append(t)
    F=q[0]*243*comb(109,2)+q[1]*81*comb(109,3)
    gap=364*K-F
    v.require(len(allowed)==24 and F==rec['forced'] and gap==rec['gap'] and gap>0,'109 completion-root gap')
    print(f'109-COMPLETION PASS: {len(allowed)} remaining noncompletion types; K={K}, forced={F}, gap={gap}.',flush=True)

def branch_check(key,rec,adm,masks,top_forbidden,complete_patterns):
    eligible=[j for j,N in enumerate(key) if 103<=N<109]
    statuses=[tuple(b['status']) for b in rec['branches']]
    required={tuple(s[eligible.index(j)] if j in eligible else -1 for j in range(3))
              for s in itertools.product((0,1),repeat=len(eligible))}
    v.require(len(statuses)==len(required) and set(statuses)==required,'Incomplete completion-status case split')
    total=0
    for branch in rec['branches']:
        state=branch['status'];r=dict(branch);r.pop('status');r['extra']=[]
        preds=[None,None,None]
        for j,N in enumerate(key):
            if state[j]==1:
                preds[j]=sub112
                for ident in completed_identities(N):r['extra'].append({'column':j,'identity':ident})
            elif state[j]==0:
                v.require(N>=103,'Completion propagation requires size >=103')
                preds[j]=lambda t:v.downwards_allowed(t,complete_patterns)
        label=' status='+''.join('-' if s<0 else str(s) for s in state)
        total+=v.local(key,r,7,45,adm,masks,top_forbidden,preds,label)
    return total

def main():
    start=time.monotonic();c=json.loads((D/'certificate.json').read_text())
    v.require(c['target_size']==279,'Wrong target')
    v.representatives();extra_representative_checks()
    hill.representative_checks();n_hill=hill.inequality_checks(D/'hill_certificate.json')
    # Register and verify all 5-dimensional spectral functions, including those
    # used only in conditional completion arguments.
    registry=dict(c);registry['six_stages']=c['six_stages']+c['completion_stages']
    v.verify_spectral_identities(registry)
    adm5=v.make_admissibility(20,v.admissible5);m5=v.make_masks(20,adm5)
    f6=[];n6=0
    for idx,stage in enumerate(c['six_stages']):
        print(f'DIMENSION SIX, UNIVERSAL STAGE {idx}: {len(stage)} cases.',flush=True)
        snapshot=list(f6)
        for k,r in sorted(stage.items()):
            key=v.parse_key(k);v.require(key not in f6,'Repeated universal type')
            n6+=v.local(key,r,6,20,adm5,m5,snapshot)
        f6.extend(v.parse_key(k) for k in stage)
    old_forbidden=list(f6)
    seeds=[tuple(t) for t in c['completion_seeds']]
    v.require(seeds==[(45,45,7),(45,43,15),(44,44,15),(45,42,20)],'Incorrect published completion seeds')
    comp=list(seeds);nc=0;new_universal=[]
    for idx,stage in enumerate(c['completion_stages']):
        print(f'DIMENSION SIX, CONDITIONAL COMPLETION STAGE {idx}: {len(stage)} cases.',flush=True)
        snapshot=old_forbidden+comp
        for k,r in sorted(stage.items()):
            key=v.parse_key(k)
            v.require(sum(key)>=103 and key not in comp,'Invalid completion-propagation size or duplicate')
            nc+=v.local(key,r,6,20,adm5,m5,snapshot)
        # No same-stage conclusion is used before the stage is finished.
        for k in stage:
            key=v.parse_key(k);comp.append(key)
            if not sub112(key):new_universal.append(key)
    completion_root(c,old_forbidden)
    f6.extend(new_universal)
    print(f'Conditional completion yielded {len(new_universal)} additional universal slice exclusions.',flush=True)
    adm6=v.make_admissibility(45,lambda t:v.original6(t) and
                             (sum(t)<109 or sub112(t)) and v.downwards_allowed(t,f6))
    m6=v.make_masks(45,adm6)
    seeds7=[tuple(t) for t in c['seven_seed_exclusions']]
    v.require(seeds7==[(112,112,29)],'Unsupported seven-dimensional seed')
    f7=list(seeds7);n7=0;nbranch=0
    for idx,stage in enumerate(c['seven_stages']):
        print(f'DIMENSION SEVEN, STAGE {idx}: {len(stage)} slice types.',flush=True)
        snapshot=list(f7)
        for k,r in sorted(stage.items()):
            key=v.parse_key(k);v.require(sum(key)==279 and key not in f7,'Wrong or repeated seven-dimensional type')
            if 'branches' in r:
                nbranch+=len(r['branches']);n7+=branch_check(key,r,adm6,m6,snapshot,comp)
            else:n7+=v.local(key,r,7,45,adm6,m6,snapshot)
        f7.extend(v.parse_key(k) for k in stage)
    root=c['root'];q=root['coeff'];K=root['K'];allowed=0;excluded=0
    v.require(q==[-305,3] and K==-5500764,'Unexpected final polynomial')
    for a in range(113):
        for b in range(a+1):
            t=(a,b,279-a-b);z=t[2]
            if not 0<=z<=b:continue
            if not v.downwards_allowed(t,f7):excluded+=1;continue
            allowed+=1
            P=3*v.e3(t)-305*v.e2(t)+5500764
            v.require(67<=z<=93 and 4*P==3*(z-93)**2*(z-67)+(305-3*z)*(a-b)**2 and P>=0,'Root factorization or nonnegativity')
    F=q[0]*729*comb(279,2)+q[1]*243*comb(279,3);gap=1093*K-F
    v.require((allowed,excluded)==(231,69) and F==root['forced'] and gap==root['gap'] and gap>0,'Final contradiction gap')
    print(f'Root: {allowed} allowed types, {excluded} excluded types, K={K}, forced={F}, gap={gap}.',flush=True)
    print(f'FULL PASS: {n6} original six-dimensional matrices; {nc} conditional six-dimensional matrices; {n7} seven-dimensional case-matrix evaluations; {nbranch} completion-status branches; {n_hill} two-112-slice state inequalities.',flush=True)
    print('Under the published mathematical inputs in README.md, no 279-point cap exists; 236 <= f(7,3) <= 278.',flush=True)
    print(f'Elapsed verification seconds: {time.monotonic()-start:.3f}',flush=True)
if __name__=='__main__':main()
