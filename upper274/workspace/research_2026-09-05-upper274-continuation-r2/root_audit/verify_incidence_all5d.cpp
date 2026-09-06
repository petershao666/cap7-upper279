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
struct Coef{vector<LL>q;LL theta=0;bool has_theta=false;map<int,LL>extra;};
bool ad5[21][21][21],ad6[46][46][46];map<Tri,Coef>coef[1];map<Tri,LL>theta;
struct Low{int n,kind;LL bound;map<Tri,LL>phi;};vector<Low>low;
LL thbound;LL qnorm[2]={},qo[7]={};
struct Hist{int col;LL bound,q;map<Tri,LL>phi;};vector<Hist>hist;
Tri ROOT;vector<LL>outerF(){vector<LL>v={121*e3(ROOT)};for(int n:ROOT){v.push_back(243*choose(n,2));v.push_back(81*choose(n,3));}return v;};
I orient(const Grid&M,int ax,int ay,int bx,int by,int j){
 Grid r={};for(int x=0;x<3;x++)for(int y=0;y<3;y++)r[(ax*x+ay*y)%3][(bx*x+by*y)%3]=M[x][y];
 Tri sums={};for(int x=0;x<3;x++)for(int y=0;y<3;y++)sums[x]+=r[x][y];Tri t=sorted(sums);auto &cf=coef[j].at(t);auto vs=sizes(t);
 LL T=0;for(int x=0;x<3;x++)for(int y=0;y<3;y++)T+=r[0][x]*r[1][y]*r[2][(6-x-y)%3];
 I out=cf.q[0]+I(cf.q[1])*(I(121)*T-I(40)*e3(t));
 for(int i=0;i<(int)vs.size();i++){
  int v=vs[i],mult=0;LL a=0,b=0;for(int x=0;x<3;x++)if(sums[x]==v){mult++;a+=e2(r[x]);b+=e3(r[x]);}
  out+=I(cf.q[2+2*i])*(I(121)*a-I(mult)*81*choose(v,2));out+=I(cf.q[3+2*i])*(I(121)*b-I(mult)*27*choose(v,3));
 }
 for(auto [f,q]:cf.extra){auto &h=low[f];LL value=0;int mult=0;for(int x=0;x<3;x++)if(sums[x]==h.n){value+=h.phi.at(sorted(r[x]));mult++;}out+=I(q)*(I(121)*value-I(h.bound)*mult);}

 return out;
}
I inner_score(const Grid&M,int j){return qnorm[1+j]+orient(M,1,0,0,1,j)+orient(M,0,1,1,0,j)+orient(M,1,1,0,1,j)+orient(M,1,2,0,1,j);}
I outer_score(const Grid&M){LL T=0;for(int i=0;i<3;i++)for(int j=0;j<3;j++)T+=M[0][i]*M[1][j]*M[2][(6-i-j)%3];vector<LL>v={T};for(int j=0;j<3;j++){v.push_back(e2(M[j]));v.push_back(e3(M[j]));}auto F=outerF();
 I out=qnorm[0];for(int i=0;i<7;i++)out+=I(qo[i])*(I(364)*v[i]-F[i]);out-=I(4)*coef[0].at(sorted(M[0])).q[0];
 for(auto&h:hist)out+=I(h.q)*(I(364)*h.phi.at(sorted(M[h.col]))-h.bound);return out;}

