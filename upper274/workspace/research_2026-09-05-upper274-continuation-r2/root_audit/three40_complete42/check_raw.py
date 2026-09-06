"""Bind and summarize root's independent raw replay; standard library only."""
from pathlib import Path
import hashlib,json,re

W=Path(__file__).resolve().parent
R=W.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
a=read(W/'ACTIVATION.json');cp=R/a['certificate_path'];c=read(cp)
assert sha(cp)==a['certificate_sha256']=='78238a2e3f389f9c7a4f93e049ad56e678c09103151fb3bfed0adc6e1dcf14bf'
s=read(W/'SUPPORT_VERIFICATION.json')
assert s['status']=='INDEPENDENT_DATA_AND_SUPPORT_MAXIMA_PASS'
assert s['certificate_sha256']==sha(cp)
assert s['input_sha256']==sha(W/'input.txt')
assert s['root_code_sha256']==sha(W/'export.py')
assert (W/'verify.err').read_bytes()==b''
accepted_inputs={
 'root_audit/actual16/ACCEPTED_HISTOGRAMS.json':'3776b3593a186ddb06b8af9f78b9b95860f7218106236fa2cc5fce693c470b28',
 'root_audit/actual17/ACCEPTED_HISTOGRAMS.json':'8ed6c68858ca68f5f9ace601a27efc25895c9a9c544f6937f1c78d1b65219936',
 'root_audit/complete41/ACCEPTED_HISTOGRAMS.json':'38193858291a37b0b71cff568a11db481080125140771e41af57f6fd973374fa',
 'hist105106/h13/table1_input_v2.json':'53c9eed8fd51492cf4b68eea42ce061aae55786e614540b6a50ab3e86bf2f470',
 'hist105106/h10/full18_states.json':'4fcdc14a30fb3a209ce4a9709aced518272abfaf9a4609535622013e814c127e',
 'hist105106/h3/hist19_20.json':'5a5da7eab7de70c62b6796b4775095447a651dbce3458bad0dea326d093d10d1',
 'hist105106/h3/clash_data.json':'ab706e8201ad00a4f55c4b54052f0cd7ea5449d04b17a679eae92761e47e4b36',
 'hist105106/h23_r105_transfer/FIXED_INPUTS.json':'67f55e2bd21955542e97e63f26b2d36930533666d02e5fac215e219507005bae',
 '../audit_2026-09-05_upper275/cap7_upper275/baseline277/baseline278/certificate.json':'2780fba39eff792892e7aac960675e1ffdf8b2cf99b0c3b9e29d1123a98435be',
 '../research_2026-09-05-capset-round1-r1/route_a/certificates.json':'e661a17a83aaaced1580c39fa2d0bb5af39a0a557be70b7ee71709c7a6ed6829',
}
for p,h in accepted_inputs.items():assert sha(R/p)==h,p
assert read(R/'hist105106/h13/table1_input_v2.json')['label_order'][21]=='20-cap'
rx=re.compile(r'CASE (\d+) N (\d+) anchor (\d+),(\d+),(\d+) raw (\d+) canonical (\d+) min (EMPTY|-?\d+) K (-?\d+) bound (-?\d+) gap (-?\d+)')
lines=(W/'verify.log').read_text().splitlines();rows=[]
for i,line in enumerate(lines[:-1]):
    m=rx.fullmatch(line);assert m,line
    z=m.groups();row=dict(index=int(z[0]),n=int(z[1]),anchor=list(map(int,z[2:5])),raw=int(z[5]),canonical=int(z[6]),minimum=None if z[7]=='EMPTY' else int(z[7]),K=int(z[8]),bound=int(z[9]),gap=int(z[10]))
    assert row['index']==i
    assert row['minimum'] is None or row['minimum']>=row['K']
    rows.append(row)
assert len(rows)==133
tot=re.fullmatch(r'PASS cases 133 raw (\d+) canonical (\d+) seconds ([\d.]+)',lines[-1]);assert tot
assert int(tot[1])==sum(z['raw']for z in rows)==7701024
assert int(tot[2])==sum(z['canonical']for z in rows)==2570134
tiers={}
for i,tier in enumerate([400,401,402]):
    rr=rows[44*i:44*(i+1)];d=c['histograms'][str(tier)]
    assert all(z['n']==40 for z in rr)
    assert sum(z['minimum'] is None for z in rr)==1
    assert rr[-1]['anchor']==[14,13,13] and rr[-1]['raw']==0
    by={tuple(z['type']):z for z in d['inner']}
    for z in rr[:-1]:
        q=by[tuple(z['anchor'])]
        assert (z['K'],z['bound'],z['canonical'])==(q['K'],q['bound'],q['count'])
    assert max(z['bound']for z in rr[:-1])==d['bound']
    assert sum(z['raw']for z in rr)==106239
    assert sum(z['canonical']for z in rr)==36455
    tiers[str(tier)]={'mathematical_size':40,'bound':d['bound'],'raw':106239,'canonical':36455,'nonempty_cases':43,'conditional_empty_cases':1}
out=rows[-1];q=c['outer'][0]
assert out['anchor']==[106,106,63] and out['n']==275
assert (out['K'],out['minimum'],out['bound'],out['gap'])==(q['K'],q['K'],q['forced'],q['gap'])
assert out['gap']==364*out['K']-out['bound']==148616699075
assert out['raw']==7382307 and out['canonical']==2460769
assert all(v==0 for v in q['coeff'][7:]),'Nonzero fixed outer upper row needs explicit theorem dependency'
result={'status':'INDEPENDENT_ROOT_RAW40_AND_OUTER_PASS','certificate_sha256':sha(cp),'tiers':tiers,'outer':out,'cases':133,'raw':7701024,'canonical':2570134,'elapsed_seconds':float(tot[3]),'finite_support_checks':s['finite_support_checks'],'arithmetic':'C++ signed128 products and sums, undefined-behavior sanitizer clean; Python arbitrary-precision support arithmetic','normalization':'First physical column sorted by one common affine relabelling of three refinement levels; all ordered second and third columns. No physical column quotient. Canonical counts only compare the cyclic cover.','scope':'All three universal40 tiers and last minimum outer case. NC106 layer requires separate P verification.','fixed_outer_upper_coefficients_all_zero':True,'input_hashes':{str(p.relative_to(R)):sha(p)for p in [cp,W/'ACTIVATION.json',W/'SUPPORT_VERIFICATION.json',W/'input.txt',W/'export.py',W/'verify.cpp',W/'verify.log',W/'verify.err',Path(__file__)]},'rows':rows}
result['accepted_input_hashes']=accepted_inputs
(W/'ROOT_RAW_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k not in ['rows','input_hashes']},indent=2))
