require 'json'
require 'set'
require 'digest'
w=File.dirname(__FILE__);h=File.expand_path('../hist105106/h3',w)
def ck(v,s);raise s unless v;end
def choose(n,k);(1..k).inject(1){|a,i|a*(n-i+1)/i};end
def e2(t);t.combination(2).sum{|a,b|a*b};end
patterns=[
  [[9,8,2],[nil,6,nil],[nil,6,nil]],
  [[9,8,2],[nil,6,nil],[nil,5,nil]],
  [[nil,8,nil],[9,6,3],[nil,6,nil]],
  [[nil,8,nil],[9,6,3],[nil,5,nil]],
  [[nil,7,nil],[9,6,3],[nil,6,nil]],
  [[8,nil,5],[1,6,nil],[8,nil,5]],
  [[8,nil,6],[1,5,nil],[8,nil,6]],
  [[9,1,9],[1,1,nil],[9,nil,nil]],
  [[9,1,9],[2,2,nil],[8,nil,nil]]]
points=(0..2).to_a.product((0..2).to_a)
maps=[]
# An affine bijection is uniquely determined by images of 0,e1,e2,
# and these images may be any ordered affinely independent triple.
points.permutation(3) do |p,q,r|
  u=q.zip(p).map{|a,b|(a-b)%3};v=r.zip(p).map{|a,b|(a-b)%3}
  next if (u[0]*v[1]-u[1]*v[0])%3==0
  maps<<points.map{|x,y|3*((p[0]+x*u[0]+y*v[0])%3)+(p[1]+x*u[1]+y*v[1])%3}
end
ck(maps.length==432&&maps.uniq.length==432,'affine bijection cover')
orbits=patterns.map do |matrix|
  specified=matrix.flatten.each_with_index.map{|v,i|[i,v] unless v.nil?}.compact
  maps.map{|p|specified.map{|i,v|[p[i],v]}.sort}.uniq.sort
end
all=orbits.flatten(1).uniq.sort
d=JSON.parse(File.read(File.join(h,'clash_data.json')))
ck(d['maps'].sort==maps.sort&&d['base_grids']==patterns,'published grid and coordinate domain')
ck(d['patterns']==all&&d['orbit_sizes']==orbits.map(&:length),'complete forbidden pattern expansion')
hist=JSON.parse(File.read(File.join(h,'hist19_20.json')))
solutions={}
hist.each do |str,g|
  n=str.to_i;tt=g['types'];valid=[]
  # Enumerate all nonnegative 40-direction histograms on the published support.
  search=lambda do |prefix,left|
    if prefix.length==tt.length-1
      counts=prefix+[left]
      if counts.zip(tt).sum{|c,t|c*e2(t)}==27*choose(n,2)&&counts.zip(tt).sum{|c,t|c*t.inject(:*)}==9*choose(n,3)
        valid<<counts
      end
    else
      (0..left).each{|c|search.call(prefix+[c],left-c)}
    end
  end
  search.call([],40)
  ck(valid==[g['histogram']],'unique integer moment solution')
  ck(g['E2_total']==27*choose(n,2)&&g['E3_total']==9*choose(n,3),'moment totals')
  solutions[str]=valid[0]
end
out={status:'PASS',affine_maps:432,forbidden_patterns:all.length,orbit_sizes:orbits.map(&:length),unique_histograms:solutions,
  authority:'Thackeray, arXiv2206.09719v1, Lemmas2.4–2.6 and 19/20-cap support stated in proof of Lemma2.3; accepted published mathematical input, not independently reproved classification.',
  independence:'Ruby affine maps from images of an affine basis; integer histogram compositions; shared primary statements only.',
  clash_data_sha256:Digest::SHA256.file(File.join(h,'clash_data.json')).hexdigest,
  hist19_20_sha256:Digest::SHA256.file(File.join(h,'hist19_20.json')).hexdigest}
File.write(File.join(w,'clashes_independent.json'),JSON.pretty_generate(out)+"\n");puts JSON.pretty_generate(out)
