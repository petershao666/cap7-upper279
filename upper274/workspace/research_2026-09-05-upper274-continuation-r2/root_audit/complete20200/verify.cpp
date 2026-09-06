#include <array>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <stdexcept>
#include <chrono>
using namespace std;using U=unsigned __int128;using H=vector<int>;
void ck(bool x,const char*s){if(!x)throw runtime_error(s);}
int xyz[243][5],tr[243][243];U dir_masks[121][2][3];
U parse(const string&s){ck(s.size()==21,"21hexdigits");U m=0;for(char c:s){int d=string("0123456789abcdef").find(c);ck(d>=0&&d<16,"hex");m=m*16+d;}ck(m<(U(1)<<81),"81bitcap");return m;}
string hexm(U m){string s(21,'0');for(int i=20;i>=0;i--){s[i]="0123456789abcdef"[int(m&15)];m>>=4;}return s;}
int pc(U x){return __builtin_popcountll(uint64_t(x))+__builtin_popcountll(uint64_t(x>>64));}
vector<int> pts(U m){vector<int>p;for(int i=0;i<81;i++)if(m>>i&1)p.push_back(i);return p;}
int main(int argc,char**argv){
 ck(argc==3,"usage catalog outputprefix");auto start=chrono::steady_clock::now();
 for(int p=0;p<243;p++){int v=p;for(int i=0;i<5;i++){xyz[p][i]=v%3;v/=3;}}
 for(int p=0;p<243;p++)for(int q=0;q<243;q++){int z=0,b=1;for(int j=0;j<5;j++,b*=3)z+=((6-xyz[p][j]-xyz[q][j])%3)*b;tr[p][q]=z;}
 U A=0;for(int p=1;p<81;p++)if((xyz[p][0]*xyz[p][0]+xyz[p][1]*xyz[p][1]+xyz[p][2]*xyz[p][2]+2*xyz[p][3]*xyz[p][3])%3==0)A|=U(1)<<p;ck(pc(A)==20,"canonical20");
 int dn=0;for(int raw=1;raw<243;raw++){int j=0;while(!xyz[raw][j])j++;if(xyz[raw][j]!=1)continue;for(int t=0;t<2;t++)for(int p=0;p<81;p++){int s=0;for(int k=0;k<5;k++)s+=xyz[raw][k]*xyz[p+81*t][k];dir_masks[dn][t][s%3]|=U(1)<<p;}dn++;}ck(dn==121,"121directions");
 vector<array<int,3>>types;map<array<int,3>,int>idx;
 for(int a=0;a<=20;a++)for(int b=0;b<=a;b++){int c=40-a-b;if(c<0||c>b)continue;idx[{a,b,c}]=types.size();types.push_back({a,b,c});}
 map<H,pair<long long,U>>counts;vector<int>a=pts(A);ifstream in(argv[1]);ck(in.good(),"readcatalog");U last=0;string s;long long all=0,pairs=0;
 while(in>>s){U B=parse(s);ck((!all||B>last)&&pc(B)==20,"sorteduniquecatalog20");last=B;auto b=pts(B);vector<int>ps=a;for(int p:b)ps.push_back(p+81);
  for(int x=0;x<40;x++)for(int y=x+1;y<40;y++){int z=tr[ps[x]][ps[y]];bool present=z<81?bool(A>>z&1):(z<162?bool(B>>(z-81)&1):false);ck(!present,"whole40cap");pairs++;}
  H h(types.size());for(int d=0;d<121;d++){array<int,3>t={};for(int z=0;z<3;z++)t[z]=pc(A&dir_masks[d][0][z])+pc(B&dir_masks[d][1][z]);sort(t.begin(),t.end(),greater<int>());ck(idx.count(t),"40profile");h[idx[t]]++;}
  auto [it,fresh]=counts.emplace(h,make_pair(0,B));it->second.first++;all++;if(all%16384==0)ck(chrono::duration<double>(chrono::steady_clock::now()-start).count()<300,"300sbound");
 }
 ck(all==682344,"acceptedcomplete20catalogue");ofstream out(string(argv[2])+"_histograms.txt");for(auto t:types)out<<t[0]<<','<<t[1]<<','<<t[2]<<' ';out<<'\n';for(auto [h,v]:counts){for(int n:h)out<<n<<' ';out<<v.first<<' '<<hexm(A)<<' '<<hexm(v.second)<<'\n';}
 cout<<"ROOT COMPLETE20200 total="<<all<<" histogram_count="<<counts.size()<<" allpairchecks="<<pairs<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
}
