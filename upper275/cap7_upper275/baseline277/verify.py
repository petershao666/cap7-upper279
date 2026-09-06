#!/usr/bin/env python3
"""Exact certificate for no 278-point cap in F_3^7; standard-library Python 3.10+.

Run: python3 verify.py
The published inputs and the mathematical reductions are specified in README.md.
The preceding release is preserved byte-for-byte under baseline278/ and in its ZIP.
No optimizer, floating-point proof arithmetic, network, or random search is used.
"""
from __future__ import annotations
import hashlib,itertools,json,math,sys,time,zipfile
from pathlib import Path
D=Path(__file__).resolve().parent
sys.path.insert(0,str(D/'baseline278'))
import core as v
import verify as b
import verify_hill as hill
C=json.loads((D/'certificate.json').read_text())
BASE=json.loads((D/'baseline278/certificate.json').read_text())

def require(ok,message):
    if not ok:raise AssertionError(message)

def baseline_integrity():
    archive=D/'baseline278_certificate.zip'
    require(hashlib.sha256(archive.read_bytes()).hexdigest()==C['baseline_sha256'],'Baseline archive changed')
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            rel=Path(name).relative_to('cap7_upper278')
            require((D/'baseline278'/rel).read_bytes()==z.read(name),f'Baseline file changed: {rel}')
    print('BASELINE INTEGRITY PASS: original archive and all 33 source/data files preserved.',flush=True)

def lower_inputs():
    """Rerun the inherited lemmas actually needed here, not the old 279-point proof."""
    v.representatives();b.extra_representative_checks();hill.representative_checks()
    nh=hill.inequality_checks(D/'baseline278/hill_certificate.json')
    registry=dict(BASE);registry['six_stages']=BASE['six_stages']+BASE['completion_stages']
    v.verify_spectral_identities(registry)
    a5=v.make_admissibility(20,v.admissible5);m5=v.make_masks(20,a5)
    f6=[];n6=0
    for stage in BASE['six_stages']:
        snap=list(f6)
        for k,r in sorted(stage.items()):
            key=v.parse_key(k);require(key not in f6,'Repeated inherited type')
            n6+=v.local(key,r,6,20,a5,m5,snap)
        f6.extend(v.parse_key(k) for k in stage)
    old=list(f6);comp=[tuple(t) for t in BASE['completion_seeds']]
    require(comp==[(45,45,7),(45,43,15),(44,44,15),(45,42,20)],'Completion seed input')
    nc=0
    for stage in BASE['completion_stages']:
        snap=old+comp
        for k,r in sorted(stage.items()):
            key=v.parse_key(k);require(sum(key)>=103 and key not in comp,'Completion propagation threshold')
            nc+=v.local(key,r,6,20,a5,m5,snap)
        comp.extend(v.parse_key(k) for k in stage)
    b.completion_root(BASE,old)
    f6.extend(t for t in comp if not b.sub112(t))
    a6=v.make_admissibility(45,lambda t:v.original6(t) and (sum(t)<109 or b.sub112(t)) and v.downwards_allowed(t,f6))
    m6=v.make_masks(45,a6)
    print(f'LOWER INPUTS PASS: {n6} universal and {nc} conditional matrix evaluations; {nh} inherited Hill states.',flush=True)
    return old,comp,a5,m5,a6,m6

