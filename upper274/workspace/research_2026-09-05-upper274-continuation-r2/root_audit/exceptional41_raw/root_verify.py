"""Verify source-row bijection, independent payload equality and all spectrum representatives."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,itertools,json,re
from collections import Counter
D=Path(__file__).resolve().parent;R=D.parent.parent;H=R/'hist105106/fullraw41';L=R/'compatibility/exceptional41_decode'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[D/f'Dim5_41_{date}_SetDim5Cap43_9And8_ExclPtCounts_Data.txt'for date in ['180617','180716']]
source={}
for p in files:
    for line,s in enumerate(p.read_text().splitlines(),1):
        if re.match(r'^\d+\t',s):source[p.name,line]=s
records=[json.loads(s)for s in (H/'ROW_METADATA.jsonl').read_text().splitlines()]
assert len(source)==len(records)==34345
assert len({(r['file'],r['line'])for r in records})==34345
assert {(r['file'],r['line']):r['raw_line']for r in records}==source
hrows=(H/'point_rows.txt').read_text().splitlines();lrows=(L/'CHECK_INPUT.txt').read_text().splitlines()
assert hrows[0]=='34345' and len(hrows)==34346 and hrows[1:]==lrows
for r,payload in zip(records,hrows[1:]):
    v=list(map(int,payload.split()));assert v[0]==r['id'] and v[1:10]==sum(r['grid'],[])
    assert hashlib.sha256(bytes(v[10:])).hexdigest()==r['point_sha256']
h=json.loads((H/'HISTOGRAMS.json').read_text());types=list(map(tuple,h['types']))
assert len(types)==len(set(types))==40
expected={(a,b,41-a-b)for a in range(21)for b in range(a+1)if 0<=41-a-b<=b}
assert set(types)==expected
normals=list(itertools.product(range(3),repeat=5))[1:];np=0
for row in h['histograms']:
    S=set(map(tuple,row['points']));assert len(S)==41
    assert all(len(p)==5 and all(c in range(3)for c in p)for p in S)
    ps=sorted(sum(p[j]*3**(4-j)for j in range(5))for p in S)
    assert ps==row['point_ids']==list(map(int,hrows[row['representative_row_id']+1].split()))[10:]
    for a,b in itertools.combinations(S,2):
        assert tuple((-x-y)%3 for x,y in zip(a,b))not in S;np+=1
    c=Counter()
    for n in normals:
        counts=Counter(sum(x*y for x,y in zip(n,p))%3 for p in S)
        c[tuple(sorted((counts[0],counts[1],counts[2]),reverse=True))]+=1
    assert set(c)<=set(types)and [c[t]for t in types]==[2*v for v in row['counts']]
assert len(h['histograms'])==41 and np==33620
out={'status':'ROOT_ACCEPTED_FULL_RAW41_SPECTRUM_OVERCOVER','source_row_count':34345,
 'original_source_rows_bijectively_preserved':True,'every_raw_line_equal':True,
 'all_H_L_point_payloads_equal':True,'representatives':41,'root_representative_pair_checks':np,
 'root_representative_nonzero_normal_checks':41*242,
 'source_files':{p.name:sha(p)for p in files},'producer_histogram_sha256':sha(H/'HISTOGRAMS.json'),
 'producer_freeze_sha256':sha(H/'FROZEN.json'),'independent_freeze_sha256':sha(L/'FROZEN.json'),
 'root_code_sha256':sha(Path(__file__)),
 'scope':'Exactly the41 spectra occurring in all34345 raw records. With explicit published list coverage, a necessary overcover of the exceptional alternative. Not by itself all41caps.',
 'independence':'Root source-line and representative tuple checks import no producer/verifier kernels. H staticJava and L workbook decoders are independently implemented; raw files, published maps and three General9 named literals shared.',
 'source_math_audit':'Root read both full decoder/checker kernels, primary six-coordinate embedding/transform specifications and Theorem6.3/Prop6.2(b). Source search completeness is a published premise, not replayed here.'}
(D/'ROOT_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
(D/'ACCEPTED_RAW_HISTOGRAMS.json').write_text(json.dumps({**h,'status':out['status'],'root_verification_sha256':sha(D/'ROOT_VERIFICATION.json')},indent=2)+'\n')
print(out['status'],sha(D/'ACCEPTED_RAW_HISTOGRAMS.json'))
