#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <sys/resource.h>
using Z=__int128_t;
using T=std::array<int,3>;
using G=std::array<uint8_t,9>;
struct Entry{bool exists=false;Z value=0;};
Entry phi[46][46][46];
Z readz(std::istream&in){std::string s;in>>s;assert(!s.empty());Z x=0;int i=s[0]=='-';for(;i<int(s.size());i++){assert(s[i]>='0'&&s[i]<='9');x=10*x+s[i]-'0';}return s[0]=='-'?-x:x;}
std::string show(Z n){if(n==0)return"0";bool neg=n<0;if(neg)n=-n;std::string s;while(n){s.push_back(char('0'+n%10));n/=10;}if(neg)s.push_back('-');std::reverse(s.begin(),s.end());return s;}
T sort(T t){std::sort(t.begin(),t.end(),std::greater<int>());return t;}
int main(int argc,char**argv){
 assert(argc==3);rlimit cpu;assert(getrlimit(RLIMIT_CPU,&cpu)==0);cpu.rlim_cur=std::min<rlim_t>(590,cpu.rlim_max);assert(setrlimit(RLIMIT_CPU,&cpu)==0);auto start=std::chrono::steady_clock::now();
 std::ifstream in(argv[1]);int n;in>>n;assert(n==79);for(int i=0;i<n;i++){T t;in>>t[0]>>t[1]>>t[2];Z v=readz(in);assert(t==sort(t)&&!phi[t[0]][t[1]][t[2]].exists);phi[t[0]][t[1]][t[2]]={true,v};}
 in>>n;assert(n==14);uint64_t all=0;std::cout<<"{\"status\":\"PASS_ALL14_EXACT_ALL_ORDERED_OLD_GRIDS\",\"cases\":[";
 for(int ci=0;ci<14;ci++){
  int id;T anchor;in>>id>>anchor[0]>>anchor[1]>>anchor[2];assert(id==ci);Z qcross=readz(in),declaredK=readz(in);Entry table[3][21][21][21];
  for(int col=0;col<3;col++){int nt;in>>nt;for(int j=0;j<nt;j++){T t;in>>t[0]>>t[1]>>t[2];Z val=readz(in);assert(t==sort(t)&&t[0]+t[1]+t[2]==anchor[col]&&!table[col][t[0]][t[1]][t[2]].exists);table[col][t[0]][t[1]][t[2]]={true,val};}}
  std::string path=std::string(argv[2])+"/case"+(ci<10?"0":"")+std::to_string(ci)+"_old_raw.u8";std::ifstream raw(path,std::ios::binary);assert(raw);G g,witness{};Z minimum=Z(1)<<120,maxabs=0;uint64_t count=0,nmin=0;
  while(raw.read(reinterpret_cast<char*>(g.data()),9)){
   for(auto x:g)assert(x<=20);Z val=0;
   for(int col=0;col<3;col++){T t=sort({g[3*col],g[3*col+1],g[3*col+2]});assert(t[0]+t[1]+t[2]==anchor[col]);auto e=table[col][t[0]][t[1]][t[2]];assert(e.exists);val+=e.value;}
   // Nine nonvertical affine lines: nx*x+y=level. Each contributes one product.
   Z cross=0;for(int nx=0;nx<3;nx++){T sums{};for(int level=0;level<3;level++){int prod=1;for(int x=0;x<3;x++){int cell=g[3*x+(9+level-nx*x)%3];sums[level]+=cell;prod*=cell;}cross+=prod;}auto t=sort(sums);assert(t[0]<=45&&phi[t[0]][t[1]][t[2]].exists);val-=phi[t[0]][t[1]][t[2]].value;}
   val+=qcross*cross;assert(val>=declaredK);Z av=val<0?-val:val;maxabs=std::max(maxabs,av);if(val<minimum){minimum=val;witness=g;nmin=1;}else if(val==minimum)nmin++;count++;
  }
  assert(raw.gcount()==0&&raw.eof()&&count>0&&minimum==declaredK);all+=count;
  if(ci)std::cout<<",";std::cout<<"\n{\"case\":"<<ci<<",\"anchor\":["<<anchor[0]<<","<<anchor[1]<<","<<anchor[2]<<"],\"raw_count\":"<<count<<",\"minimum\":\""<<show(minimum)<<"\",\"minimizer_count\":"<<nmin<<",\"maximum_abs_value\":\""<<show(maxabs)<<"\",\"witness\":[";for(int j=0;j<9;j++){if(j)std::cout<<",";std::cout<<int(witness[j]);}std::cout<<"]}"<<std::flush;
 }
 rusage usage;assert(getrusage(RUSAGE_SELF,&usage)==0);assert(usage.ru_maxrss<1024LL*1024*1024);std::cout<<"\n],\"all_raw_count\":"<<all<<",\"elapsed_seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<",\"peak_rss_macos_bytes\":"<<usage.ru_maxrss<<",\"signed128_integer_arithmetic\":true}\n";
}
