require 'json'
require 'digest'
require 'pathname'
started=Process.clock_gettime(Process::CLOCK_MONOTONIC)
own=Pathname.new(__dir__); base=own.parent.parent
sha=->(p){Digest::SHA256.file(p).hexdigest}
producer=base+'compatibility/physical40_interface_gate'
w=JSON.parse((producer+'WITNESS.json').read)
raise 'Witness identity' unless sha.call(producer+'WITNESS.json')=='664e33284b89acbe9ec03ac5d8abc4606f4558fd0acce9be43de0b1e8f5b2738'
w['input_sha256'].each{|name,h|raise "source identity #{name}" unless sha.call(base+name)==h}
types=w['types']; raise unless types.uniq.length==7 && types.all?{|t|t.sum==40&&t.sort.reverse==t}
rat=->(a){a.map{|v|Rational(v)}}
bar=rat.call(w['hbar']);v=w['v_numerator'].map{|n|Rational(n,w['v_denominator'])}
zp=rat.call(w['z_plus']);zm=rat.call(w['z_minus']);z3=rat.call(w['third_marginal'])
raise unless zp==bar.zip(v).map{|a,b|a+b}&&zm==bar.zip(v).map{|a,b|a-b}&&z3==bar
raise unless [zp,zm,z3].all?{|z|z.all?{|x|x>=0}}
raise unless zp.zip(zm,z3).map{|a,b,c|(a+b+c)/3}==bar

# Use P's independently generated actual20200 catalogue, not L's endpoint generator.
catalogue_path=base+'root_potential/complete20200/HISTOGRAMS.json'
catalogue=JSON.parse(catalogue_path.read)
actual=catalogue['histograms'].map{|h|catalogue['types'].zip(h['counts']).to_h}
raise unless actual.length==8
lo=actual.min_by{|h|h.fetch([18,18,4],0)};hi=actual.max_by{|h|h.fetch([18,18,4],0)}
raise unless lo.fetch([18,18,4])==0&&hi.fetch([18,18,4])==10
raise unless [lo,hi].all?{|h|h.all?{|t,n|n==0||types.include?(t)}}
raise unless bar==types.map{|t|Rational(lo.fetch(t),2)+Rational(hi.fetch(t),2)}

e2=->(t){a,b,c=t;a*b+a*c+b*c};e3=->(t){t.reduce(:*)}
rows=[Array.new(7,1),types.map(&e2),types.map(&e3)]
choose=->(n,k){(1..k).reduce(1){|a,i|a*(n-i+1)/i}}
totals=[121,81*choose.call(40,2),27*choose.call(40,3)]
raise unless rows==w['exact_moment_rows']&&totals==w['exact_moment_totals']
dot=->(a,b){a.zip(b).sum{|x,y|x*y}}
raise unless rows.all?{|r|dot.call(r,v)==0}
raise unless [zp,zm,z3].all?{|z|rows.map{|r|dot.call(r,z)}==totals}
h3path=base+'hist105106/h3/h3_result.json';h3=JSON.parse(h3path.read)['histograms']['40']
f=h3['types'].zip(h3['phi']).to_h
fh=types.map{|t|f.fetch(t)}
raise unless fh==w['H3_values']&&h3['bound']==w['H3_bound']
raise unless dot.call(fh,v)==0
sums=[zp,zm,z3].map{|z|dot.call(fh,z)}
raise unless sums.uniq==[Rational(w['H3_sum_at_all_three'])]
slack=h3['bound']-sums[0];raise unless slack==w['H3_slack']&&slack>0
idx=types.index([20,20,0]);raise unless [zp[idx],zm[idx],z3[idx]]==[2,0,1]
raise unless zp[idx]-1==w['strict_violation_at_z_plus']

