from pathlib import Path
from collections import Counter
import json,re,hashlib,zipfile,xml.etree.ElementTree as E,time
W=Path(__file__).resolve().parent;R=W.parents[1];H=R/'hist105106/h9';RAW=R/'root_audit/exceptional41_raw';start=time.monotonic()
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
files=[RAW/'Dim5_41_180617_SetDim5Cap43_9And8_ExclPtCounts_Data.txt',RAW/'Dim5_41_180716_SetDim5Cap43_9And8_ExclPtCounts_Data.txt']
source=[*files,H/'SetDim5Cap43_8sc_ListOfCaps.xlsx',H/'SetDim5Cap43_8cu_ListOfCaps.xlsx',H/'SetDim5Cap43_8sa_ListOfCaps.xlsx',H/'SetDim5Cap43_9asifsa_ListOfCaps.xlsx',H/'SetDim5Cap43_9General_ExclPtCounts.java',H/'SetDim5Cap43_8sc_ExclPtCounts.java',RAW/'SetDim5Cap43_8cu_ExclPtCounts.java',RAW/'SetDim5Cap43_8sa_ExclPtCounts.java']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(W/'INPUTS.json').write_text(json.dumps({'source_hashes':{str(p.relative_to(R)):sha(p)for p in source},'H_generated_pointsets_read':False,'shared_named_input':'Only General9 named918F,918I,972I coordinate literals from primary source;17-point bottom sections and all8 formats use workbook columnsA/B. Root explicitly accepted this shared input boundary.','example_disclosure':'Root says earlier one-record format example was shared; not used as evidence or imported here.'},indent=2)+'\n')
def workbook(path):
 out={}
 with zipfile.ZipFile(path)as z:
  ss=[''.join(t.text or''for t in si.iter()if t.tag.endswith('}t'))for si in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
  rel={x.attrib['Id']:x.attrib['Target']for x in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
  for sheet in E.fromstring(z.read('xl/workbook.xml')).findall('.//m:sheet',ns):
   target=rel[sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']];target='xl/'+target if not target.startswith('/')else target.lstrip('/')
   name=sheet.attrib['name'].replace('Sheet','');entries={}
   for row in E.fromstring(z.read(target)).findall('.//m:row',ns):
    cells={}
    for c in row.findall('m:c',ns):
     v=c.find('m:v',ns)
     if v is not None:cells[re.sub(r'\d','',c.attrib['r'])]=ss[int(v.text)]if c.attrib.get('t')=='s'else v.text
    if 'B'in cells:
     assert 'A'in cells and re.fullmatch(r'\d+',cells['A']);entries[int(cells['A'])]=cells['B']
   assert set(entries)==set(range(len(entries)));out[name]=entries
 return out
books={k:workbook(H/f'SetDim5Cap43_{k}_ListOfCaps.xlsx')for k in ['8sc','8cu','8sa','9asifsa']}
# Only three named-coordinate data strings are absent from these workbook families.
s=(H/'SetDim5Cap43_9General_ExclPtCounts.java').read_text();named={}
for prof,code in [('918','981F'),('918','981I'),('972','981I')]:
 a=s.index('case "'+prof+'":');b=re.search(r'case "\d{3}":',s[a+7:]);piece=s[a:a+7+b.start()]if b else s[a:]
 match=re.search(r'if\(code\.equals\("'+code+r'"\)\)\s*return\s*((?:"[^"]*"\s*\+?\s*)+);',piece);assert match,(prof,code)
 named[prof,code]=''.join(re.findall(r'"([^"]*)"',match.group(1)))

def parse_cap(text):
 groups=text.split(':');assert len(groups)==3
 ans=[]
 for y,group in zip((2,0,1),groups):
  pts=[]
  for p in group.split(';'):
   if not p:continue
   v=tuple(map(int,p.split(',')));assert len(v)==4 and v[0]==y and all(0<=x<3 for x in v);pts.append(v[1:])
  ans.append(pts)
 return ans
parsed={}
def cap(kind,prof,code):
 key=kind,prof,code
 if key not in parsed:
  if kind=='9General':text=books['9asifsa'][prof][int(code.split(':')[1])]if ':'in code else named[prof,code]
  else:text=books[kind][prof][int(code)]
  parsed[key]=parse_cap(text)
 return parsed[key]

I=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1))
def matrix(rows):return tuple(tuple(r)+(0,)for r in rows)+((0,0,0,1),)
def mul(A,B):return tuple(tuple(sum(A[i][k]*B[k][j]for k in range(4))%3 for j in range(4))for i in range(4))
def power(A,n):
 B=I
 while n:
  if n&1:B=mul(B,A)
  A=mul(A,A);n//=2
 return B
RS=matrix(((0,0,2),(0,2,0),(1,0,0)));MS=matrix(((0,0,1),(0,1,0),(1,0,0)))
RG=matrix(((2,0,0),(0,1,1),(0,2,1)));MG=matrix(((1,0,0),(0,1,0),(0,0,2)))
T1=((1,2,0,1),(0,1,0,1),(0,0,1,0),(0,0,0,1));T2=((1,0,2,1),(0,1,0,0),(0,0,1,1),(0,0,0,1))
perms=[(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)];lut={}
def affine(kind,r,m,t1=0,t2=0):
 key=kind,r,m,t1,t2
 if key in lut:return lut[key]
 if kind=='8sc':assert 0<=r<4 and 0<=m<2;A=mul(power(MS,m),power(RS,r))
 elif kind in ('8sa','9General'):
  assert 0<=r<8 and 0<=m<2;A=mul(power(MG,m),power(RG,r))
  if kind=='9General':assert 0<=t1<3 and 0<=t2<3;A=mul(A,mul(power(T2,t2),power(T1,t1)))
 else:
  assert kind=='8cu'and 0<=r<6 and 0<=m<8
  P=matrix(tuple(tuple(int(j==perms[r][i])for j in range(3))for i in range(3)))
  D=matrix(tuple(tuple((1+((m>>(2-i))&1))*int(i==j)for j in range(3))for i in range(3)));A=mul(D,P)
 result=[]
 for p in range(27):
  v=(p//9,p//3%3,p%3,1);result.append(tuple(sum(A[i][j]*v[j]for j in range(4))%3 for i in range(3)))
 assert len(set(result))==27;lut[key]=result;return result
pack=lambda v:sum(x*3**(4-i)for i,x in enumerate(v))
records=[];counts=Counter();blocks=[]
for fi,p in enumerate(files):
 kind=None;block=None
 for line,l in enumerate(p.read_text().splitlines(),1):
  m=re.fullmatch(r'SetDim5Cap43_(\w+)_ExclPtCounts:',l.strip())
  if m:kind=m.group(1)
  if l.startswith('3-flat point count:'):
   assert block is None;head=[list(map(int,z.split(',')))for z in l.split(':',1)[1].strip().split(';')];assert len(head)==3 and all(len(v)==3 for v in head)
   block={'file':fi,'line':line,'matrix':head,'rows':0,'kind':kind}
  elif l.startswith('Excluded point counts:')and block is not None:block['excluded']=[list(map(int,z.split(',')))for z in l.split(':',1)[1].strip().split(';')]
  elif block is not None and re.match(r'^\d+\t',l):
   f=l.split('\t');assert kind in ('8sc','8cu','8sa','9General')
   if kind=='9General':assert len(f)==12;t1,t2,rr,mm=map(int,f[:4]);ap,ai,bp,bi=f[4:8];free=f[8:]
   else:assert len(f)==10;rr,mm=map(int,f[:2]);t1=t2=0;ap,ai,bp,bi=f[2:6];free=f[6:]
   A=cap(kind,ap,ai);B=cap(kind,bp,bi);assert set(A[0])==set(B[0]),('shared',fi,line)
   trans=affine(kind,rr,mm,t1,t2)
   assert {trans[9*x+3*y+z]for x,y,z in A[0]}==set(A[0]),('shared_symmetry',fi,line)
   pts=[(2,2,*v)for v in A[0]]
   for k,y in [(1,0),(2,1)]:pts +=[(2,y,*trans[9*x+3*z+y0])for x,z,y0 in A[k]]
   for k,x in [(1,0),(2,1)]:pts +=[(x,2,*v)for v in B[k]]
   for text,(x,y)in zip(free,[(0,0),(1,0),(0,1),(1,1)]):
    ids=[]if text==''else list(map(int,text.split(',')));assert len(ids)==len(set(ids))and all(0<=v<27 for v in ids)
    pts +=[(x,y,z//9,z//3%3,z%3)for z in ids]
   pts=sorted(pts);assert len(pts)==41 and len(set(pts))==41,('size',fi,line)
   cc=[[sum(q[0]==x and q[1]==y for q in pts)for y in(2,0,1)]for x in(2,0,1)];assert cc==head,('matrix',fi,line,cc,head)
   codes=[pack(v)for v in pts];pointsha=hashlib.sha256(json.dumps(pts,separators=(',',':')).encode()).hexdigest()
   records.append({'index':len(records),'file':fi,'source_line':line,'block_line':block['line'],'kind':kind,'matrix':head,'excluded':block.get('excluded',[]),'point_sha256':pointsha,'points_encoded':codes});counts[kind]+=1;block['rows']+=1
  elif l.startswith('Cap configurations:'):
   assert block is not None and block['rows']==int(l.split(':')[1]);blocks.append(block);block=None
 assert block is None
assert dict(counts)=={'9General':60,'8sc':33549,'8cu':432,'8sa':304},counts
with (W/'ROWS.jsonl').open('w')as o,(W/'CHECK_INPUT.txt').open('w')as c:
 for x in records:
  o.write(json.dumps(x,separators=(',',':'))+'\n');c.write(' '.join(map(str,[x['index'],*[v for t in x['matrix']for v in t],*x['points_encoded']]))+'\n')
(W/'DECODE_STATUS.json').write_text(json.dumps({'status':'ALL_ROWS_COORDINATES_AND_STATED_MATRICES_DECODED_PENDING_PAIRS_AND_HISTOGRAMS','rows':len(records),'shape_counts':counts,'workbook_code_counts':{k:{p:len(v)for p,v in b.items()}for k,b in books.items()},'seconds':time.monotonic()-start,'named_G9_shared_data_keys':[list(k)for k in named],'raw_printed_axis_order':[2,0,1],'point_encoding':'81*x1+27*x2+9*x3+3*x4+x5; point SHA256 is compact JSON of lexicographically sorted5-tuples'},indent=2)+'\n')
print('ALL_DECODED',len(records),dict(counts),'seconds',time.monotonic()-start,flush=True)
