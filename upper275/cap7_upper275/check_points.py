#!/usr/bin/env python3
"""Check the explicit cap236.txt list, its formula, and every unordered pair."""
from pathlib import Path
from itertools import combinations, product

def main() -> None:
    rows=Path(__file__).with_name('cap236.txt').read_text().splitlines()
    points=[tuple(map(int,row.strip())) for row in rows if row.strip()]
    if len(points)!=236 or len(set(points))!=236:
        raise AssertionError('Wrong number of points or duplicate points')
    if not all(len(p)==7 and set(p)<={0,1,2} for p in points):
        raise AssertionError('Invalid ternary vector')
    B0={frozenset(int(c)-1 for c in word) for word in
        ('123','124','135','146','156','236','245','256','345','346')}
    B1={frozenset(range(6))-b for b in B0}
    expected=set()
    for p in product(range(3),repeat=6):
        support=frozenset(i for i,v in enumerate(p) if v)
        R=all(p) and p.count(2)%2==0
        if R or support in B0:expected.add((0,)+p)
        if R or support in B1:expected.add((1,)+p)
        if len(support)==1:expected.add((2,)+p)
    if set(points)!=expected:
        raise AssertionError('Point list differs from the stated formula')
    count=0
    for x,y in combinations(points,2):
        z=tuple((-a-b)%3 for a,b in zip(x,y))
        if z in expected:
            raise AssertionError(f'Forbidden triple: {x}, {y}, {z}')
        count+=1
    print(f'PASS: formula matches cap236.txt; 236 distinct ternary vectors; {count} pairs; no forbidden triple.')
if __name__=='__main__':
    main()
