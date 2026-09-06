#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
int xyz[243][5],third[243][243],dp[121][243],ix[21][21];
int main(int argc,char**argv){assert(argc==3);auto st=chrono::steady_clock::now();
 for(int p=0;p<243;p++){int z=p;for(int k=4;k>=0;k--){xyz[p][k]=z%3;z/=3;}}
 for(int p=0;p<243;p++)for(int q=0;q<243;q++){int c=0;for(int k=0;k<5;k++)c=3*c+(6-xyz[p][k]-xyz[q][k])%3;third[p][q]=c;}
 int nd=0;for(int v=1;v<243;v++){int first=0;while(!xyz[v][first])first++;if(xyz[v][first]!=1)continue;for(int p=0;p<243;p++){int s=0;for(int k=0;k<5;k++)s+=xyz[p][k]*xyz[v][k];dp[nd][p]=s%3;}nd++;}assert(nd==121);
 vector<array<int,3>>types;fill(&ix[0][0],&ix[0][0]+441,-1);for(int a=0;a<=20;a++)for(int b=0;b<=a;b++){int c=41-a-b;if(c<0||c>b)continue;ix[a][b]=types.size();types.push_back({a,b,c});}
 ifstream in(argv[1]);ofstream out(argv[2]);assert(in.good()&&out.good());out<<types.size();for(auto t:types)out<<" "<<t[0]<<" "<<t[1]<<" "<<t[2];out<<"\n";
 int row,count=0;long long npairs=0;while(in>>row){assert(row==count);int want[9],pts[41],grid[9]{};bool used[243]{};for(int&v:want)in>>v;for(int&p:pts){in>>p;assert(p>=0&&p<243&&!used[p]);used[p]=true;int x=xyz[p][0],y=xyz[p][1];int xpos=x==2?0:x+1,ypos=y==2?0:y+1;grid[3*xpos+ypos]++;}for(int i=0;i<9;i++)assert(grid[i]==want[i]);
  for(int i=0;i<41;i++)for(int j=i+1;j<41;j++){if(used[third[pts[i]][pts[j]]]){cerr<<"BAD_PAIR row="<<row<<" p="<<pts[i]<<" q="<<pts[j]<<" third="<<third[pts[i]][pts[j]]<<"\n";return 2;}npairs++;}
  vector<int>hist(types.size());for(int d=0;d<121;d++){array<int,3>c{};for(int p:pts)c[dp[d][p]]++;sort(c.begin(),c.end(),greater<int>());assert(c[0]<=20);int id=ix[c[0]][c[1]];assert(id>=0);hist[id]++;}
  long long e2=0,e3=0;int total=0;for(int i=0;i<(int)types.size();i++){auto[a,b,c]=types[i];total+=hist[i];e2+=(a*b+a*c+b*c)*hist[i];e3+=a*b*c*hist[i];}assert(total==121&&e2==66420&&e3==287820);
  out<<row;for(int n:hist)out<<" "<<n;out<<"\n";count++;if((count%1024)==0)assert(chrono::duration<double>(chrono::steady_clock::now()-st).count()<570);
 }
 assert(in.eof()&&count==34345&&npairs==28162900);cerr<<"PASS rows="<<count<<" pairs="<<npairs<<" directions="<<121LL*count<<" types="<<types.size()<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-st).count()<<"\n";
}