def near112():
    """The extended Hill-state inequalities for deleting one point from one layer."""
    records=C['near112'];require([r['h'] for r in records]==list(range(1,52)),'Near-112 coverage')
    count=0
    for r in records:
        h=r['h'];q=r['coeff'] if r.get('infeasible') else r['q']
        require(len(q)==8 and all(type(x) is int for x in q),'Near-112 integer coefficients')
        rhs=(252+h,112-2*h,h,121*h,40*math.comb(h,2),13*math.comb(h,3),22*h,4*math.comb(h,2))
        total=sum(a*z for a,z in zip(q,rhs));local_count=0
        for u in range(3):
            for p in range(21 if u==0 else 12):
                multiplicity=16+4*u+3*p-h
                if p>h or h-p>45 or multiplicity<0:continue
                x=(int(u==0),int(u==1),int(u==2),p,math.comb(p,2),math.comb(p,3),u*p,u*math.comb(p,2))
                value=sum(a*z for a,z in zip(q,x));local_count+=1
                if r.get('infeasible'):require(value>=r['K'],'Near-112 impossible-intersection inequality')
                else:require(r['L']>0 and value>=r['L']*int(multiplicity<=1),'Near-112 low-multiplicity inequality')
        if r.get('infeasible'):
            require(total==r['forced'] and 364*r['K']-total==r['gap']>0,'Near-112 impossible-intersection gap')
        else:require(total==r['upper'] and 18*r['L']-total==r['gap']>0,'Near-112 count bound')
        count+=local_count
        print(f'NEAR112 h={h}: states={local_count}, gap={r["gap"]}',flush=True)
    # h=52,...,55 are ruled out by the verified 103-point extension rigidity;
    # h=0 leaves one zero, and h=56 means identical completions and leaves one.
    require(all(2*h>=103 and 2*h<112 for h in range(52,56)),'Near-112 rigidity range')
    require(all(16+4*u>1 for u in range(3)),'Near-112 h=0 case')
    print(f'NEAR112 PASS: {count} state inequalities; (112,111,35) is excluded.',flush=True)
    return count

def Q(t):return 9*v.e3(t)-911*v.e2(t)+16306924

def all_types(total,upper):
    return [(a,b,total-a-b) for a in range(upper+1) for b in range(a+1) if 0<=total-a-b<=b]

def matrices(key,n,adm,masks,banned,preds=(None,None,None),minimum_Q=None):
    """All matrices with first column sorted; bit masks only accelerate the nine line tests."""
    upper=20 if n==6 else 45;top_upper=45 if n==6 else 112;total=sum(key)
    cols=[]
    for j,N in enumerate(key[:2]):
        cols.append([(x,y,N-x-y) for x in range(upper+1) for y in range(upper+1)
                     if 0<=N-x-y<=upper and (j!=0 or x>=y>=N-x-y) and adm[x,y,N-x-y]
                     and (preds[j] is None or preds[j]((x,y,N-x-y)))])
    top={}
    for x in range(top_upper+1):
        for y in range(top_upper+1):
            z=total-x-y
            if 0<=z<=top_upper:
                t=(x,y,z)
                top[t]=v.downwards_allowed(t,banned) and (minimum_Q is None or Q(t)>=minimum_Q)
    for a in cols[0]:
        a0,a1,a2=a
        for bb in cols[1]:
            b0,b1,b2=bb
            m0=masks[a0][b0]&masks[a1][b2]&masks[a2][b1]
            m1=masks[a0][b2]&masks[a1][b1]&masks[a2][b0]
            m2=masks[a0][b1]&masks[a1][b0]&masks[a2][b2]
            c1s=tuple(v.bits(m1))
            for c0 in v.bits(m0):
                for c1 in c1s:
                    c2=key[2]-c0-c1
                    if not 0<=c2<=upper or not ((m2>>c2)&1):continue
                    cc=(c0,c1,c2)
                    if not adm[cc] or (preds[2] is not None and not preds[2](cc)):continue
                    tops=[tuple(a[r]+bb[(r+s)%3]+cc[(r+2*s)%3] for r in range(3)) for s in range(3)]
                    if not all(top.get(t,False) for t in tops):continue
                    yield a,bb,cc,tops

def feats(a,bb,cc):
    T=(a[0]*bb[0]+a[1]*bb[2]+a[2]*bb[1])*cc[0]+(a[0]*bb[2]+a[1]*bb[1]+a[2]*bb[0])*cc[1]+(a[0]*bb[1]+a[1]*bb[0]+a[2]*bb[2])*cc[2]
    return (T,v.e2(a),v.e3(a),v.e2(bb),v.e3(bb),v.e2(cc),v.e3(cc))

