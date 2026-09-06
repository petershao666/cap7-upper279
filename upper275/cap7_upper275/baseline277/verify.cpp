// Exact direct-Cartesian-product verifier for f(7,3)<=277.
// c++ -std=c++17 -O2 -Wall -Wextra -fsanitize=undefined -fno-sanitize-recover=all verify.cpp -o verify
// The published dependencies and all new reductions are specified in README.md.
#include "baseline_kernel.hpp"
#include <functional>
#include <sstream>
struct InnerRecord{Triple key;std::vector<I> q;I K,bound;std::vector<std::pair<int,Triple>> extra;};
struct ExtremalRecord{Triple key;std::vector<I> q;I K,forced,gap;Triple status;bool nested;};
#include "certificate_data.hpp"
I Q(const Triple&t){return 9*e3(t)-911*e2(t)+16306924;}
int tsum(const Triple&t){return t[0]+t[1]+t[2];}
std::vector<Triple> alltypes(int total,int upper){std::vector<Triple>v;for(int a=0;a<=upper;++a)for(int b=0;b<=a;++b){int c=total-a-b;if(c>=0&&c<=b)v.push_back({a,b,c});}return v;}
std::string show(const Triple&t){std::ostringstream o;o<<"("<<t[0]<<", "<<t[1]<<", "<<t[2]<<")";return o.str();}
I scalar(const std::vector<I>&q,const std::vector<I>&f){check(q.size()==f.size(),"dot product dimension");I ans=0;for(size_t j=0;j<q.size();++j)ans+=q[j]*f[j];return ans;}
std::vector<I> features(const Triple&a,const Triple&b,const Triple&c){I T=0;for(int i=0;i<3;++i)for(int j=0;j<3;++j)T+=I(a[i])*b[j]*c[(6-i-j)%3];return {T,e2(a),e3(a),e2(b),e3(b),e2(c),e3(c)};}

