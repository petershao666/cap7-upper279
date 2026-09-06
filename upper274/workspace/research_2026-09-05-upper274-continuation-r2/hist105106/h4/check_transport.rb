require 'json'
w=File.dirname(__FILE__);h=JSON.parse(File.read(File.join(w,'../h3/h3_result.json')))['histograms']['40'];phi={};h['types'].zip(h['phi']).each{|t,v|phi[t]=v};data=JSON.parse(File.read(File.join(w,'transport_tables.json')))
def cb(n,k);return 0 if k<0||k>n;(1..k).inject(1){|x,j|x*(n-j+1)/j};end
checked=0;terms=0
data.each{|sm,d|m=sm.to_i;raise unless d['bound']==cb(m,40)*h['bound'];d['types'].zip(d['phi']).each{|t,want|v=0;mass=0;holes=m-40;(0..holes).each{|a|(0..holes-a).each{|b|c=holes-a-b;next if a>t[0]||b>t[1]||c>t[2];weight=cb(t[0],a)*cb(t[1],b)*cb(t[2],c);v+=weight*phi[[t[0]-a,t[1]-b,t[2]-c].sort.reverse];mass+=weight;terms+=1}};raise unless v==want&&mass==cb(m,40);checked+=1}}
r={status:'PASS',profiles:checked,deletion_terms:terms,arithmetic:'Ruby Integer exact; hole-composition enumeration'};File.write(File.join(w,'transport_check.json'),JSON.pretty_generate(r)+"\n");puts JSON.generate(r)
