"""Exact 41-cap histogram bounds from 4-dimensional local counts.
External inputs: Thackeray arXiv:2206.09719v1 Lemma 2.3 and Proposition 6.1.
This module contains no optimizer and reads no numerical discovery caches.
"""
from itertools import combinations, product
from math import comb
EXCLUDED41=((20,19,2),(20,18,3),(19,19,3),(19,18,4))

def demand(ok,message):
    if not ok: raise AssertionError(message)
def e2(t):return t[0]*t[1]+t[0]*t[2]+t[1]*t[2]
def e3(t):return t[0]*t[1]*t[2]
def triples(s,u):return [(a,b,s-a-b) for a in range(u+1) for b in range(a+1) if 0<=s-a-b<=b]
def prove_small_bound():
    space=list(product(range(3),repeat=2));tested=0
    for subset in combinations(space,5):
        S=set(subset)
        demand(any(tuple((-a-b)%3 for a,b in zip(x,y)) in S for x,y in combinations(subset,2)), 'five-cap in dimension two')
        tested+=1
    demand(tested==126,'two-dimensional enumeration count')
    # A hypothetical 10-cap in dimension three has plane sections at most four.
    # Its 13 directions have sum(E2)=9*binom(10,2), below their minimum.
    T=triples(10,4)
    demand(13*min(map(e2,T))>9*comb(10,2),'three-dimensional pair-moment gap')

def adm4(t):
    if min(t)<0 or max(t)>9 or sum(t)>20:return False
    a,b,c=sorted(t,reverse=True)
    if (a==9 and b>=7) or (a,b)==(8,8):return c<=2
    if (a,b) in ((9,6),(8,7)):return c<=3
    if (a,b) in ((9,5),(7,7)):return c<=4
    return True

def force5(t):
    a,b,c=t
    return [13*a*b*c,27*comb(a,2),9*comb(a,3),27*comb(b,2),9*comb(b,3),27*comb(c,2),9*comb(c,3)]

def all_matrices5(key,allowed,absent=()):
    cols=[]
    for j,N in enumerate(key):
        cols.append([(a,b,N-a-b) for a in range(10) for b in range(10)
                     if (j!=0 or a>=b>=N-a-b) and adm4((a,b,N-a-b))])
    for a in cols[0]:
        for b in cols[1]:
            for c in cols[2]:
                if not all(adm4((a[i],b[j],c[(-i-j)%3])) for i in range(3) for j in range(3)):continue
                tops=[tuple(sorted((a[r]+b[(r+s)%3]+c[(r+2*s)%3] for r in range(3)),reverse=True)) for s in range(3)]
                if any(t not in allowed or t in absent for t in tops):continue
                T=sum(a[i]*b[j]*c[(-i-j)%3] for i in range(3) for j in range(3))
                yield [T,e2(a),e3(a),e2(b),e3(b),e2(c),e3(c)],tops

def verify_cut(data,cut_id):
    demand(data['m']==41 and not data.get('hist4'), 'only the basic 41-cap lemma is implemented')
    types=[t for t in triples(41,20) if t not in EXCLUDED41]
    demand(types==list(map(tuple,data['types'])) and len(data['phi'])==len(types),'41-cap function support')
    demand(all(type(v) is int for v in data['phi']),'integer 41-cap function')
    phi=dict(zip(types,data['phi']));allowed=set(types)
    required=[t for t in types if t in ((20,20,1),(18,18,5)) or 20>=t[0]>=17>=t[1]>=16>=t[2]]
    records=data['inner'];anchors=[tuple(r['type']) for r in records]
    demand(set(anchors)==set(required) and len(anchors)==len(required),'Proposition6.1 anchor coverage')
    count=0;bounds=[]
    for i,r in enumerate(records):
        key=tuple(r['type']);q=r['coeff'];demand(len(q)==7 and all(type(v) is int for v in q),'41-cap coefficients')
        absent=list(map(tuple,r.get('absent_types',[])))
        demand(not absent or absent==anchors[:i],'41-cap priority scope')
        U=sum(x*y for x,y in zip(q,force5(key)));B=phi[key]+U-40*r['K']
        demand(B==r['bound'],'41-cap full histogram bound')
        n=0;minimum=None
        for f,tops in all_matrices5(key,allowed,absent):
            value=sum(x*y for x,y in zip(q,f))-sum(phi[t] for t in tops)
            demand(value>=r['K'],'41-cap local inequality')
            minimum=value if minimum is None else min(minimum,value);n+=1
        demand(n==r['matrices'] and n>0,'41-cap exhaustive count')
        count+=n;bounds.append(B)
        print(f'AUX41 INNER {cut_id} {key}: matrices={n}, minimum={minimum}, K={r["K"]}, bound={B}',flush=True)
    demand(max(bounds)==data['bound'],'41-cap maximum over all possible anchors')
    print(f'AUX41 PASS {cut_id}: bound={data["bound"]}, matrices={count}',flush=True)
    return phi,data['bound'],count
