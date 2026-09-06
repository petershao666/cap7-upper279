#include <array>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <vector>
#include <cstdint>
#include <stdexcept>
using namespace std;using U=uint32_t;using H=array<int,13>;
void ck(bool x,const char*s){if(!x)throw runtime_error(s);}
int d3[27][3],negp[27],third[27][27],third4[81][81];U masks[40][3][3];map<int,int> ti;vector<int>codes;map<H,array<U,3>> hist;
long long branches[5]={},pairchecks=0;vector<U> cap8;
bool cap(U a){for(int x=0;x<27;x++)if(a>>x&1)for(int y=x+1;y<27;y++)if(a>>y&1)if(a>>third[x][y]&1)return false;return true;}
void emit(U a,U b,int label,int bi,bool singleton){
 ck(__builtin_popcount(a)+__builtin_popcount(b)+singleton==17,"size17");uint64_t pts=uint64_t(a)|(uint64_t(b)<<27)|(singleton?uint64_t(1)<<54:0);
 vector<int>ls;for(int x=0;x<55;x++)if(pts>>x&1)ls.push_back(x);ck(ls.size()==17,"distinct17");
 for(int x=0;x<17;x++)for(int y=x+1;y<17;y++){int z=third4[ls[x]][ls[y]];ck(z>=64||!(pts>>z&1),"cap17pair");pairchecks++;}
 H h={};for(int j=0;j<40;j++){array<int,3>c={};for(int z=0;z<3;z++)c[z]=__builtin_popcount(a&masks[j][0][z])+__builtin_popcount(b&masks[j][1][z])+(singleton&&bool(masks[j][2][z]&1));sort(c.begin(),c.end(),greater<int>());int code=c[0]*100+c[1]*10+c[2];ck(ti.count(code),"17profile");h[ti[code]]++;}
 hist.emplace(h,array<U,3>{U(label),a,b});branches[bi]++;
}
void dfs(vector<int>pool,int at,int need,U chosen,U forbid,U a,int label,int bi){
 if(!need){emit(a,chosen,label,bi,true);return;}if(int(pool.size())-at<need)return;
 for(int i=at;i<=int(pool.size())-need;i++){
  int p=pool[i];if(forbid>>p&1)continue;U ff=forbid;
  for(int x=0;x<27;x++)if(chosen>>x&1)ff|=U(1)<<third[p][x];
  dfs(pool,i+1,need-1,chosen|(U(1)<<p),ff,a,label,bi);
 }
}
int main(int argc,char**argv){
 ck(argc==4,"inputs:orbits caps8 output");for(int p=0;p<27;p++){int x=p;negp[p]=0;for(int i=0,base=1;i<3;i++,base*=3){d3[p][i]=x%3;x/=3;negp[p]+=((3-d3[p][i])%3)*base;}}
 for(int x=0;x<81;x++)for(int y=0;y<81;y++){int xx=x,yy=y,z=0;for(int i=0,p=1;i<4;i++,p*=3){z+=((6-xx%3-yy%3)%3)*p;xx/=3;yy/=3;}third4[x][y]=z;if(x<27&&y<27)third[x][y]=z;}
 for(int a=9;a>=0;a--)for(int b=a;b>=0;b--){int c=17-a-b;if(c<0||c>b)continue;ti[a*100+b*10+c]=codes.size();codes.push_back(a*100+b*10+c);}ck(codes.size()==13,"13types");
 int nd=0;for(int raw=1;raw<81;raw++){array<int,4>v={};int x=raw;for(int j=0;j<4;j++){v[j]=x%3;x/=3;}int first=0;while(!v[first])first++;if(v[first]!=1)continue;for(int layer=0;layer<3;layer++)for(int p=0;p<27;p++){int z=(v[0]*d3[p][0]+v[1]*d3[p][1]+v[2]*d3[p][2]+v[3]*layer)%3;masks[nd][layer][z]|=U(1)<<p;}nd++;}ck(nd==40,"40directions");
 ifstream cf(argv[2]);U p;while(cf>>p){ck(__builtin_popcount(p)==8&&cap(p),"sourcecap8");cap8.push_back(p);}ck(cap8.size()==63180&&is_sorted(cap8.begin(),cap8.end()),"full63180sortedinput");
 ifstream in(argv[1]);int nr;in>>nr;ck(nr==4,"1+3orbits");int oi8=0;
 for(int z=0;z<nr;z++){int n;U a;in>>n>>a;ck(__builtin_popcount(a)==n&&cap(a),"orbitrep");if(n==9){for(auto b:cap8)emit(a,b,980,0,false);}U na=0;for(int p=0;p<27;p++)if(a>>p&1)na|=U(1)<<negp[p];vector<int>pool;for(int p=0;p<27;p++)if(!(na>>p&1))pool.push_back(p);ck(pool.size()==27-n,"complement");if(n==9)dfs(pool,0,7,0,0,a,971,1);else{ck(n==8,"cap8orbit");dfs(pool,0,8,0,0,a,881,2+oi8);oi8++;}}
 ck(oi8==3,"three8orbits");ofstream out(argv[3]);for(auto c:codes)out<<c<<' ';out<<'\n';for(auto [h,rep]:hist){for(auto x:h)out<<x<<' ';out<<rep[0]<<' '<<rep[1]<<' '<<rep[2]<<'\n';}
 cout<<"ROOT ACTUAL17 unique_histograms="<<hist.size()<<" pairchecks="<<pairchecks<<" branches=";for(auto n:branches)cout<<n<<',';cout<<'\n';
}
