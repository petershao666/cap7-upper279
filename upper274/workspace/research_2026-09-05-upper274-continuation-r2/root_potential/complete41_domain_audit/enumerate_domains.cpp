#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include <sys/resource.h>
using Triple=std::array<int,3>;
using Grid=std::array<uint8_t,9>;
using Feature=std::array<int,19>;
using Clock=std::chrono::steady_clock;
Triple sorted(Triple t){std::sort(t.begin(),t.end(),std::greater<int>());return t;}
int e2(Triple t){return t[0]*t[1]+t[0]*t[2]+t[1]*t[2];}
int e3(Triple t){return t[0]*t[1]*t[2];}
bool avoids(Triple t,const std::vector<Triple>& ban){t=sorted(t);for(auto b:ban)if(t[0]>=b[0]&&t[1]>=b[1]&&t[2]>=b[2])return false;return true;}
std::vector<Triple> read(std::istream& in){int n;in>>n;std::vector<Triple> a(n);for(auto&t:a)in>>t[0]>>t[1]>>t[2];return a;}
Triple column(const Grid& g,int x){return {g[3*x],g[3*x+1],g[3*x+2]};}
bool cover(const Grid&g){auto a=column(g,0),b=column(g,1);return a==sorted(a)&&b>=Triple{b[1],b[2],b[0]}&&b>=Triple{b[2],b[0],b[1]};}
Grid change(const Grid&g,int u,int v,int w){Grid z;for(int x=0;x<3;x++)for(int y=0;y<3;y++)z[3*x+(u*y+v+w*x)%3]=g[3*x+y];return z;}
Grid canonical(const Grid&g){Grid z=g;for(int u=1;u<=2;u++)for(int v=0;v<3;v++)for(int w=0;w<3;w++)z=std::max(z,change(g,u,v,w));return z;}
void putgrid(std::ofstream&out,const Grid&g){out.write(reinterpret_cast<const char*>(g.data()),9);}
void putfeature(std::ofstream&out,const Feature&f){for(int n:f){assert(n>=0);uint32_t u=n;char b[4];for(int j=0;j<4;j++)b[j]=char((u>>(8*j))&255);out.write(b,4);}}
struct Orbit{uint64_t raw=0,discovery=0;bool new_ok=false,initialized=false;};
bool adm[2][21][21][21];
bool top[14][46][46][46];
std::array<std::array<int,3>,12> lines;
int typeid106[46][46][46];
bool eligible(const Grid&g,int mode,int ci){for(auto l:lines)if(!adm[mode][g[l[0]]][g[l[1]]][g[l[2]]])return false;for(int s=0;s<3;s++){Triple t{};for(int r=0;r<3;r++)for(int x=0;x<3;x++)t[r]+=g[3*x+(r+s*x)%3];if(t[0]>45||t[1]>45||t[2]>45||!top[ci][t[0]][t[1]][t[2]])return false;}return true;}
Feature feature(const Grid&g){Feature f{};for(int l=3;l<12;l++)f[0]+=g[lines[l][0]]*g[lines[l][1]]*g[lines[l][2]];for(int x=0;x<3;x++){auto t=column(g,x);f[1+2*x]=e2(t);f[2+2*x]=e3(t);t=sorted(t);for(int j=0;j<3;j++)f[7+3*x+j]=t[j];}for(int s=0;s<3;s++){Triple t{};for(int r=0;r<3;r++)for(int x=0;x<3;x++)t[r]+=g[3*x+(r+s*x)%3];int id=typeid106[t[0]][t[1]][t[2]];assert(id>=0);f[16+s]=id;}return f;}
int main(int argc,char**argv){
 assert(argc==3);rlimit cpu;assert(getrlimit(RLIMIT_CPU,&cpu)==0);cpu.rlim_cur=std::min<rlim_t>(180,cpu.rlim_max);assert(setrlimit(RLIMIT_CPU,&cpu)==0);
 auto start=Clock::now();std::ifstream in(argv[1]);auto old6=read(in),comp=read(in),old41=read(in),zero41=read(in),support=read(in),anchors=read(in);assert(support.size()==79&&anchors.size()==14);std::vector<Triple> large[46];for(int n=42;n<=45;n++)large[n]=read(in);assert(in);
 for(int x=0;x<3;x++)for(int y=0;y<3;y++)lines[x][y]=3*x+y;for(int s=0;s<3;s++)for(int r=0;r<3;r++)for(int x=0;x<3;x++)lines[3+3*s+r][x]=3*x+(r+s*x)%3;
 std::set<std::array<int,3>> linecheck;for(auto l:lines){auto q=l;std::sort(q.begin(),q.end());linecheck.insert(q);}assert(linecheck.size()==12);
 int pcount[2]={};for(int a=0;a<=20;a++)for(int b=0;b<=20;b++)for(int c=0;c<=20;c++){Triple t=sorted({a,b,c});int n=a+b+c;bool base=n<=45;if(n>=42&&n<=45)base=std::find(large[n].begin(),large[n].end(),t)!=large[n].end();adm[0][a][b][c]=base&&avoids(t,old41);adm[1][a][b][c]=adm[0][a][b][c]&&avoids(t,zero41);for(int m=0;m<2;m++)pcount[m]+=adm[m][a][b][c];}
 std::fill(&typeid106[0][0][0],&typeid106[0][0][0]+46*46*46,-1);for(int j=0;j<int(support.size());j++){auto t=support[j];std::sort(t.begin(),t.end());do{typeid106[t[0]][t[1]][t[2]]=j;}while(std::next_permutation(t.begin(),t.end()));}
 auto bans=old6;bans.insert(bans.end(),comp.begin(),comp.end());for(int ci=0;ci<14;ci++){for(int a=0;a<=45;a++)for(int b=0;b<=45;b++){int c=106-a-b;if(c<0||c>45)continue;top[ci][a][b][c]=avoids({a,b,c},bans);assert(!top[ci][a][b][c]||typeid106[a][b][c]>=0);}bans.push_back(anchors[ci]);}
 std::cout<<"{\"status\":\"PASS_COMPLETE_ALL14_OLD_NEW_DOMAINS\",\"ordered_5D_profile_counts\":["<<pcount[0]<<","<<pcount[1]<<"],\"cases\":[\n";
 for(int ci=0;ci<14;ci++){
  assert(std::chrono::duration<double>(Clock::now()-start).count()<175);auto t0=Clock::now();auto A=anchors[ci];std::vector<Triple> cols[3];for(int x=0;x<3;x++)for(int a=0;a<=20;a++)for(int b=0;b<=20;b++){int c=A[x]-a-b;if(c>=0&&c<=20&&adm[0][a][b][c])cols[x].push_back({a,b,c});}
  std::string pre=std::string(argv[2])+"/case"+(ci<10?"0":"")+std::to_string(ci);std::ofstream raw[2],dis[2],can[2],fea[2],uf[2];for(int m=0;m<2;m++){auto p=pre+(m?"_new":"_old");raw[m].open(p+"_raw.u8",std::ios::binary);dis[m].open(p+"_cover.u8",std::ios::binary);can[m].open(p+"_canonical.u8",std::ios::binary);fea[m].open(p+"_features.i32le",std::ios::binary);uf[m].open(p+"_unique_features.i32le",std::ios::binary);assert(raw[m]&&dis[m]&&can[m]&&fea[m]&&uf[m]);}
  uint64_t nr[2]={},na[2]={},nd[2]={},nc[2]={};std::map<Grid,Orbit> orbits;std::set<Feature> features[2];
  for(auto a:cols[0])for(auto b:cols[1])for(auto c:cols[2]){Grid g;for(int y=0;y<3;y++){g[y]=a[y];g[3+y]=b[y];g[6+y]=c[y];}if(!eligible(g,0,ci))continue;bool isnew=eligible(g,1,ci),iscov=cover(g);auto canon=canonical(g);auto &rec=orbits[canon];if(rec.initialized)assert(rec.new_ok==isnew);else{rec.initialized=true;rec.new_ok=isnew;}rec.raw++;rec.discovery+=iscov;for(int mode=0;mode<=int(isnew);mode++){nr[mode]++;putgrid(raw[mode],g);na[mode]+=(a==sorted(a));if(iscov){nd[mode]++;putgrid(dis[mode],g);auto f=feature(g);putfeature(fea[mode],f);features[mode].insert(f);}}assert(orbits.size()+features[0].size()+features[1].size()<1000000);}
  std::map<std::array<uint64_t,3>,uint64_t> multiplicities[2];std::ofstream orb(pre+"_orbit_ledger.tsv");orb<<"a0\ta1\ta2\tb0\tb1\tb2\tc0\tc1\tc2\torbit_size\tcover_multiplicity\tnew_retained\n";
  for(auto [g,rec]:orbits){std::set<Grid> images;for(int u=1;u<=2;u++)for(int v=0;v<3;v++)for(int w=0;w<3;w++)images.insert(change(g,u,v,w));uint64_t ncover=0;for(auto z:images){assert(eligible(z,0,ci));assert(eligible(z,1,ci)==rec.new_ok);ncover+=cover(z);}assert(images.size()==rec.raw&&ncover==rec.discovery&&ncover>0&&cover(g));for(int mode=0;mode<=int(rec.new_ok);mode++){nc[mode]++;putgrid(can[mode],g);multiplicities[mode][{rec.raw,rec.discovery,18/rec.raw}]++;}for(auto x:g)orb<<int(x)<<'\t';orb<<rec.raw<<'\t'<<rec.discovery<<'\t'<<rec.new_ok<<'\n';}
  for(int mode=0;mode<2;mode++)for(auto f:features[mode])putfeature(uf[mode],f);
  if(ci)std::cout<<",\n";std::cout<<"{\"case\":"<<ci<<",\"anchor\":["<<A[0]<<","<<A[1]<<","<<A[2]<<"],\"column_candidates_old\":["<<cols[0].size()<<","<<cols[1].size()<<","<<cols[2].size()<<"],\"modes\":[";
  for(int mode=0;mode<2;mode++){if(mode)std::cout<<",";std::cout<<"{\"mode\":\""<<(mode?"new":"old")<<"\",\"raw\":"<<nr[mode]<<",\"alpha_sorted\":"<<na[mode]<<",\"discovery_cover\":"<<nd[mode]<<",\"true_orbits\":"<<nc[mode]<<",\"unique19features\":"<<features[mode].size()<<",\"multiplicity_classes\":[";bool first=true;for(auto [cl,n]:multiplicities[mode]){if(!first)std::cout<<",";first=false;std::cout<<"["<<cl[0]<<","<<cl[1]<<","<<cl[2]<<","<<n<<"]";}std::cout<<"]}";}
  std::cout<<"],\"seconds\":"<<std::chrono::duration<double>(Clock::now()-t0).count()<<"}"<<std::flush;
 }
 rusage usage;assert(getrusage(RUSAGE_SELF,&usage)==0);std::cout<<"\n],\"elapsed_seconds\":"<<std::chrono::duration<double>(Clock::now()-start).count()<<",\"peak_rss_macos_bytes\":"<<usage.ru_maxrss<<",\"all_orbit_multiplicities_checked\":true,\"point_realizability_or_exclusion_claimed\":false}\n";assert(usage.ru_maxrss<1024LL*1024*1024);
}
