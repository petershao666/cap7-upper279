require 'json'
require 'digest'
directory = File.dirname(File.expand_path(__FILE__))
frozen = JSON.parse(File.read(File.join(directory, 'FROZEN.json')))
frozen.fetch('files').each do |name, digest|
  raise "hash changed #{name}" unless Digest::SHA256.file(File.join(directory,name)).hexdigest == digest
end
packet = JSON.parse(File.read(File.join(directory, 'HISTOGRAMS.json')))
result = JSON.parse(File.read(File.join(directory, 'RESULT.json')))
decode = lambda { |number,n| Array.new(n) { v=number%3;number/=3;v } }
a = packet.fetch('canonical_A_points')
raise 'canonical size' unless a.size == 20 && a.uniq.size == 20
computed = (1...81).map { |i| decode.call(i,4) }.select { |p| (p[0]**2+p[1]**2+p[2]*p[3])%3 == 0 }
raise 'canonical zeros' unless a.sort == computed.sort
canonical_checks=0
a.combination(2) do |u,v|
  raise 'canonical line' if a.include?(4.times.map { |k| (-u[k]-v[k])%3 })
  canonical_checks+=1
end
types = packet.fetch('types')
expected = packet.fetch('histograms').map { |h| h.fetch('counts') }
all_masks=File.readlines(File.join(directory,'ALL20_MASKS.txt')).map { |line| line.strip.to_i(16) }
raise 'all masks inventory' unless all_masks.size == result.fetch('distinct_all20_caps') && all_masks.each_cons(2).all? { |u,v| u<v }
b_masks=File.readlines(File.join(directory,'B20_DISJOINT_MASKS.txt')).map { |line| line.strip.to_i(16) }
raise 'B count' unless b_masks.size == result.fetch('admissible_B20_disjoint_minusA') && b_masks.uniq.size == b_masks.size
minus_a_mask=0
a.each do |p|
  value=0;4.times { |k| value+=((-p[k])%3)*3**k };minus_a_mask|=1<<value
end
expected_b=all_masks.select { |m| (m&minus_a_mask)==0 }
raise 'B filter complete' unless expected_b==b_masks
directions=(1...243).map { |i| decode.call(i,5) }
families=Hash.new(0);pair_checks=0;direction_evaluations=0
b_masks.each do |mask|
  b=(0...81).select { |i| mask[i]==1 }.map { |i| decode.call(i,4) }
  raise 'B size' unless b.size==20
  cap=a.map { |p| [0]+p }+b.map { |p| [1]+p }+[[2,0,0,0,0]]
  lookup={};cap.each { |p| raise 'duplicate point' if lookup[p]; lookup[p]=true }
  cap.combination(2) do |u,v|
    third=5.times.map { |k| (-u[k]-v[k])%3 }
    raise 'lifted line' if lookup[third]
    pair_checks+=1
  end
  raw=Hash.new(0)
  directions.each do |d|
    counts=[0,0,0]
    cap.each { |p| z=0;5.times { |k| z+=d[k]*p[k] }; counts[z%3]+=1 }
    raw[counts.sort.reverse]+=1;direction_evaluations+=1
  end
  raise 'unknown type' unless (raw.keys-types).empty?
  histogram=types.map { |t| raise 'odd scalar multiplicity' unless raw[t].even?; raw[t]/2 }
  raise 'histogram outside frozen family' unless expected.include?(histogram)
  raise 'normalization' unless histogram.inject(0,:+)==121
  e2=0;e3=0;types.zip(histogram).each { |(x,y,z),n| e2+=n*(x*y+x*z+y*z);e3+=n*x*y*z }
  raise 'exact moments' unless e2==66420 && e3==287820
  families[histogram]+=1
end
packet.fetch('histograms').each do |h|
  raise 'family frequency' unless families[h.fetch('counts')]==h.fetch('normalized_B_frequency')
  indices=h.fetch('point_indices')
  raise 'point encoding' unless indices.map { |i| decode.call(i,5) }==h.fetch('points')
  bm=h.fetch('B_mask').to_i(16)
  actual=a.map { |p| [0]+p }+(0...81).select { |i| bm[i]==1 }.map { |i| [1]+decode.call(i,4) }+[[2,0,0,0,0]]
  raise 'explicit representative' unless actual.sort==h.fetch('points').sort
end
report={status:'EXACT_FROZEN_POINT_AND_DIRECTION_REPLAY_PASS',shared_dependencies:['frozen polynomial output masks, profiles and points; no C++ helper code'],catalogue_polynomial_completeness_rerun:false,canonical_pair_checks:canonical_checks,lifted_pair_checks:pair_checks,nonzero_normal_evaluations:direction_evaluations,scalar_direction_method:'all 242 nonzero normals, exact histogram division by two',all20_mask_count:all_masks.size,independently_refiltered_B_count:b_masks.size,histogram_count:families.size,input_histograms_sha256:Digest::SHA256.file(File.join(directory,'HISTOGRAMS.json')).hexdigest}
File.write(File.join(directory,'POINT_REPLAY.json'),JSON.pretty_generate(report)+"\n")
puts JSON.generate(report)
