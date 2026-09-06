require 'json';require 'digest'
W=File.dirname(__FILE__);R=File.expand_path('..',W);B=File.expand_path('../audit_2026-09-05_upper275/cap7_upper275',R)
def readj(p);JSON.parse(File.read(p));end
def ck(v,s);raise s unless v;end
def choose(n,k);return 0 if k<0||k>n;(1..k).inject(1){|a,i|a*(n-i+1)/i};end
def e2(t);t[0]*t[1]+t[0]*t[2]+t[1]*t[2];end
def e3(t);t.inject(:*);end
def dot(a,b);a.zip(b).sum{|x,y|x*y};end
def dominates(t,bads);t=t.sort.reverse;bads.any?{|s|s.zip(t).all?{|x,y|y>=x}};end
frozen=readj(File.join(B,'baseline277/baseline278/certificate.json'))
old=frozen['six_stages'].flat_map{|s|s.keys.map{|k|k.split(',').map(&:to_i)}}
comp=frozen['completion_seeds']+frozen['completion_stages'].flat_map{|s|s.keys.map{|k|k.split(',').map(&:to_i)}}
sources=readj(File.join(B,'results/size276/proof.json'))['new_histograms']
sources += [readj(File.join(B,'baseline277/certificate.json'))['nested108'].merge('id'=>'psi108','m'=>108)]
h3=readj(File.join(R,'hist105106/h3/h3_result.json'));upper=h3['upper5']
upper.each_value{|h|h['lookup']=h['types'].zip(h['phi']).to_h}
all=sources+readj(File.join(R,'root_potential/transfer_tables.json'))['functions']+readj(File.join(W,'h3_transport_tables.json'))['functions']
lookup=all.to_h{|h|[h['id'],h.merge('lookup'=>h['types'].zip(h['phi']).to_h)]}
path=File.join(W,'pointed_joint_audit_input.json');data=readj(path)
readj(File.join(R,'root_potential/pointed_transfer_tables.json'))['functions'].each{|h|lookup[h['id']]=h.merge('lookup'=>h['types'].zip(h['phi']).to_h)}
h=data['new_target'];lookup[h['id']]=h.merge('lookup'=>h['types'].zip(h['phi']).to_h)
ck(h['types']==lookup['nested107_size276']['types'],'new function full support')
targets=data['source_functions'].map{|id|lookup.fetch(id)}
ck(targets.all?{|h|h['m']==107},'conditional target size')
anchors=lookup['nested107_size276']['inner'].map{|c|c['type']};ck(data['anchors']==anchors&&data['ledger'].length==3*anchors.length,'complete anchor/mark cover')
t108=[];(0..45).each{|a|(0..a).each{|b|c=108-a-b;t=[a,b,c];t108<<t if c.between?(0,b)&&!dominates(t,old+comp)}}
ck(t108==lookup['psi108']['types'],'full restored support')
adm={}
(0..20).each{|a|(0..20).each{|b|(0..20).each{|c|
 t=[a,b,c];s=t.sum;ok=s<42||(s<=45&&frozen['spectrum5'][s.to_s]['types'].include?(t.sort.reverse))
 adm[t]=s<=45&&ok&&!dominates(t,[[20,19,2],[20,18,3],[19,19,3],[19,18,4]])
}}}
minima={};checked=0;canonical=0;excluded=0;uppercases=0;forbidden=0
bounds=targets.to_h{|h|[h['id'],[]]}
anchors.each_with_index do |key,ai|
 bans=old+comp+anchors.take(ai)
 cols=key.each_with_index.map do |n,j|
  out=[];(0..20).each{|a|(0..20).each{|b|c=n-a-b;t=[a,b,c];out<<t if c.between?(0,20)&&adm[t]}};out
 end
 matrices=[]
 cols[0].each{|a|cols[1].each{|b|cols[2].each{|c|
  next unless (0..2).all?{|i|(0..2).all?{|j|adm[[a[i],b[j],c[(-i-j)%3]]]}}
  tops=(0..2).map{|s|(0..2).map{|i|a[i]+b[(i+s)%3]+c[(i+2*s)%3]}.sort.reverse}
  next unless tops.all?{|t|t.max<=45&&!dominates(t,bans)}
  ts=targets.map{|h|tops.sum{|t|h['lookup'].fetch(t)}}
  triple_value=(0..2).sum{|i|(0..2).sum{|j|a[i]*b[j]*c[(-i-j)%3]}}
  matrices<<[[a,b,c],tops,[triple_value,e2(a),e3(a),e2(b),e3(b),e2(c),e3(c)],ts]
 }}}
 sourcecanonical=matrices.count{|cc,*_|b=cc[1];cc[0]==cc[0].sort.reverse&&(b<=>b.rotate(1))>=0&&(b<=>b.rotate(2))>=0}
 3.times do |j|
  rec=data['ledger'][3*ai+j];ck(rec['anchor107']==key&&rec['marked_column']==j&&rec['source_count']==sourcecanonical,'ledger alignment')
  restored=key.dup;restored[j]+=1;restored.sort!.reverse!
  ck(restored==rec['anchor108'],'restored anchor')
  if !t108.include?(restored)
   ck(rec['status']=='FORBIDDEN_RESTORED_ANCHOR','forbidden restored type');forbidden+=1;next
  end
  ck(['ENUMERATED','EXACT_MARKED_BRANCH_EXCLUSION_CANDIDATE'].include?(rec['status']),'branch certificate required')
  forced_values=[40*key.inject(:*)]+key.flat_map{|n|[81*choose(n,2),27*choose(n,3)]};positive=[]
  rec['features'].each do |e|
   if e[0].is_a?(Integer)
    col,kind,arg,bd=e
    if kind=='exact'
     sp=frozen['spectrum5'][key[col].to_s];ck(sp['spectra'].length==1&&sp['spectra'][0][sp['types'].index(arg)]==bd,'original exact spectrum')
    else
     h=upper.fetch(arg);ck(kind=='upper'&&h['m']==key[col]&&h['bound']==bd,'original upper spectrum');positive<<forced_values.length
    end
    forced_values<<bd
   elsif e[0]=='point'
    other=(0..2).to_a-[j]
    forced_values<<({'cell'=>40*key[j],'opposite_product'=>27*choose(key[j],2),'cross_product'=>40*key[other[0]]*key[other[1]]}.fetch(e[1]))
   elsif e[0]=='restored_column'
    _,col,kind,arg,bd=e;ck(col==j,'restored column identity')
    if kind=='exact'
     sp=frozen['spectrum5'][(key[j]+1).to_s];ck(sp['spectra'].length==1&&sp['spectra'][0][sp['types'].index(arg)]==bd,'restored exact spectrum')
    else
     h=upper.fetch(arg);ck(kind=='upper'&&h['m']==key[j]+1&&h['bound']==bd,'restored upper spectrum');positive<<forced_values.length
    end
    forced_values<<bd
   else
    ck(e[0]=='restored_global'&&data['input_108_functions'].include?(e[1]),'restored global feature')
    h=lookup.fetch(e[1]);ck(h['m']==108,'restored size');positive<<forced_values.length;forced_values<<h['bound']-h['lookup'].fetch(restored)
   end
  end
  ck(forced_values==rec['forced']&&positive==rec['positive'],'forced sums and signs reconstructed')
  is_excluded=rec['status']=='EXACT_MARKED_BRANCH_EXCLUSION_CANDIDATE'
  certificates=is_excluded ? [rec['exclusion']] : targets.map{|h|rec['results'].find{|z|z['id']==h['id']}.fetch('certificate')}
  certificates.each{|c|ck(c['coeff'].length==forced_values.length&&positive.all?{|i|c['coeff'][i]>=0},'certificate signs')}
  mins=Array.new(certificates.length);n=0;can=0
  matrices.each do |cc,tops,features,oldsum|
   3.times do |mark|
    updated=cc.map(&:dup);updated[j][mark]+=1
    next if updated[j][mark]>20||!updated.all?{|t|adm[t]}
    next unless (0..2).all?{|u|(0..2).all?{|v|adm[[updated[0][u],updated[1][v],updated[2][(-u-v)%3]]]}}
    topsnew=(0..2).map{|s|(0..2).map{|u|updated[0][u]+updated[1][(u+s)%3]+updated[2][(u+2*s)%3]}.sort.reverse}
    next unless topsnew.all?{|t|t108.include?(t)}
    x=features.dup
    rec['features'].each do |e|
     if e[0].is_a?(Integer)
      col,kind,arg,_=e;t=cc[col].sort.reverse;x<<(kind=='exact' ? (t==arg ? 1:0) : upper.fetch(arg)['lookup'].fetch(t))
     elsif e[0]=='point'
      other=(0..2).to_a-[j]
      case e[1]
      when 'cell';x<<cc[j][mark]
      when 'opposite_product';x<<cc[j][(mark+1)%3]*cc[j][(mark+2)%3]
      when 'cross_product';x<<(0..2).sum{|u|cc[other[0]][u]*cc[other[1]][(-u-mark)%3]}
      end
     elsif e[0]=='restored_column'
      _,col,kind,arg,_=e;t=updated[col].sort.reverse;x<<(kind=='exact' ? (t==arg ? 1:0) : upper.fetch(arg)['lookup'].fetch(t))
     else
      h=lookup.fetch(e[1]);x<<topsnew.sum{|t|h['lookup'].fetch(t)}
     end
    end
    certificates.each_with_index do |c,k|
     v=dot(c['coeff'],x);v-=c['denominator']*oldsum[k] unless is_excluded
     ck(v>=c['K'],'pointed local inequality');mins[k]=mins[k].nil? ? v : [v,mins[k]].min
    end
    n+=1;b=cc[1];can+=1 if cc[0]==cc[0].sort.reverse&&(b<=>b.rotate(1))>=0&&(b<=>b.rotate(2))>=0
   end
  end
  ck(n>0&&can==rec['count'],'complete marked enumeration count')
  certificates.each_with_index do |c,k|
   ck(mins[k]==c['K'],'exact attained minimum')
   if is_excluded
    u=dot(c['coeff'],forced_values);ck(u==c['forced']&&121*c['K']-u==c['gap']&&c['gap']>0,'marked branch exclusion gap')
   else
    h=targets[k];num=c['denominator']*h['lookup'].fetch(key)+dot(c['coeff'],forced_values)-121*c['K']
    ck(num==c['bound_numerator'],'conditional bound');bounds[h['id']]<<Rational(num,c['denominator'])
   end
  end
  checked+=n;canonical+=can;is_excluded ? excluded+=1 : uppercases+=1
  puts "anchor #{key} mark #{j} ordered #{n} canonical #{can} #{is_excluded ? 'EXCLUDED' : 'BOUNDED'}"
 end
end
data['conditional_bounds'].each{|r|bd=bounds.fetch(r['id']).max;ck(bd==Rational(r['numerator'],r['denominator'])&&bd==lookup[r['id']]['bound'],'complete conditional maximum')}
out={status:'PASS',anchor_mark_strata:data['ledger'].length,forbidden_restored_anchors:forbidden,exact_marked_exclusions:excluded,bounded_strata:uppercases,ordered_marked_matrices:checked,canonical_marked_matrices:canonical,conditional_bounds:data['conditional_bounds'],certificate_sha256:Digest::SHA256.file(path).hexdigest,original_joint_sha256:data['original_joint_sha256'],
 scope:'New P3b histogram bound for NC107 caps admitting an NC108 extension; not an unconditional107 bound; outer exclusion checked separately',independence:'Standalone Ruby exact integer/rational replay, all ordered alpha/beta/gamma columns and all marked rows; shared frozen mathematical inputs only'}
File.write(File.join(W,'pointed_joint_independent.json'),JSON.pretty_generate(out)+"\n");puts JSON.pretty_generate(out)
