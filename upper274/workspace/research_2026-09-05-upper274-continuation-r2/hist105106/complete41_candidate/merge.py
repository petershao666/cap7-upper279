"""Static source-family union and representative checks; no LP/full raw replay."""
from pathlib import Path
from itertools import product,combinations
from collections import Counter
import json,hashlib,time

W=Path(__file__).resolve().parent;ROOT=W.parents[1]
TYPES=[(a,b,41-a-b)for a in range(21)for b in range(a+1)if 0<=41-a-b<=b]
assert len(TYPES)==40
NORMALS=[v for v in product(range(3),repeat=5)if any(v)and next(x for x in v if x)==1]
assert len(NORMALS)==121

def read(path):return json.loads((ROOT/path).read_text())
def full(types,counts):
    d=dict(zip(map(tuple,types),counts));assert len(d)==len(types)and set(d)<=set(TYPES)
    h=tuple(int(d.get(t,0))for t in TYPES);assert all(x>=0 for x in h)and sum(h)==121
    return h

def verify(points):
    ps=sorted(tuple(p)for p in points);assert len(ps)==len(set(ps))==41
    assert all(len(p)==5 and all(0<=x<3 for x in p)for p in ps)
    ss=set(ps)
    for p,q in combinations(ps,2):assert tuple((-a-b)%3 for a,b in zip(p,q))not in ss
    hist=Counter()
    for v in NORMALS:
        c=Counter(sum(a*b for a,b in zip(v,p))%3 for p in ps)
        hist[tuple(sorted([c[i]for i in range(3)],reverse=True))]+=1
    h=full(list(hist),list(hist.values()))
    assert sum(n*(a*b+a*c+b*c)for n,(a,b,c)in zip(h,TYPES))==66420
    assert sum(n*a*b*c for n,(a,b,c)in zip(h,TYPES))==287820
    return ps,h