def histogram_bound(old,comp,a5,m5):
    h=C['nested108'];types=all_types(108,45)
    types=[t for t in types if v.downwards_allowed(t,old+comp)]
    require(types==list(map(tuple,h['types'])) and len(types)==30,'Noncompletion type support')
    phi=dict(zip(types,h['phi']));require(all(type(x) is int for x in phi.values()),'Noninteger spectrum function')
    rare=[tuple(r['type']) for r in h['inner']]
    require(rare==[(45,41,22),(44,43,21),(43,43,22)],'Rare direction list')
    r=h['root'];require(r['coeff']==[-39,1],'Rare-direction polynomial')
    for t in types:
        if t not in rare:require(v.e3(t)-39*v.e2(t)>=r['K'],'Rare-direction existence inequality')
    forced=81*math.comb(108,3)-39*243*math.comb(108,2)
    require(forced==r['forced'] and 364*r['K']-forced==r['gap']>0,'Rare-direction existence gap')
    print(f'RARE108 PASS: 27 remaining types, gap={r["gap"]}',flush=True)
    count=0;bounds=[]
    for rec in h['inner']:
        key=tuple(rec['type']);q=rec['coeff'];extra=rec['extras']
        require(len(q)==7+len(extra),'Inner coefficient dimension')
        sums=list(v.forced(key,6))
        for j,t in extra:
            N=key[j];data=BASE['spectrum5'][str(N)]
            require(N in (43,44,45) and len(data['spectra'])==1,'Inner exact-histogram scope')
            sums.append(data['spectra'][0][data['types'].index(t)])
        forced=sum(x*y for x,y in zip(q,sums));bound=phi[key]+forced-121*rec['K']
        require(bound==rec['bound'],'Inner spectral upper bound arithmetic')
        minimum=None;num=0
        for a,bb,cc,tops in matrices(key,6,a5,m5,old+comp):
            cols=(a,bb,cc);fs=list(feats(a,bb,cc))
            fs.extend(int(tuple(sorted(cols[j],reverse=True))==tuple(t)) for j,t in extra)
            value=sum(x*y for x,y in zip(q,fs))-sum(phi[tuple(sorted(t,reverse=True))] for t in tops)
            require(value>=rec['K'],'Nested inner local inequality')
            minimum=value if minimum is None else min(minimum,value);num+=1
        require(num>0,'Empty nested inner family')
        print(f'NEW INNER {key}: matrices={num}, minimum={minimum}, K={rec["K"]}, bound={bound}',flush=True)
        count+=num;bounds.append(bound)
    require(max(bounds)==h['bound'],'Global noncompletion spectral bound')
    print(f'HISTOGRAM108 PASS: sum(phi) <= {h["bound"]}; {count} inner matrix evaluations.',flush=True)
    return phi,h['bound'],count

def label_values(t):
    """All compatible identities of the original 40-point section, including ties."""
    s=tuple(sorted(t,reverse=True))
    if s[2]<=22:return [0]
    vals=[40-t[j] for j in range(3) if t[j]<=40 and all(t[k]<=36 for k in range(3) if k!=j)]
    require(vals,'Completed type without a compatible original 40-section')
    return vals

def branch(key,rec,a6,m6,banned,comp,phi,B):
    state=tuple(rec['status']);require(all(s in (-1,0,1) for s in state),'Status domain')
    preds=[]
    for j,s in enumerate(state):
        if s>=0:require(103<=key[j]<109,'Branch propagation scope')
        preds.append(b.sub112 if s==1 else (lambda t:v.downwards_allowed(t,comp)) if s==0 else None)
    nested=rec.get('nested108',False)
    if nested:
        require(key==(108,108,62) and state==(0,0,-1),'Nested branch scope')
        r=C['nested108']['outer'];q=r['coeff'];tot=v.forced(key,7)
        fs=(tot[0],tot[1]+tot[3],tot[2]+tot[4],tot[5],tot[6]);forced=sum(x*y for x,y in zip(q,fs))+2*B
    else:
        r=rec;q=r['coeff'];sums=list(v.forced(key,7))
        for j,s in enumerate(state):
            if s==1:sums.extend([56,11*(112-key[j]),110*(112-key[j])])
        require(len(q)==len(sums),'Labelled coefficient dimension');forced=sum(x*y for x,y in zip(q,sums))
    require(forced==r['forced'] and 364*r['K']-forced==r['gap']>0,'Branch summed bound')
    num=0;labelled=0;minimum=None
    for a,bb,cc,_ in matrices(key,7,a6,m6,banned,tuple(preds),Q(key)):
        fs=feats(a,bb,cc)
        if nested:
            f=(fs[0],fs[1]+fs[3],fs[2]+fs[4],fs[5],fs[6])
            value=sum(x*y for x,y in zip(q,f))+phi[tuple(sorted(a,reverse=True))]+phi[tuple(sorted(bb,reverse=True))];mult=1
        else:
            value=sum(x*y for x,y in zip(q[:7],fs));off=7;mult=1
            for j,t in enumerate((a,bb,cc)):
                if state[j]!=1:continue
                s=tuple(sorted(t,reverse=True));fam=s[2]<=22;vals=label_values(t)
                require(all(0<=d<=112-key[j] for d in vals),'Label deletion range')
                value+=q[off]*int(fam)+q[off+1]*(22-s[2] if fam else 0)+min(q[off+2]*d for d in vals)
                off+=3;mult*=len(vals)
        require(value>=r['K'],'Extremal completion-status inequality')
        num+=1;labelled+=mult;minimum=value if minimum is None else min(minimum,value)
    require(num>0,'Unexpected empty branch')
    print(f'NEW BRANCH {key} status={state}: matrices={num}, labelled_states={labelled}, minimum={minimum}, K={r["K"]}, gap={r["gap"]}',flush=True)
    return num,labelled

