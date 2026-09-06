// Symmetric107 audit adapted from root independent incidence kernel.
// Z is the average of the two actual107 line distributions; no cap-isomorphism hypothesis.
// No discovery code, cached matrices, or quotient feature records are read.
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <vector>
using namespace std;using Tri=array<int,3>;using Grid=array<Tri,3>;using LL=long long;using I=__int128_t;
void ck(bool v,const char*s){if(!v)throw runtime_error(s);}
Tri sorted(Tri t){sort(t.begin(),t.end(),greater<int>());return t;}
LL e2(Tri t){return t[0]*t[1]+t[0]*t[2]+t[1]*t[2];}
LL e3(Tri t){return t[0]*t[1]*t[2];}
LL choose(int n,int k){LL v=1;for(int i=1;i<=k;i++)v=v*(n-i+1)/i;return v;}
bool dom(Tri t,const vector<Tri>&bad){t=sorted(t);for(auto s:bad)if(t[0]>=s[0]&&t[1]>=s[1]&&t[2]>=s[2])return true;return false;}
bool completion(Tri t){t=sorted(t);return t[2]<=22||(t[0]<=40&&t[1]<=36);}
LL Q(Tri t){return 9*e3(t)-899*e2(t)+15730000;}
string dec(I x){if(!x)return "0";bool neg=x<0;if(neg)x=-x;string s;while(x){s+=char('0'+x%10);x/=10;}if(neg)s+='-';reverse(s.begin(),s.end());return s;}
vector<int> sizes(Tri t){vector<int>v(t.begin(),t.end());sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());return v;}
struct Coef{vector<LL>q;LL theta=0;bool has_theta=false;};
bool ad5[21][21][21],ad6[46][46][46];map<Tri,Coef>coef[1];map<Tri,LL>theta;
LL thbound;LL qnorm[2]={},qo[5]={};
I orient(const Grid&M,int ax,int ay,int bx,int by,int j){
 Grid r={};for(int x=0;x<3;x++)for(int y=0;y<3;y++)r[(ax*x+ay*y)%3][(bx*x+by*y)%3]=M[x][y];
 Tri sums={};for(int x=0;x<3;x++)for(int y=0;y<3;y++)sums[x]+=r[x][y];Tri t=sorted(sums);auto &cf=coef[j].at(t);auto vs=sizes(t);
 LL T=0;for(int x=0;x<3;x++)for(int y=0;y<3;y++)T+=r[0][x]*r[1][y]*r[2][(6-x-y)%3];
 I out=cf.q[0]+I(cf.q[1])*(I(121)*T-I(40)*e3(t));
 for(int i=0;i<(int)vs.size();i++){
  int v=vs[i],mult=0;LL a=0,b=0;for(int x=0;x<3;x++)if(sums[x]==v){mult++;a+=e2(r[x]);b+=e3(r[x]);}
  out+=I(cf.q[2+2*i])*(I(121)*a-I(mult)*81*choose(v,2));out+=I(cf.q[3+2*i])*(I(121)*b-I(mult)*27*choose(v,3));
 }
 if(cf.has_theta){LL value=0;int mult=0;for(int x=0;x<3;x++)if(sums[x]==40){value+=theta.at(sorted(r[x]));mult++;}out+=I(cf.theta)*(I(121)*value-I(thbound)*mult);}
 return out;
}
I inner_score(const Grid&M,int j){return qnorm[1+j]+orient(M,1,0,0,1,j)+orient(M,0,1,1,0,j)+orient(M,1,1,0,1,j)+orient(M,1,2,0,1,j);}
I outer_score(const Grid&M){LL T=0;for(int i=0;i<3;i++)for(int j=0;j<3;j++)T+=M[0][i]*M[1][j]*M[2][(6-i-j)%3];
 I out=qnorm[0]+I(364)*(I(qo[0])*T+I(qo[1])*(e2(M[0])+e2(M[1]))+I(qo[2])*(e3(M[0])+e3(M[1]))+I(qo[3])*e2(M[2])+I(qo[4])*e3(M[2]));
 for(int j=0;j<2;j++)out-=I(2)*coef[0].at(sorted(M[j])).q[0];return out;}

