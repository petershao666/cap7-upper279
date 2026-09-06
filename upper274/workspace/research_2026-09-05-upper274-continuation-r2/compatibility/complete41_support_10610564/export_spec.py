"""Export mathematical data, never import this module in an independent checker.
The read-only producer loader supplies frozen constants, not precomputed grids.
No optimizer or large matrix enumeration is called here.
"""
from pathlib import Path
import json, hashlib, math, sys, time
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W))
import run as D

def pure(x):
    if hasattr(x,'tolist'): return x.tolist()
    if isinstance(x,dict): return {str(k):pure(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [pure(v) for v in x]
    return x

def forced(key,d):
    a,b,c=key
    return [((3**(d-2)-1)//2)*a*b*c]+[v for n in key for v in (3**(d-2)*math.comb(n,2),3**(d-3)*math.comb(n,3))]

def feature_rows(c,d,upper):
    key=c['type'];F=forced(key,d)
    desc=[{'index':0,'kind':'exact','definition':'sum_i,j a_i*b_j*c_(-i-j mod3)'}]
    for j in range(3):
        desc += [dict(index=1+2*j,kind='exact',definition='E2 of sorted physical column',column=j),dict(index=2+2*j,kind='exact',definition='E3 of sorted physical column',column=j)]
    for ex in c['extra']:
        k=len(F);F.append(ex[-1]);desc.append(dict(index=k,kind='upper' if k in upper else 'exact',descriptor=ex))
    assert len(F)==len(c['coeff'])
    for k,z in enumerate(desc):z['forced']=F[k];z['coefficient']=c['coeff'][k]
    assert all(c['coeff'][j]>=0 for j in upper)
    return F,desc

def main():
    started=time.monotonic();r=json.loads((W/'RESULT.json').read_text());freeze=json.loads((W/'CANDIDATE_FROZEN.json').read_text())
    assert r['claim']=='CANDIDATE_EXACT_CERTIFICATE'
    for name,sha in freeze['files'].items():assert hashlib.sha256((W/name).read_bytes()).hexdigest()==sha
    check=json.loads((W/'INTERFACE_CHECK.json').read_text());features={(z['m'],tuple(z['key'])):z for z in check['case_features']}
    cs=[]
    for m,d,order in [(40,5,D.ORDER40),(106,6,D.ANCH[106])]:
        records={tuple(c['type']):c for c in r['histograms'][str(m)]['inner']}
        for i,key in enumerate(order):
            z=dict(layer_size=m,dimension=d,case_index=i,anchor=key,refinement_count=(3**(d-1)-1)//2,whole_direction_count=(3**d-1)//2,first_anchor_prefix=order[:i],ordinary_whole_bans=[] if m==40 else D.OLD,NC_completion_bans=[] if m==40 else D.COMP)
            if key not in records:
                assert m==40 and key==(14,13,13);z.update(empty=True,expected_normalized_cover_count=0)
            else:
                c=records[key];fi=features[m,key];F,desc=feature_rows(c,d,fi['upper_indices']);z.update(empty=False,certificate=c,forced=F,features=desc,upper_indices=fi['upper_indices'],expected_normalized_cover_count=c['count'])
            cs.append(z)
    oc=r['outer'][0];outer_extra=features[275,tuple(oc['type'])]['features'];outer=dict(oc,extra=outer_extra)
    F,desc=feature_rows(outer,7,list(range(7,len(outer['coeff']))))
    outer.update(dimension=7,refinement_count=364,forced_feature_vector=F,features=desc,ordinary_bans=r['ordinary_bans'],minimum_potential=dict(definition='9abc-899(ab+ac+bc)+15730000',anchor_value=D.Q(tuple(oc['type'])),predicate='every transverse whole275 type t has Q67(t)>=Q67(anchor)'),NC_columns=[0,1],NC_completion_bans=D.COMP,new_phi106_columns=[0])
    T4=[(a,b,c)for a in range(10)for b in range(a+1)for c in range(b+1)if D.S40.D.A4[a,b,c]]
    T5=[(a,b,c)for a in range(21)for b in range(a+1)for c in range(b+1)if D.J.ADM5[a,b,c]]
    outer_adm=D.en.__globals__['ADM'];U=outer_adm.shape[0]-1;T6=[(a,b,c)for a in range(U+1)for b in range(a+1)for c in range(b+1)if outer_adm[a,b,c]]
    sources={}
    root=W.parents[1].parents[0]
    for mod in list(sys.modules.values()):
        p=getattr(mod,'__file__',None)
        if p:
            p=Path(p).resolve()
            if p.suffix=='.py' and p.is_relative_to(root) and p.exists():sources[str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
    spec=dict(status='FROZEN_INTEGER_CANDIDATE_PURE_DATA_SPEC_ROOT_AUDIT_PENDING',candidate_sha256=freeze['files']['RESULT.json'],target=[106,105,64],grid_convention=dict(columns=['a0,a1,a2','b0,b1,b2','c0,c1,c2'],row_major_clash_flat='a0,b0,c0,a1,b1,c1,a2,b2,c2',transverse_profile='sort_desc([a[r]+b[(r+s)%3]+c[(r+2*s)%3] for r in0..2]), s=0,1,2',nine_transversal_cell_triples='(a[i],b[j],c[(-i-j)%3]), i,j=0..2',normalization='a descending; b lexicographically maximal among its3 cyclic shifts; c all ordered; no further dedup',normalization_scope='complete cover, not asserted unique orbit representatives'),cases=cs,main_functions=r['histograms'],local_supports=r['local_supports'],conditional_functions=r['conditional_functions'],conditional_types=r['conditional_types'],conditional_bounds=r['conditional_bounds'],allowed_ordered18_pairs=D.PAIR,allowed_conditional20182_full18_states=D.COND,physical18_state_histograms=D.H18,physical18_state_order_input=D.ST,actual16=D.ACTUAL16,actual17=D.ACTUAL17,actual41=D.ACTUAL41,upper5_functions=r['upper5'],fixed6_functions=r['fixed6_functions'],outer=outer,allowed_cell_line_profiles={'4D_sections':T4,'5D_sections_with_old4_bans_only':T5,'6D_sections_outer':T6},lower40_clashes=dict(base_grids=sys.modules['clashes'].GRIDS,expanded_patterns=D.S40.PATTERNS,group='all432 AGL(2,3) maps on row-major grid labels'),additional_lower40_predicates=['Every physical size18 column sorted profile belongs to the12-type full18 profile domain.', 'First-anchor prefixes apply only to this whole40 case.', 'No full41 zero-profile hard pruning is used in NC106.'],old6_ordinary_bans=D.OLD,NC_completion_bans=D.COMP,NC106_support=D.SUP[106],NC106_anchor_cover_root=D.ROOT[106],lower40_order=D.ORDER40,source_python_hashes=sources,export_seconds=time.monotonic()-started,no_optimizer_or_matrix_enumeration_called=True)
    # Export explicit support-family maxima for convenient independent replay.
    hs={16:D.H16,17:D.H17,18:D.H18,41:D.H41}
    maxima={}
    for name,l in r['local_supports'].items():
        vals=[sum(int(a)*int(b)for a,b in zip(h,l['phi']))for h in hs[l['m']]]
        assert max(vals)==l['bound'];maxima[name]=dict(maximum=max(vals),maximizing_histogram_indices=[i for i,x in enumerate(vals)if x==max(vals)])
    spec['support_maximizers']=maxima
    (W/'RAW_AUDIT_SPEC.json').write_text(json.dumps(pure(spec),indent=2)+'\n')
    for name,sha in freeze['files'].items():assert hashlib.sha256((W/name).read_bytes()).hexdigest()==sha
    out=dict(status='PURE_DATA_EXPORT_PASS',sha256=hashlib.sha256((W/'RAW_AUDIT_SPEC.json').read_bytes()).hexdigest(),case_count=len(cs),source_code_hashes=len(sources),seconds=time.monotonic()-started)
    (W/'RAW_AUDIT_SPEC_FROZEN.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
