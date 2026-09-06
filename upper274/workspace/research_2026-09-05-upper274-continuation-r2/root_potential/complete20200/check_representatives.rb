require 'json'
require 'digest'
here=File.dirname(File.expand_path(__FILE__))
frozen=JSON.parse(File.read(File.join(here,'FROZEN.json')))
frozen.fetch('files').each do |name,digest|
  raise "changed #{name}" unless Digest::SHA256.file(File.join(here,name)).hexdigest==digest
end
input=File.join(here,'..','complete20201','ALL20_MASKS.txt')
raise 'catalogue hash' unless Digest::SHA256.file(input).hexdigest=='66946f5ef9ea1e10164a5b3e56cf89dede2b85efc50d8a8eb1e392e5862d2f41'
packet=JSON.parse(File.read(File.join(here,'HISTOGRAMS.json')))
decode=lambda { |n,k| Array.new(k) { digit=n%3;n/=3;digit } }
normals=(1...243).map { |i| decode.call(i,5) }
frequencies=Hash.new(0)
File.foreach(File.join(here,'B_HISTOGRAM_IDS.txt')) { |line| frequencies[Integer(line)]+=1 }
raise 'total assignments' unless frequencies.values.inject(0,:+)==682344
raise 'assignment domain' unless frequencies.keys.sort==(0...packet['histograms'].size).to_a
pair_checks=0;normal_counts=0;parameters=[]
packet['histograms'].each do |h|
  cap=h['points'];ids=h['point_indices'];counts=h['counts'];types=packet['types']
  raise 'distinct points' unless cap.size==40 && cap.uniq.size==40
  raise 'encoding' unless ids.map { |i| decode.call(i,5) }==cap
  raise 'frequency' unless frequencies[h['id']]==h['normalized_B_frequency']
  lookup={};cap.each { |p| lookup[p]=true }
  cap.combination(2) do |a,b|
    raise 'collinear triple' if lookup[5.times.map { |k| (-a[k]-b[k])%3 }]
    pair_checks+=1
  end
  raw=Hash.new(0)
  normals.each do |d|
    profile=[0,0,0]
    cap.each { |p| val=0;5.times { |k| val+=d[k]*p[k] };profile[val%3]+=1 }
    raw[profile.sort.reverse]+=1;normal_counts+=1
  end
  raise 'unknown type' unless (raw.keys-types).empty?
  raise 'scalar multiplicity' unless raw.values.all? { |n| n.even? }
  raise 'full representative histogram' unless types.map { |t| raw[t]/2 }==counts
  r=raw[[18,18,4]]/2
  parameters<<r
  formula={ [14,14,12]=>40+2*r,[15,15,10]=>20-2*r,[16,12,12]=>20+r,[17,15,8]=>40-4*r,[18,11,11]=>2*r,[18,18,4]=>r,[20,20,0]=>1 }
  raise 'parametric formula' unless types.map { |t| formula.fetch(t,0) }==counts
  a=cap.select { |p| p[0]==0 }.map { |p| p[1..-1] }
  b=cap.select { |p| p[0]==1 }.map { |p| p[1..-1] }
  raise 'layer counts' unless a.size==20 && b.size==20 && cap.none? { |p| p[0]==2 }
  shared=0
  (1...81).each do |d_id|
    d=decode.call(d_id,4)
    profiles=[a,b].map do |layer|
      profile=[0,0,0]
      layer.each { |p| val=0;4.times { |k| val+=d[k]*p[k] };profile[val%3]+=1 }
      profile.sort.reverse
    end
    raise '20-cap profile type' unless profiles.all? { |t| [[9,9,2],[8,6,6]].include?(t) }
    shared+=1 if profiles==[[9,9,2],[9,9,2]]
  end
  raise 'geometric r' unless shared==2*r
end
raise 'parameter set' unless parameters.sort==[0,1,2,3,4,5,6,10]
report={status:'EXACT_REPRESENTATIVE_AND_ASSIGNMENT_FREQUENCY_REPLAY_PASS',representatives:parameters.size,representative_pairs:pair_checks,nonzero_normal_evaluations:normal_counts,full_assignment_count:frequencies.values.inject(0,:+),parameter_set:parameters.sort,full_assignment_histograms_recomputed:false,shared_inputs:['frozen P representative and assignment outputs','accepted complete 20-cap catalogue hash'],enumerator_kernel_imported:false,histograms_sha256:Digest::SHA256.file(File.join(here,'HISTOGRAMS.json')).hexdigest}
File.write(File.join(here,'REPRESENTATIVE_REPLAY.json'),JSON.pretty_generate(report)+"\n")
puts JSON.generate(report)
