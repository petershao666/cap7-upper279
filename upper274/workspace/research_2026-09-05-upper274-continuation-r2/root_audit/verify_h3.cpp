// Independent full ordered matrix verifier. No discovery headers or kernels.
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>
using namespace std;
using Tri=array<int,3>;using I=__int128_t;using LL=long long;
void ck(bool v,const char*s){if(!v)throw runtime_error(s);}
Tri st(Tri t){sort(t.begin(),t.end(),greater<int>());return t;}
bool dom(Tri t,const vector<Tri>&bs){t=st(t);for(auto b:bs)if(t[0]>=b[0]&&t[1]>=b[1]&&t[2]>=b[2])return true;return false;}
LL cbin(int n,int k){LL z=1;for(int i=1;i<=k;i++)z=z*(n-i+1)/i;return z;}
LL e2(Tri t){return t[0]*t[1]+t[0]*t[2]+t[1]*t[2];}
LL e3(Tri t){return t[0]*t[1]*t[2];}
LL Q(Tri t){return 9*e3(t)-899*e2(t)+15730000;}
bool completed(Tri t){t=st(t);return t[2]<=22||(t[0]<=40&&t[1]<=36);}
string dec(I v){if(v==0)return "0";bool neg=v<0;if(neg)v=-v;string s;while(v){s+=char('0'+v%10);v/=10;}if(neg)s+='-';reverse(s.begin(),s.end());return s;}
struct Hist{int n;LL bound;map<Tri,LL> phi;LL at(Tri t)const {return phi.at(st(t));}};
Hist readhist(){Hist h;int z;cin>>h.n>>h.bound>>z;for(int i=0;i<z;i++){Tri t;LL v;cin>>t[0]>>t[1]>>t[2]>>v;ck(t==st(t),"hist sorting");ck(h.phi.emplace(t,v).second,"duplicate hist key");}return h;}
bool adm4[10][10][10],adm5[21][21][21],adm6[46][46][46];
int main(){
 int no,nc,nu,np,ncase;cin>>no>>nc>>nu>>np>>ncase;vector<Tri>old(no),comp(nc);for(auto&t:old)for(auto&x:t)cin>>x;for(auto&t:comp)for(auto&x:t)cin>>x;
 map<int,vector<Tri>> spec;
 for(int i=0;i<4;i++){int n,k;cin>>n>>k;ck(n==42+i,"spectrum size");for(int j=0;j<k;j++){Tri t;for(auto&v:t)cin>>v;spec[n].push_back(t);}}
 vector<Hist> upper;for(int i=0;i<nu;i++)upper.push_back(readhist());Hist h40=readhist(),h105=readhist();ck(h40.n==40&&h105.n==105,"hist sizes");
 vector<array<int,9>> pats(np);for(auto &p:pats)for(auto&x:p)cin>>x;
 for(int x=0;x<=9;x++)for(int y=0;y<=9;y++)for(int z=0;z<=9;z++){
  Tri t=st({x,y,z});int a=t[0],b=t[1],c=t[2];bool ok=a+b+c<=20;
  if((a==9&&b>=7)||(a==8&&b==8))ok&=c<=2;
  if((a==9&&b==6)||(a==8&&b==7))ok&=c<=3;
  if((a==9&&b==5)||(a==7&&b==7))ok&=c<=4;
  adm4[x][y][z]=ok;
 }
 vector<Tri> excluded5={{20,19,2},{20,18,3},{19,19,3},{19,18,4}};
 for(int x=0;x<=20;x++)for(int y=0;y<=20;y++)for(int z=0;z<=20;z++){
  Tri t=st({x,y,z});int n=x+y+z;bool ok=n<42;
  if(n>=42&&n<=45)ok=find(spec.at(n).begin(),spec.at(n).end(),t)!=spec.at(n).end();
  adm5[x][y][z]=n<=45&&ok&&!dom(t,excluded5);
 }
 vector<Tri>ordinary=old;for(auto t:comp)if(!completed(t))ordinary.push_back(t);
 for(int x=0;x<=45;x++)for(int y=0;y<=45;y++)for(int z=0;z<=45;z++){
  Tri t={x,y,z};int n=x+y+z;adm6[x][y][z]=n<=112&&(n<109||completed(t))&&!dom(t,ordinary);
 }
 LL total=0,can_total=0;
 for(int idx=0;idx<ncase;idx++){
  int n,empty,nb,ne,nq;Tri key;LL expected;cin>>n>>key[0]>>key[1]>>key[2]>>empty>>nb>>ne>>nq>>expected;
  ck(n==40||n==105||n==275,"case size");ck(key==st(key)&&key[0]+key[1]+key[2]==n,"anchor");
  vector<Tri>bad(nb);for(auto&t:bad)for(auto&x:t)cin>>x;
  struct Extra{int col,kind;Tri type;int id;LL forced;};vector<Extra>ext(ne);
  for(auto&e:ext)cin>>e.col>>e.kind>>e.type[0]>>e.type[1]>>e.type[2]>>e.id>>e.forced;
  vector<LL>q(nq);for(auto&v:q)cin>>v;LL K,B,gap;cin>>K>>B>>gap;
  int cap=n==40?9:n==105?20:45,topcap=n==40?20:n==105?45:112,D=n==40?40:n==105?121:364;
  auto admissible=[&](Tri t){if(*min_element(t.begin(),t.end())<0||*max_element(t.begin(),t.end())>cap)return false;return n==40?adm4[t[0]][t[1]][t[2]]:n==105?adm5[t[0]][t[1]][t[2]]:adm6[t[0]][t[1]][t[2]];};
  auto topok=[&](Tri t){return *min_element(t.begin(),t.end())>=0&&*max_element(t.begin(),t.end())<=topcap&&!dom(t,bad)&&(n!=275||Q(t)>=Q(key));};
  I U=0;
  if(!empty){
    ck(nq==7+ne,"features");int fT=n==40?13:n==105?40:121,f2=n==40?27:n==105?81:243,f3=f2/3;
    vector<I>F={I(fT)*key[0]*key[1]*key[2]};for(int N:key){F.push_back(I(f2)*cbin(N,2));F.push_back(I(f3)*cbin(N,3));}
    for(auto&e:ext){ck(e.col>=0&&e.col<3,"extra column");if(e.kind==1){ck(e.id>=0&&e.id<nu&&upper[e.id].n==key[e.col]&&upper[e.id].bound==e.forced,"upper scope");ck(q[F.size()]>=0,"upper sign");}F.push_back(e.forced);}
    for(int i=0;i<nq;i++)U+=I(q[i])*F[i];
    if(n==40)ck(I(h40.at(key))+U-I(D)*K==B&&B<=h40.bound,"40 histogram bound");
    if(n==105){for(int N:key)if(N==40)U+=h40.bound;ck(I(h105.at(key))+U-I(D)*K==B&&B<=h105.bound,"105 histogram bound");}
    if(n==275){U+=I(2)*h105.bound;ck(U==B&&I(D)*K-U==gap&&gap>0,"outer positive gap");}
  }else ck(n==40&&nq==0&&expected==0,"empty scope");
  vector<Tri>cols[3];
  for(int j=0;j<3;j++)for(int a=0;a<=cap;a++)for(int b=0;b<=cap;b++){
    Tri t={a,b,key[j]-a-b};if(!admissible(t)||(j==0&&t!=st(t)))continue;
    if(n==275&&j<2&&dom(t,comp))continue;cols[j].push_back(t);
  }
  LL count=0,canonical=0;I minimum=I(1)<<120;
  for(auto a:cols[0])for(auto b:cols[1])for(auto c:cols[2]){
    bool ok=true;for(int i=0;i<3&&ok;i++)for(int j=0;j<3;j++)if(!admissible({a[i],b[j],c[(6-i-j)%3]})){ok=false;break;}if(!ok)continue;
    array<Tri,3>tops;
    for(int s=0;s<3;s++){Tri t;for(int i=0;i<3;i++)t[i]=a[i]+b[(i+s)%3]+c[(i+2*s)%3];tops[s]=st(t);if(!topok(t)){ok=false;break;}}if(!ok)continue;
    if(n==40){array<int,9>flat;for(int i=0;i<3;i++){flat[3*i]=a[i];flat[3*i+1]=b[i];flat[3*i+2]=c[i];}for(auto&p:pats){bool match=true;for(int j=0;j<9;j++)if(p[j]>=0&&p[j]!=flat[j]){match=false;break;}if(match){ok=false;break;}}if(!ok)continue;}
    ck(!empty,"alleged empty branch has matrix");
    LL T=0;for(int i=0;i<3;i++)for(int j=0;j<3;j++)T+=a[i]*b[j]*c[(6-i-j)%3];
    array<LL,7>f={T,e2(a),e3(a),e2(b),e3(b),e2(c),e3(c)};I value=0;for(int i=0;i<7;i++)value+=I(q[i])*f[i];array<Tri,3>cc={a,b,c};
    for(int j=0;j<ne;j++){auto&e=ext[j];LL v=e.kind==0 ? LL(st(cc[e.col])==e.type) : upper[e.id].at(cc[e.col]);value+=I(q[7+j])*v;}
    if(n==40)for(auto t:tops)value-=h40.at(t);
    if(n==105){for(auto t:tops)value-=h105.at(t);for(int j=0;j<3;j++)if(key[j]==40)value+=h40.at(cc[j]);}
    if(n==275)value+=I(h105.at(a))+h105.at(b);
    if(value<K){cerr<<"FAIL case="<<idx<<" value="<<dec(value)<<" K="<<K<<endl;return 2;}
    minimum=min(minimum,value);count++;
    if(b>=Tri{b[1],b[2],b[0]}&&b>=Tri{b[2],b[0],b[1]})canonical++;
  }
  ck(canonical==expected,"independent canonical count mismatch");ck(empty?count==0:count>0,"nonempty check");
  total+=count;can_total+=canonical;
  cout<<idx<<" N="<<n<<" key="<<key[0]<<","<<key[1]<<","<<key[2]<<" ordered="<<count<<" canonical="<<canonical<<" minimum="<<(empty?"EMPTY":dec(minimum))<<" K="<<K<<" gap="<<gap<<endl;
 }
 ck(cin.good(),"input parse");cout<<"PASS cases="<<ncase<<" full_ordered_matrices="<<total<<" canonical_matrices="<<can_total<<endl;
}
