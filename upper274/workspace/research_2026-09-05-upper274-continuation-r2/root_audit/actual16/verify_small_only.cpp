#include <array>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <cstdint>
#include <stdexcept>
#include <chrono>
using namespace std;
using U=uint32_t; using H=array<int,14>;
void ck(bool ok,const char*s){if(!ok)throw runtime_error(s);}
int third[81][81],coords[81][4],neg[27]; U masks[40][3][3];
vector<int> types; map<int,int> pos; vector<U> cats[10];
map<H,array<U,4>> hist; map<int,long long> counts,bcandidates;map<int,set<H>> familyhist;
long long npairs=0,nsets=0,nvisited=0;auto started=chrono::steady_clock::now();
bool cap(U m){for(int p=0;p<27;p++)if(m>>p&1)for(int q=p+1;q<27;q++)if(m>>q&1)if(m>>third[p][q]&1)return false;return true;}
void emit(U a,U b,U c,int label){
  nvisited++; if(nvisited%65536==0)ck(chrono::duration<double>(chrono::steady_clock::now()-started).count()<600,"600s bound");
  U layers[3]={a,b,c};int points[16],n=0;
  for(int t=0;t<3;t++)for(int p=0;p<27;p++)if(layers[t]>>p&1){ck(n<16,"too many points");points[n++]=p+27*t;}
  ck(n==16,"size16");
  for(int p=0;p<16;p++)for(int q=p+1;q<16;q++){int r=third[points[p]][points[q]];ck(!(layers[r/27]>>(r%27)&1),"cap16 pair");npairs++;}
  H h={};for(int d=0;d<40;d++){array<int,3>s={};for(int z=0;z<3;z++)for(int t=0;t<3;t++)s[z]+=__builtin_popcount(layers[t]&masks[d][t][z]);sort(s.begin(),s.end(),greater<int>());int code=100*s[0]+10*s[1]+s[2];ck(pos.count(code),"profile16");h[pos[code]]++;}
  for(int code:types)if(code/100>=8&&h[pos[code]])return;
  hist.emplace(h,array<U,4>{U(label),a,b,c});familyhist[label].insert(h);counts[label]++;nsets++;
  if(nsets%65536==0)ck(chrono::duration<double>(chrono::steady_clock::now()-started).count()<600,"600s bound");
}
void choose_c(U remaining,int need,U chosen,U a,U b,int label){
 if(!need){emit(a,b,chosen,label);return;}if(__builtin_popcount(remaining)<need)return;
 while(remaining){int p=__builtin_ctz(remaining);remaining&=remaining-1;
   bool ok=true;for(int x=0;x<27&&ok;x++)if(chosen>>x&1)if(chosen>>third[x][p]&1)ok=false;
   if(ok)choose_c(remaining,need-1,chosen|(U(1)<<p),a,b,label);
 }
}
int main(int argc,char**argv){
 ck(argc==3,"usage inputdirectory outputprefix");
 for(int x=0;x<81;x++){int y=x;for(int k=0;k<4;k++){coords[x][k]=y%3;y/=3;}}
 for(int x=0;x<81;x++)for(int y=0;y<81;y++){int z=0,p=1;for(int k=0;k<4;k++,p*=3)z+=((6-coords[x][k]-coords[y][k])%3)*p;third[x][y]=z;}
 for(int p=0;p<27;p++)neg[p]=third[0][p];
 for(int a=9;a>=0;a--)for(int b=a;b>=0;b--){int c=16-a-b;if(c<0||c>b)continue;int code=100*a+10*b+c;pos[code]=types.size();types.push_back(code);}ck(types.size()==14,"14 types");
 int nd=0;for(int v=1;v<81;v++){int first=0;while(!coords[v][first])first++;if(coords[v][first]!=1)continue;for(int t=0;t<3;t++)for(int p=0;p<27;p++){int z=0;for(int k=0;k<4;k++)z+=coords[v][k]*coords[p+27*t][k];masks[nd][t][z%3]|=U(1)<<p;}nd++;}ck(nd==40,"40 normals");
 int expected[9]={1,27,351,2808,14742,50544,107406,126360,63180};
 for(int n=4;n<=8;n++){
   string fn=string(argv[1])+"/"+(n==8?string("h17_actual_caps8.txt"):string("small3d_actual_caps")+to_string(n)+".txt");
   ifstream in(fn);ck(in.good(),"open catalogue");U m;while(in>>m){ck(m<(U(1)<<27)&&__builtin_popcount(m)==n&&cap(m),"actual input cap");cats[n].push_back(m);}
   ck(int(cats[n].size())==expected[n]&&is_sorted(cats[n].begin(),cats[n].end())&&adjacent_find(cats[n].begin(),cats[n].end())==cats[n].end(),"complete catalogue by actual unique count");
 }
 vector<pair<int,U>> reps; for(U a8:{U(13851),U(13867),U(14987)})for(int p=0;p<27;p++)if(a8>>p&1)reps.emplace_back(7,a8^(U(1)<<p)); ck(reps.size()==24,"24deletioncover");
 for(auto [na,a]:reps){ck(__builtin_popcount(a)==na&&cap(a),"anchor cap");U negA=0;for(int p=0;p<27;p++)if(a>>p&1)negA|=U(1)<<neg[p];
   for(int c=2;c<=3;c++){int nb=16-na-c;if(nb>na||nb<c)continue;int label=100*na+10*nb+c;
     for(U b:cats[nb]){if(c&&bool(b&negA))continue;bcandidates[label]++;
       if(!c){emit(a,b,0,label);continue;}
       U free=(U(1)<<27)-1;for(int p=0;p<27;p++)if(a>>p&1)for(int q=0;q<27;q++)if(b>>q&1)free&=~(U(1)<<third[p][q]);ck(free&1,"normalized singleton free");
       choose_c(free&~U(1),c-1,1,a,b,label);
     }
     cout<<"anchor "<<label<<" rep "<<a<<" emitted_cumulative "<<counts[label]<<" histograms "<<familyhist[label].size()<<endl;
   }
 }
 ofstream out(string(argv[2])+"_histograms.txt");for(int code:types)out<<code<<' ';out<<'\n';for(auto [h,rep]:hist){for(int x:h)out<<x<<' ';for(U r:rep)out<<r<<' ';out<<'\n';}
 ofstream ct(string(argv[2])+"_counts.txt");for(auto [k,v]:counts)ct<<k<<' '<<v<<' '<<familyhist[k].size()<<' '<<bcandidates[k]<<'\n';
 cout<<"ROOT_SMALL_ONLY16 actual_histograms="<<hist.size()<<" visited_caps="<<nvisited<<" normalized_small_caps="<<nsets<<" pairs="<<npairs<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-started).count()<<endl;
}
