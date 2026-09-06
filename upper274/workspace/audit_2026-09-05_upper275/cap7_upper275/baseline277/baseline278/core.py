#!/usr/bin/env python3
"""Shared exact verification kernel for the upper-278 certificate.

Python 3.10+, standard library only. Run from any directory:
    python3 verify.py

Mathematical dependencies (not re-proved by this program): the published
four-, five-, and six-dimensional classification results specified in README.md.
All new finite claims are checked exhaustively using integer arithmetic.
No optimizer, floating-point arithmetic, downloaded data, or heuristic search
is part of this verifier.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import time

Triple = tuple[int,int,int]

def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)

def e2(t):
    a,b,c=t
    return a*b+a*c+b*c

def e3(t):
    return t[0]*t[1]*t[2]

def forced(key,n):
    A,B,C=key
    return (((3**(n-2)-1)//2)*A*B*C,
            3**(n-2)*comb(A,2),3**(n-3)*comb(A,3),
            3**(n-2)*comb(B,2),3**(n-3)*comb(B,3),
            3**(n-2)*comb(C,2),3**(n-3)*comb(C,3))

def blocks():
    return {frozenset(int(i)-1 for i in word) for word in
            ('123','124','135','146','156','236','245','256','345','346')}

def check_cap(points,dimension):
    S=set(points)
    require(len(S)==len(points),'Duplicate points')
    require(all(len(p)==dimension and all(v in (0,1,2) for v in p) for p in S),
            'Invalid point')
    for x,y in combinations(points,2):
        require(tuple((-a-b)%3 for a,b in zip(x,y)) not in S,'Forbidden triple')

def representatives():
    space=list(product(range(3),repeat=6));B0=blocks()
    B1={frozenset(range(6))-b for b in B0}
    R=[p for p in space if all(p) and p.count(2)%2==0]
    D0=[p for p in space if frozenset(i for i,v in enumerate(p) if v) in B0]
    D1=[p for p in space if frozenset(i for i,v in enumerate(p) if v) in B1]
    S=R+D0
    require(len(S)==112,'Wrong representative size')
    check_cap(S,6)
    secants=Counter(tuple((-a-b)%3 for a,b in zip(x,y)) for x,y in combinations(S,2))
    require(Counter(secants[p] for p in space if p not in set(S))==Counter({10:616,56:1}),
            'Exterior secant distribution')
    dirs=[d for d in space if next((v for v in d if v),0)==1]
    spectrum=Counter()
    for d in dirs:
        h=[0,0,0]
        for p in S:h[sum(a*b for a,b in zip(d,p))%3]+=1
        spectrum[tuple(sorted(h,reverse=True))]+=1
    require(len(dirs)==364 and spectrum==Counter({(45,45,22):56,(40,36,36):308}),
            '112-cap spectrum')
    U=[p for p in space if sum(v!=0 for v in p)==1]
    cap=[(0,)+p for p in R+D0]+[(1,)+p for p in R+D1]+[(2,)+p for p in U]
    require(len(cap)==236,'Wrong lower-bound cardinality')
    check_cap(cap,7)
    print('112-cap: cap, spectrum, and secants verified. 236-cap: all 27730 pairs verified.',flush=True)

DELTA={(20,16,6):3,(18,18,6):4,(18,17,7):18,(18,12,12):6,
       (16,15,11):24,(16,14,12):36,(15,15,12):3,(14,14,14):27}

def admissible5(t):
    a,b,c=sorted(t,reverse=True);s=a+b+c
    if c<0 or a>20 or s>45:return False
    if s<42:return True
    subset45=(a<=18 and b<=18 and c<=9) or a<=15
    if s>=43:return subset45
    return subset45 or (a,b,c) in DELTA

def original6(t):
    a,b,c=sorted(t,reverse=True);s=a+b+c
    if c<0 or a>45 or s>112:return False
    if s<110:return True
    return c<=22 or (a<=40 and b<=36)

def downwards_allowed(t,forbidden):
    ordered=sorted(t,reverse=True)
    return not any(all(u>=v for u,v in zip(ordered,k)) for k in forbidden)

def make_admissibility(upper,predicate):
    # All lookup entries are explicitly generated; no absent entry is assumed true.
    return {(a,b,c):predicate((a,b,c)) for a,b,c in product(range(upper+1),repeat=3)}

def make_masks(upper,adm):
    return [[sum(1<<c for c in range(upper+1) if adm[a,b,c])
             for b in range(upper+1)] for a in range(upper+1)]

def bits(mask):
    while mask:
        bit=mask&-mask
        yield bit.bit_length()-1
        mask-=bit

def parse_key(key):
    t=tuple(map(int,key.split(',')))
    require(len(t)==3 and t[0]>=t[1]>=t[2]>=0,'Invalid certificate key')
    return t

def local(key,record,n,upper,adm,masks,top_forbidden=(),column_predicates=None,label=""):
    A,B,C=key
    if column_predicates is None: column_predicates=(None,None,None)
    empty=record.get('empty',False)
    if empty:record={'coeff':[0]*7,'K':0,'forced':0,'gap':0}
    coeff=record['coeff'];K=record['K']
    require(len(coeff)==7+len(record.get('extra',[])) and all(type(x) is int for x in coeff+[K]),'Noninteger coefficients')
    nd=(3**(n-1)-1)//2
    S=sum(x*y for x,y in zip(coeff[:7],forced(key,n)))
    phis=[{} for _ in range(3)]
    for q,extra in zip(coeff[7:],record.get('extra',[])):
        j=extra['column'];N=key[j];identity=extra['identity']
        require(N in SPECTRAL_IDENTITIES and identity in SPECTRAL_IDENTITIES[N], 'Unverified spectral identity')
        require(identity.get('bound','exact') == 'exact' or q >= 0, 'Negative multiplier of upper bound')
        S+=q*identity['sum']
        for t,v in zip(SPECTRAL_TYPES[N],identity['coeff']):
            for perm in set(__import__('itertools').permutations(t)):
                phis[j][perm]=phis[j].get(perm,0)+q*v
    gap=nd*K-S
    require(S==record['forced'] and gap==record['gap'] and (gap>0 or empty),'Incorrect or nonpositive gap')
    colA=[(a,b,A-a-b) for a in range(upper+1) for b in range(a+1)
          if 0<=A-a-b<=b and adm[a,b,A-a-b] and (column_predicates[0] is None or column_predicates[0]((a,b,A-a-b))) ]
    colB=[(a,b,B-a-b) for a in range(upper+1) for b in range(upper+1)
          if 0<=B-a-b<=upper and adm[a,b,B-a-b] and (column_predicates[1] is None or column_predicates[1]((a,b,B-a-b))) ]
    # Precompute the complete top-level admissibility table for this case.
    total=A+B+C
    top={}
    if top_forbidden:
        top_upper=45 if n==6 else 112
        for a in range(top_upper+1):
            for b in range(top_upper+1):
                c=total-a-b
                if 0<=c<=top_upper:
                    top[a,b,c]=downwards_allowed((a,b,c),top_forbidden)
    count=0;minimum=None;witness=None
    ct,ca2,ca3,cb2,cb3,cc2,cc3=coeff[:7]
    for a in colA:
        a0,a1,a2=a;av=ca2*e2(a)+ca3*e3(a)+phis[0].get(a,0)
        for b in colB:
            b0,b1,b2=b
            fixed=av+cb2*e2(b)+cb3*e3(b)+phis[1].get(b,0)
            m0=masks[a0][b0]&masks[a1][b2]&masks[a2][b1]
            m1=masks[a0][b2]&masks[a1][b1]&masks[a2][b0]
            m2=masks[a0][b1]&masks[a1][b0]&masks[a2][b2]
            w0=a0*b0+a1*b2+a2*b1;w1=a0*b2+a1*b1+a2*b0;w2=a0*b1+a1*b0+a2*b2
            c1s=tuple(bits(m1))
            for c0 in bits(m0):
                for c1 in c1s:
                    c2=C-c0-c1
                    if not 0<=c2<=upper or not ((m2>>c2)&1):continue
                    c=(c0,c1,c2)
                    if not adm[c] or (column_predicates[2] is not None and not column_predicates[2](c)):continue
                    if top_forbidden and any(not top.get(tuple(a[r]+b[(r+s)%3]+c[(r+2*s)%3]
                                                       for r in range(3)),False) for s in range(3)):
                        continue
                    T=w0*c0+w1*c1+w2*c2
                    value=ct*T+fixed+cc2*(c0*c1+c0*c2+c1*c2)+cc3*c0*c1*c2+phis[2].get(c,0)
                    require(value>=K,f'Local certificate failed: n={n}, {key}, {a},{b},{c}, value={value}, K={K}')
                    count+=1
                    if minimum is None or value<minimum:minimum=value;witness=a,b,c
    if empty:
        require(count==0,'Nonempty family in empty-family certificate')
        print(f'n={n} {key}{label}: EMPTY family verified.',flush=True)
        return 0
    require(count>0,'Empty enumeration unexpectedly encountered')
    a,b,c=witness
    directT=sum(a[i]*b[j]*c[k] for i,j,k in product(range(3),repeat=3) if (i+j+k)%3==0)
    features=(directT,e2(a),e3(a),e2(b),e3(b),e2(c),e3(c))
    require(sum(q*v for q,v in zip(coeff[:7],features))+phis[0].get(a,0)+phis[1].get(b,0)+phis[2].get(c,0)==minimum,'Independent minimum-witness check failed')
    print(f'n={n} {key}{label}: matrices={count}, minimum={minimum}, certified_K={K}, gap={gap}',flush=True)
    return count

SPECTRAL_TYPES={}
SPECTRAL_IDENTITIES={}

def verify_spectral_identities(certificate):
    """Check every additional identity on every relevant deleted subset of a
    45-cap, and (for size 42) on the published Delta686 histogram.
    The completeness of this family is a cited classification input.
    """
    space=list(product(range(3),repeat=6));B0=blocks()
    S=[p for p in space if (all(p) and p.count(2)%2==0) or
       frozenset(i for i,v in enumerate(p) if v) in B0]
    cap45=None
    for d in space[1:]:
        buckets=[[p for p in S if sum(x*y for x,y in zip(p,d))%3==v] for v in range(3)]
        for pts in buckets:
            if len(pts)==45:
                pivot=next(i for i,v in enumerate(d) if v)
                cap45=[p[:pivot]+p[pivot+1:] for p in pts]
                break
        if cap45 is not None:break
    require(cap45 is not None,'45-cap representative not found')
    check_cap(cap45,5)
    directions=[d for d in product(range(3),repeat=5) if next((v for v in d if v),0)==1]
    projections=[[sum(x*y for x,y in zip(p,d))%3 for p in cap45] for d in directions]
    original=[[row.count(v) for v in range(3)] for row in projections]
    for size in (42,43,44,45):
        data=certificate['spectrum5'][str(size)]
        types=[tuple(t) for t in data['types']]
        expected=[(a,b,size-a-b) for a in range(21) for b in range(a+1)
                  if 0<=size-a-b<=b and admissible5((a,b,size-a-b))]
        require(types==expected,'Incorrect spectral type index')
        identities=[]
        for stage in certificate['six_stages']:
            for key,rec in stage.items():
                counts=parse_key(key)
                for ex in rec.get('extra',[]):
                    if counts[ex['column']]==size and ex['identity'] not in identities:
                        identities.append(ex['identity'])
        index={t:i for i,t in enumerate(types)};spectra=set();nsubsets=0
        for deleted in combinations(range(45),45-size):
            histogram=[0]*len(types)
            for row,h0 in zip(projections,original):
                h=list(h0)
                for j in deleted:h[row[j]]-=1
                t=tuple(sorted(h,reverse=True))
                require(t in index,'Unexpected deletion spectrum type')
                histogram[index[t]]+=1
            spectra.add(tuple(histogram));nsubsets+=1
            for ident in identities:
                require(ident.get('bound','exact') in ('upper','exact') and type(ident['sum']) is int and len(ident['coeff'])==len(types) and all(type(x) is int for x in ident['coeff']),
                        'Malformed spectral identity')
                value=sum(x*y for x,y in zip(histogram,ident['coeff']))
                require(value <= ident['sum'] if ident.get('bound') == 'upper' else value == ident['sum'],
                        f'Spectral constraint failed: size={size}, deleted={deleted}')
        if size==42:
            histogram=tuple(DELTA.get(t,0) for t in types);spectra.add(histogram)
            for ident in identities:
                value=sum(x*y for x,y in zip(histogram,ident['coeff']))
                require(value <= ident['sum'] if ident.get('bound') == 'upper' else value == ident['sum'],
                        'Spectral constraint failed on Delta686')
        require(spectra==set(map(tuple,data['spectra'])),'Wrong set of deletion spectra')
        SPECTRAL_TYPES[size]=types;SPECTRAL_IDENTITIES[size]=identities
        print(f'Size-{size} spectrum: {nsubsets} deleted subsets, {len(spectra)} histograms, '
              f'{len(identities)} integer spectral constraints verified.',flush=True)