int main(){
 int no,nc,nb,nth,nq;LL claimed;cin>>no>>nc>>nb>>nth>>nq>>claimed;vector<Tri>old(no),comp(nc),ban(nb);for(auto&t:old)for(auto&v:t)cin>>v;for(auto&t:comp)for(auto&v:t)cin>>v;for(auto&t:ban)for(auto&v:t)cin>>v;
 map<int,set<Tri>>spec;for(int k=0;k<4;k++){int n,s;cin>>n>>s;ck(n==42+k,"spectrum order");for(int i=0;i<s;i++){Tri t;for(auto&v:t)cin>>v;spec[n].insert(t);}}
 cin>>thbound;ck(thbound==475918720,"centered theta bound");for(int i=0;i<nth;i++){Tri t;LL v;for(auto&x:t)cin>>x;cin>>v;theta[t]=v;}ck(theta.size()==44,"theta support");
 vector<Tri>ncban=old;ncban.insert(ncban.end(),comp.begin(),comp.end());
 vector<Tri>types[1];for(int j=0;j<1;j++){int n=107;for(int a=0;a<=45;a++)for(int b=0;b<=a;b++){int c=n-a-b;Tri t={a,b,c};if(c<0||c>b||dom(t,ncban))continue;types[j].push_back(t);Coef cf;cf.q.assign(2+2*sizes(t).size(),0);coef[j][t]=cf;}}
 ck(types[0].size()==47,"full NC supports");
 set<array<int,6>>seen;int upper=0;
 for(int i=0;i<nq;i++){
  LL q;int tag,j,k;Tri t;cin>>q>>tag>>j>>t[0]>>t[1]>>t[2]>>k;ck(seen.insert({tag,j,t[0],t[1],t[2],k}).second,"duplicate row");
  if(tag==0){ck(j==-1&&k==-1,"outer norm row");qnorm[0]=q;}
  else if(tag==1){ck(j==0,"inner norm row");qnorm[j+1]=q;}
  else if(tag==2){ck(j==-1&&k>=0&&k<5,"outer moment row");qo[k]=q;}
  else if(tag==3){ck(j==0,"conditional row slice");auto&cf=coef[j].at(t);ck(k>=0&&k<(int)cf.q.size(),"conditional feature index");cf.q[k]=q;}
  else{ck(tag==4&&(j==0)&&k==-1&&find(t.begin(),t.end(),40)!=t.end()&&q<=0,"theta inequality sign/scope");auto&cf=coef[j].at(t);cf.theta=q;cf.has_theta=true;upper++;}
 }
 int expected=7;for(int j=0;j<1;j++)for(auto t:types[j]){expected+=coef[j][t].q.size();if(find(t.begin(),t.end(),40)!=t.end()){expected++;ck(coef[j][t].has_theta,"theta row coverage");}}
 ck(expected==375&&nq==expected&&upper==12,"all mathematical rows covered");
 vector<Tri>ex5={{20,19,2},{20,18,3},{19,19,3},{19,18,4}};
 for(int a=0;a<=20;a++)for(int b=0;b<=20;b++)for(int c=0;c<=20;c++){int n=a+b+c;Tri t={a,b,c};ad5[a][b][c]=n<=45&&(n<42||spec[n].count(sorted(t)))&&!dom(t,ex5);}
 vector<Tri>f6=old;for(auto t:comp)if(!completion(t))f6.push_back(t);
 for(int a=0;a<=45;a++)for(int b=0;b<=45;b++)for(int c=0;c<=45;c++){int n=a+b+c;Tri t={a,b,c};ad6[a][b][c]=n<=112&&(n<109||completion(t))&&!dom(t,f6);}
 auto enumerate=[&](Tri key,bool outer,int jj)->pair<LL,I>{
  int u=outer?45:20,v=outer?112:45;vector<Tri>cols[3];int total=key[0]+key[1]+key[2];
  auto admissible=[&](Tri t){if(*min_element(t.begin(),t.end())<0||*max_element(t.begin(),t.end())>u)return false;return outer?ad6[t[0]][t[1]][t[2]]:ad5[t[0]][t[1]][t[2]];};
  for(int j=0;j<3;j++)for(int a=0;a<=u;a++)for(int b=0;b<=u;b++){Tri t={a,b,key[j]-a-b};if(!admissible(t)||(j==0&&t!=sorted(t)))continue;if(outer&&j<2&&dom(t,comp))continue;cols[j].push_back(t);}
  bool top[113][113]={};for(int a=0;a<=v;a++)for(int b=0;b<=v;b++){int c=total-a-b;if(c<0||c>v)continue;Tri t={a,b,c};top[a][b]=outer?(!dom(t,ban)&&Q(t)>=Q(key)):!dom(t,ncban);}
  LL count=0;I mx=-(I(1)<<120);
  for(auto a:cols[0])for(auto b:cols[1])for(auto c:cols[2]){
   bool ok=true;for(int i=0;i<3&&ok;i++)for(int j=0;j<3;j++)if(!admissible({a[i],b[j],c[(6-i-j)%3]})){ok=false;break;}if(!ok)continue;
   for(int s=0;s<3;s++){int x=a[0]+b[s]+c[2*s%3],y=a[1]+b[(1+s)%3]+c[(1+2*s)%3];if(x>v||y>v||!top[x][y]){ok=false;break;}}if(!ok)continue;
   Grid M={a,b,c};I value=outer?outer_score(M):inner_score(M,jj);if(value>0){cerr<<"COUNTEREXAMPLE value="<<dec(value)<<" key="<<key[0]<<","<<key[1]<<","<<key[2]<<endl;throw runtime_error("positive Farkas column");}mx=max(mx,value);count++;
  }
  return {count,mx};
 };
 I rhs=I(qnorm[0])+qnorm[1];Tri key={107,107,61};vector<LL>F={121*e3(key),2*243*choose(107,2),2*81*choose(107,3),243*choose(61,2),81*choose(61,3)};for(int i=0;i<5;i++)rhs+=I(qo[i])*F[i];ck(rhs==claimed&&rhs>0,"positive exact Farkas RHS");
 LL count=0;I maximum=-(I(1)<<120);for(auto t:types[0]){auto [n,mx]=enumerate(t,false,0);count+=n;maximum=max(maximum,mx);}ck(count==1407366,"complete inner count");cout<<"INNER N=107 tables="<<count<<" maximum="<<dec(maximum)<<endl;
 auto [outcount,outmax]=enumerate(key,true,-1);ck(outcount==3772668,"complete outer count");
 cout<<"OUTER tables="<<outcount<<" maximum="<<dec(outmax)<<endl;
 cout<<"PASS exact_rhs="<<dec(rhs)<<" all_mathematical_tables="<<count+outcount<<" upper_slack_signs="<<upper<<endl;
}