nc=JSON.parse((base+'root_potential/complete41_domain_audit/INPUTS.json').read)['anchors106']
slots=nc.each_with_index.flat_map{|t,i|t.each_index.select{|j|t[j]==40}.map{|j|{'NC106_case_index'=>i,'anchor'=>t,'physical_column'=>j}}}
raise unless slots==w['parent_sections']&&slots.length==3
interface=JSON.parse((base+'compatibility/complete41_support_10610564/INTERFACE_CHECK.json').read)
lower=interface['case_features'].select{|c|c['m']==40}
h23=JSON.parse((base+'hist105106/h23_run/h23_result.json').read)
fulltypes=(0..20).flat_map{|a|(0..a).map{|b|c=40-a-b;[a,b,c] if c>=0&&c<=b}.compact}.reverse
actual_order=h23['counts'].select{|c|c['m']==40}.map{|c|c['type']}
empty=h23['empty_cases'].select{|c|c['m']==40}.map{|c|c['type']}
raise unless fulltypes.length==44&&actual_order==fulltypes.reject{|t|empty.include?(t)}&&empty==[[14,13,13]]
raise unless lower.map{|c|c['key']}==actual_order
qcount=lower.sum{|c|c['feature_count']}; ngrid=lower.sum{|c|c['count']}
raise unless qcount==379&&ngrid==36455
lowvars=10*(14+1)+10*(13+1)+8*(12+1)
jointvars=3*12+2
one=44+1+qcount+lowvars+jointvars
rows_per_copy=10*376+10*102+8*17+267+16
raise unless one==w['one_complete40_tier_variables']&&2*one==w['additional_variables']
raise unless rows_per_copy*3+6*44==w['finite_support_rows']&&3*ngrid==w['lower40_table_evaluations']
raise unless w['no_parent_grid_lift_claimed']&&w['no_optimizer_or_new_enumeration']

out={'status'=>'PASS_EXACT_RATIONAL_INTERFACE_WITNESS_AND_COPY_ARITHMETIC',
 'witness_sha256'=>sha.call(producer+'WITNESS.json'),
 'independent_actual20200_catalogue_sha256'=>sha.call(catalogue_path),
 'actual_endpoint_histograms'=>{'types'=>catalogue['types'],'h0'=>catalogue['types'].map{|t|lo[t]},'h10'=>catalogue['types'].map{|t|hi[t]}},
 'all_nonnegative'=>true,'all_three_averages_equal_actual_endpoint_midpoint'=>true,
 'computed_moment_totals'=>totals,'perturbation_moment_dots'=>rows.map{|r|dot.call(r,v).to_s},
 'H3_perturbation_dot'=>dot.call(fh,v).to_s,'H3_sums'=>sums.map(&:to_s),'H3_slack'=>slack.to_s,
 'centered_H3_sums'=>sums.map{|x|(x+121*10**10).to_s},'centered_H3_bound'=>h3['bound']+121*10**10,
 'indicator_20200_values'=>[zp[idx],zm[idx],z3[idx]].map(&:to_s),'indicator_bound'=>1,
 'physical_slots'=>slots,'full40_anchor_order'=>fulltypes,'conditional_empty_case'=>empty,
 'copy_counts'=>{'one_tier_variables'=>one,'additional_variables'=>2*one,'finite_support_rows'=>3*rows_per_copy+264,'lower40_table_evaluations'=>3*ngrid},
 'arithmetic_code_sha256'=>sha.call(Pathname.new(__FILE__)),
 'seconds'=>Process.clock_gettime(Process::CLOCK_MONOTONIC)-started,
 'independence'=>'Ruby Rational arithmetic and P own accepted20200 catalogue; no L generation code read/imported. Published/accepted spectra and H3 theorem shared.',
 'scope'=>'Strict separation of the isolated shared-versus-individual40 marginal block, retaining fixed H3 separately; no full-parent feasibility or optimizer success claim.',
 'separate_optional_absorption_claim'=>'Not established merely by this witness. H3 membership in the particular descending-anchor C40 proof cone needs an explicit proof or the fixed H3 row should remain.'}
(own+'RATIONAL_VERIFICATION.json').write(JSON.pretty_generate(out)+"\n")
puts JSON.pretty_generate(out.reject{|k,v|['actual_endpoint_histograms','full40_anchor_order','independence','scope','separate_optional_absorption_claim'].include?(k)})