// No bit masks or rotational canonicalization: visit the literal product of
// sorted alpha, all ordered beta, and all ordered gamma. Labels are NOT used
// to reject matrices; every permitted original-40-section identity is tested.
template<class Callback>
I enumerate_new(const Triple&key,const Table&adm,const Table&top,const std::vector<Triple>&complete,const Triple&state,Callback callback){
 std::array<std::vector<Triple>,3> cols;
 for(int j=0;j<3;++j){cols[j]=columns(key[j],adm,j==0);check(state[j]>=-1&&state[j]<=1,"status range");if(state[j]>=0){check(key[j]>=103&&key[j]<109,"whole-slice status range");auto&v=cols[j];v.erase(std::remove_if(v.begin(),v.end(),[&](const Triple&t){return state[j]==1?!sub112(t):dominates(t,complete);}),v.end());}}
 I count=0;
 for(const auto&a:cols[0])for(const auto&b:cols[1])for(const auto&c:cols[2]){
  bool ok=true;
  for(int r=0;r<3&&ok;++r)for(int s=0;s<3;++s)if(!adm.at(a[r],b[(r+s)%3],c[(r+2*s)%3])){ok=false;break;}
  if(!ok)continue;
  std::array<Triple,3> tops{};
  for(int s=0;s<3;++s){for(int r=0;r<3;++r)tops[s][r]=a[r]+b[(r+s)%3]+c[(r+2*s)%3];if(!top.at(tops[s][0],tops[s][1],tops[s][2])){ok=false;break;}}
  if(!ok)continue;
  ++count;callback(a,b,c,tops);
 }
 return count;
}
struct LowerInputs{std::vector<Triple>old,complete;Table a5,a6;LowerInputs():a5(20),a6(45){}};
LowerInputs verify_lower(){
 LowerInputs x;auto S=representative();completion_representative(S);hill_representative(S);I nh=hill_inequalities();spectral(S);
 for(int a=0;a<=20;++a)for(int b=0;b<=20;++b)for(int c=0;c<=20;++c)x.a5.set(a,b,c,admissible5(a,b,c));
 I n6=0,nc=0;std::vector<Triple> f6;
 for(const auto&stage:SIX){auto top=top_table(45,f6);for(const auto&r:stage)n6+=local(r,6,x.a5,&top);for(const auto&r:stage){check(std::find(f6.begin(),f6.end(),r.key)==f6.end(),"duplicate inherited type");f6.push_back(r.key);}}
 x.old=f6;x.complete=COMPLETION_SEEDS;
 check(x.complete==std::vector<Triple>{{45,45,7},{45,43,15},{44,44,15},{45,42,20}},"published completion seed list");
 for(const auto&stage:CONDITIONAL){auto ban=x.old;ban.insert(ban.end(),x.complete.begin(),x.complete.end());auto top=top_table(45,ban);for(const auto&r:stage){check(tsum(r.key)>=103,"extension-rigidity threshold");nc+=local(r,6,x.a5,&top);}for(const auto&r:stage)x.complete.push_back(r.key);}
 completion_root(x.old,x.complete);
 for(auto t:x.complete)if(!sub112(t))f6.push_back(t);
 for(int a=0;a<=45;++a)for(int b=0;b<=45;++b)for(int c=0;c<=45;++c){Triple t{a,b,c};x.a6.set(a,b,c,original6(a,b,c)&&(a+b+c<109||sub112(t))&&!dominates(t,f6));}
 std::cout<<"LOWER INPUTS PASS: "<<n6<<" universal and "<<nc<<" conditional matrix evaluations; "<<nh<<" inherited Hill states.\n";
 return x;
}
I verify_near112(){
 check(NEAR112.size()==51,"near112 coverage");I count=0;
 for(size_t j=0;j<NEAR112.size();++j){const auto&r=NEAR112[j];check(r.h==int(j)+1&&r.q.size()==8,"near112 case ordering");auto tot=hill_rhs(r.h);I U=0;for(int k=0;k<8;++k)U+=r.q[k]*tot[k];check(U==r.U,"near112 total");I n=0;
  for(int u=0;u<3;++u)for(int p=0;p<=(u==0?20:11);++p){I m=16+4*u+3*p-r.h;if(p>r.h||r.h-p>45||m<0)continue;auto row=hill_row(u,p);I val=0;for(int k=0;k<8;++k)val+=r.q[k]*row[k];++n;if(r.impossible)check(val>=r.K,"near112 impossible-state inequality");else check(r.L>0&&val>=r.L*I(m<=1),"near112 low-multiplicity inequality");}
  I gap=r.impossible?364*r.K-U:18*r.L-U;check(gap==r.gap&&gap>0,"near112 gap");count+=n;std::cout<<"NEAR112 h="<<r.h<<": states="<<n<<", gap="<<gap<<"\n";
 }
 for(int h=52;h<=55;++h)check(2*h>=103&&2*h<112,"near112 rigidity range");
 for(int u=0;u<3;++u)check(16+4*u>1,"near112 zero-intersection range");
 std::cout<<"NEAR112 PASS: "<<count<<" state inequalities; (112,111,35) is excluded.\n";return count;
}
I verify_nested108(const LowerInputs&x){
 auto banned=x.old;banned.insert(banned.end(),x.complete.begin(),x.complete.end());std::vector<Triple>allowed,expected;for(auto t:alltypes(108,45))if(!dominates(t,banned))allowed.push_back(t);for(auto p:PSI108)expected.push_back(p.first);check(allowed==expected&&allowed.size()==30,"noncompletion108 support");
 std::vector<Triple>rare;for(const auto&r:INNER108)rare.push_back(r.key);check(rare==std::vector<Triple>{{45,41,22},{44,43,21},{43,43,22}},"rare108 list");
 for(auto t:allowed)if(std::find(rare.begin(),rare.end(),t)==rare.end())check(e3(t)-39*e2(t)>=-105001,"rare-direction local inequality");
 I root=81*c3(108)-39*243*c2(108);check(root==-38221470&&364LL*(-105001)-root==1106,"rare108 root gap");std::cout<<"RARE108 PASS: 27 remaining types, gap=1106\n";
 I count=0,maxbound=std::numeric_limits<I>::min();auto top=top_table(45,banned,108);
 for(const auto&r:INNER108){check(r.q.size()==7+r.extra.size(),"inner108 coefficient length");auto arr=forced(r.key,6);std::vector<I>sum(arr.begin(),arr.end());
  for(auto ex:r.extra){int N=r.key[ex.first];check(N>=43&&N<=45&&HISTOGRAMS.at(N).size()==1,"inner108 histogram equality scope");const auto&types=TYPES.at(N);auto it=std::find(types.begin(),types.end(),ex.second);check(it!=types.end(),"inner108 histogram type");sum.push_back(HISTOGRAMS.at(N).begin()->at(size_t(it-types.begin())));}
  I bound=PSI108.at(r.key)+scalar(r.q,sum)-121*r.K;check(bound==r.bound,"inner108 summed bound");I minimum=std::numeric_limits<I>::max();
  I n=enumerate_new(r.key,x.a5,top,{},Triple{-1,-1,-1},[&](const Triple&a,const Triple&b,const Triple&c,const std::array<Triple,3>&tops){auto f=features(a,b,c);std::array<Triple,3>cols{a,b,c};for(auto ex:r.extra)f.push_back(sort3(cols[ex.first])==ex.second);I val=scalar(r.q,f);for(auto t:tops)val-=PSI108.at(sort3(t));check(val>=r.K,"nested108 inner local inequality");minimum=std::min(minimum,val);});
  check(n>0,"inner108 nonempty family");count+=n;maxbound=std::max(maxbound,bound);std::cout<<"NEW INNER "<<show(r.key)<<": matrices="<<n<<", minimum="<<minimum<<", K="<<r.K<<", bound="<<bound<<"\n";
 }
 check(maxbound==SPECTRAL108_BOUND,"noncompletion108 uniform spectral bound");std::cout<<"HISTOGRAM108 PASS: sum(phi) <= "<<maxbound<<"; "<<count<<" inner matrix evaluations.\n";return count;
}
std::vector<int> labels(const Triple&t){auto s=sort3(t);if(s[2]<=22)return {0};std::vector<int>d;for(int j=0;j<3;++j){bool good=t[j]<=40;for(int k=0;k<3;++k)if(k!=j)good=good&&t[k]<=36;if(good)d.push_back(40-t[j]);}check(!d.empty(),"compatible original40 labels");return d;}
std::pair<I,I> verify_branch(const ExtremalRecord&r,const LowerInputs&x,const std::vector<Triple>&banned){
 auto top=top_table(112,banned,278);for(int a=0;a<=112;++a)for(int b=0;b<=112;++b){int c=278-a-b;if(c>=0&&c<=112&&Q({a,b,c})<Q(r.key))top.set(a,b,c,false);}
 auto arr=forced(r.key,7);I U=0;
 if(r.nested){check(r.key==Triple{108,108,62}&&r.status==Triple{0,0,-1}&&r.q==OUTER108_Q,"nested branch scope");std::vector<I>sum{arr[0],arr[1]+arr[3],arr[2]+arr[4],arr[5],arr[6]};U=scalar(r.q,sum)+2*SPECTRAL108_BOUND;}
 else{std::vector<I>sum(arr.begin(),arr.end());for(int j=0;j<3;++j)if(r.status[j]==1){int d=112-r.key[j];sum.push_back(56);sum.push_back(11*d);sum.push_back(110*d);}U=scalar(r.q,sum);}
 check(U==r.forced&&364*r.K-U==r.gap&&r.gap>0,"new branch summed bound");I minimum=std::numeric_limits<I>::max(),labelled=0;
 I n=enumerate_new(r.key,x.a6,top,x.complete,r.status,[&](const Triple&a,const Triple&b,const Triple&c,const std::array<Triple,3>&){auto f=features(a,b,c);I value=0,mult=1;
  if(r.nested){std::vector<I>ff{f[0],f[1]+f[3],f[2]+f[4],f[5],f[6]};value=scalar(r.q,ff)+PSI108.at(sort3(a))+PSI108.at(sort3(b));}
  else{for(int i=0;i<7;++i)value+=r.q[i]*f[i];std::array<Triple,3>cols{a,b,c};size_t off=7;
   for(int j=0;j<3;++j)if(r.status[j]==1){auto s=sort3(cols[j]);bool fam=s[2]<=22;auto ds=labels(cols[j]);I low=std::numeric_limits<I>::max();for(int d:ds){check(d>=0&&d<=112-r.key[j],"original40 deletion range");low=std::min(low,r.q[off+2]*d);}value+=r.q[off]*I(fam)+r.q[off+1]*(fam?22-s[2]:0)+low;off+=3;mult*=I(ds.size());}
   check(off==r.q.size(),"labelled branch feature length");
  }
  check(value>=r.K,"new extremal branch local inequality");minimum=std::min(minimum,value);labelled+=mult;
 });
 check(n>0,"nonempty extremal branch");std::cout<<"NEW BRANCH "<<show(r.key)<<" status="<<show(r.status)<<": matrices="<<n<<", labelled_states="<<labelled<<", minimum="<<minimum<<", K="<<r.K<<", gap="<<r.gap<<"\n";return {n,labelled};
}
int main(){
 std::cout.setf(std::ios::unitbuf);auto start=std::chrono::steady_clock::now();auto lower=verify_lower();I near=verify_near112(),inner=verify_nested108(lower);
 std::vector<Triple>f7{{112,112,29}};I ordinary=0;
 for(size_t s=0;s<NEW_ORDINARY.size();++s){const auto&stage=NEW_ORDINARY[s];auto top=top_table(112,f7,278);std::cout<<"NEW ORDINARY STAGE "<<s<<": "<<stage.size()<<" cases.\n";for(const auto&r:stage){check(tsum(r.key)==278&&!dominates(r.key,f7),"ordinary stage independence");ordinary+=local(r,7,lower.a6,&top);}for(const auto&r:stage)f7.push_back(r.key);}
 f7.push_back({112,111,35});auto types=alltypes(278,112);check(types.size()==310,"global type count");std::set<Triple>expected,provided;
 for(auto t:types)if(Q(t)<0&&!dominates(t,f7))expected.insert(t);
 std::map<Triple,std::vector<const ExtremalRecord*>>groups;for(const auto&r:EXTREMAL){groups[r.key].push_back(&r);provided.insert(r.key);}check(expected==provided&&expected.size()==9,"extremal negative case coverage");
 I extremal=0,labelled=0,branches=0;
 for(const auto&group:groups){auto key=group.first;const auto&rs=group.second;
  if(rs.size()==1&&rs[0]->status==Triple{-1,-1,-1}){const auto&r=*rs[0];check(!r.nested&&r.q.size()==7,"plain extremal scope");auto ban=f7;for(auto t:types)if(Q(t)<Q(key))ban.push_back(t);auto top=top_table(112,ban,278);Record old{r.key,r.q,r.K,r.forced,r.gap,{},false,{-1,-1,-1}};extremal+=local(old,7,lower.a6,&top);}
  else{std::set<Triple>states,wanted;for(auto p:rs)states.insert(p->status);for(int a=0;a<2;++a)for(int b=0;b<2;++b){check(key[0]>=103&&key[0]<109&&key[1]>=103&&key[1]<109&&key[2]<103,"branch sizes");wanted.insert({a,b,-1});}check(states==wanted&&rs.size()==4,"complete fixed-status split");for(auto r:rs){auto n=verify_branch(*r,lower,f7);extremal+=n.first;labelled+=n.second;++branches;}}
 }
 // Extremal cases are NOT inserted into f7: all nine alternatives use the
 // same unconditional baseline, and only Q(other direction)>=Q(selected).
 for(auto t:types){I a=t[0],b=t[1],c=t[2];check(4*Q(t)==(3*c-278)*(3*c-278)*(c-67)+(911-9*c)*(a-b)*(a-b),"root algebraic identity");}
 I total=9*243*c3(278)-911*729*c2(278)+16306924LL*1093;check(total==-148313,"root forced sum");
 std::cout<<"NEW ROOT PASS: 310 types; "<<expected.size()<<" remaining negative minimum-direction cases all excluded; sum(Q)="<<total<<".\n";
 std::cout<<"NEW COMPUTATIONS PASS: ordinary="<<ordinary<<"; extremal="<<extremal<<"; inner="<<inner<<"; labelled_branch_states="<<labelled<<"; completion_branches="<<branches<<"; near112_states="<<near<<".\n";
 std::cout<<"FULL PASS: under the published inputs specified in README.md, no 278-point cap exists; 236 <= f(7,3) <= 277.\n";
 std::cout<<"Elapsed verification seconds: "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"\n";
}
