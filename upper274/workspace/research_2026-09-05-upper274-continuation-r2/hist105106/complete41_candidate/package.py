from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;ROOT=W.parents[1]
u=json.loads((W/'CANDIDATE_UNION.json').read_text());support=json.loads((W/'PROFILE_SUPPORT.json').read_text())
source='https://arxiv.org/html/2206.09719v1'
alternatives=[]
for a in range(1,14):
 occurrences=[s for h in u['histograms']for s in h['sources']if s['alternative']==a]
 labels=['45-cap minus four points','Delta686 minus one point']+['41'+c for c in 'ABCDEFGHI']+['complete cap admitting (20,20,1)','complete cap with no (18,18,5), and a saddled cube shared by an 18-section of an (18,17,6) or (18,16,7) direction and another section of size 18, 17 or 16']
 alternatives.append({'alternative':a,'published_option_paraphrase':labels[a-1],'source_locator':source+'#S6.Thmtheorem3.p1.1','covering_input_families':sorted(set(s['family']for s in occurrences)),'source_occurrence_count':len(occurrences),'all_input_occurrences_individually_accepted':all(s['family_verification_status']=='ROOT_ACCEPTED'for s in occurrences),'scope_note':('All four-deletions of one affine-unique 45-cap; all are extendable.'if a==1 else 'All 42 single deletions, grouped into two spectra; all are extendable.'if a==2 else 'Named source point representative; published remark states completeness and absence of (20,20,1).'if 3<=a<=11 else 'Input includes every cap admitting (20,20,1); completeness is not imposed. This safely covers the narrower complete subclass.'if a==12 else 'All 34345 positive raw outputs retained. Proposition6.2(b) and Theorem6.3 proof cover the required exceptional subclass. No completeness or absence-(18,18,5) filtering is needed for a safe overcover.')})
(W/'SOURCE_ALTERNATIVES.json').write_text(json.dumps({'status':'COVERAGE_PROOF_PENDING_ROOT_FINAL_ACCEPTANCE','alternatives':alternatives,'source_html_sha256':u['source_hashes']['hist105106/h13/source_article.html'],'outside_last_alternative_exactly_one_of_first_twelve':True,'last_alternative_overlap_permitted':True},indent=2)+'\n')
nodes=[
 {'id':'c4_bound','kind':'published_premise','claim':'Every affine 4D cap has at most20 points; hence the forty sorted41-types exhaust all directions.'},
 {'id':'thm63','kind':'published_premise','locator':source+'#S6.Thmtheorem3.p1.1','claim':'Every 5D41-cap is in one of the13 listed alternatives; outside alternative13 it is in exactly one other alternative.'},
 {'id':'prop62b','kind':'published_premise','locator':source+'#S6.I1.ix2.p1.1','claim':'Supplementary lists cover all isomorphism classes in the stated saddled-cube exceptional option, allowing duplicate representatives.'},
 {'id':'thm63proof','kind':'published_premise','locator':source+'#S6.p10.1','claim':'The supplementary-list coverage is explicitly restated for alternative13 itself.'},
 {'id':'unique45','kind':'published_premise','locator':source+'#S4.p1.1','claim':'There is one affine-isomorphism class of45-caps; the paper proves this again in Section4.'},
 {'id':'named_AE','kind':'accepted_finite_input','file':'root_audit/named41_pdf/ACCEPTED_POINTS.json'},
 {'id':'named_FI_delta','kind':'accepted_finite_input','file':'root_audit/h9_named_independent.json'},
 {'id':'four_delete','kind':'accepted_finite_input','file':'root_audit/fortyfive/ACCEPTED_FOUR_DELETE_HISTOGRAMS.json','count':148995,'spectra':27},
 {'id':'all20201','kind':'accepted_finite_input','file':'root_audit/complete20201/ACCEPTED_HISTOGRAM.json','spectra':1},
 {'id':'raw_family','kind':'accepted_finite_input','file':'root_audit/exceptional41_raw/ACCEPTED_RAW_HISTOGRAMS.json','positive_rows':34345,'spectra':41,'note':'Primary search/list completeness remains a literature premise; independent decoding does not reprove that search.'},
 {'id':'static_union','kind':'this_finite_integration','file':'CANDIDATE_UNION.json','spectra':44,'source_occurrences':80,'status':'PENDING_ROOT_FINAL_COVERAGE_AND_UNION_AUDIT'},
 {'id':'ordinary_profile_zeros','kind':'conditional_corollary','file':'PROFILE_SUPPORT.json','absent_types':len(support['absent_types']),'status':'PENDING_COMPLETE_FAMILY_ACCEPTANCE'},
 {'id':'global274','kind':'not_claimed','status':'NO_GLOBAL_BOUND_IMPROVEMENT_FROM_THIS_TASK'}]
edges=[['unique45','four_delete'],['prop62b','raw_family'],['thm63proof','raw_family']]+[[n,'static_union']for n in ['thm63','c4_bound','named_AE','named_FI_delta','four_delete','all20201','raw_family']]+[['static_union','ordinary_profile_zeros']]
(W/'DEPENDENCY_DAG.json').write_text(json.dumps({'nodes':nodes,'edges':edges,'edge_meaning':'first is an explicit premise for second','shared_dependency_boundary':'All decoders and the source coverage audit share the published classification and primary supplementary outputs. H and L used independent static-coordinate decoders, but shared a prior one-SC-record format fixture; full outputs were independently frozen before comparison.'},indent=2)+'\n')
with (W/'REPRESENTATIVE_POINTS.tsv').open('w') as f:
 f.write('histogram_id\tpoint_number\tx1\tx2\tx3\tx4\tx5\n')
 for h in u['histograms']:
  for j,p in enumerate(h['representative_points']):f.write('\t'.join(map(str,[h['id'],j,*p]))+'\n')
status={'status':'CANDIDATE_COMPLETE_41_HISTOGRAM_FAMILY_FROZEN_PENDING_ROOT_UNION_AND_SOURCE_ACCEPTANCE','histogram_count':44,'types':40,'present_types':26,'absent_types':14,'source_occurrences':80,'all13_alternatives_covered_conditionally_on_published_inputs':True,'all_individual_family_inputs_root_accepted':True,'pending':['root_final_union_audit','independent_P_source_coverage_confirmation'],'proof_scope':'Exact actual histogram family is conditional on the cited published classification/list completeness and final union audit. This is input recovery, not new global mathematics.','LP_runs':0,'full_raw_rows_reverified':0,'computation_seconds_runs':[0.171,0.22114195814356208,0.18005333305336535],'all_computation_under_180_seconds':True,'global_upper_bound_improvement_claimed':False}
(W/'FINAL_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
