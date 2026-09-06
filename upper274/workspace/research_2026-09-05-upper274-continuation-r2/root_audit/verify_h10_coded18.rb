require 'json';require 'set';require 'digest'
w=File.dirname(__FILE__);r=File.dirname(w);src=File.join(r,'hist105106/h9/SetDim5Cap43_9General_ExclPtCounts.java');lines=File.read(src).lines;data=JSON.parse(File.read(File.join(r,'hist105106/h10/coded18_points_histograms.json')))
names=['990A1','990A2','990A3','990B']+('A'..'J').map{|c|'981'+c}+['972A','963A','963B','954A'];decoded={};active=nil;collect=false;raw=''
lines.each do |line|
 m=line.match(/code\.equals\("([^"]+)"\)/)
 if m
  active=names.include?(m[1])&&!decoded.key?(m[1]) ? m[1]:nil;collect=false;raw=''
 end
 next unless active
 collect=true if line.include?('return ')
 next unless collect
 chunks=line.scan(/"([012,;:]*)"/).flatten;raw+=chunks.join
 if line.rstrip.end_with?(';')
  pts=raw.scan(/[012],[012],[012],[012]/).map{|p|p.split(',').map(&:to_i)}
  raise 'literal residue' unless raw.gsub(/[012],[012],[012],[012]/,'').delete(';:').empty?
  raise unless pts.length==18;decoded[active]=pts;active=nil
 end
end
raise unless decoded.keys.sort==names.sort
vectors=(0...81).map{|i|(0...4).map{|j|(i/3**(3-j))%3}};normals=vectors.drop(1);results={}
decoded.each do |name,pts|
 ss=pts.to_set;raise unless ss.size==18&&ss==data[name]['points'].to_set
 hist=Hash.new(0);nlines=0
 normals.each do |u|
  cc=[0,0,0];pts.each{|p|cc[u.zip(p).sum{|a,b|a*b}%3]+=1};hist[cc.sort.reverse]+=1
  first=u.index{|v|v!=0};next unless u[first]==1
  vectors.each do |base|
   next unless base[first]==0
   collinear=(0..2).count{|k|ss.include?(base.zip(u).map{|a,b|(a+k*b)%3})};raise 'noncap' if collinear==3;nlines+=1
  end
 end
 raise unless nlines==1080&&hist.values.all?(&:even?);hist.transform_values!{|v|v/2};raise unless hist==data[name]['types'].zip(data[name]['histogram']).to_h
 results[name]={affine_lines:nlines,types:hist.keys.sort,histogram:hist.keys.sort.map{|t|hist[t]}}
end
out={status:'PASS',classes:18,affine_lines_checked:19440,distinct_full_histograms:results.values.map{|v|[v[:types],v[:histogram]]}.uniq.length,source_sha256:Digest::SHA256.file(src).hexdigest,producer_data_sha256:Digest::SHA256.file(File.join(r,'hist105106/h10/coded18_points_histograms.json')).hexdigest,scope:'Exact recovery of18namedpublished4Dclasses; join with independentlytranscribed882A1/A2 forfull20-classinput; classification completeness remains published premise',independence:'Line-oriented literal-only parser, no Java execution; Ruby allaffinelines andall80linearforms, independentofproducerPythonpairs/40normalvectors',histograms:results}
File.write(File.join(w,'h10_coded18_independent.json'),JSON.pretty_generate(out)+"\n");puts "PASS #{results.length} codedclasses,19440affinelines,#{out[:distinct_full_histograms]}distincthistograms"
