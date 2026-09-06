from pathlib import Path
from hashlib import sha256
import json,struct,time
start=time.monotonic()
p=Path(__file__).resolve().parent;b=p.parent.parent
digest=lambda f:sha256(f.read_bytes()).hexdigest()
frozen=json.loads((p/'FROZEN.json').read_text())
for name,h in frozen['files'].items():assert digest(p/name)==h,name
own=json.loads((p/'COUNTS.json').read_text());inp=json.loads((p/'INPUTS.json').read_text())
hdir=b/'hist105106/h22_complete41'
manifest=json.loads((hdir/'DOMAIN_EXPORT.json').read_text())
assert manifest['SUP106']==inp['support106']
pr=json.loads((hdir/'ordinary5D_pruning.json').read_text())
assert [pr['ordinary5D_old_admissible_ordered_profiles'],pr['ordinary5D_new_admissible_ordered_profiles']]==own['ordered_5D_profile_counts']
assert pr['ordinary5D41_zero_types']==inp['zero41']
lpath=b/'compatibility/complete41_support_10610564/RESULT.json'
assert digest(lpath)=='0fde44267b424bac9570b72813e8af4f0a44e0e7e87ba5ce9ae118af57881e97'
lc=json.loads(lpath.read_text())['histograms']['106']['inner']
details=[]
for r,h,q,l in zip(own['cases'],manifest['cases'],pr['nc106_cases'],lc,strict=True):
    i=r['case'];old,new=r['modes']
    assert r['anchor']==h['anchor']==q['type']==l['type']
    assert old['discovery_cover']==q['before']==l['count']
    assert new['discovery_cover']==q['after']==h['count']
    source=hdir/h['file'];assert digest(source)==h['sha256']
    raw=(p/f'case{i:02d}_new_features.i32le').read_bytes()
    with source.open() as stream:
        assert int(next(stream))==h['count']
        for k,line in enumerate(stream):
            row=tuple(map(int,line.split()));assert len(row)==19
            assert struct.pack('<19i',*row)==raw[76*k:76*(k+1)],(i,k)
        assert k+1==h['count']
    details.append({'case':i,'anchor':r['anchor'],'old_cover':old['discovery_cover'],'new_cover':new['discovery_cover'],'all_H_19_integer_rows_equal_in_order':True,'H_file_sha256':h['sha256'],'own_new_feature_sha256':digest(p/f'case{i:02d}_new_features.i32le')})
res={'status':'PASS_ALL14_H_FULL_ORDERED_FEATURE_ROWS_AND_L_OLD_CASE_COUNTS',
     'own_prefreeze_sha256':digest(p/'FROZEN.json'),'H_export_sha256':digest(hdir/'DOMAIN_EXPORT.json'),
     'L_candidate_sha256':digest(lpath),'cases':details,
     'old_total_raw':sum(r['modes'][0]['raw'] for r in own['cases']),
     'new_total_raw':sum(r['modes'][1]['raw'] for r in own['cases']),
     'old_total_cover':sum(r['modes'][0]['discovery_cover'] for r in own['cases']),
     'new_total_cover':sum(r['modes'][1]['discovery_cover'] for r in own['cases']),
     'comparison_seconds':time.monotonic()-start,
     'boundary':'All H new-domain rows compared, preserving ordered transverse IDs and duplicate multiplicities. L old-domain case counts and explicitly identical normalization/predicate definitions compared; L full row bytes were not supplied or claimed compared. The independent full old raw grids are available for integer candidate replay.'}
(p/'INDEPENDENT_COMPARISON.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k!='cases'},indent=2))
