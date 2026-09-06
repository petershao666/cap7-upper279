// Root full raw integer grids. No discovery header, generator or cache imported.
#include <algorithm>
#include <array>
#include <chrono>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>
using namespace std;using Tri=array<int,3>;using LL=long long;using I=__int128_t;
void ck(bool v,const char*s){if(!v)throw runtime_error(s);}
Tri sorted(Tri t){sort(t.begin(),t.end(),greater<int>());return t;}
bool dom(Tri t,const vector<Tri>&bs){t=sorted(t);for(auto b:bs)if(t[0]>=b[0]&&t[1]>=b[1]&&t[2]>=b[2])return true;return false;}
LL choose(int n,int k){LL v=1;for(int i=1;i<=k;i++)v=v*(n-i+1)/i;return v;}
LL e2(Tri t){return t[0]*t[1]+t[0]*t[2]+t[1]*t[2];}
LL Q(Tri t){return 9LL*t[0]*t[1]*t[2]-899*e2(t)+15730000;}
bool completion(Tri t){t=sorted(t);return t[2]<=22||(t[0]<=40&&t[1]<=36);}
string str(I v){if(!v)return "0";bool neg=v<0;if(neg)v=-v;string s;while(v){s+=char('0'+v%10);v/=10;}if(neg)s+='-';reverse(s.begin(),s.end());return s;}
struct Fn{int n;LL bound;map<Tri,LL>phi;LL at(Tri t)const{return phi.at(sorted(t));}};
bool a4[10][10][10],a6[46][46][46];
int main(){try{
 auto start=chrono::steady_clock::now();int no,nc,nf,np,ncase,main40;cin>>no>>nc>>nf>>np>>ncase>>main40;
 vector<Tri>old(no),comp(nc);for(auto&t:old)for(int&v:t)cin>>v;for(auto&t:comp)for(int&v:t)cin>>v;
 for(int n=42;n<=45;n++){int nn,k;cin>>nn>>k;ck(nn==n,"size metadata");for(int i=0;i<k;i++){Tri t;for(int&v:t)cin>>v;}}
 vector<Fn>f(nf);for(auto &z:f){int k;cin>>z.n>>z.bound>>k;for(int i=0;i<k;i++){Tri t;LL v;cin>>t[0]>>t[1]>>t[2]>>v;ck(t==sorted(t),"function sorting");ck(z.phi.emplace(t,v).second,"duplicate type");ck(v<100000000000000000LL&&v>-100000000000000000LL,"coefficient magnitude");}}
 ck(main40>=0&&main40<nf&&f[main40].n==40,"main40");int n18;cin>>n18;vector<Tri>t18(n18);for(auto&t:t18)for(int&v:t)cin>>v;
 vector<array<int,9>>patterns(np);for(auto&p:patterns)for(int&v:p)cin>>v;
 for(int x=0;x<=9;x++)for(int y=0;y<=9;y++)for(int z=0;z<=9;z++){
  auto t=sorted({x,y,z});auto[a,b,c]=t;bool ok=a+b+c<=20;
  if((a==9&&b>=7)||(a==8&&b==8))ok&=c<=2;
  if((a==9&&b==6)||(a==8&&b==7))ok&=c<=3;
  if((a==9&&b==5)||(a==7&&b==7))ok&=c<=4;
  a4[x][y][z]=ok;
 }
 auto ordinary=old;for(auto t:comp)if(!completion(t))ordinary.push_back(t);
 for(int x=0;x<=45;x++)for(int y=0;y<=45;y++)for(int z=0;z<=45;z++)a6[x][y][z]=x+y+z<=112&&(x+y+z<109||completion({x,y,z}))&&!dom({x,y,z},ordinary);
 long long total=0,can_total=0;I highest40=-(I(1)<<120);
 for(int ci=0;ci<ncase;ci++){
  int n,empty,nb,ne,nt,nq;Tri key;LL expected,tb;cin>>n>>key[0]>>key[1]>>key[2]>>empty>>nb>>ne>>nt>>nq>>expected>>tb;
  ck(n==40||n==275,"layer");ck(key==sorted(key)&&key[0]+key[1]+key[2]==n,"anchor");
  vector<Tri>bad(nb);for(auto&t:bad)for(int&v:t)cin>>v;
  struct Extra{int col,kind;Tri type;int id;LL forced;};vector<Extra>ext(ne);
  for(auto&e:ext)cin>>e.col>>e.kind>>e.type[0]>>e.type[1]>>e.type[2]>>e.id>>e.forced;
  vector<pair<int,int>>terms(nt);for(auto &[j,id]:terms)cin>>j>>id;
  vector<LL>q(nq);for(LL&v:q){cin>>v;ck(v<100000000000000000LL&&v>-100000000000000000LL,"q magnitude");}
  LL K,B,gap;cin>>K>>B>>gap;int cap=n==40?9:45,D=n==40?40:364;
  I U=tb;
  if(!empty){
   ck(nq==7+ne,"feature count");int fT=n==40?13:121,f2=n==40?27:243,f3=f2/3;
   vector<I>F={I(fT)*key[0]*key[1]*key[2]};for(int v:key){F.push_back(I(f2)*choose(v,2));F.push_back(I(f3)*choose(v,3));}
   for(int j=0;j<ne;j++){auto e=ext[j];ck(e.col>=0&&e.col<3,"column");if(e.kind!=0)ck(q[7+j]>=0,"upper sign");if(e.kind==1)ck(e.id>=0&&e.id<nf&&f[e.id].n==key[e.col]&&f[e.id].bound==e.forced,"fixed function scope/bound");F.push_back(e.forced);}
   for(int j=0;j<nq;j++)U+=I(q[j])*F[j];
   for(auto [j,id]:terms)ck(j>=0&&j<3&&id>=0&&id<nf&&f[id].n==key[j],"term scope");
   if(n==40){I b=f[main40].at(key)+U-I(D)*K;ck(b==B&&b<=f[main40].bound,"40 summed bound");highest40=max(highest40,b);}
   else ck(U==B&&I(D)*K-U==gap&&gap>0,"positive outer gap");
  }else ck(n==40&&nq==0&&expected==0,"empty metadata");
  auto adm=[&](Tri t){if(*min_element(t.begin(),t.end())<0||*max_element(t.begin(),t.end())>cap)return false;return n==40?a4[t[0]][t[1]][t[2]]:a6[t[0]][t[1]][t[2]];};
  auto topok=[&](Tri t){return *min_element(t.begin(),t.end())>=0&&*max_element(t.begin(),t.end())<=(n==40?20:112)&&!dom(t,bad)&&(n!=275||Q(t)>=Q(key));};
  vector<Tri>cols[3];for(int j=0;j<3;j++)for(int a=0;a<=cap;a++)for(int b=0;b<=cap;b++){
   Tri t={a,b,key[j]-a-b};if(!adm(t)||(j==0&&t!=sorted(t)))continue;
   if(n==275&&j<2&&dom(t,comp))continue;
   if(n==40&&key[j]==18&&find(t18.begin(),t18.end(),sorted(t))==t18.end())continue;
   cols[j].push_back(t);
  }
  LL count=0,canonical=0;I minimum=I(1)<<120;
  for(auto a:cols[0])for(auto b:cols[1])for(auto c:cols[2]){
   bool ok=true;for(int i=0;i<3&&ok;i++)for(int j=0;j<3;j++)if(!adm({a[i],b[j],c[(6-i-j)%3]})){ok=false;break;}if(!ok)continue;
   array<Tri,3>tops;for(int s=0;s<3;s++){Tri t;for(int i=0;i<3;i++)t[i]=a[i]+b[(i+s)%3]+c[(i+2*s)%3];tops[s]=sorted(t);if(!topok(t)){ok=false;break;}}if(!ok)continue;
   if(n==40){array<int,9>x;for(int i=0;i<3;i++){x[3*i]=a[i];x[3*i+1]=b[i];x[3*i+2]=c[i];}for(auto p:patterns){bool match=true;for(int j=0;j<9;j++)if(p[j]>=0&&p[j]!=x[j]){match=false;break;}if(match){ok=false;break;}}if(!ok)continue;}
   ck(!empty,"nonempty allegedly empty case");LL T=0;for(int i=0;i<3;i++)for(int j=0;j<3;j++)T+=a[i]*b[j]*c[(6-i-j)%3];
   array<LL,7>mom={T,e2(a),LL(a[0])*a[1]*a[2],e2(b),LL(b[0])*b[1]*b[2],e2(c),LL(c[0])*c[1]*c[2]};I value=0;for(int j=0;j<7;j++)value+=I(q[j])*mom[j];array<Tri,3>cc={a,b,c};
   for(int j=0;j<ne;j++){auto e=ext[j];auto t=sorted(cc[e.col]);LL v=0;if(e.kind==0)v=t==e.type;else if(e.kind==1)v=f[e.id].at(t);else{ck(e.kind==2,"extra kind");v=-(t==Tri{9,8,0}||t==Tri{9,7,1}||t==Tri{8,8,1});}value+=I(q[7+j])*v;}
   for(auto [j,id]:terms)value+=f[id].at(cc[j]);if(n==40)for(auto t:tops)value-=f[main40].at(t);
   if(value<K){cerr<<"FAIL case="<<ci<<" value="<<str(value)<<" K="<<K<<" grid=";for(auto t:cc)for(int v:t)cerr<<v<<',';cerr<<endl;return 2;}
   minimum=min(minimum,value);count++;if(b>=Tri{b[1],b[2],b[0]}&&b>=Tri{b[2],b[0],b[1]})canonical++;
  }
  ck(canonical==expected,"canonical domain count mismatch");ck(empty?count==0:count>0,"domain empty status");
  total+=count;can_total+=canonical;
  cout<<"CASE "<<ci<<" N "<<n<<" anchor "<<key[0]<<","<<key[1]<<","<<key[2]<<" raw "<<count<<" canonical "<<canonical<<" min "<<(empty?"EMPTY":str(minimum))<<" K "<<K<<" bound "<<B<<" gap "<<gap<<endl;
  ck(chrono::duration<double>(chrono::steady_clock::now()-start).count()<600,"600second finite bound");
 }
 ck(highest40==f[main40].bound,"max40 equality");ck(cin.good(),"input parse");cout<<"PASS cases "<<ncase<<" raw "<<total<<" canonical "<<can_total<<" seconds "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
}catch(const exception&e){cerr<<"CHECK_FAILURE "<<e.what()<<endl;return 1;}}
