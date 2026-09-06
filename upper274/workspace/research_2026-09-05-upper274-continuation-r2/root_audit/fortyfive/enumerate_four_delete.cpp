#include <array>
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <vector>
#include <stdexcept>
#include <chrono>
using namespace std;
void ck(bool a,const char*s){if(!a)throw runtime_error(s);}
struct Rec{long long count=0;array<int,4>del;};
int main(int argc,char**argv){
 ck(argc==3,"input output");auto start=chrono::steady_clock::now();ifstream in(argv[1]);vector<array<int,5>>p;int z;
 while(in>>z){array<int,5>x;for(int k=0;k<5;k++){x[k]=z%3;z/=3;}ck(!z,"ternarypoint");p.push_back(x);}ck(p.size()==45,"45input");
 int dot[121][45],base[121][3]={},dn=0;
 for(int raw=1;raw<243;raw++){int v=raw;array<int,5>u;for(int j=0;j<5;j++){u[j]=v%3;v/=3;}int j=0;while(!u[j])j++;if(u[j]!=1)continue;for(int i=0;i<45;i++){int s=0;for(int k=0;k<5;k++)s+=u[k]*p[i][k];dot[dn][i]=s%3;base[dn][s%3]++;}dn++;}ck(dn==121,"121normals");
 vector<array<int,3>>types;int index[21][21][21];for(auto &plane:index)for(auto &row:plane)for(int &v:row)v=-1;
 for(int a=0;a<=20;a++)for(int b=0;b<=a;b++){int c=41-a-b;if(c<0||c>b)continue;index[a][b][c]=types.size();types.push_back({a,b,c});}
 map<vector<int>,Rec>hist;long long nc=0;
 for(int a=0;a<42;a++)for(int b=a+1;b<43;b++)for(int c=b+1;c<44;c++)for(int d=c+1;d<45;d++){
  vector<int>h(types.size());for(int v=0;v<121;v++){array<int,3>t={base[v][0],base[v][1],base[v][2]};t[dot[v][a]]--;t[dot[v][b]]--;t[dot[v][c]]--;t[dot[v][d]]--;sort(t.begin(),t.end(),greater<int>());ck(t[0]<=18&&t[2]>=0,"deletionprofile");int k=index[t[0]][t[1]][t[2]];ck(k>=0,"profileindex");h[k]++;}
  auto &e=hist[h];if(!e.count)e.del={a,b,c,d};e.count++;nc++;if(nc%4096==0)ck(chrono::duration<double>(chrono::steady_clock::now()-start).count()<120,"120sbound");
 }
 ck(nc==148995,"all4subsets");ofstream out(argv[2]);for(auto t:types)out<<t[0]<<','<<t[1]<<','<<t[2]<<' ';out<<'\n';for(auto [h,r]:hist){for(int x:h)out<<x<<' ';out<<r.count<<' ';for(int i:r.del)out<<i<<' ';out<<'\n';}
 cout<<"ROOT_SUB45_FOUR_DELETE histograms="<<hist.size()<<" subsets="<<nc<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
}
