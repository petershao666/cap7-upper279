"""Translate primary static literals and raw rows; never execute Java."""
from pathlib import Path
from functools import lru_cache
from collections import Counter
import re,json,hashlib,time

W=Path(__file__).resolve().parent;ROOT=W.parents[1]
SOURCES={'8sc':W.parent/'h9/SetDim5Cap43_8sc_ExclPtCounts.java','9General':W.parent/'h9/SetDim5Cap43_9General_ExclPtCounts.java','8cu':W/'SetDim5Cap43_8cu_ExclPtCounts.java','8sa':W/'SetDim5Cap43_8sa_ExclPtCounts.java'}
RAWS=[ROOT/'root_audit/exceptional41_raw'/('Dim5_41_'+date+'_SetDim5Cap43_9And8_ExclPtCounts_Data.txt')for date in ['180617','180716']]
EXPECTED={'8sc':33549,'9General':60,'8cu':432,'8sa':304}
COORD3=[(v//9,(v//3)%3,v%3)for v in range(27)]
PERM=[(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]

def parse_catalogue(path,shape):
    source=path.read_text();beg=source.index('public static String cap(');end=source.index('public static Mod3Vector[]',beg);body=source[beg:end]
    pattern=r'case "(?P<profile>[0-9]{3})":|if\(code\.equals\("(?P<name>[^"]+)"\)\)|case (?P<index>[0-9]+):|return\s+(?P<literal>(?:"[0-9,;:]*"\s*(?:\+\s*)?)+);'
    table={};profile=None;key=None
    for m in re.finditer(pattern,body):
        if m['profile'] is not None:profile=m['profile'];key=None
        elif m['name'] is not None:key=m['name']
        elif m['index'] is not None:key=profile+':'+m['index'] if shape=='9General' else m['index']
        else:
            assert profile is not None and key is not None
            value=''.join(re.findall(r'"([0-9,;:]*)"',m['literal']))
            groups=[[]if not g else[tuple(map(int,p.split(',')))for p in g.split(';')]for g in value.split(':')]
            assert len(groups)==3 and [len(g)for g in groups]==list(map(int,profile)),(shape,profile,key)
            assert all(len(p)==4 and p[0]==c and all(0<=a<3 for a in p)for c,g in zip([2,0,1],groups)for p in g)
            code=(profile,key);assert code not in table
            table[code]=([tuple(p[1:])for p in g]for g in groups)
            table[code]=tuple(tuple(g)for g in table[code])
    assert table
    return table

def transform(p,shape,r,m,t1=0,t2=0):
    a,b,c=p
    if shape=='8cu':
        assert 0<=r<6 and 0<=m<8
        q=[p[i]for i in PERM[r]]
        return tuple((x*(1+((m//k)%2)))%3 for x,k in zip(q,[4,2,1]))
    if shape=='8sc':
        assert 0<=r<4 and 0<=m<2 and t1==t2==0
        for _ in range(r):a,b,c=2*c%3,2*b%3,a
        if m:a,b,c=c,b,a
        return a,b,c
    assert shape in ['8sa','9General'] and 0<=r<8 and 0<=m<2
    if shape=='9General':
        assert 0<=t1<3 and 0<=t2<3
        for _ in range(t1):a,b,c=(a+2*b+1)%3,(b+1)%3,c
        for _ in range(t2):a,b,c=(a+2*c+1)%3,b,(c+1)%3
    else:assert t1==t2==0
    for _ in range(r):a,b,c=2*a%3,(b+c)%3,(2*b+c)%3
    if m:c=2*c%3
    return a,b,c

def read_records():
    records=[];blocks=[];counts=Counter()
    for path in RAWS:
        shape=None;base_shape=None;override=None;header=None;rows=[];header_line=None
        for ln,line in enumerate(path.read_text().splitlines(),1):
            mt=re.search(r'SetDim5Cap43_(9General|8sc|8cu|8sa)_ExclPtCounts:',line)
            if mt:
                assert not rows
                if line.lstrip().startswith('--'):override=mt.group(1)
                else:base_shape=mt.group(1);override=None
                header=None
            elif line.startswith('3-flat point count: '):
                assert not rows
                shape=override or base_shape
                assert shape is not None
                txt=line.split(': ',1)[1];header=[list(map(int,s.split(',')))for s in txt.split(';')]
                assert len(header)==3 and all(len(a)==3 for a in header) and sum(map(sum,header))==41
                assert header[0][0]==(9 if shape=='9General' else 8),(path.name,ln,shape,header)
                header_line=ln
            elif line.startswith('Cap configurations: '):
                declared=int(line.split(': ',1)[1]);assert header is not None and declared==len(rows),(path.name,ln,declared,len(rows))
                blocks.append({'file':path.name,'shape':shape,'header_line':header_line,'end_line':ln,'grid':header,'declared_records':declared,'record_ids':rows})
                header=None;rows=[];override=None
            elif re.match(r'^\d+\t\d+\t',line):
                assert shape is not None and header is not None,(path.name,ln)
                fields=line.split('\t');assert len(fields)==(12 if shape=='9General' else 10),(path.name,ln,len(fields))
                rid=len(records);records.append({'id':rid,'file':path.name,'line':ln,'shape':shape,'header_line':header_line,'grid':header,'raw_fields':fields,'raw_line':line});rows.append(rid);counts[shape]+=1
        assert not rows,(path.name,'unterminated')
    assert dict(counts)==EXPECTED,(counts,EXPECTED)
    return records,blocks

def main():
    start=time.monotonic();tables={s:parse_catalogue(p,s)for s,p in SOURCES.items()}
    records,blocks=read_records()
    manifest={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in list(SOURCES.values())+RAWS+[W.parent/'h9/Mod3Vector.java']}
    (W/'SOURCE_INPUTS.json').write_text(json.dumps({'sources':manifest,'raw_counts':EXPECTED,'static_template_counts':{s:len(t)for s,t in tables.items()},'prior_SC_fixture':'../exceptional41_decoder/ONE_RECORD.json; mathematical format shared, no external decoder kernel imported'},indent=2)+'\n')
    (W/'RAW_BLOCKS.json').write_text(json.dumps(blocks,indent=2)+'\n')
    @lru_cache(None)
    def fixed(shape,lp,lc,bp,bc,r,m,t1,t2):
        left=tables[shape][lp,lc];bottom=tables[shape][bp,bc]
        assert set(left[0])==set(bottom[0])
        assert {transform(p,shape,r,m,t1,t2)for p in left[0]}==set(left[0])
        return {(2,2):left[0],(2,0):tuple(transform(p,shape,r,m,t1,t2)for p in left[1]),(2,1):tuple(transform(p,shape,r,m,t1,t2)for p in left[2]),(0,2):bottom[1],(1,2):bottom[2]}
    with (W/'point_rows.txt').open('w')as output,(W/'ROW_METADATA.jsonl').open('w')as metadata:
        output.write(str(len(records))+'\n')
        for z in records:
            if time.monotonic()-start>570:raise RuntimeError('preparation time limit')
            try:
                f=z['raw_fields'];shape=z['shape']
                if shape=='9General':t1,t2,r,m=map(int,f[:4]);lp,lc,bp,bc=f[4:8];free=f[8:]
                else:t1=t2=0;r,m=map(int,f[:2]);lp,lc,bp,bc=f[2:6];free=f[6:]
                cells=dict(fixed(shape,lp,lc,bp,bc,r,m,t1,t2))
                for cell,value in zip([(0,0),(1,0),(0,1),(1,1)],free):
                    codes=[]if value==''else list(map(int,value.split(',')))
                    assert all(0<=v<27 for v in codes)and len(codes)==len(set(codes))
                    cells[cell]=[COORD3[v]for v in codes]
                grid=[[len(cells[a,b])for b in [2,0,1]]for a in [2,0,1]]
                assert grid==z['grid'],('grid',grid,z['grid'])
                ps=sorted(81*a+27*b+9*p[0]+3*p[1]+p[2]for (a,b),group in cells.items()for p in group)
                assert len(ps)==len(set(ps))==41
                z['point_sha256']=hashlib.sha256(bytes(ps)).hexdigest()
                metadata.write(json.dumps(z,separators=(',',':'))+'\n')
                output.write(' '.join(map(str,[z['id']]+[a for row in grid for a in row]+ps))+'\n')
            except Exception as e:
                (W/'FORMAT_FAILURE.json').write_text(json.dumps({'error':repr(e),'record':z},indent=2)+'\n');raise
    (W/'PREPARE_STATUS.json').write_text(json.dumps({'status':'ALL_ROWS_DECODED_PENDING_FULL_CAP_AND_HIST_CHECK','records':len(records),'format_counts':EXPECTED,'seconds':time.monotonic()-start,'canonical_point_encoding':'81*x1+27*x2+9*x3+3*x4+x5; point hash SHA256(bytes(sorted41pointIDs))'},indent=2)+'\n')
    print('PREPARED',len(records),dict(Counter(z['shape']for z in records)),time.monotonic()-start,flush=True)
if __name__=='__main__':main()