int main(){
 int no,nc,nb,nth,nq,nh,nlow;LL claimed;cin>>ROOT[0]>>ROOT[1]>>ROOT[2]>>no>>nc>>nb>>nth>>nq>>nh>>nlow>>claimed;ck((ROOT==Tri{107,106,62})||(ROOT==Tri{106,105,64}),"registered target");vector<Tri>old(no),comp(nc),ban(nb);for(auto&t:old)for(auto&v:t)cin>>v;for(auto&t:comp)for(auto&v:t)cin>>v;for(auto&t:ban)for(auto&v:t)cin>>v;
 map<int,set<Tri>>spec;for(int k=0;k<4;k++){int n,s;cin>>n>>s;ck(n==42+k,"spectrum order");for(int i=0;i<s;i++){Tri t;for(auto&v:t)cin>>v;spec[n].insert(t);}}
 cin>>thbound;ck(thbound==475918720,"centered theta bound");for(int i=0;i<nth;i++){Tri t;LL v;for(auto&x:t)cin>>x;cin>>v;theta[t]=v;}ck(theta.size()==44,"theta support");
 for(int i=0;i<nh;i++){Hist h;int nt;cin>>h.col>>h.bound>>nt;ck(h.col>=0&&h.col<2,"upper histogram column");h.q=0;for(int k=0;k<nt;k++){Tri t;LL v;for(auto&x:t)cin>>x;cin>>v;ck(t[0]+t[1]+t[2]==ROOT[h.col],"histogram dimension");h.phi[t]=v;}hist.push_back(h);}
 for(int i=0;i<nlow;i++){Low h;int nt;cin>>h.n>>h.kind>>h.bound>>nt;ck(h.n>=40&&h.n<=45&&(h.kind==0||h.kind==1),"lowfunctionkind");for(int k=0;k<nt;k++){Tri t;LL v;for(auto&x:t)cin>>x;cin>>v;ck(t[0]+t[1]+t[2]==h.n,"lowfunctiondimension");h.phi[t]=v;}low.push_back(h);}ck(nlow==33,"complete33functioninput");
 vector<Tri>ncban=old;ncban.insert(ncban.end(),comp.begin(),comp.end());
 vector<Tri>types[1];for(int j=0;j<1;j++){int n=ROOT[0];for(int a=0;a<=45;a++)for(int b=0;b<=a;b++){int c=n-a-b;Tri t={a,b,c};if(c<0||c>b||dom(t,ncban))continue;types[j].push_back(t);Coef cf;cf.q.assign(2+2*sizes(t).size(),0);coef[j][t]=cf;}}
 ck(types[0].size()==(ROOT[0]==107?47:79),"full NC supports");
 set<array<int,6>>seen;int upper=0;
 for(int i=0;i<nq;i++){
  LL q;int tag,j,k;Tri t;cin>>q>>tag>>j>>t[0]>>t[1]>>t[2]>>k;ck(seen.insert({tag,j,t[0],t[1],t[2],k}).second,"duplicate row");
  if(tag==0){ck(j==-1&&k==-1,"outer norm row");qnorm[0]=q;}
  else if(tag==1){ck(j==0,"inner norm row");qnorm[j+1]=q;}
  else if(tag==2){ck(j==-1&&k>=0&&k<7,"outer moment row");qo[k]=q;}
  else if(tag==3){ck(j==0,"conditional row slice");auto&cf=coef[j].at(t);ck(k>=0&&k<(int)cf.q.size(),"conditional feature index");cf.q[k]=q;}
  else if(tag==5){ck(j==-1&&k>=0&&k<nh&&q<=0,"outer upper sign");hist[k].q=q;upper++;}
  else{ck(tag==4&&j==0&&k>=0&&k<nlow,"lowfunctionrow");auto &h=low[k];ck(find(t.begin(),t.end(),h.n)!=t.end(),"lowfunctionrowdimensions");if(h.kind==0){ck(q<=0,"conditionalupper sign");upper++;}coef[0].at(t).extra[k]=q;}
 }
 int expected=9+nh,expectedupper=nh;for(auto t:types[0]){expected+=coef[0][t].q.size();for(int f=0;f<nlow;f++)if(find(t.begin(),t.end(),low[f].n)!=t.end()){expected++;ck(coef[0][t].extra.count(f),"allconditionalfunctionrowscovered");if(low[f].kind==0)expectedupper++;}}
 ck(nq==expected&&upper==expectedupper,"allmathematicalrowsandsignscovered");

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
 I rhs=I(qnorm[0])+qnorm[1];Tri key=ROOT;ck(rhs==claimed&&rhs>0,"positive exact Farkas RHS");
 LL count=0;I maximum=-(I(1)<<120);for(auto t:types[0]){auto [n,mx]=enumerate(t,false,0);count+=n;maximum=max(maximum,mx);}ck(count==(ROOT[0]==107?1407366:4220643),"complete inner count");cout<<"INNER N="<<ROOT[0]<<" tables="<<count<<" maximum="<<dec(maximum)<<endl;
 auto [outcount,outmax]=enumerate(key,true,-1);ck(outcount>0,"nonempty complete outer domain");
 cout<<"OUTER tables="<<outcount<<" maximum="<<dec(outmax)<<endl;
 cout<<"PASS exact_rhs="<<dec(rhs)<<" all_mathematical_tables="<<count+outcount<<" upper_slack_signs="<<upper<<endl;
}
