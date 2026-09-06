// Baseline verification functions, with its old entry point omitted.
// Independent, direct-Cartesian-product integer verifier.
// c++ -std=c++17 -O2 verify.cpp -o verify && ./verify
// Standard C++ only. All mathematical dependencies are listed in README.md.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <vector>
using I=long long;
using Triple=std::array<int,3>;
using P6=std::array<int,6>;
using P5=std::array<int,5>;
struct Spec {int size;std::vector<I> q;I total;bool bounded;};
struct Extra {int column,id;};
struct Record {Triple key;std::vector<I> q;I K,forced,gap;std::vector<Extra> extra;bool empty;Triple status;};
struct HillRecord {int h;bool impossible;std::vector<I> q;I K,L,U,gap;};
#include "baseline278/certificate_data.hpp"
void check(bool b,const char* msg){if(!b){std::cerr<<"FAIL: "<<msg<<'\n';std::exit(1);}}
I c2(I n){return n*(n-1)/2;} I c3(I n){return n*(n-1)*(n-2)/6;}
I e2(const Triple&t){return I(t[0])*t[1]+I(t[0])*t[2]+I(t[1])*t[2];}
I e3(const Triple&t){return I(t[0])*t[1]*t[2];}
Triple sort3(Triple t){std::sort(t.begin(),t.end(),std::greater<int>());return t;}
std::map<Triple,int> DELTA={{{20,16,6},3},{{18,18,6},4},{{18,17,7},18},{{18,12,12},6},{{16,15,11},24},{{16,14,12},36},{{15,15,12},3},{{14,14,14},27}};
bool admissible5(int a,int b,int c){
 if(a<0||b<0||c<0||a>20||b>20||c>20||a+b+c>45)return false;
 if(a+b+c<42)return true;
 auto t=sort3({a,b,c});
 bool from45=(t[0]<=18&&t[1]<=18&&t[2]<=9)||t[0]<=15;
 return from45||(a+b+c==42&&DELTA.count(t));
}
bool original6(int a,int b,int c){
 if(a<0||b<0||c<0||a>45||b>45||c>45||a+b+c>112)return false;
 if(a+b+c<110)return true;
 return a<=22||b<=22||c<=22||(a<=40&&b<=40&&c<=40&&((a<=36&&b<=36)||(a<=36&&c<=36)||(b<=36&&c<=36)));
}
bool dominates(Triple t,const std::vector<Triple>&forbidden){
 t=sort3(t);for(auto k:forbidden)if(t[0]>=k[0]&&t[1]>=k[1]&&t[2]>=k[2])return true;
 return false;
}
template<size_t N> std::array<int,N> decode(int x){std::array<int,N> p{};for(int j=int(N)-1;j>=0;--j){p[j]=x%3;x/=3;}return p;}
template<size_t N> int encode(const std::array<int,N>&p){int x=0;for(int v:p)x=3*x+v;return x;}
template<size_t N> void capcheck(const std::vector<std::array<int,N>>&p){
 std::set<int> nums;for(auto x:p)nums.insert(encode(x));check(nums.size()==p.size(),"duplicate representative points");
 for(size_t i=0;i<p.size();++i)for(size_t j=0;j<i;++j){std::array<int,N> z{};for(size_t k=0;k<N;++k)z[k]=(6-p[i][k]-p[j][k])%3;check(!nums.count(encode(z)),"representative forbidden triple");}
}
std::vector<P6> representative(){
 const std::array<Triple,10> bl={{{1,2,3},{1,2,4},{1,3,5},{1,4,6},{1,5,6},{2,3,6},{2,4,5},{2,5,6},{3,4,5},{3,4,6}}};
 std::set<int> masks;for(auto t:bl)masks.insert((1<<(t[0]-1))|(1<<(t[1]-1))|(1<<(t[2]-1)));
 std::vector<P6> S,R,D0,D1,U;std::set<int> ids;
 for(int x=0;x<729;++x){auto p=decode<6>(x);int mask=0,twos=0,weight=0;for(int j=0;j<6;++j){if(p[j]){mask|=1<<j;++weight;}twos+=p[j]==2;}
  if(mask==63&&twos%2==0)R.push_back(p);
  if(masks.count(mask))D0.push_back(p);
  if(masks.count(63^mask))D1.push_back(p);
  if(weight==1)U.push_back(p);
 }
 S=R;S.insert(S.end(),D0.begin(),D0.end());check(S.size()==112,"112 size");capcheck(S);for(auto p:S)ids.insert(encode(p));
 std::array<int,729> sec{};for(size_t i=0;i<S.size();++i)for(size_t j=0;j<i;++j){P6 z;for(int k=0;k<6;++k)z[k]=(6-S[i][k]-S[j][k])%3;++sec[encode(z)];}
 std::map<int,int> distribution;for(int x=0;x<729;++x)if(!ids.count(x))++distribution[sec[x]];
 check(distribution==std::map<int,int>{{10,616},{56,1}},"112 secants");
 std::map<Triple,int> hist;int nd=0;for(int d=1;d<729;++d){auto v=decode<6>(d);auto j=std::find_if(v.begin(),v.end(),[](int x){return x!=0;});if(j==v.end()||*j!=1)continue;++nd;Triple t{};for(auto p:S){int z=0;for(int k=0;k<6;++k)z+=p[k]*v[k];++t[z%3];}++hist[sort3(t)];}
 check(nd==364&&hist==std::map<Triple,int>{{{45,45,22},56},{{40,36,36},308}},"112 spectrum");
 std::vector<std::array<int,7>> cap;
 for(int layer=0;layer<3;++layer){std::vector<P6> selected;if(layer==2)selected=U;else{selected=R;const auto&d=layer==0?D0:D1;selected.insert(selected.end(),d.begin(),d.end());}for(auto p:selected){std::array<int,7> q{};q[0]=layer;std::copy(p.begin(),p.end(),q.begin()+1);cap.push_back(q);}}
 check(cap.size()==236,"236 size");capcheck(cap);
 std::cout<<"112-cap: cap, spectrum, and secants verified. 236-cap: all 27730 pairs verified.\n";
 return S;
}
void spectral(const std::vector<P6>&S){
 std::vector<P5> cap;for(int d=1;d<729&&cap.empty();++d){auto v=decode<6>(d);std::array<std::vector<P6>,3>buckets;for(auto p:S){int z=0;for(int k=0;k<6;++k)z+=p[k]*v[k];buckets[z%3].push_back(p);}for(const auto&b:buckets)if(b.size()==45){int pivot=0;while(!v[pivot])++pivot;for(auto p:b){P5 q{};int k=0;for(int j=0;j<6;++j)if(j!=pivot)q[k++]=p[j];cap.push_back(q);}break;}}
 check(cap.size()==45,"45 representative");capcheck(cap);
 std::vector<std::array<int,45>> projections;std::vector<Triple> original;
 for(int d=1;d<243;++d){auto v=decode<5>(d);auto j=std::find_if(v.begin(),v.end(),[](int x){return x!=0;});if(j==v.end()||*j!=1)continue;std::array<int,45> vals{};Triple t{};for(int i=0;i<45;++i){int z=0;for(int k=0;k<5;++k)z+=v[k]*cap[i][k];vals[i]=z%3;++t[z%3];}projections.push_back(vals);original.push_back(t);}
 check(projections.size()==121,"45 direction count");
 for(int size:{42,43,44,45}){
  const auto&types=TYPES.at(size);std::map<Triple,int> index;for(size_t i=0;i<types.size();++i)index[types[i]]=int(i);
  std::vector<Triple> expected;for(int a=0;a<=20;++a)for(int b=0;b<=a;++b){int c=size-a-b;if(c>=0&&c<=b&&admissible5(a,b,c))expected.push_back({a,b,c});}check(types==expected,"spectral type indexing");
  std::set<std::vector<I>> spectra;I subsets=0;
  auto test=[&](std::vector<I> h){spectra.insert(h);for(const auto&sp:SPECS)if(sp.size==size){check(sp.q.size()==h.size(),"spectrum coefficient length");I sum=0;for(size_t i=0;i<h.size();++i)sum+=h[i]*sp.q[i];check(sp.bounded?sum<=sp.total:sum==sp.total,"spectral constraint");}};
  auto deleted=[&](int i,int j,int k){std::vector<I> h(types.size());for(size_t d=0;d<projections.size();++d){Triple t=original[d];if(i>=0)--t[projections[d][i]];if(j>=0)--t[projections[d][j]];if(k>=0)--t[projections[d][k]];auto it=index.find(sort3(t));check(it!=index.end(),"unexpected deletion type");++h[it->second];}test(h);++subsets;};
  if(size==45)deleted(-1,-1,-1);
  else if(size==44){for(int i=0;i<45;++i)deleted(i,-1,-1);}
  else for(int i=0;i<45;++i)for(int j=i+1;j<45;++j){if(size==43)deleted(i,j,-1);else for(int k=j+1;k<45;++k)deleted(i,j,k);}
  if(size==42){std::vector<I>h(types.size());for(size_t i=0;i<types.size();++i){auto it=DELTA.find(types[i]);if(it!=DELTA.end())h[i]=it->second;}test(h);}
  check(spectra==HISTOGRAMS.at(size),"all spectrum histograms");int ni=0;for(const auto&sp:SPECS)ni+=sp.size==size;
  std::cout<<"Size-"<<size<<" spectrum: "<<subsets<<" deleted subsets, "<<spectra.size()<<" histograms, "<<ni<<" integer spectral constraints verified.\n";
 }
}
struct Table {int m;std::vector<unsigned char>v;Table(int upper):m(upper+1),v(m*m*m){};bool at(int a,int b,int c)const{return a>=0&&b>=0&&c>=0&&a<m&&b<m&&c<m&&v[(a*m+b)*m+c];}void set(int a,int b,int c,bool ok){v[(a*m+b)*m+c]=ok;}};
std::vector<Triple> columns(int total,const Table&adm,bool sorted){std::vector<Triple>ans;for(int a=0;a<adm.m;++a)for(int b=0;b<adm.m;++b){int c=total-a-b;if((!sorted||(a>=b&&b>=c))&&adm.at(a,b,c))ans.push_back({a,b,c});}return ans;}
std::array<I,7> forced(const Triple&t,int n){I r=n==6?81:243,u=n==6?27:81,z=n==6?40:121;return {z*t[0]*t[1]*t[2],r*c2(t[0]),u*c3(t[0]),r*c2(t[1]),u*c3(t[1]),r*c2(t[2]),u*c3(t[2])};}
bool sub112(Triple t){t=sort3(t);return t[2]>=0&&t[0]<=45&&(t[2]<=22||(t[0]<=40&&t[1]<=36));}
std::string status_label(const Triple&s){if(s==Triple{-1,-1,-1})return "";std::string z=" status=";for(int v:s)z+=v<0?'-':char('0'+v);return z;}
I local(const Record&r,int n,const Table&adm,const Table*top,const std::vector<Triple>&complete={}){
 auto a=columns(r.key[0],adm,true),b=columns(r.key[1],adm,false),c=columns(r.key[2],adm,false);

 auto filter=[&](std::vector<Triple>&cols,int j){if(r.status[j]==-1)return;check(n==7&&r.key[j]>=103&&r.key[j]<109,"branch size");cols.erase(std::remove_if(cols.begin(),cols.end(),[&](const Triple&t){return r.status[j]==1?!sub112(t):dominates(t,complete);}),cols.end());};
 filter(a,0);filter(b,1);filter(c,2);
 auto q=r.q;if(r.empty)q=std::vector<I>(7,0);
 std::array<int,3> starts{{-1,-1,-1}};size_t nf=7+r.extra.size();for(int j=0;j<3;++j)if(r.status[j]==1){starts[j]=int(nf);nf+=2+(r.key[j]>=108);}
 check(q.size()==nf,"coefficient dimension");
 I S=0;auto totals=forced(r.key,n);for(int i=0;i<7;++i)S+=q[i]*totals[i];
 std::array<std::map<Triple,I>,3> phi;
 for(size_t k=0;k<r.extra.size();++k){auto ex=r.extra[k];const auto&sp=SPECS.at(ex.id);check(sp.size==r.key[ex.column],"wrong spectral size");check(!sp.bounded||q[7+k]>=0,"negative multiplier of upper bound");S+=q[7+k]*sp.total;const auto&ts=TYPES.at(sp.size);for(size_t j=0;j<ts.size();++j)phi[ex.column][ts[j]]+=q[7+k]*sp.q[j];}
 for(int j=0;j<3;++j)if(starts[j]>=0){int off=starts[j],d=112-r.key[j];S+=56*q[off]+11*d*q[off+1];if(r.key[j]>=108)S+=110*d*q[off+2];}
 I D=n==6?121:364;check(r.empty||(S==r.forced&&D*r.K-S==r.gap&&r.gap>0),"forced local gap");
 auto fcol=[&](const Triple&t,int j){I ans=q[1+2*j]*e2(t)+q[2+2*j]*e3(t);auto it=phi[j].find(sort3(t));if(it!=phi[j].end())ans+=it->second;
  if(starts[j]>=0){auto s=sort3(t);bool fam=s[2]<=22;int off=starts[j];ans+=q[off]*I(fam)+q[off+1]*(fam?22-s[2]:0);if(r.key[j]>=108)ans+=q[off+2]*(fam?0:40-s[0]);}
  return ans;};
 std::vector<I>fa,fb,fc;for(auto t:a)fa.push_back(fcol(t,0));for(auto t:b)fb.push_back(fcol(t,1));for(auto t:c)fc.push_back(fcol(t,2));
 I count=0,minimum=std::numeric_limits<I>::max();
 // Literal Cartesian product; no bit masks, feature deduplication, or column rotations.
 for(size_t i=0;i<a.size();++i)for(size_t j=0;j<b.size();++j)for(size_t k=0;k<c.size();++k){
  bool good=true;I T=0;
  for(int row=0;row<3&&good;++row)for(int slope=0;slope<3;++slope){int av=a[i][row],bv=b[j][(row+slope)%3],cv=c[k][(row+2*slope)%3];if(!adm.at(av,bv,cv)){good=false;break;}T+=I(av)*bv*cv;}
  if(!good)continue;
  if(top){for(int slope=0;slope<3;++slope){Triple sums{};for(int row=0;row<3;++row)sums[row]=a[i][row]+b[j][(row+slope)%3]+c[k][(row+2*slope)%3];if(!top->at(sums[0],sums[1],sums[2])){good=false;break;}}}
  if(!good)continue;
  ++count;I value=q[0]*T+fa[i]+fb[j]+fc[k];check(!r.empty&&value>=r.K,"local inequality or empty-family certificate");minimum=std::min(minimum,value);
 }
 if(r.empty){check(count==0,"empty family");std::cout<<"n="<<n<<" ("<<r.key[0]<<", "<<r.key[1]<<", "<<r.key[2]<<")"<<status_label(r.status)<<": EMPTY family verified.\n";}
 else{check(count>0,"unexpected empty family");std::cout<<"n="<<n<<" ("<<r.key[0]<<", "<<r.key[1]<<", "<<r.key[2]<<")"<<status_label(r.status)<<": matrices="<<count<<", minimum="<<minimum<<", certified_K="<<r.K<<", gap="<<r.gap<<"\n";}
 return count;
}
template<size_t N> int dot(const std::array<int,N>&a,const std::array<int,N>&b){int z=0;for(size_t j=0;j<N;++j)z+=a[j]*b[j];return z%3;}
template<size_t N> std::array<int,N> negative(std::array<int,N> p){for(auto&v:p)v=(3-v)%3;return p;}
template<size_t N> bool projective(const std::array<int,N>&p){auto it=std::find_if(p.begin(),p.end(),[](int x){return x!=0;});return it!=p.end()&&*it==1;}
void completion_representative(const std::vector<P6>&S){
 std::vector<P6> fam1,fam2;std::vector<P5>P;
 for(int k=1;k<729;++k){auto d=decode<6>(k);if(!projective(d))continue;std::array<std::vector<P6>,3>b;for(auto p:S)b[dot(d,p)].push_back(p);Triple h{int(b[0].size()),int(b[1].size()),int(b[2].size())};check(h==Triple{22,45,45}||h==Triple{40,36,36},"centered spectrum");(h[0]==22?fam1:fam2).push_back(d);
  if(P.empty()&&h[1]==45){int pivot=0;while(!d[pivot])++pivot;for(auto p:b[1]){P5 q;int j=0;for(int i=0;i<6;++i)if(i!=pivot)q[j++]=p[i];P.push_back(q);}}
 }
 check(fam1.size()==56&&fam2.size()==308,"center family counts");
 for(auto p:S){int n1=0,n2=0;for(auto d:fam1)n1+=dot(d,p)==0;for(auto d:fam2)n2+=dot(d,p)==0;check(n1==11&&n2==110,"point incidences in centered direction families");}
 check(P.size()==45,"reflected-pair representative size");capcheck(P);
 std::array<int,243> diff{};for(auto p:P)for(auto q:P){P5 z;for(int i=0;i<5;++i)z[i]=(3+p[i]-q[i])%3;++diff[encode(z)];}
 std::map<int,int> distribution;for(auto x:diff)++distribution[x];check(distribution==std::map<int,int>{{0,22},{9,220},{45,1}},"reflected-pair difference distribution");
 std::vector<P6> joined;for(auto p:P){P6 a,b;a[0]=0;b[0]=1;for(int i=0;i<5;++i){a[i+1]=p[i];b[i+1]=(3-p[i])%3;}joined.push_back(a);joined.push_back(b);}
 for(int i=0;i<243;++i)if(diff[i]==0){P6 p;p[0]=2;auto q=decode<5>(i);std::copy(q.begin(),q.end(),p.begin()+1);joined.push_back(p);}
 check(joined.size()==112,"reflected union size");capcheck(joined);
 std::cout<<"Completion representative: reflected 45-pair has 22 allowed points; positive multiplicities >=9; union is a 112-cap.\n";
 std::cout<<"Completed-slice identities: all 112 points have incidence 11 in the 56 small-center directions and 110 in the 308 large-center directions.\n";
}
void hill_representative(const std::vector<P6>&S){
 std::set<int> ss;for(auto p:S)ss.insert(encode(p));check(!ss.count(0),"Hill center in cap");for(auto p:S)check(ss.count(encode(negative(p))),"Hill representative not central");
 std::vector<P6>D,pd;
 for(int i=1;i<729;++i){auto d=decode<6>(i);Triple h{};for(auto p:S)++h[dot(d,p)];check(h[1]==h[2]&&(h==Triple{22,45,45}||h==Triple{40,36,36}),"Hill Fourier levels");if(h[0]-h[1]==-23){D.push_back(d);if(projective(d))pd.push_back(d);}}
 check(D.size()==112&&pd.size()==56,"Hill dual size");capcheck(D);std::set<int>ds;for(auto d:D)ds.insert(encode(d));for(auto d:D)check(ds.count(encode(negative(d))),"Hill dual not central");
 int pairs=0;for(size_t i=0;i<pd.size();++i)for(size_t j=0;j<i;++j){int ct=0;for(auto p:S)ct+=dot(p,pd[i])==0&&dot(p,pd[j])==0;check(ct==4,"Hill pair incidence");++pairs;}check(pairs==1540,"Hill pair count");
 for(int i=1;i<729;++i){auto x=decode<6>(i);Triple h{};for(auto d:D)++h[dot(x,d)];check(h[1]==h[2]&&h[0]-h[1]==4-27*I(ss.count(i)),"Hill dual Fourier formula");}
 std::cout<<"Hill representative: S and D are central 112-caps; both Fourier formulas and all 1540 pair incidences verified.\n";
}
std::array<I,8> hill_row(I u,I p){return {u==0,u==1,u==2,p,c2(p),c3(p),u*p,u*c2(p)};}
std::array<I,8> hill_rhs(I h){return {252+h,112-2*h,h,121*h,40*c2(h),13*c3(h),22*h,4*c2(h)};}
I hill_inequalities(){
 check(HILL.size()==56,"Hill certificate length");I checked=0;
 for(size_t i=0;i<HILL.size();++i){const auto&r=HILL[i];check(r.h==int(i)+1&&r.q.size()==8,"Hill case index or coefficient length");I F=0;auto tot=hill_rhs(r.h);for(int j=0;j<8;++j)F+=r.q[j]*tot[j];check(F==r.U,"Hill forced total");
  for(int u=0;u<3;++u)for(int p=0;p<=(u==0?20:11);++p){if(p>r.h||r.h-p>45)continue;++checked;auto row=hill_row(u,p);I value=0;for(int j=0;j<8;++j)value+=r.q[j]*row[j];if(r.impossible)check(value>=r.K,"Hill local intersection inequality");else{check(r.L>0,"Hill zero-count positive scale");check(value>=r.L*I(16+4*u+3*p-r.h==0),"Hill local zero-count inequality");}}
  I gap=r.impossible?364*r.K-F:15*r.L-F;check(gap==r.gap&&gap>0,"Hill final gap");
  if(r.impossible)std::cout<<"h="<<r.h<<": intersection impossible, gap="<<gap<<".\n";
  else std::cout<<"h="<<r.h<<": zero directions <= "<<F<<"/"<<r.L<<" < 15, exact gap="<<gap<<".\n";
 }
 for(int u=0;u<3;++u)check(16+4*u>0,"h=0 nonzero points");
 check(checked==2022,"Hill state count");std::cout<<"HILL LEMMA PASS: 56 cases and "<<checked<<" integer state inequalities; at most 28 zero-convolution points (h=0 gives one).\n";return checked;
}
Table top_table(int upper,const std::vector<Triple>&banned,int total=-1){Table t(upper);for(int a=0;a<=upper;++a)for(int b=0;b<=upper;++b){if(total>=0){int c=total-a-b;if(c>=0&&c<=upper)t.set(a,b,c,!dominates({a,b,c},banned));}else for(int c=0;c<=upper;++c)t.set(a,b,c,!dominates({a,b,c},banned));}return t;}
void completion_root(const std::vector<Triple>&old,const std::vector<Triple>&complete){
 check(COMPLETION_ROOT_Q2==-39&&COMPLETION_ROOT_Q3==1,"completion root coefficients");
 std::vector<Triple>banned=old;banned.insert(banned.end(),COMPLETION_SEEDS.begin(),COMPLETION_SEEDS.end());for(auto t:COMPLETION_ROOT_USES){check(std::find(complete.begin(),complete.end(),t)!=complete.end(),"unproved completion root dependency");banned.push_back(t);}
 int count=0;for(int a=0;a<=45;++a)for(int b=0;b<=a;++b){int c=109-a-b;if(c<0||c>b||!original6(a,b,c)||dominates({a,b,c},banned))continue;++count;check(COMPLETION_ROOT_Q2*e2({a,b,c})+COMPLETION_ROOT_Q3*e3({a,b,c})>=COMPLETION_ROOT_K,"completion root local inequality");}
 I F=COMPLETION_ROOT_Q2*243*c2(109)+COMPLETION_ROOT_Q3*81*c3(109);I gap=364*COMPLETION_ROOT_K-F;check(count==24&&F==COMPLETION_ROOT_FORCED&&gap==COMPLETION_ROOT_GAP&&gap>0,"completion root contradiction");
 std::cout<<"109-COMPLETION PASS: "<<count<<" remaining noncompletion types; K="<<COMPLETION_ROOT_K<<", forced="<<F<<", gap="<<gap<<".\n";
}
