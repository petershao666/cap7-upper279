#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using U=unsigned __int128;
using P=std::array<int,4>;
struct Trans { U mask; int center, centered_id; };
std::string hx(U m){std::string s(21,'0');for(int j=20;j>=0;--j){s[j]="0123456789abcdef"[int(m&15)];m>>=4;}return s;}
std::vector<int> points(U m){std::vector<int>v;for(int p=0;p<81;++p)if((m>>p)&1)v.push_back(p);return v;}
void ints(std::ostream&o,const std::vector<int>&v){o<<'[';for(size_t j=0;j<v.size();++j)o<<(j?",":"")<<v[j];o<<']';}
int main(int argc,char**argv){
 try{
  if(argc!=2)throw std::runtime_error("output directory required");
  std::string dir=argv[1];auto begin=std::chrono::steady_clock::now();
  auto bounded=[&](){if(std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()>580)throw std::runtime_error("enumeration time budget exceeded");};
  std::array<P,81>coord{}; int add[81][81],negadd[81][81];
  for(int p=0;p<81;++p){int z=p;for(int i=0;i<4;++i){coord[p][i]=z%3;z/=3;}}
  for(int p=0;p<81;++p)for(int q=0;q<81;++q){int a=0,n=0,k=1;for(int i=0;i<4;++i){int z=(coord[p][i]+coord[q][i])%3;a+=k*z;n+=k*((3-z)%3);k*=3;}add[p][q]=a;negadd[p][q]=n;}
  long long form_pair_checks=0;
  auto cap4=[&](U mask){auto v=points(mask);for(size_t i=0;i<v.size();++i)for(size_t j=i+1;j<v.size();++j){++form_pair_checks;if((mask>>negadd[v[i]][v[j]])&1)return false;}return true;};
  int mon[81][10]{};for(int p=0;p<81;++p){int k=0;for(int i=0;i<4;++i)for(int j=i;j<4;++j)mon[p][k++]=((i==j?1:2)*coord[p][i]*coord[p][j])%3;}
  U canonical=0;for(int p=1;p<81;++p){auto x=coord[p];if((x[0]*x[0]+x[1]*x[1]+x[2]*x[2]+2*x[3]*x[3])%3==0)canonical|=U(1)<<p;}
  if(points(canonical).size()!=20||!cap4(canonical))throw std::runtime_error("canonical cap failure");
  std::map<U,int> centered_map;int forms_twenty_zeros=0,forms_cap=0;
  for(int code=0;code<59049;++code){int z=code,c[10];for(int k=0;k<10;++k){c[k]=z%3;z/=3;}U mask=0;int n=0;for(int p=1;p<81;++p){int v=0;for(int k=0;k<10;++k)v+=c[k]*mon[p][k];if(v%3==0){mask|=U(1)<<p;++n;}}if(n!=20)continue;++forms_twenty_zeros;if(!cap4(mask))continue;++forms_cap;centered_map.emplace(mask,code);}
  bounded();
  std::vector<std::pair<U,int>> centered(centered_map.begin(),centered_map.end());
  std::ofstream cfile(dir+"/centered20.json");cfile<<"{\"canonical_mask\":\""<<hx(canonical)<<"\",\"canonical_points\":";ints(cfile,points(canonical));cfile<<",\"centered\":[";
  for(size_t i=0;i<centered.size();++i){if(i)cfile<<',';cfile<<"{\"id\":"<<i<<",\"mask\":\""<<hx(centered[i].first)<<"\",\"matrix_code\":"<<centered[i].second<<",\"point_ids\":";ints(cfile,points(centered[i].first));cfile<<'}';}cfile<<"]}\n";cfile.close();
  std::vector<Trans> all;all.reserve(centered.size()*81);
  for(size_t i=0;i<centered.size();++i){auto ps=points(centered[i].first);for(int t=0;t<81;++t){U mask=0;for(int p:ps)mask|=U(1)<<add[p][t];all.push_back({mask,t,int(i)});}}
  std::sort(all.begin(),all.end(),[](auto&a,auto&b){return a.mask<b.mask;});
  for(size_t i=1;i<all.size();++i)if(all[i-1].mask==all[i].mask)throw std::runtime_error("duplicate translated mask");
  std::ofstream acat(dir+"/all20_catalogue.tsv"),amasks(dir+"/all20_masks.txt");
  for(auto x:all){acat<<hx(x.mask)<<'\t'<<x.center<<'\t'<<x.centered_id<<'\n';amasks<<hx(x.mask)<<'\n';}acat.close();amasks.close();
  bounded();
  std::vector<std::array<int,5>> normals;std::array<std::array<int,5>,243>coord5{};
  for(int p=0;p<243;++p){int z=p;for(int i=0;i<5;++i){coord5[p][i]=z%3;z/=3;}if(p){int first=0;for(int a:coord5[p])if(a){first=a;break;}if(first==1)normals.push_back(coord5[p]);}}
  int neg5[243][243];for(int p=0;p<243;++p)for(int q=0;q<243;++q){int k=1,z=0;for(int i=0;i<5;++i){z+=k*((6-coord5[p][i]-coord5[q][i])%3);k*=3;}neg5[p][q]=z;}
  int dot[121][243];for(int d=0;d<121;++d)for(int p=0;p<243;++p){int z=0;for(int j=0;j<5;++j)z+=normals[d][j]*coord5[p][j];dot[d][p]=z%3;}
  std::vector<std::array<int,3>>types;for(int a=0;a<=20;++a)for(int b=0;b<=a;++b){int c=41-a-b;if(0<=c&&c<=b)types.push_back({a,b,c});}
  std::map<std::array<int,3>,int>ti;for(size_t i=0;i<types.size();++i)ti[types[i]]=i;
  std::map<std::vector<int>,int>hi;std::vector<std::vector<int>>hist,reps;std::vector<Trans>repB;
  auto A=points(canonical);long long eligible=0,pairs41=0;std::ofstream led(dir+"/eligible41_ledger.tsv");
  for(auto x:all){if(x.mask&canonical)continue;++eligible;std::vector<int>ps;for(int p:A)ps.push_back(3*p);for(int p:points(x.mask))ps.push_back(1+3*p);ps.push_back(2);std::sort(ps.begin(),ps.end());bool present[243]={};for(int p:ps)present[p]=true;
   for(int i=0;i<41;++i)for(int j=i+1;j<41;++j){++pairs41;if(present[neg5[ps[i]][ps[j]]])throw std::runtime_error("lift cap failure");}
   std::vector<int>h(types.size());for(int d=0;d<121;++d){std::array<int,3>n{};for(int p:ps)++n[dot[d][p]];std::sort(n.begin(),n.end(),std::greater<int>());if(!ti.count(n))throw std::runtime_error("twenty bound failure");++h[ti.at(n)];}
   long long e2=0,e3=0;for(size_t i=0;i<types.size();++i){auto t=types[i];e2+=h[i]*(t[0]*t[1]+t[0]*t[2]+t[1]*t[2]);e3+=h[i]*t[0]*t[1]*t[2];}if(e2!=81LL*41*40/2||e3!=27LL*41*40*39/6)throw std::runtime_error("histogram moment failure");
   int id;auto it=hi.find(h);if(it==hi.end()){id=int(hist.size());hi[h]=id;hist.push_back(h);reps.push_back(ps);repB.push_back(x);}else id=it->second;
   led<<hx(x.mask)<<'\t'<<x.center<<'\t'<<x.centered_id<<'\t'<<id<<'\n';
  }led.close();bounded();
  std::ofstream hf(dir+"/histograms41.json");hf<<"{\"scope\":\"ALL_41_CAPS_ADMITTING_20_20_1\",\"types\":[";for(size_t i=0;i<types.size();++i){if(i)hf<<',';ints(hf,{types[i][0],types[i][1],types[i][2]});}hf<<"],\"histograms\":[";
  for(size_t i=0;i<hist.size();++i){if(i)hf<<',';hf<<"{\"id\":"<<i<<",\"counts\":";ints(hf,hist[i]);hf<<",\"B_mask\":\""<<hx(repB[i].mask)<<"\",\"center\":"<<repB[i].center<<",\"centered_id\":"<<repB[i].centered_id<<",\"point_ids\":";ints(hf,reps[i]);hf<<",\"points\":[";for(size_t j=0;j<reps[i].size();++j){if(j)hf<<',';std::vector<int>p(coord5[reps[i][j]].begin(),coord5[reps[i][j]].end());ints(hf,p);}hf<<"]}";}hf<<"]}\n";hf.close();
  double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
  std::ofstream sf(dir+"/enumeration_statistics.json");sf<<"{\"forms_examined\":59049,\"forms_with_twenty_nonzero_zeros\":"<<forms_twenty_zeros<<",\"forms_passing_cap_check\":"<<forms_cap<<",\"centered_caps\":"<<centered.size()<<",\"translated_caps\":"<<all.size()<<",\"eligible_B_caps\":"<<eligible<<",\"distinct_histograms41\":"<<hist.size()<<",\"form_and_canonical_pair_checks\":"<<form_pair_checks<<",\"lift_pair_checks\":"<<pairs41<<",\"histogram_directions_checked\":"<<eligible*121<<",\"seconds\":"<<seconds<<"}\n";sf.close();
  std::cout<<"COMPLETED forms="<<59049<<" centered="<<centered.size()<<" translated="<<all.size()<<" eligible="<<eligible<<" histograms="<<hist.size()<<" seconds="<<seconds<<'\n';
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}return 0;
}
