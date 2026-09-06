require 'json';require 'digest'
w=File.dirname(__FILE__);r=File.expand_path('..',w);b=File.expand_path('../audit_2026-09-05_upper275/cap7_upper275',r)
def ck(x,s);raise s unless x;end
def choose(n,k);k=[k,n-k].min;(1..k).inject(1){|a,i|a*(n-i+1)/i};end
source=JSON.parse(File.read(File.join(r,'hist105106/h3/h3_result.json')))['histograms']['105']
low=JSON.parse(File.read(File.join(b,'baseline277/baseline278/certificate.json')))
bans=low['completion_seeds']+(low['six_stages']+low['completion_stages']).flat_map{|s|s.keys.map{|k|k.split(',').map(&:to_i)}}
phi=source['types'].zip(source['phi']).to_h
p=File.join(w,'h3_transport_tables.json');data=JSON.parse(File.read(p));ck(data['functions'].length==4,'scope')
checked=0;deletedsets=0
data['functions'].each do |h|
 n=h['m'];d=n-105
 if d==0
  ck(h['types']==source['types']&&h['phi']==source['phi']&&h['bound']==source['bound'],'source identity');next
 end
 domain=[];(0..45).each{|a|(0..a).each{|b|c=n-a-b;next unless c.between?(0,b);t=[a,b,c];next if bans.any?{|v|v.zip(t).all?{|x,y|y>=x}};domain<<t}}
 ck(h['types']==domain&&d==h['deleted'],'parent domain')
 vals=domain.map do |t|
  labels=t.each_with_index.flat_map{|a,i|[i]*a};freq=Hash.new(0)
  (0...n).to_a.combination(d){|ids|u=t.dup;ids.each{|i|u[labels[i]]-=1};freq[u.sort.reverse]+=1}
  ck(freq.values.sum==choose(n,d),'subset count');deletedsets+=freq.values.sum;checked+=1
  freq.sum{|u,k|ck(phi.key?(u),'complete105domain');k*phi.fetch(u)}
 end
 bd=choose(n,d)*source['bound'];g=(vals+[bd]).reduce(0){|a,v|a.gcd(v)}
 ck(g==h['positive_gcd']&&h['phi']==vals.map{|v|v/g}&&h['bound']==bd/g,'exact transported values')
end
out={status:'PASS',new_transfers:3,table_values:checked,labeled_deletion_sets:deletedsets,source_sha256:data['source_sha256'],table_sha256:Digest::SHA256.file(p).hexdigest,scope:'H3 Phi105 transported to all NC106/107/108 caps conditional on accepted103-extension rigidity; no outer exclusion by this checker',independence:'Ruby enumerates labeled deletion-index sets, independent of Python binomial multiplicities and discovery kernels'}
File.write(File.join(w,'h3_transport_independent.json'),JSON.pretty_generate(out)+"\n");puts JSON.pretty_generate(out)
