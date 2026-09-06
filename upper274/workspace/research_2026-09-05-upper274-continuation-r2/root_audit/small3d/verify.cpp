#include <array>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <map>
#include <stdexcept>
#include <vector>
using namespace std;using U=uint32_t;int d[27][3],tr[27][27];U masks[13][3];vector<int>types[8];map<int,int>ti[8];map<vector<int>,U>sets[8];long long counts[8]={};
void ck(bool b,const char*s){if(!b)throw runtime_error(s);}
void visit(int next,int n,U chosen,U forbid){
 vector<int>h(types[n].size());for(int j=0;j<13;j++){array<int,3>t={};for(int k=0;k<3;k++)t[k]=__builtin_popcount(chosen&masks[j][k]);sort(t.begin(),t.end(),greater<int>());int code=100*t[0]+10*t[1]+t[2];ck(ti[n].count(code),"profile <=4");h[ti[n][code]]++;}sets[n].emplace(h,chosen);counts[n]++;
 if(n==7)return;
 for(int p=next;p<27;p++)if(!(forbid>>p&1)){
  U ff=forbid;for(int x=0;x<27;x++)if(chosen>>x&1)ff|=U(1)<<tr[p][x];visit(p+1,n+1,chosen|(U(1)<<p),ff);
 }
}
int main(int argc,char**argv){ck(argc==2,"output file");
 for(int p=0;p<27;p++){int x=p;for(int i=0;i<3;i++){d[p][i]=x%3;x/=3;}}
 for(int x=0;x<27;x++)for(int y=0;y<27;y++){tr[x][y]=0;for(int j=0,p=1;j<3;j++,p*=3)tr[x][y]+=((6-d[x][j]-d[y][j])%3)*p;}
 int n=0;for(int p=1;p<27;p++){int f=0;while(!d[p][f])f++;if(d[p][f]!=1)continue;for(int q=0;q<27;q++){int z=0;for(int j=0;j<3;j++)z+=d[p][j]*d[q][j];masks[n][z%3]|=U(1)<<q;}n++;}ck(n==13,"13directions");
 for(int n=0;n<8;n++)for(int a=4;a>=0;a--)for(int b=a;b>=0;b--){int c=n-a-b;if(c<0||c>b)continue;int code=100*a+10*b+c;ti[n][code]=types[n].size();types[n].push_back(code);}
 visit(0,0,0,0);ofstream out(argv[1]);
 for(int n=0;n<8;n++){out<<n<<' '<<counts[n]<<' '<<types[n].size()<<' '<<sets[n].size()<<'\n';for(auto c:types[n])out<<c<<' ';out<<'\n';for(auto [h,rep]:sets[n]){for(int c:h)out<<c<<' ';out<<rep<<'\n';}cout<<"N="<<n<<" caps="<<counts[n]<<" histograms="<<sets[n].size()<<'\n';}
}
