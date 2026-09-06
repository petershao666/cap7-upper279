require 'json'
require 'digest'
r=File.expand_path('..',__dir__); h=r+'/hist105106/h13/'
s=File.read(h+'source_article.html');table=s.split('id="S3.T1"',2)[1].split('</table>',2)[0]
clean=lambda{|x| x.gsub(/<math\b[^>]*alttext="([^"]*)".*?<\/math>/m){$1}.gsub(/<[^>]+>/,'').gsub(/[\s_{}]/,'')}
rows=table.scan(/<tr\b[^>]*>(.*?)<\/tr>/m).map{|x|x[0].scan(/<t[hd]\b[^>]*>(.*?)<\/t[hd]>/m).map{|y|clean.call(y[0])}}
labels=rows.shift.drop(1);d=JSON.parse(File.read(h+'table1_input_v2.json'));raise 'labels' unless labels==d['label_order']
mat=Array.new(22){Array.new(22)};count=0
rows.each{|row|a=labels.index(row[0]);raise 'rowlabel' unless a;row.drop(1).each_with_index{|s,b|next if s.empty?;raise 'integer' unless s=~/\A[0-9]+\z/;v=s.to_i;raise 'conflict' if mat[a][b]&&mat[a][b]!=v;mat[a][b]=mat[b][a]=v;count+=1}}
raise 'coverage' unless count==253&&mat.flatten.none?(&:nil?)
raise 'capacities' unless mat==d['symmetric_capacity_matrix']
raise 'triangular' unless mat.each_with_index.map{|row,i|row.take(i+1)}==d['lower_triangular_rows']
states=JSON.parse(File.read(r+'/hist105106/h10/full18_states.json'));raise 'full class cover' unless states.flat_map{|x|x['classes']}.sort==labels.take(20).sort
cap=lambda{|a,b| a['classes'].product(b['classes']).map{|x,y|mat[labels.index(x)][labels.index(y)]}.max}
pairs=states.product(states).select{|a,b|cap.call(a,b)>=4}.map{|a,b|[a['id'],b['id']]}
ok19=states.select{|a|a['classes'].map{|c|mat[20][labels.index(c)]}.max>=3}.map{|a|a['id']}
ok20=states.select{|a|a['classes'].map{|c|mat[21][labels.index(c)]}.max>=2}.map{|a|a['id']}
raise 'projected counts' unless [pairs.size,ok19.size,ok20.size]==[267,17,16]
out={status:'PRIMARY_SOURCE_INPUT_EXACT_PASS',source_sha256:Digest::SHA256.file(h+'source_article.html').hexdigest,input_sha256:Digest::SHA256.file(h+'table1_input_v2.json').hexdigest,labels:22,independent_entries:count,allowed18184_pairs:pairs,allowed19183_histogram_ids:ok19,allowed20182_histogram_ids:ok20,scope:'Published Table1 capacities only; root parsed primary HTML directly without producer parser. Full18 histograms were independently audited earlier; maximum over class preimages is a safe overcover, no identification of classes by histogram.'}
File.write(__dir__+'/h13_table_independent.json',JSON.pretty_generate(out)+"\n");puts "PASS 253 entries; projected sizes #{[pairs.size,ok19.size,ok20.size]}"