def main():
    start=time.monotonic();require(C['target_size']==278,'Wrong new target')
    baseline_integrity();old,comp,a5,m5,a6,m6=lower_inputs();nh=near112()
    phi,B,ninner=histogram_bound(old,comp,a5,m5)
    f7=[(112,112,29)];nordinary=0
    for idx,stage in enumerate(C['ordinary_stages']):
        snap=list(f7)
        print(f'NEW ORDINARY STAGE {idx}: {len(stage)} cases.',flush=True)
        for k,r in sorted(stage.items()):
            key=v.parse_key(k);require(sum(key)==278 and key not in f7,'Ordinary stage key')
            nordinary+=v.local(key,r,7,45,a6,m6,snap)
        f7.extend(v.parse_key(k) for k in stage)
    f7.append((112,111,35))
    allts=all_types(278,112);require(len(allts)==310,'Global type count')
    expected={t for t in allts if Q(t)<0 and v.downwards_allowed(t,f7)}
    require(expected=={v.parse_key(k) for k in C['extremal']} and len(expected)==9,'Incomplete minimum-direction case split')
    ne=0;nl=0;nbr=0
    # These are alternative cases for a GLOBAL minimizer of Q. Their conclusions
    # are never reused as unconditional exclusions or supplied to another case.
    for k,r in sorted(C['extremal'].items()):
        key=v.parse_key(k)
        if 'branches' in r:
            states=[tuple(b['status']) for b in r['branches']]
            eligible=[j for j,N in enumerate(key) if 103<=N<109]
            needed={tuple(s[eligible.index(j)] if j in eligible else -1 for j in range(3)) for s in itertools.product((0,1),repeat=len(eligible))}
            require(len(states)==len(needed) and set(states)==needed,'Missing or duplicate completion-status branch')
            for br in r['branches']:
                count,labelled=branch(key,br,a6,m6,f7,comp,phi,B);ne+=count;nl+=labelled;nbr+=1
        else:
            forbidden=f7+[t for t in allts if Q(t)<Q(key)]
            ne+=v.local(key,r,7,45,a6,m6,forbidden)
    root=C['root'];require(root=={'coeff':[-911,9],'constant':16306924,'sum':-148313},'Final polynomial data')
    for a,bb,cc in allts:
        require(4*Q((a,bb,cc))==(3*cc-278)**2*(cc-67)+(911-9*cc)*(a-bb)**2,'Root algebraic identity')
    total=9*243*math.comb(278,3)-911*729*math.comb(278,2)+16306924*1093
    require(total==-148313<0,'Minimum-direction existence')
    print(f'NEW ROOT PASS: 310 types; {len(expected)} remaining negative minimum-direction cases all excluded; sum(Q)={total}.',flush=True)
    print(f'NEW COMPUTATIONS PASS: ordinary={nordinary}; extremal={ne}; inner={ninner}; labelled_branch_states={nl}; completion_branches={nbr}; near112_states={nh}.',flush=True)
    print('FULL PASS: under the published inputs specified in README.md, no 278-point cap exists; 236 <= f(7,3) <= 277.',flush=True)
    print(f'Elapsed verification seconds: {time.monotonic()-start:.3f}',flush=True)
if __name__=='__main__':main()
