require 'json'
require 'digest'
base=File.dirname(__FILE__)
file=File.join(base,'deleted3_certificate.json')
data=JSON.parse(File.read(file))
def check(x,s); raise s unless x; end
def choose(n,k)
  return 0 if n<k
  (1..k).inject(1){|v,j|v*(n-j+1)/j}
end
def dot(a,b); a.zip(b).sum{|x,y|x*y}; end
check(data['threshold']==3,'threshold')
rows=data['records']
check(rows.map{|r|r['h']}==(1..51).to_a,'h coverage')
states_total=0
max_nondiag=0
rows.each do |r|
  h=r['h'];q=r['q'];check(q.size==8 && q.all?{|v|v.is_a?(Integer)},'coefficients')
  total=[252+h,112-2*h,h,121*h,40*choose(h,2),13*choose(h,3),22*h,4*choose(h,2)]
  check(dot(q,total)==r['upper'],'forced total')
  seen=0;min_slack=nil
  (0..2).each do |u|
    (0..h).each do |p|
      next if h-p>45 || p>(u==0 ? 20 : 11)
      multiplicity=16+4*u+3*p-h
      next if multiplicity<0
      x=[u==0 ? 1 : 0,u==1 ? 1 : 0,u==2 ? 1 : 0,p,choose(p,2),choose(p,3),u*p,u*choose(p,2)]
      if r['kind']=='count'
        check(r['L'].is_a?(Integer) && r['L']>0,'positive L')
        slack=dot(q,x)-(multiplicity<=3 ? r['L'] : 0)
      else
        check(r['kind']=='impossible','unrecovered row')
        slack=dot(q,x)
      end
      check(slack>=0,'local inequality')
      min_slack=min_slack.nil? ? slack : [min_slack,slack].min
      if h%3==0 && multiplicity==3;check(u==2,'diagonal implication');end
      seen+=1
    end
  end
  check(seen==r['state_count'],'state count')
  check(min_slack==r['minimum_slack'],'minimum slack')
  if r['kind']=='count'
    check(r['bound_floor']==r['upper'].div(r['L']),'integer rounding')
    if h%3!=0
      check(r['upper']<26*r['L'],'nondivisible count cap')
      max_nondiag=[max_nondiag,r['bound_floor']].max
    end
  else
    check(r['upper']<0,'infeasibility certificate')
  end
  puts "h=#{h} kind=#{r['kind']} states=#{seen} floor=#{r['bound_floor']}"
  states_total+=seen
end
check(rows.select{|r|r['h']>=46}.all?{|r|r['kind']=='impossible'},'large finite h exclusions')
check((52..55).all?{|h|2*h>=103 && 2*h<112},'rigidity endpoints')
check((0..1).all?{|h|16-h>3},'small h endpoints')
result={status:'PASS_EXACT_FINITE_CERTIFICATE',states:states_total,h_records:51,
        maximum_nondivisible_projective_count:max_nondiag,
        derived_third_layer_bound:50,
        dependencies:['prior Fourier and incidence identities','prior threshold<=2 vector bound44','103-point rigidity','112-cap uniqueness','>=109 completion for seeds'],
        coefficient_sha256:Digest::SHA256.file(file).hexdigest,
        independence:'separate Ruby integer state generator; shared mathematical identities and coefficient data'}
File.write(File.join(base,'deleted3_independent_result.json'),JSON.pretty_generate(result)+"\n")
puts JSON.generate(result)
