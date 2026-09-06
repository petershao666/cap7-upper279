"""Pure JSON terminal packaging, including explicit function-ID units.
No optimizer, coefficient modification or geometry enumeration.
"""
from pathlib import Path
from math import comb
import hashlib,json
W=Path(__file__).resolve().parent;R=W.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def size(function):return 40 if int(function)in(400,401,402)else int(function)
def force(t,d):
    a,b,c=t;return [((3**(d-2)-1)//2)*a*b*c]+[v for n in t for v in (3**(d-2)*comb(n,2),3**(d-3)*comb(n,3))]
def main():
    static=json.loads((W/'STATIC_FROZEN.json').read_text())
    assert all(sha(W/n)==h for n,h in static['files'].items())
    raw=json.loads((W/'RESULT.json').read_text());candidate=raw['claim']=='CANDIDATE_EXACT_CERTIFICATE'
    out=json.loads(json.dumps(raw));out['source_result_sha256']=sha(W/'RESULT.json')
    out['function_id_units']='400/401/402 are different functions on mathematical size40 caps'
    for key in ['counts','empty_cases']:
        for x in out.get(key,[]):x['function_id']=x['m'];x['mathematical_size']=size(x['m'])
    layout=json.loads((W/'REALIZED_COPY_LAYOUT.json').read_text());out['copy_layout']=layout
    out['ordinary5D_pruning_metadata']=json.loads((W/'ordinary5D_pruning.json').read_text())
    signs=json.loads((W/'SIGNS_AND_FEATURES.json').read_text());out['fixed_inputs_and_signs']=signs
    for x in out['fixed_inputs_and_signs']['inner']:x['function_id']=x['m'];x['mathematical_size']=size(x['m'])
    if candidate:
        for name,l in out['local_supports'].items():l['mathematical_size']=l['m'];l['parent_function_id']=l['case_dimension_size'];l['parent_mathematical_size']=size(l['case_dimension_size'])
        for function,h in out['histograms'].items():
            h['function_id']=int(function);h['mathematical_size']=size(function);d=5 if size(function)==40 else 6
            for c in h['inner']:
                c['function_id']=int(function);c['mathematical_size']=size(function);c['forced_feature_vector']=force(c['type'],d)+[ex[-1]for ex in c['extra']]
                assert len(c['forced_feature_vector'])==len(c['coeff'])
        for c in out['outer']:c['forced_feature_vector']=force(c['type'],7)+[ex[-1]for ex in c['extra']];assert len(c['forced_feature_vector'])==len(c['coeff'])
    old=json.loads((R.parent/'research_2026-09-05-capset-round1-r1/route_a/certificates.json').read_text());bans=old['seeds']+[[112,109,51],[111,110,51]]+[[int(v)for v in k.split(',')]for st in old['stages']for k in st];assert len(bans)==18
    out['ordinary7D_bans']=bans;out['ordinary_exclusion']=False;out['global_upper_not_promoted_by_packager']=True
    name='NORMALIZED_CERTIFICATE.json'if candidate else'NORMALIZED_TERMINAL.json'
    (W/name).write_text(json.dumps(out,indent=2)+'\n')
    files=['RESULT.json','run.py','verify.py','INPUTS.json','STATIC_FROZEN.json','PLANNED_COPY_LAYOUT.json','REALIZED_COPY_LAYOUT.json','interface_check.json','all_case_coverage.json','SIGNS_AND_FEATURES.json','FUNCTION_ID_SCHEMA.md','DERIVATION.md',name]
    freeze=dict(status='CANDIDATE_FROZEN_PENDING_EXACT_REPLAYS'if candidate else'BOUNDED_NO_INTEGER_CERTIFICATE',files={n:sha(W/n)for n in files},target=[106,106,63],ordinary_exclusion=False,candidate_gap=raw['outer'][0]['gap']if candidate else None,numerical_stop=raw['numerical_status'],discovery_seconds=raw['elapsed'],iterations=raw['iterations'])
    (W/'TERMINAL_FROZEN.json').write_text(json.dumps(freeze,indent=2)+'\n');print(json.dumps(freeze,indent=2))
if __name__=='__main__':main()
