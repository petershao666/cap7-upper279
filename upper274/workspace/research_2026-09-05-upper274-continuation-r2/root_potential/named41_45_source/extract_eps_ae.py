"""Read only EPS marker paths and a predeclared labelled grid; never execute EPS."""
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import re

here=Path(__file__).resolve().parent
num=r'[-+]?\d+(?:\.\d+)?'
pattern=re.compile(r'('+num+r')\s+('+num+r')\s+m\s+((?:(?:'+num+r'\s+){6}c\s*){4})f\b')
u=F(720,127);origin=(F('96.754'),F('85.414'));tol=F(1,100)
grid=[]
for p in itertools.product([-1,0,1],repeat=5):
    a,b,c,d,e=p
    grid.append((p,origin[0]+u*(10*a-c+3*d),origin[1]+u*(-10*b+c-3*e)))
assert len({(x,y) for p,x,y in grid})==243
orbit=json.loads((here/'ORBIT45_POINTS.json').read_text())
caps=[];max_error=F(0)
for figure,name,size in [(3,'45',45),(4,'41A',41),(6,'41B',41),(7,'41C',41),(8,'41D',41),(9,'41E',41)]:
    source=here/('Fig%02dEPS.eps'%figure)
    text=source.read_text(encoding='ascii')
    markers=[]
    for match in pattern.finditer(text):
        values=[F(v) for v in re.findall(num,match.group(0))]
        assert len(values)==26
        coordinates=list(zip(values[0::2],values[1::2]))
        xs=[x for x,y in coordinates];ys=[y for x,y in coordinates]
        center=((min(xs)+max(xs))/2,(min(ys)+max(ys))/2)
        radius=((max(xs)-min(xs))/2,(max(ys)-min(ys))/2)
        assert all(F('2.12')<r<F('2.14') for r in radius)
        assert coordinates[0]==coordinates[-1]
        ends=[coordinates[0]]+[coordinates[3*i] for i in range(1,5)]
        for x,y in ends:
            dx=abs(x-center[0]);dy=abs(y-center[1])
            assert (dx<=F('0.003') and abs(dy-radius[1])<=F('0.003')) or (dy<=F('0.003') and abs(dx-radius[0])<=F('0.003'))
        hits=[(p,x,y) for p,x,y in grid if abs(center[0]-x)<=tol and abs(center[1]-y)<=tol]
        assert len(hits)==1,(name,center,len(hits))
        signed,x,y=hits[0];error=max(abs(center[0]-x),abs(center[1]-y));max_error=max(max_error,error)
        markers.append({'EPS_line':text.count('\n',0,match.start())+1,'EPS_start_byte':match.start(),'center_rational':[str(q) for q in center],'expected_center_rational':[str(x),str(y)],'signed_coordinates':signed,'point':tuple(q%3 for q in signed)})
    points=sorted(tuple(m['point']) for m in markers)
    assert len(points)==len(set(points))==size
    if name=='45': assert points==sorted(tuple(p) for p in orbit['points'])
    lookup=set(points)
    pairs=0
    for a,b in itertools.combinations(points,2):
        assert tuple((-x-y)%3 for x,y in zip(a,b)) not in lookup
        pairs+=1
    raw=Counter()
    for d in itertools.product(range(3),repeat=5):
        if not any(d):continue
        counts=Counter(sum(x*y for x,y in zip(d,p))%3 for p in points)
        raw[tuple(sorted((counts[j] for j in range(3)),reverse=True))]+=1
    assert all(n%2==0 for n in raw.values())
    hist=[{'type':t,'count':n//2} for t,n in sorted(raw.items())]
    assert sum(row['count'] for row in hist)==121
    if name!='45':assert max(max(row['type']) for row in hist)<=18
    caps.append({'name':name,'figure':figure,'source_file':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'points':points,'point_indices':[sum(v*3**j for j,v in enumerate(p)) for p in points],'pair_checks':pairs,'histogram':hist,'marker_coordinate_witnesses':markers})
out={'status':'PRIMARY_EPS_GEOMETRY_DECODED_CAPS_PASS_PENDING_ROOT_FIGURE_AUDIT','coordinate_order':['x1','x2','x3','x4','x5'],'geometry_proof':'EPS_GEOMETRY.md','grid_unit_rational':str(u),'grid_origin_rational':[str(q) for q in origin],'max_coordinate_matching_error_rational':str(max_error),'tolerance_rational':str(tol),'figure3_exactly_matches_independent_published_orbit':True,'PS_executed':False,'affine_fit_search_run':False,'caps':caps}
(here/'EPS_POINTS.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',[(c['name'],len(c['points']),c['pair_checks']) for c in caps])
print('max planar grid error',str(max_error))
print('SHA256',hashlib.sha256((here/'EPS_POINTS.json').read_bytes()).hexdigest())
