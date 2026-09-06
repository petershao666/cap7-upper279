"""Published partial-grid predicate; all and only AGL(2,3) coordinate images."""
from itertools import product
from pathlib import Path
import json
# Row-major indexing with row and column labels0,1,2. Translating paper's(-1,0,1)
# labels to these labels is itself affine; transposition also lies inAGL.
GRIDS=[
 [[9,8,2],[None,6,None],[None,6,None]],
 [[9,8,2],[None,6,None],[None,5,None]],
 [[None,8,None],[9,6,3],[None,6,None]],
 [[None,8,None],[9,6,3],[None,5,None]],
 [[None,7,None],[9,6,3],[None,6,None]],
 [[8,None,5],[1,6,None],[8,None,5]],
 [[8,None,6],[1,5,None],[8,None,6]],
 [[9,1,9],[1,1,None],[9,None,None]],
 [[9,1,9],[2,2,None],[8,None,None]],
]
def affine_maps():
 out=[]
 for a,b,c,d,e,f in product(range(3),repeat=6):
  if (a*d-b*c)%3==0:continue
  p=tuple(3*((a*r+b*s+e)%3)+(c*r+d*s+f)%3 for r,s in product(range(3),repeat=2))
  assert len(set(p))==9
  out.append(p)
 assert len(out)==len(set(out))==432
 return tuple(out)
MAPS=affine_maps()
def pattern_orbits():
 pats=set();bybase=[]
 for grid in GRIDS:
  base=[(3*i+j,v)for i,row in enumerate(grid)for j,v in enumerate(row)if v is not None]
  orb={tuple(sorted((p[i],v)for i,v in base))for p in MAPS};bybase.append(sorted(orb));pats|=orb
 return tuple(sorted(pats)),bybase
PATTERNS,ORBITS=pattern_orbits()
def forbidden(grid):
 flat=tuple(grid)if len(grid)==9 else tuple(v for row in grid for v in row)
 return any(all(flat[i]==v for i,v in pat)for pat in PATTERNS)
def shape_clash(grid):
 flat=tuple(grid)if len(grid)==9 else tuple(v for row in grid for v in row)
 labels=[set()for _ in range(9)]
 for a,b in ((1,0),(0,1),(1,1),(1,2)):
  for c in range(3):
   ix=[3*r+s for r,s in product(range(3),repeat=2)if(a*r+b*s)%3==c];ty=tuple(sorted((flat[i]for i in ix),reverse=True))
   if ty in ((9,9,2),(9,9,1),(9,8,2)):
    for i in ix:
     if flat[i]==8:labels[i].add('antiprism8')
   if ty in ((8,6,6),(8,6,5),(7,6,6)):
    for i in ix:
     if flat[i]==8:labels[i].add('cube8')
     if flat[i]==6:labels[i].add('longdiag6')
   if ty==(9,6,3):
    for i in ix:
     if flat[i]==6:labels[i].add('notlongdiag6')
 return any({'antiprism8','cube8'}<=s or {'longdiag6','notlongdiag6'}<=s for s in labels)
if __name__=='__main__':
 W=Path(__file__).resolve().parent
 data=dict(source='https://arxiv.org/html/2206.09719v1',lemmas=['2.2','2.4','2.5','2.6'],maps=MAPS,base_grids=GRIDS,patterns=PATTERNS,orbit_sizes=[len(x)for x in ORBITS])
 (W/'clash_data.json').write_text(json.dumps(data,indent=2)+'\n')
 print('affine_maps',len(MAPS),'pattern_orbits',[len(x)for x in ORBITS],'deduplicated_patterns',len(PATTERNS))
