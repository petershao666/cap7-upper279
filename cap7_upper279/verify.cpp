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
struct Record {Triple key;std::vector<I> q;I K,forced,gap;std::vector<Extra> extra;bool empty;};
#include "certificate_data.hpp"
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
I local(const Record&r,int n,const Table&adm,const Table*top){
 auto a=columns(r.key[0],adm,true),b=columns(r.key[1],adm,false),c=columns(r.key[2],adm,false);
 auto q=r.q;if(r.empty)q=std::vector<I>(7,0);check(q.size()==7+r.extra.size(),"coefficient dimension");
 I S=0;auto totals=forced(r.key,n);for(int i=0;i<7;++i)S+=q[i]*totals[i];
 std::array<std::map<Triple,I>,3> phi;
 for(size_t k=0;k<r.extra.size();++k){auto ex=r.extra[k];const auto&sp=SPECS.at(ex.id);check(sp.size==r.key[ex.column],"wrong spectral size");check(!sp.bounded||q[7+k]>=0,"negative multiplier of upper bound");S+=q[7+k]*sp.total;const auto&ts=TYPES.at(sp.size);for(size_t j=0;j<ts.size();++j)phi[ex.column][ts[j]]+=q[7+k]*sp.q[j];}
 I D=n==6?121:364;check(r.empty||(S==r.forced&&D*r.K-S==r.gap&&r.gap>0),"forced local gap");
 auto fcol=[&](const Triple&t,int j){I ans=q[1+2*j]*e2(t)+q[2+2*j]*e3(t);auto it=phi[j].find(sort3(t));if(it!=phi[j].end())ans+=it->second;return ans;};
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
 if(r.empty){check(count==0,"empty family");std::cout<<"n="<<n<<" ("<<r.key[0]<<", "<<r.key[1]<<", "<<r.key[2]<<"): EMPTY family verified.\n";}
 else{check(count>0,"unexpected empty family");std::cout<<"n="<<n<<" ("<<r.key[0]<<", "<<r.key[1]<<", "<<r.key[2]<<"): matrices="<<count<<", minimum="<<minimum<<", certified_K="<<r.K<<", gap="<<r.gap<<"\n";}
 return count;
}
int main(){
 auto begin=std::chrono::steady_clock::now();auto S=representative();spectral(S);
 Table a5(20);for(int a=0;a<=20;++a)for(int b=0;b<=20;++b)for(int c=0;c<=20;++c)a5.set(a,b,c,admissible5(a,b,c));
 std::vector<Triple>f6,f7;I n6=0,n7=0;
 for(size_t st=0;st<SIX.size();++st){Table top(45);for(int a=0;a<=45;++a)for(int b=0;b<=45;++b)for(int c=0;c<=45;++c)top.set(a,b,c,!dominates({a,b,c},f6));std::cout<<"DIMENSION SIX, STAGE "<<st<<": "<<SIX[st].size()<<" cases.\n";for(const auto&r:SIX[st]){check(std::find(f6.begin(),f6.end(),r.key)==f6.end(),"repeated 6 case");n6+=local(r,6,a5,f6.empty()?nullptr:&top);}for(const auto&r:SIX[st])f6.push_back(r.key);}
 Table a6(45);for(int a=0;a<=45;++a)for(int b=0;b<=45;++b)for(int c=0;c<=45;++c)a6.set(a,b,c,original6(a,b,c)&&!dominates({a,b,c},f6));
 for(size_t st=0;st<SEVEN.size();++st){Table top(112);for(int a=0;a<=112;++a)for(int b=0;b<=112;++b)for(int c=0;c<=112;++c)top.set(a,b,c,!dominates({a,b,c},f7));std::cout<<"DIMENSION SEVEN, STAGE "<<st<<": "<<SEVEN[st].size()<<" cases.\n";for(const auto&r:SEVEN[st]){check(std::find(f7.begin(),f7.end(),r.key)==f7.end()&&r.key[0]+r.key[1]+r.key[2]==TARGET,"repeated/wrong 7 case");n7+=local(r,7,a6,f7.empty()?nullptr:&top);}for(const auto&r:SEVEN[st])f7.push_back(r.key);}
 int remaining=0,excluded=0;for(int a=0;a<=112;++a)for(int b=0;b<=a;++b){int c=TARGET-a-b;if(c<0||c>b)continue;if(dominates({a,b,c},f7)){++excluded;continue;}++remaining;check(ROOT_Q2*e2({a,b,c})+ROOT_Q3*I(a)*b*c>=ROOT_K,"root inequality");}
 I root=ROOT_Q2*729*c2(TARGET)+ROOT_Q3*243*c3(TARGET);check(root==ROOT_FORCED&&1093*ROOT_K-root==ROOT_GAP&&ROOT_GAP>0,"root contradiction");
 std::cout<<"Root: "<<remaining<<" allowed types, "<<excluded<<" excluded types, K="<<ROOT_K<<", forced="<<root<<", gap="<<ROOT_GAP<<".\n";
 std::cout<<"FULL PASS: "<<n6<<" dimension-six matrices; "<<n7<<" dimension-seven matrices.\nUnder the published classification inputs in README.md, no "<<TARGET<<"-point cap exists; 236 <= f(7,3) <= "<<TARGET-1<<".\n";
 std::cout<<"Elapsed verification seconds: "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()<<'\n';
}
