#include <algorithm>
#include <array>
#include <cassert>
#include <fstream>
#include <iostream>
#include <vector>
#include <climits>
using namespace std;
using Z=__int128_t;
using Tri=array<int,3>;
using Grid=array<Tri,3>;
struct Row {int kind,j,a,b,c,k;long long q;};
struct Profile {bool exists=false;long long q[8]={0};long long qt=0;};
vector<Tri> old,comp,ban;
Profile pf[2][46][46];
long long normq[3]={0},outerq[7]={0};
long long theta[21][21];bool thpresent[21][21];
bool p5[21][21][21],p6[46][46][46],nc[46][46][46];
vector<Row> rows;
Tri sorted(Tri t){sort(t.begin(),t.end(),greater<int>());return t;}
int sum(Tri t){return t[0]+t[1]+t[2];}
long long e2(Tri t){return 1LL*t[0]*t[1]+1LL*t[0]*t[2]+1LL*t[1]*t[2];}
long long e3(Tri t){return 1LL*t[0]*t[1]*t[2];}
long long choose2(int n){return 1LL*n*(n-1)/2;}
long long choose3(int n){return 1LL*n*(n-1)*(n-2)/6;}
bool avoid(Tri t,const vector<Tri>& bans){t=sorted(t);for(Tri b:bans)if(t[0]>=b[0]&&t[1]>=b[1]&&t[2]>=b[2])return false;return true;}
bool complete(Tri t){t=sorted(t);return t[2]<=22||(t[0]<=40&&t[1]<=36);}
long long Q(Tri t){return 9*e3(t)-899*e2(t)+15730000;}
long long mixed(const Grid&m){long long r=0;for(int a=0;a<3;a++)for(int b=0;b<3;b++)r+=1LL*m[0][a]*m[1][b]*m[2][(6-a-b)%3];return r;}
vector<long long> force(Tri t){vector<long long> f={40*e3(t)};for(int v=0;v<=45;v++){int n=count(t.begin(),t.end(),v);if(n){f.push_back(n*81*choose2(v));f.push_back(n*27*choose3(v));}}return f;}
vector<long long> features(const Grid&m){vector<long long> f={mixed(m)};Tri t={sum(m[0]),sum(m[1]),sum(m[2])};for(int v=0;v<=45;v++){long long x=0,y=0;bool yes=false;for(int c=0;c<3;c++)if(t[c]==v){yes=true;x+=e2(m[c]);y+=e3(m[c]);}if(yes){f.push_back(x);f.push_back(y);}}return f;}
Z inner_score(const Grid&m,int j){
  Z result=normq[j+1];
  const int dirs[4][2]={{1,0},{0,1},{1,1},{1,2}};
  for(int d=0;d<4;d++){
    int ax=dirs[d][0],ay=dirs[d][1];Grid r{};
    // Chosen complement is y if ax=1, and x otherwise.
    for(int x=0;x<3;x++)for(int y=0;y<3;y++)r[(ax*x+ay*y)%3][ax?y:x]=m[x][y];
    Tri t=sorted({sum(r[0]),sum(r[1]),sum(r[2])});Profile &p=pf[j][t[0]][t[1]];assert(p.exists);
    vector<long long> f=features(r),F=force(t);assert(f.size()==F.size());result+=p.q[0];
    for(size_t k=0;k<f.size();k++)result+=(Z)p.q[k+1]*(121*f[k]-F[k]);
    if(count(t.begin(),t.end(),40)){
      long long th=0;int mult=0;
      for(int c=0;c<3;c++)if(sum(r[c])==40){Tri a=sorted(r[c]);assert(thpresent[a[0]][a[1]]);th+=theta[a[0]][a[1]];mult++;}
      result+=(Z)p.qt*(121*th-475918720LL*mult);
    } else assert(p.qt==0);
  }
  return result;
}
Z outer_score(const Grid&m){
 Z r=normq[0]+(Z)364*outerq[0]*mixed(m);
 r+=(Z)364*outerq[1]*(e2(m[0])+e2(m[1]));r+=(Z)364*outerq[2]*(e3(m[0])+e3(m[1]));
 r+=(Z)364*outerq[3]*e2(m[2]);r+=(Z)364*outerq[4]*e3(m[2]);
 for(int j=0;j<2;j++){Tri t=sorted(m[j]);assert(pf[0][t[0]][t[1]].exists);r-=2*(Z)pf[0][t[0]][t[1]].q[0];}return r;
}
void initialize(){
 vector<Tri> bad41={{20,19,2},{20,18,3},{19,19,3},{19,18,4}};
 vector<Tri> delta={{20,16,6},{18,18,6},{18,17,7},{18,12,12},{16,15,11},{16,14,12},{15,15,12},{14,14,14}};
 vector<Tri> f6=old;for(Tri t:comp)if(!complete(t))f6.push_back(t);
 for(int a=0;a<=45;a++)for(int b=0;b<=45;b++)for(int c=0;c<=45;c++){
  Tri t={a,b,c},s=sorted(t);int n=sum(t);
  p6[a][b][c]=n<=112&&(n<109||complete(t))&&avoid(t,f6);
  nc[a][b][c]=p6[a][b][c]&&avoid(t,comp);
  if(a<=20&&b<=20&&c<=20){bool yes=n<=45&&(n<42||(s[0]<=18&&s[1]<=18&&s[2]<=9)||s[0]<=15||(n==42&&find(delta.begin(),delta.end(),s)!=delta.end()));p5[a][b][c]=yes&&avoid(t,bad41);}
 }
}
bool local(Tri t,bool out){return out?p6[t[0]][t[1]][t[2]]:p5[t[0]][t[1]][t[2]];}
vector<Tri> compositions(int n,int limit,int col,bool out){vector<Tri> v;for(int a=0;a<=limit;a++)for(int b=0;b<=limit;b++){int c=n-a-b;if(c<0||c>limit)continue;Tri t={a,b,c};if(col==0&&(a<b||b<c))continue;if(!local(t,out))continue;if(out&&col<2&&!nc[a][b][c])continue;v.push_back(t);}return v;}
bool valid(const Grid &m,bool out,int total){
 for(int slope=0;slope<3;slope++){
  Tri sums{};
  for(int intercept=0;intercept<3;intercept++){
   Tri line={m[0][intercept],m[1][(intercept+slope)%3],m[2][(intercept+2*slope)%3]};
   if(!local(line,out))return false;sums[intercept]=sum(line);
  }
  if(out){if(*max_element(sums.begin(),sums.end())>112||!avoid(sums,ban)||Q(sums)<Q({107,107,61}))return false;}
  else {if(*max_element(sums.begin(),sums.end())>45||!avoid(sums,old)||!avoid(sums,comp))return false;}
  assert(sum(sums)==total);
 }
 return true;
}
struct Result{long long count=0;Z maximum=-(Z(1)<<100);};
Result run(Tri target,int j){bool out=j<0;int limit=out?45:20;vector<Tri> list[3];for(int c=0;c<3;c++)list[c]=compositions(target[c],limit,c,out);Result r;
 for(const Tri&a:list[0])for(const Tri&b:list[1])for(const Tri&c:list[2]){Grid m={a,b,c};if(!valid(m,out,sum(target)))continue;r.count++;Z v=out?outer_score(m):inner_score(m,j);r.maximum=max(r.maximum,v);assert(v<=0);}
 return r;
}
vector<Tri> readtriples(ifstream&f){int n;f>>n;vector<Tri> v(n);for(auto&t:v)f>>t[0]>>t[1]>>t[2];return v;}
int main(int argc,char**argv){assert(argc==2);ifstream f(argv[1]);assert(f.good());int nr;f>>nr;assert(nr==375);int upper=0;
 for(int i=0;i<nr;i++){Row r;f>>r.kind>>r.j>>r.a>>r.b>>r.c>>r.k>>r.q;rows.push_back(r);if(r.kind==0)normq[0]=r.q;else if(r.kind==1)normq[1+r.j]=r.q;else if(r.kind==2)outerq[r.k]=r.q;else {auto&p=pf[r.j][r.a][r.b];p.exists=true;if(r.kind==3)p.q[r.k]=r.q;else {assert(r.kind==4&&r.q<=0);p.qt=r.q;upper++;}}}
 assert(upper==12);old=readtriples(f);comp=readtriples(f);ban=readtriples(f);int nth;f>>nth;assert(nth==44);for(int i=0;i<nth;i++){int a,b,c;long long v;f>>a>>b>>c>>v;assert(a+b+c==40);theta[a][b]=v;thpresent[a][b]=true;}assert(f.good());
 // Validate every metadata row against a freshly generated exact row catalogue.
 vector<Row> expected={{0,0,0,0,0,0,0},{1,0,0,0,0,0,0}};for(int k=0;k<5;k++)expected.push_back({2,0,0,0,0,k,0});
 vector<Tri> types[2];for(int j=0;j<1;j++){int N=107;for(int a=0;a<=45;a++)for(int b=0;b<=a;b++){int c=N-a-b;if(c<0||c>b)continue;Tri t={a,b,c};if(!avoid(t,old)||!avoid(t,comp))continue;types[j].push_back(t);for(int k=0;k<=int(force(t).size());k++)expected.push_back({3,j,a,b,c,k,0});}}
 for(int j=0;j<1;j++)for(Tri t:types[j])if(count(t.begin(),t.end(),40))expected.push_back({4,j,t[0],t[1],t[2],0,0});assert(expected.size()==rows.size());
 for(size_t i=0;i<rows.size();i++){Row a=rows[i],b=expected[i];assert(a.kind==b.kind&&a.j==b.j&&a.a==b.a&&a.b==b.b&&a.c==b.c&&a.k==b.k);}
 assert(types[0].size()==47);initialize();
 Z rhs=normq[0]+normq[1]+(Z)outerq[0]*121*107*107*61;
 rhs+=(Z)outerq[1]*2*243*choose2(107)+(Z)outerq[2]*2*81*choose3(107)+(Z)outerq[3]*243*choose2(61)+(Z)outerq[4]*81*choose3(61);assert(rhs==9410019729LL);
 Result result[2];result[0]=run({107,107,61},-1);for(Tri t:types[0]){Result r=run(t,0);result[1].count+=r.count;result[1].maximum=max(result[1].maximum,r.maximum);}
 cout<<"{\"rhs\":"<<(long long)rhs<<",\"upper_rows\":"<<upper<<",\"counts\":[";for(int j=0;j<2;j++)cout<<(j?",":"")<<result[j].count;cout<<"],\"maximum_columns\":[";for(int j=0;j<2;j++){assert(result[j].maximum>=LLONG_MIN&&result[j].maximum<=LLONG_MAX);cout<<(j?",":"")<<(long long)result[j].maximum;}cout<<"]}\n";
}
