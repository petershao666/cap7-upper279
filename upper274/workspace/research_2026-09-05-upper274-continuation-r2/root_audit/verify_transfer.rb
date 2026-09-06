require 'json'
require 'digest'
ROOT=File.dirname(__FILE__)
ROUND=File.expand_path('..',ROOT)
BASE=File.expand_path('../audit_2026-09-05_upper275/cap7_upper275',ROUND)
def ck(v,msg);raise msg unless v;end
def readj(p);JSON.parse(File.read(p));end
def choose(n,k);return 0 if k<0||k>n;k=[k,n-k].min;(1..k).inject(1){|a,i|a*(n-i+1)/i};end
def e2(t);t.combination(2).sum{|a,b|a*b};end
def e3(t);t.inject(:*);end
low=readj(File.join(BASE,'baseline277/baseline278/certificate.json'))
comp=low['completion_seeds']+low['completion_stages'].flat_map{|s|s.keys.map{|k|k.split(',').map(&:to_i)}}
old=low['six_stages'].flat_map{|s|s.keys.map{|k|k.split(',').map(&:to_i)}}
sources=readj(File.join(BASE,'results/size276/proof.json'))['new_histograms']
sources += [readj(File.join(BASE,'baseline277/certificate.json'))['nested108'].merge('id'=>'psi108','m'=>108)]
sources=sources.to_h{|s|[s['id'],s]}
tablepath=File.join(ROUND,'root_potential/transfer_tables.json')
cmpath=File.join(ROUND,'root_potential/transfer_redundancy.json')
trans=readj(tablepath)['functions'];ck(trans.length==7,'seven functions')
checked=0
trans.each do |h|
  n=h['m'];m=h['source_m'];d=n-m;ck([1,2].include?(d),'scope')
  source=sources.fetch(h['source_id'])
  ck(h['source_types']==source['types']&&h['source_phi']==source['phi']&&h['source_bound']==source['bound'],'source identity')
  source_phi=source['types'].zip(source['phi']).to_h
  domain=[]
  (0..45).each do |a|
    (0..a).each do |b|
      c=n-a-b;next unless c.between?(0,b)
      t=[a,b,c];next if (old+comp).any?{|s|s.zip(t).all?{|x,y|y>=x}}
      domain << t
    end
  end
  ck(h['all_parent_types']==domain&&h['types']==domain&&h['missing'].empty?,'complete parent domain')
  raw=domain.map do |t|
    # Label all N points only by their slice. Enumerate actual deleted index
    # sets, independently of the producer's binomial multiplicity formula.
    labels=t.each_with_index.flat_map{|a,i|[i]*a}
    counts=Hash.new(0)
    (0...n).to_a.combination(d) do |indices|
      u=t.dup;indices.each{|i|u[labels[i]]-=1};counts[u.sort.reverse]+=1
    end
    ck(counts.values.sum==choose(n,d),'all deletions counted')
    ck(counts.keys.all?{|u|source_phi.key?(u)},'no omitted source profile')
    checked+=1;counts.sum{|u,c|c*source_phi.fetch(u)}
  end
  bound=choose(n,m)*source['bound'];g=(raw+[bound]).reduce(0){|a,b|a.gcd(b)}
  ck(g>0&&g==h['positive_gcd'],'gcd')
  ck(raw.map{|v|v/g}==h['phi']&&bound/g==h['bound'],'transport formula')
end
lookup=trans.to_h{|h|[h['id'],h]};majorants=0;witnesses=0
readj(cmpath).each do |r|
  h=lookup.fetch(r['id']);n=h['m']
  direct=r['direct_ids'].map{|id|sources.fetch(id)}
  phis=direct.map{|s|s['types'].zip(s['phi']).to_h}
  features=h['types'].map{|t|[e2(t),e3(t)]+phis.map{|f|f.fetch(t)}}
  total=[243*choose(n,2),81*choose(n,3)]+direct.map{|s|s['bound']}
  case r['status']
  when 'EXACT_OLD_MODEL_DOMINATES'
    c=r['coefficients'].map{|v|Rational(v)}
    ck(c.length==total.length+1&&c.drop(3).all?{|v|v>=0},'valid inequality signs')
    features.zip(h['phi']).each{|x,y|ck(c[0]+c.drop(1).zip(x).sum{|a,b|a*b}>=y,'pointwise majorant')}
    v=364*c[0]+c.drop(1).zip(total).sum{|a,b|a*b}
    ck(v==Rational(r['exact_upper'])&&h['bound']-v==Rational(r['exact_margin'])&&v<=h['bound'],'majorant bound')
    majorants+=1
  when 'EXACT_NONREDUNDANCY_IN_OLD_HISTOGRAM_RELAXATION'
    sums=Array.new(total.length){Rational(0)};mass=Rational(0);v=Rational(0)
    r['witness'].each do |entry|
      i=h['types'].index(entry['profile']);ck(!i.nil?,'witness support')
      w=Rational(entry['weight']);ck(w>=0,'witness sign');mass+=w
      sums.each_index{|j|sums[j]+=w*features[i][j]};v+=w*h['phi'][i]
    end
    ck(mass==1,'witness mass')
    total.each_index{|j|ck(j<2 ? 364*sums[j]==total[j] : 364*sums[j]<=total[j],'old constraints')}
    ck(v==Rational(r['new_feature_sum'])&&364*v>h['bound']&&364*v-h['bound']==Rational(r['violation_after364']),'new constraint violated')
    witnesses+=1
  else
    raise 'uncertified comparison'
  end
end
ck(majorants==4&&witnesses==3,'comparison coverage')
out={status:'PASS',transfer_functions:7,table_values:checked,exact_dominance_certificates:majorants,exact_nonredundancy_witnesses:witnesses,
  scope:'Exact inequalities for all punctured NC107/108 caps conditional on accepted 103-extension rigidity; relation to old histogram relaxation only. No outer exclusion.',
  shared_dependencies:'Frozen theorem inputs and certificate values; Ruby reconstructs domains, labeled deletion sets, and rational comparisons without Python kernels.',
  transfer_sha256:Digest::SHA256.file(tablepath).hexdigest,comparison_sha256:Digest::SHA256.file(cmpath).hexdigest}
File.write(File.join(ROOT,'transfer_independent.json'),JSON.pretty_generate(out)+"\n");puts JSON.pretty_generate(out)
