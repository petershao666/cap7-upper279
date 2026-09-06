require 'json';require 'set';require 'digest'
w=File.dirname(__FILE__);h=File.join(File.dirname(w),'hist105106/h9');src=File.join(h,'Dim5_41_CapsFoundArguments.txt');lines=File.read(src).lines.map(&:strip);data=JSON.parse(File.read(File.join(h,'named_points.json')));want=JSON.parse(File.read(File.join(h,'named_histograms.json')))
# Parse the published legend directly, without the producer's expansion table.
legend={};['+','x','|','-','.','o'].each_with_index{|ch,k|legend[ch]=lines[2,3].map{|s|s.split[k]}}
spec={'41F'=>[[66,67,68],false,true],'Delta686'=>[[15,16,17],false,true],'41H'=>[[142,143,144,146,147,148,150,151,152],false,false],'41I'=>[[155,156,157,159,160,161,163,164,165],false,false],'41G'=>[[284,285,286,288,289,290,292,293,294],true,false]}
# Root coordinates: outer-column, outer-row, middle-column, inner-column, inner-row.
def digits(n,k);(0...k).map{|i|(n/3**i)%3}.reverse;end
vectors=(0...243).map{|i|digits(i,5)};allnormals=vectors.drop(1)
def histogram(pts,normals)
 hist=Hash.new(0)
 normals.each{|u|cc=[0,0,0];pts.each{|p|cc[u.zip(p).sum{|a,b|a*b}%3]+=1};hist[cc.sort.reverse]+=1}
 raise unless hist.values.all?(&:even?);hist.transform_values{|v|v/2}
end
results={};allpoints={}
spec.each do |name,(ix,right,compact)|
 pts=[]
 if compact
  ix.each_with_index do |line,outerrow|
   symbols=lines[line-1].delete(' ');raise unless symbols.size==9
   symbols.chars.each_with_index do |ch,pos|
    legend.fetch(ch).each_with_index do |s,innrow|
     s.chars.each_with_index{|bit,k|pts<<[pos/3,outerrow,pos%3,k,innrow] if bit=='.'}
    end
   end
  end
 else
  ix.each_with_index do |line,row|
   s=lines[line-1];s=s.split("\t").last if right
   tokens=s.split;raise unless tokens.length==9&&tokens.all?{|t|t.length==3}
   tokens.each_with_index{|t,k|t.chars.each_with_index{|bit,col|pts<<[k/3,row/3,k%3,col,row%3] if bit=='.'}}
  end
 end
 ss=pts.to_set;raise unless ss.size==(name=='Delta686' ? 42:41)
 reference=data[name]['points'].map{|p|[p[2],p[0],p[3],p[4],p[1]]}.to_set;raise 'source-point mismatch' unless ss==reference
 # Enumerate all affine lines, independently of producer's unordered pairs.
 covered=ss.dup;linecount=0
 allnormals.each do |d|
  k=d.index{|x|x!=0};next unless d[k]==1
  vectors.each do |p|
   next unless p[k]==0
   line=(0..2).map{|a|p.zip(d).map{|x,y|(x+a*y)%3}}
   occupied=line.count{|x|ss.include?(x)};raise 'collinear triple' if occupied==3
   line.each{|x|covered.add(x)} if occupied==2;linecount+=1
  end
 end
 raise unless linecount==9801&&covered.size==243
 hh=histogram(pts,allnormals);wh=want[name]['types'].zip(want[name]['histogram']).to_h;raise 'hist mismatch' unless hh==wh
 results[name]={size:ss.size,affine_lines_checked:linecount,complete:true,full_histogram:hh.map{|t,v|[t,v]}.sort};allpoints[name]=pts
end
# Every possible marked deletion is retained, then compare histogram families.
families=Hash.new{|hh,k|hh[k]=0};p=allpoints['Delta686'];p.each_index{|j|hh=histogram(p.each_with_index.reject{|x,k|k==j}.map(&:first),allnormals);families[hh.to_a.sort]+=1}
wf=want['Delta686_minus1_family'].map{|z|[z['types'].zip(z['histogram']).sort,z['deleted_point_indices'].length]}.to_h
raise 'deletion family mismatch' unless families==wf
out={status:'PASS',named_representatives:results,delta_deletion_family_sizes:families.values.sort,source_sha256:Digest::SHA256.file(src).hexdigest,producer_points_sha256:Digest::SHA256.file(File.join(h,'named_points.json')).hexdigest,producer_histograms_sha256:Digest::SHA256.file(File.join(h,'named_histograms.json')).hexdigest,scope:'Published named41F/G/H/I andDelta686 only, with all42 Delta single deletions; not a complete41classification',independence:'Ruby parses legend and selected source diagrams directly with permuted coordinates, checks everyaffineline and uses all242normalvectors; producer point/histogram data used only for comparison'}
File.write(File.join(w,'h9_named_independent.json'),JSON.pretty_generate(out)+"\n");puts 'PASS five primary namedrepresentatives,49005affinelines,42Delta deletions'