def main():
    started=time.monotonic();sources={};items=[];groups={}
    def add(family,alternative,status,path,points,expected=None,**extra):
        assert time.monotonic()-started<175
        sources[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        ps,h=verify(points)
        if expected is not None:assert h==expected,(family,extra)
        point_bytes=bytes(81*p[0]+27*p[1]+9*p[2]+3*p[3]+p[4]for p in ps)
        occurrence={'family':family,'alternative':alternative,'family_verification_status':status,'source_file':path,'source_sha256':sources[path],'representative_points':ps,'representative_point_sha256':hashlib.sha256(point_bytes).hexdigest(),**extra}
        if h not in groups:
            groups[h]=len(items);items.append({'id':len(items),'counts':list(h),'representative_points':ps,'sources':[]})
        items[groups[h]]['sources'].append(occurrence)

    path='root_audit/exceptional41_raw/ACCEPTED_RAW_HISTOGRAMS.json';raw=read(path)
    for z in raw['histograms']:
        add('raw_exceptional_overcover',13,'ROOT_ACCEPTED',path,z['points'],full(raw['types'],z['counts']),source_histogram_id=z['id'],raw_representative_row=z['representative_row_id'])

    path='hist105106/h20_20201/histograms41.json';twenty=read(path);accepted=read('root_audit/complete20201/ACCEPTED_HISTOGRAM.json')
    assert set(full(accepted['types'],h)for h in accepted['histograms'])==set(full(twenty['types'],z['counts'])for z in twenty['histograms'])
    for z in twenty['histograms']:
        add('all_20201_41_caps',12,'ROOT_ACCEPTED',path,z['points'],full(twenty['types'],z['counts']),source_histogram_id=z['id'],covers_complete_and_extendable=True)

    path='hist105106/h9/named_points.json';named=read(path);nh=read('hist105106/h9/named_histograms.json')
    for letter in 'FGHI':
        name='41'+letter;z=nh[name]
        add(name,3+ord(letter)-ord('A'),'ROOT_ACCEPTED',path,named[name]['points'],full(z['types'],z['histogram']),named_source=named[name]['source_url'])
    delta=named['Delta686']['points'];assert len(delta)==42
    families=nh['Delta686_minus1_family'];assert sorted(i for f in families for i in f['deleted_point_indices'])==list(range(42))
    for k,f in enumerate(families):
        deletion=f['deleted_point_indices'][0];ps=[p for i,p in enumerate(delta)if i!=deletion]
        add('Delta686_minus1',2,'ROOT_ACCEPTED',path,ps,full(f['types'],f['histogram']),source_histogram_id=k,representative_deleted_index=deletion,all_deleted_indices_for_this_histogram=f['deleted_point_indices'],histogram_source_file='hist105106/h9/named_histograms.json')

    path='root_audit/named41_pdf/ACCEPTED_POINTS.json';eps=read(path);caps={z['name']:z for z in eps['caps']};original_eps=read('root_potential/named41_45_source/EPS_POINTS.json');original_caps={z['name']:z for z in original_eps['caps']}
    for letter in 'ABCDE':
        name='41'+letter;z=caps[name]
        assert sorted(z['points'])==sorted(original_caps[name]['points'])
        add(name,3+ord(letter)-ord('A'),'ROOT_ACCEPTED',path,z['points'],figure=z['figure'],primary_eps_source_file=original_caps[name]['source_file'],primary_eps_source_sha256=original_caps[name]['source_sha256'])

    path='root_audit/fortyfive/ACCEPTED_FOUR_DELETE_HISTOGRAMS.json';fortyfive=read(path)
    assert fortyfive['full_subsets']==148995 and sum(z['four_deletion_frequency']for z in fortyfive['histograms'])==148995
    for k,z in enumerate(fortyfive['histograms']):
        add('45_minus4',1,'ROOT_ACCEPTED',path,z['points'],full(fortyfive['types'],z['counts']),source_histogram_id=k,deleted_input_indices=z['deleted_input_indices'],four_deletion_frequency=z['four_deletion_frequency'])

    sources['hist105106/h9/named_histograms.json']=hashlib.sha256((ROOT/'hist105106/h9/named_histograms.json').read_bytes()).hexdigest()
    sources['root_audit/complete20201/ACCEPTED_HISTOGRAM.json']=hashlib.sha256((ROOT/'root_audit/complete20201/ACCEPTED_HISTOGRAM.json').read_bytes()).hexdigest()
    sources['hist105106/h13/source_article.html']=hashlib.sha256((ROOT/'hist105106/h13/source_article.html').read_bytes()).hexdigest()
    for extra_path in ['root_potential/named41_45_source/EPS_POINTS.json','root_audit/fortyfive/ACCEPTED_POINTS.json','root_audit/h9_named_independent.json','hist105106/fullraw41/INDEPENDENT_COMPARISON.json','compatibility/exceptional41_decode/INDEPENDENT_COMPARISON.json']:
        sources[extra_path]=hashlib.sha256((ROOT/extra_path).read_bytes()).hexdigest()
    for z in items:
        z['has_nonpending_source_occurrence']=any(not s['family_verification_status'].startswith('PENDING')for s in z['sources'])
    present=[i for i in range(40)if any(z['counts'][i]for z in items)]
    support={'status':'CANDIDATE_ORDINARY_5D41_DIRECTION_SUPPORT_PENDING_ROOT_COMPLETE_FAMILY_ACCEPTANCE','types':TYPES,'present_indices':present,'present_types':[TYPES[i]for i in present],'absent_indices':[i for i in range(40)if i not in present],'absent_types':[TYPES[i]for i in range(40)if i not in present],'scope':'After complete family acceptance these zeros exclude ordinary 5D41 profiles universally; they do not convert any 7D minimum-only constraint into an ordinary prohibition.'}
    (W/'PROFILE_SUPPORT.json').write_text(json.dumps(support,indent=2)+'\n')
    occurrences=sum(len(z['sources'])for z in items)
    result={'status':'SOURCE_COMPLETE_CANDIDATE_UNION_PENDING_ROOT_FINAL_COVERAGE_AUDIT','scope':'Candidate support family for every5D41cap under Theorem6.3 and the explicit source coverage DAG. Not accepted for downstream proof yet.','types':TYPES,'histograms':items,'histogram_count':len(items),'source_occurrence_count':occurrences,'representative_pair_checks':820*occurrences,'representative_direction_checks':121*occurrences,'all13_source_alternatives_present':sorted({s['alternative']for z in items for s in z['sources']})==list(range(1,14)),'pending_family_nodes':[],'pending_acceptance_nodes':['root_final_source_coverage_and_union_audit'],'global_upper_bound_improvement_claimed':False,'source_hashes':sources,'seconds':time.monotonic()-started}
    assert result['all13_source_alternatives_present']
    (W/'CANDIDATE_UNION.json').write_text(json.dumps(result,indent=2)+'\n')
    (W/'INPUT_SNAPSHOT.json').write_text(json.dumps({'status':'INDIVIDUALLY_VERIFIED_INPUT_SNAPSHOT_PENDING_FINAL_UNION_AUDIT','source_hashes':sources,'pending_acceptance_unchanged_by_vector_overlap':True},indent=2)+'\n')
    summary={k:v for k,v in result.items()if k not in ['histograms','source_hashes','types']}
    summary['family_vector_counts']=dict(Counter(s['family']for z in items for s in z['sources']))
    (W/'MERGE_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
