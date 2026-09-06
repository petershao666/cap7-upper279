"""Independent published-grid decoding from PDF strokes, not EPS parsing."""
import sys
sys.dont_write_bytecode = True
import hashlib, itertools, json, statistics, time
from pathlib import Path
import pdfplumber

D=Path(__file__).resolve().parent
R=D.parent.parent
src=R/'root_audit/exceptional41_raw/source_2206.09719v1.pdf'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
started=time.monotonic()
signed=list(itertools.product((-1,0,1),repeat=5))
normals=list(itertools.product(range(3),repeat=5))[1:]
out={}
with pdfplumber.open(src) as doc:
    for name,pg,fig in [('45',5,0),('A',6,0),('B',7,0),('C',7,1),('D',8,0),('E',8,1)]:
        page=doc.pages[pg]
        geometry=page.lines+page.curves
        vertical=[o for o in geometry if o['stroke'] and o['width']<.01 and 169<o['height']<171]
        tops=sorted(set(round(o['top'],5) for o in vertical))
        top=tops[fig]
        frame=sorted((o for o in vertical if abs(o['top']-top)<.01),key=lambda o:o['x0'])
        assert len(frame)==3
        left=frame[0]['x0']; height=frame[0]['height']; u=height/30
        hs=[o for o in geometry if o['stroke'] and o['height']<.01 and 33<o['width']<35
            and left+10*u<(o['x0']+o['x1'])/2<left+20*u
            and top+10*u<o['top']<top+20*u]
        assert len(hs)==9,(name,len(hs))
        ox=statistics.median((o['x0']+o['x1'])/2 for o in hs)
        oy=statistics.median(o['top'] for o in hs)
        model=[(s,ox+u*(10*s[0]-s[2]+3*s[3]),oy+u*(-10*s[1]+s[2]-3*s[4])) for s in signed]
        circles=[c for c in page.curves if c['fill'] and top<c['top'] and c['bottom']<top+height]
        assert len(circles)==(45 if name=='45' else 41),(name,len(circles))
        points=[]; witnesses=[]; err=0
        for c in circles:
            assert 4<c['width']<4.4 and 4<c['height']<4.4
            assert [v[0] for v in c['path']]==['m','c','c','c','c']
            x=(c['x0']+c['x1'])/2; y=(c['top']+c['bottom'])/2
            matches=[(s,a,b) for s,a,b in model if abs(x-a)<.5 and abs(y-b)<.5]
            assert len(matches)==1,(name,x,y,matches)
            s,a,b=matches[0]; p=tuple(t%3 for t in s)
            points.append(p);err=max(err,abs(x-a),abs(y-b))
            witnesses.append({'pdf_center':[x,y],'signed':s,'residues':p,'grid_center':[a,b]})
        S=set(points); assert len(S)==len(points)
        pairs=0
        for a,b in itertools.combinations(S,2):
            assert tuple((-x-y)%3 for x,y in zip(a,b)) not in S
            pairs+=1
        h={}
        for n in normals:
            ns=[0,0,0]
            for p in S:ns[sum(a*b for a,b in zip(n,p))%3]+=1
            t=tuple(sorted(ns,reverse=True));h[t]=h.get(t,0)+1
        assert all(v%2==0 for v in h.values())
        hist=[{'type':t,'count':v//2} for t,v in sorted(h.items(),reverse=True)]
        assert sum(r['count'] for r in hist)==121
        out[name]={'points':sorted(S),'histogram':hist,'pair_checks':pairs,'page_index':pg,
                   'frame_top':top,'u':u,'origin_from_strokes':[ox,oy],
                   'max_planar_error':err,'marker_witnesses':witnesses}
accepted=json.loads((D.parent/'fortyfive/ACCEPTED_POINTS.json').read_text())
assert sorted(map(tuple,out['45']['points']))==sorted(map(tuple,accepted['points']))
result={'status':'ROOT_PDF_FROZEN_BEFORE_READING_EPS_POINT_OUTPUT','source_sha256':sha(src),
        'code_sha256':sha(Path(__file__)),'elapsed_seconds':time.monotonic()-started,
        'figure3_matches_accepted_45':True,'figures':out}
(D/'PDF_POINTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'sha256':sha(D/'PDF_POINTS.json'),
 'figures':{k:{'points':len(v['points']),'max_error':v['max_planar_error']} for k,v in out.items()}}))
