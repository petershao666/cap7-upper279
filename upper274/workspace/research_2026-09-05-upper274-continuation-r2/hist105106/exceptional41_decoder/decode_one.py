"""Read-only Java literal decoder; executes no Java and decodes exactly one record."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import re,json,hashlib

W=Path(__file__).resolve().parent
ROOT=W.parents[1]
JAVA=W.parent/'h9/SetDim5Cap43_8sc_ExclPtCounts.java'
VECTOR=W.parent/'h9/Mod3Vector.java'
RAW=ROOT/'root_audit/exceptional41_raw/Dim5_41_180716_SetDim5Cap43_9And8_ExclPtCounts_Data.txt'

def literal(profile,index):
    text=JAVA.read_text()
    block=re.search(r'case "'+re.escape(profile)+r'":\s*switch\(code\)\s*\{(.*?)default: return null;',text,re.S)
    assert block
    record=re.search(r'case '+str(index)+r': return "([0-9,;:]+)";',block.group(1))
    assert record
    value=record.group(1)
    groups=[[tuple(map(int,p.split(','))) for p in group.split(';')]for group in value.split(':')]
    assert [len(g)for g in groups]==list(map(int,profile))
    assert all(len(p)==4 and p[0]==c for c,g in zip([2,0,1],groups)for p in g)
    line=text[:text.index('case '+str(index)+': return "'+value+'";',block.start())].count('\n')+1
    return [[p[1:]for p in g]for g in groups],{'profile':profile,'zero_based_index':index,'java_line':line,'literal':value}

def rotate(p):
    a,b,c=p
    return ((2*c)%3,(2*b)%3,a)

def reflect(p):return (p[2],p[1],p[0])

def transformed(p,r,m):
    for _ in range(r):p=rotate(p)
    for _ in range(m):p=reflect(p)
    return p

def decode(record):
    fields=record.split('\t');assert len(fields)==10
    r,m=int(fields[0]),int(fields[1]);assert 0<=r<4 and 0<=m<2
    left,L=literal(fields[2],int(fields[3]));bottom,B=literal(fields[4],int(fields[5]))
    assert set(left[0])==set(bottom[0])
    assert {transformed(p,r,m)for p in left[0]}==set(left[0])
    cells={(2,2):left[0],(2,0):[transformed(p,r,m)for p in left[1]],(2,1):[transformed(p,r,m)for p in left[2]],(0,2):bottom[1],(1,2):bottom[2]}
    for cell,value in zip([(0,0),(1,0),(0,1),(1,1)],fields[6:]):
        codes=[] if value=='' else list(map(int,value.split(',')))
        assert all(0<=v<27 for v in codes) and len(codes)==len(set(codes))
        cells[cell]=[(v//9,(v//3)%3,v%3)for v in codes]
    points=sorted((a,b,*p)for (a,b),ps in cells.items()for p in ps)
    return points,cells,{'r':r,'m':m,'left_template':L,'bottom_template':B}

def main():
    lines=RAW.read_text().splitlines();line_number=831;header_line=826
    assert lines[header_line-1]=='3-flat point count: 8,2,8;5,2,0;5,3,8'
    assert lines[733]=='SetDim5Cap43_8sc_ExclPtCounts:'
    record=lines[line_number-1];assert record.startswith('3\t1\t828\t7\t855\t8\t')
    points,cells,metadata=decode(record)
    assert len(points)==len(set(points))==41
    ps=set(points)
    pairs=0
    for p,q in combinations(points,2):
        pairs+=1
        assert tuple((-a-b)%3 for a,b in zip(p,q))not in ps
    grid=[[len(cells[a,b])for b in [2,0,1]]for a in [2,0,1]]
    assert grid==[[8,2,8],[5,2,0],[5,3,8]]
    normals=[v for v in product(range(3),repeat=5)if any(v)and next(x for x in v if x)==1]
    hist=Counter()
    for v in normals:
        counts=Counter(sum(a*b for a,b in zip(v,p))%3 for p in points)
        hist[tuple(sorted([counts[i]for i in range(3)],reverse=True))]+=1
    assert len(normals)==121 and sum(hist.values())==121
    assert sum(k*(a*b+a*c+b*c)for(a,b,c),k in hist.items())==81*41*40//2
    assert sum(k*a*b*c for(a,b,c),k in hist.items())==27*41*40*39//6
    result={'status':'ONE_RECORD_FORMAT_CHECK_PASS_NOT_FULL_LIST_COVERAGE','sources':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [JAVA,VECTOR,RAW]},'raw_line_number':line_number,'block_label_line':734,'header_line_number':header_line,'record':record,'decoder_metadata':metadata,'coordinate_order':['x1','x2','x3','x4','x5'],'grid_row_and_column_value_order':[2,0,1],'grid':grid,'points':points,'point_pair_checks':pairs,'projective_directions':121,'histogram': [{'type':t,'count':n}for t,n in sorted(hist.items())],'external_java_executed':False,'batch_records_decoded':1}
    (W/'ONE_RECORD.json').write_text(json.dumps(result,indent=2)+'\n')
    (W/'ONE_RECORD_POINTS.tsv').write_text('x1\tx2\tx3\tx4\tx5\n'+''.join('\t'.join(map(str,p))+'\n'for p in points))
    print(json.dumps({k:v for k,v in result.items()if k in ['status','raw_line_number','grid','point_pair_checks','projective_directions','histogram']}))
if __name__=='__main__':main()
