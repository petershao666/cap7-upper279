// Independent direct-enumeration verifier for a target-specific reduction.
// Compile with -DSTEP_DATA="results/size277/step_data.hpp" for upper 276.
#define main preserved_baseline277_main
#include "baseline277/verify.cpp"
#undef main
#include <string>
template<class Callback>
I enumerate_step(const Triple&key,const Table&adm,const Table&top,const std::vector<Triple>&complete,const Triple&state,Callback callback){
 std::array<std::vector<Triple>,3> cols;
 for(int j=0;j<3;++j){cols[j]=columns(key[j],adm,j==0);check(state[j]>=-1&&state[j]<=1,"status range");if(state[j]>=0){check(key[j]>=103&&key[j]<=112&&(state[j]==1||key[j]<109),"whole-slice status range");auto&v=cols[j];v.erase(std::remove_if(v.begin(),v.end(),[&](const Triple&t){return state[j]==1?!sub112(t):dominates(t,complete);}),v.end());}}
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

#include "auxiliary41.hpp"
struct GeneralSpectrum{int column;std::vector<Triple>types;std::vector<I>phi;I bound;};
struct GeneralInner{Triple key;std::vector<I>q;I K,bound;std::vector<std::pair<int,Triple>>extra;std::vector<GeneralSpectrum>spectra;std::vector<Triple>absent;std::vector<UpperCutUse>upper;};
struct GeneralHistogram{std::string id;int m;std::vector<Triple>types;std::vector<I>phi;I bound;std::vector<I>root_q;I root_K,root_forced,root_gap;std::vector<GeneralInner>inner;std::vector<Triple>extra5;};
struct StepRecord{Triple key;std::vector<I>q;I K,U,gap;Triple status;std::vector<std::pair<int,std::string>>extra;bool empty;};
#ifndef STEP_DATA
#define STEP_DATA "results/size277/step_data.hpp"
#endif
#include STEP_DATA
I stepQ(const Triple&t){return 9*e3(t)-(4*STEP_SIZE-3*STEP_K)*e2(t)+I(STEP_SIZE)*STEP_SIZE*(STEP_SIZE-STEP_K);}
std::map<std::string,std::map<Triple,I>> registry;
std::map<std::string,I> registry_bounds;
I verify_deleted2(){
 check(DELETED2.size()==51,"two deletion coverage");I count=0;
 for(size_t j=0;j<DELETED2.size();++j){const auto&r=DELETED2[j];check(r.h==int(j)+1&&r.q.size()==8,"two deletion ordering");auto rhs=hill_rhs(r.h);I U=0;for(int i=0;i<8;++i)U+=r.q[i]*rhs[i];check(U==r.U,"two deletion total");
  for(int u=0;u<3;++u)for(int p=0;p<=(u==0?20:11);++p){I m=16+4*u+3*p-r.h;if(p>r.h||r.h-p>45||m<0)continue;auto f=hill_row(u,p);I value=0;for(int i=0;i<8;++i)value+=r.q[i]*f[i];if(r.impossible)check(value>=r.K,"two deletion infeasible inequality");else check(r.L>0&&value>=r.L*I(m<=2),"two deletion count inequality");++count;}
  I gap=r.impossible?364*r.K-U:23*r.L-U;check(gap==r.gap&&gap>0,"two deletion gap");
 }
 // h=0,1: all nonzero multiplicities exceed2, so at most the origin opens.
 for(int h=0;h<=1;++h)for(int u=0;u<3;++u)check(16+4*u-h>2,"two deletion small intersection");
 // h=52..55 impossible by rigidity; h=56 identical completions, only diagonal
 // representations of multiplicity1 can open, at most2 positions.
 for(int h=52;h<=55;++h)check(2*h>=103&&2*h<112,"two deletion rigidity");
 std::cout<<"DELETED2 PASS: "<<count<<" integer states; two deletions from two 112-caps leave at most44 positions.\n";return count;
}
I verify_hist(const GeneralHistogram&h,const LowerInputs&lower){
 auto banned=lower.old;banned.insert(banned.end(),lower.complete.begin(),lower.complete.end());std::vector<Triple>T;for(auto t:alltypes(h.m,45))if(!dominates(t,banned))T.push_back(t);check(T==h.types&&h.phi.size()==T.size(),"new histogram type coverage");
 std::map<Triple,I>phi;for(size_t i=0;i<T.size();++i)phi[T[i]]=h.phi[i];std::set<Triple>rare;for(auto r:h.inner){check(rare.insert(r.key).second&&phi.count(r.key),"new histogram rare key");}
 check(h.root_q.size()==2,"rare root dimension");I U=h.root_q[0]*243*c2(h.m)+h.root_q[1]*81*c3(h.m);check(U==h.root_forced&&364*h.root_K-U==h.root_gap&&h.root_gap>0,"rare existence gap");
 for(auto t:T)if(!rare.count(t))check(h.root_q[0]*e2(t)+h.root_q[1]*e3(t)>=h.root_K,"rare existence local inequality");
 Table a5=lower.a5;check(h.extra5.empty()||h.extra5==std::vector<Triple>{{20,19,2},{20,18,3},{19,19,3},{19,18,4}},"published Proposition6.1 exclusions");for(int a=0;a<21;++a)for(int b=0;b<21;++b)for(int c=0;c<21;++c)if(dominates({a,b,c},h.extra5))a5.set(a,b,c,false);std::vector<Triple>earlier;I count=0,Bb=std::numeric_limits<I>::min();
 for(const auto&r:h.inner){check(r.absent.empty()||r.absent==earlier,"first-occurring rare direction");auto ban=banned;ban.insert(ban.end(),r.absent.begin(),r.absent.end());auto top=top_table(45,ban,h.m);earlier.push_back(r.key);auto fixed=forced(r.key,6);std::vector<I>sums(fixed.begin(),fixed.end());
  for(auto ex:r.extra){int N=r.key[ex.first];check(N>=43&&N<=45&&HISTOGRAMS.at(N).size()==1,"inner histogram exact scope");const auto&tt=TYPES.at(N);auto it=std::find(tt.begin(),tt.end(),ex.second);check(it!=tt.end(),"inner histogram exact type");sums.push_back(HISTOGRAMS.at(N).begin()->at(size_t(it-tt.begin())));}
  for(auto u:r.upper){check(r.key[u.column]==41&&AUXPHI.count(u.id)&&r.q.at(sums.size())>=0,"41-cap upper-bound scope/sign");sums.push_back(AUXBOUND.at(u.id));}I total=scalar(r.q,sums);std::vector<std::map<Triple,I>>specmaps;
  for(const auto&sp:r.spectra){int N=r.key[sp.column];check(N==42&&sp.types==TYPES.at(N)&&sp.types.size()==sp.phi.size(),"inner spectral scope");I largest=std::numeric_limits<I>::min();for(const auto&hist:HISTOGRAMS.at(N)){I v=0;for(size_t k=0;k<hist.size();++k)v+=hist[k]*sp.phi[k];largest=std::max(largest,v);}check(largest==sp.bound,"inner spectral upper bound");total+=sp.bound;std::map<Triple,I>mp;for(size_t k=0;k<sp.types.size();++k)mp[sp.types[k]]=sp.phi[k];specmaps.push_back(mp);}
  I bound=phi.at(r.key)+total-121*r.K;check(bound==r.bound,"inner global bound");I minimum=std::numeric_limits<I>::max();
  I n=enumerate_step(r.key,a5,top,{},Triple{-1,-1,-1},[&](const Triple&a,const Triple&b,const Triple&c,const std::array<Triple,3>&tops){auto f=features(a,b,c);std::array<Triple,3>cols{a,b,c};for(auto ex:r.extra)f.push_back(sort3(cols[ex.first])==ex.second);for(auto u:r.upper)f.push_back(AUXPHI.at(u.id).at(sort3(cols[u.column])));I value=scalar(r.q,f);for(size_t j=0;j<r.spectra.size();++j)value+=specmaps[j].at(sort3(cols[r.spectra[j].column]));for(auto t:tops)value-=phi.at(sort3(t));check(value>=r.K,"new histogram inner inequality");minimum=std::min(minimum,value);});
  check(n>0,"new histogram nonempty inner");count+=n;Bb=std::max(Bb,bound);std::cout<<"STEP INNER "<<h.id<<" "<<show(r.key)<<": matrices="<<n<<", minimum="<<minimum<<", K="<<r.K<<", bound="<<bound<<"\n";
 }
 check(Bb==h.bound,"new uniform histogram bound");registry[h.id]=phi;registry_bounds[h.id]=h.bound;std::cout<<"HISTOGRAM PASS "<<h.id<<": types="<<T.size()<<", rare="<<rare.size()<<", bound="<<h.bound<<", matrices="<<count<<"\n";return count;
}
I verify_step_case(const StepRecord&r,const LowerInputs&lower,const std::vector<Triple>&banned,bool extremal){
 check(tsum(r.key)==STEP_SIZE,"new target size");auto top=top_table(112,banned,STEP_SIZE);
 if(extremal)for(int a=0;a<=112;++a)for(int b=0;b<=112;++b){int c=STEP_SIZE-a-b;if(c>=0&&c<=112&&stepQ({a,b,c})<stepQ(r.key))top.set(a,b,c,false);}
 auto ff=forced(r.key,7);std::vector<I>sums(ff.begin(),ff.end());for(size_t i=0;i<r.extra.size();++i){auto ex=r.extra[i];int col=ex.first;check(col>=0&&col<3,"extra column");int d=112-r.key[col];if(ex.second=="fam"||ex.second=="small"||ex.second=="label40"){check(r.status[col]==1&&d>=0&&d<=9,"completed statistic scope");sums.push_back(ex.second=="fam"?56:ex.second=="small"?11*d:110*d);}else{check(r.status[col]==0&&registry.count(ex.second)&&r.q.at(7+i)>=0,"histogram feature scope and sign");check(registry.at(ex.second).begin()->first[0]+registry.at(ex.second).begin()->first[1]+registry.at(ex.second).begin()->first[2]==r.key[col],"histogram size");sums.push_back(registry_bounds.at(ex.second));}}
 if(!r.empty)check(scalar(r.q,sums)==r.U&&364*r.K-r.U==r.gap&&r.gap>0,"step local summed gap");I minimum=std::numeric_limits<I>::max();
 I n=enumerate_step(r.key,lower.a6,top,lower.complete,r.status,[&](const Triple&a,const Triple&b,const Triple&c,const std::array<Triple,3>&){check(!r.empty,"claimed empty family has matrix");auto f=features(a,b,c);std::array<Triple,3>cols{a,b,c};I value=0;for(int j=0;j<7;++j)value+=r.q[j]*f[j];for(size_t j=0;j<r.extra.size();++j){auto ex=r.extra[j];auto col=cols[ex.first];auto s=sort3(col);I q=r.q[7+j];if(ex.second=="fam")value+=q*I(s[2]<=22);else if(ex.second=="small")value+=q*(s[2]<=22?22-s[2]:0);else if(ex.second=="label40"){auto ds=labels(col);I lo=std::numeric_limits<I>::max();for(int d:ds)lo=std::min(lo,q*d);value+=lo;}else value+=q*registry.at(ex.second).at(s);}check(value>=r.K,"new target local inequality");minimum=std::min(minimum,value);});
 if(r.empty)check(n==0,"empty case");else check(n>0,"nonempty certificate family");std::cout<<"STEP "<<(extremal?"EXTREMAL ":"ORDINARY ")<<show(r.key)<<" status="<<show(r.status)<<": matrices="<<n<<", minimum="<<(r.empty?0:minimum)<<", K="<<r.K<<", gap="<<r.gap<<"\n";return n;
}
int main(){std::cout.setf(std::ios::unitbuf);auto start=std::chrono::steady_clock::now();auto lower=verify_lower();verify_near112();verify_nested108(lower);verify_deleted2();registry["psi108"]=PSI108;registry_bounds["psi108"]=SPECTRAL108_BOUND;if(!STEP_AUX41.empty())prove_small_bound();for(const auto&h:STEP_AUX41)verify_aux41(h);I inner=0;for(const auto&h:STEP_HISTOGRAMS)inner+=verify_hist(h,lower);
 check(STEP_INITIAL_SEEDS==std::vector<Triple>{{112,112,29},{112,111,35}},"initial new seeds");check(STEP_SEEDS==std::vector<Triple>{{112,112,29},{112,111,35},{112,110,45},{111,111,45}},"all new seeds");
 std::vector<Triple>ban=STEP_INITIAL_SEEDS;I ordinary=0,extreme=0;for(const auto&stage:STEP_ORDINARY){auto snap=ban;for(const auto&r:stage){check(r.status==Triple{-1,-1,-1}&&r.extra.empty()&&!dominates(r.key,ban),"ordinary stage scope");ordinary+=verify_step_case(r,lower,snap,false);}for(const auto&r:stage)ban.push_back(r.key);}
 ban.push_back({112,110,45});ban.push_back({111,111,45});std::set<Triple>expected,got;auto all=alltypes(STEP_SIZE,112);for(auto t:all)if(stepQ(t)<0&&!dominates(t,ban))expected.insert(t);std::map<Triple,std::vector<StepRecord>>groups;for(auto r:STEP_EXTREMAL){groups[r.key].push_back(r);got.insert(r.key);}check(got==expected,"complete extremal type coverage");
 for(const auto&gg:groups){const auto&key=gg.first;const auto&rs=gg.second;if(rs.size()==1&&rs[0].status==Triple{-1,-1,-1})extreme+=verify_step_case(rs[0],lower,ban,true);else{std::set<Triple>want,have;std::vector<int>eligible;for(int j=0;j<3;++j)if(key[j]>=103&&key[j]<109)eligible.push_back(j);for(int mask=0;mask<(1<<eligible.size());++mask){Triple state{-1,-1,-1};for(int j=0;j<3;++j)if(key[j]>=109)state[j]=1;for(size_t j=0;j<eligible.size();++j)state[eligible[j]]=(mask>>j)&1;want.insert(state);}for(auto r:rs)have.insert(r.status);check(have==want&&rs.size()==want.size(),"all fixed completion statuses");for(auto r:rs)extreme+=verify_step_case(r,lower,ban,true);}}
 for(auto t:all){I a=t[0],b=t[1],c=t[2];check(4*stepQ(t)==(3*c-STEP_SIZE)*(3*c-STEP_SIZE)*(c-STEP_K)+(4*STEP_SIZE-3*STEP_K-9*c)*(a-b)*(a-b),"step polynomial identity");}I sum=9*243*c3(STEP_SIZE)-(4*STEP_SIZE-3*STEP_K)*729*c2(STEP_SIZE)+I(STEP_SIZE)*STEP_SIZE*(STEP_SIZE-STEP_K)*1093;check(sum<0,"negative total for minimizer");
 std::cout<<"STEP FULL PASS: no "<<STEP_SIZE<<"-point cap; f(7,3) <= "<<STEP_SIZE-1<<"; ordinary_matrices="<<ordinary<<"; extremal_matrices="<<extreme<<"; new_inner_matrices="<<inner<<"; minimum_cases="<<got.size()<<"; global_sum="<<sum<<".\n";std::cout<<"Elapsed seconds: "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"\n";
}
