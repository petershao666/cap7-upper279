#include <algorithm>
#include <array>
#include <cassert>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;using I=__int128_t;using Tr=array<int,3>;
Tr order(Tr t){sort(t.begin(),t.end(),greater<int>());return t;}
bool allowed(Tr t,const vector<Tr>&b){t=order(t);for(auto s:b)if(t[0]>=s[0]&&t[1]>=s[1]&&t[2]>=s[2])return false;return true;}
long long E2(Tr t){return t[0]*t[1]+t[0]*t[2]+t[1]*t[2];}long long E3(Tr t){return t[0]*t[1]*t[2];}
long long cb(int n,int k){long long v=1;for(int j=1;j<=k;j++)v=v*(n-j+1)/j;return v;}long long pw(int n){long long x=1;while(n--)x*=3;return x;}
long long Q(Tr t){return 9*E3(t)-899*E2(t)+15730000;}
bool sub(Tr t){t=order(t);return t[2]<=22||(t[0]<=40&&t[1]<=36);}
string str(I x){if(!x)return "0";bool neg=x<0;if(neg)x=-x;string s;while(x){s+=char('0'+x%10);x/=10;}if(neg)s+='-';reverse(s.begin(),s.end());return s;}
vector<Tr>F6,COMP;vector<array<int,9>>patterns;
bool adm4(Tr t){t=order(t);int a=t[0],b=t[1],c=t[2];if(c<0||a>9||a+b+c>20)return false;if((a==9&&b>=7)||(a==8&&b==8))return c<=2;if((a==9&&b==6)||(a==8&&b==7))return c<=3;if((a==9&&b==5)||(a==7&&b==7))return c<=4;return true;}
bool adm5(Tr t){t=order(t);int a=t[0],b=t[1],c=t[2],s=a+b+c;if(c<0||a>20||s>45)return false;vector<Tr>bad={{20,19,2},{20,18,3},{19,19,3},{19,18,4}};if(!allowed(t,bad))return false;if(s<42)return true;if((a<=18&&b<=18&&c<=9)||a<=15)return true;vector<Tr>d={{20,16,6},{18,18,6},{18,17,7},{18,12,12},{16,15,11},{16,14,12},{15,15,12},{14,14,14}};return s==42&&find(d.begin(),d.end(),t)!=d.end();}
bool adm6(Tr t){int s=t[0]+t[1]+t[2];return *min_element(t.begin(),t.end())>=0&&*max_element(t.begin(),t.end())<=45&&s<=112&&(s<109||sub(t))&&allowed(t,F6);}
bool clash(Tr a,Tr b,Tr c){array<int,9>x={a[0],b[0],c[0],a[1],b[1],c[1],a[2],b[2],c[2]};for(auto p:patterns){bool ok=true;for(int i=0;i<9;i++)if(p[i]>=0&&x[i]!=p[i]){ok=false;break;}if(ok)return true;}return false;}
struct Fun{int col;long long q,bound;vector<long long>tab;int sign;};
int main(int argc,char**argv){ifstream in(argv[1]);int nn;in>>nn;F6.resize(nn);for(auto&t:F6)for(auto&x:t)in>>x;in>>nn;COMP.resize(nn);for(auto&t:COMP)for(auto&x:t)in>>x;in>>nn;patterns.resize(nn);for(auto&p:patterns)for(auto&x:p)in>>x;assert(patterns.size()==2664);in>>nn;long long total=0;
for(int z=0;z<nn;z++){string name;int n,ism,empty,nb,nx,target;Tr key;long long K,U,B;in>>name>>n;for(auto&x:key)in>>x;in>>ism>>empty>>K>>U>>B>>nb;vector<Tr>ban(nb);for(auto&t:ban)for(auto&x:t)in>>x;array<long long,7>q;for(auto&x:q)in>>x;in>>nx;vector<Fun>fs(nx);for(auto&f:fs){in>>f.col>>f.q>>f.bound>>f.sign;assert(f.sign==0||f.q>=0);f.tab.resize(46*46);for(auto&x:f.tab)in>>x;}in>>target;vector<long long>phi(113*113);if(target)for(auto&x:phi)in>>x;
long long D=(pw(n-1)-1)/2;vector<long long>F={(pw(n-2)-1)/2*key[0]*key[1]*key[2]};for(int m:key){F.push_back(pw(n-2)*cb(m,2));F.push_back(pw(n-3)*cb(m,3));}I forced=0;for(int j=0;j<7;j++)forced+=I(q[j])*F[j];for(auto f:fs)forced+=I(f.q)*f.bound;
if(!empty){assert(forced==U);if(target){assert(I(phi[key[0]*113+key[1]])+forced-D*I(K)==B);}else assert(D*I(K)-forced==B&&B>0);}
int up=n==5?9:n==6?20:45,topup=n==5?20:n==6?45:112,s=key[0]+key[1]+key[2];vector<bool>adm(46*46*46,false);auto idx=[](int a,int b,int c){return(a*46+b)*46+c;};for(int a=0;a<=up;a++)for(int b=0;b<=up;b++)for(int c=0;c<=up;c++)adm[idx(a,b,c)]=n==5?adm4({a,b,c}):n==6?adm5({a,b,c}):adm6({a,b,c});
vector<Tr>cols[3];for(int j=0;j<3;j++)for(int a=0;a<=up;a++)for(int b=0;b<=up;b++){int c=key[j]-a-b;if(c<0||c>up||(j==0&&!(a>=b&&b>=c))||!adm[idx(a,b,c)])continue;Tr t={a,b,c};if(n==7&&j<2&&!allowed(t,COMP))continue;cols[j].push_back(t);}
vector<bool>top(113*113,false);for(int a=0;a<=topup;a++)for(int b=0;b<=topup;b++){int c=s-a-b;if(c<0||c>topup)continue;Tr t={a,b,c};top[a*113+b]=allowed(t,ban)&&(!ism||Q(t)>=Q(key));}
long long count=0,preclash=0;I mn=I(1)<<120;
for(auto a:cols[0])for(auto b:cols[1])for(auto c:cols[2]){bool ok=true;for(int i=0;i<3&&ok;i++)for(int j=0;j<3;j++)if(!adm[idx(a[i],b[j],c[(6-i-j)%3])]){ok=false;break;}if(!ok)continue;Tr ts[3];for(int v=0;v<3;v++){for(int r=0;r<3;r++)ts[v][r]=a[r]+b[(r+v)%3]+c[(r+2*v)%3];if(ts[v][0]>topup||ts[v][1]>topup||!top[ts[v][0]*113+ts[v][1]]){ok=false;break;}}if(!ok)continue;preclash++;if(n==5&&clash(a,b,c))continue;count++;assert(!empty);Tr cc[3]={a,b,c};long long T=0;for(int i=0;i<3;i++)for(int j=0;j<3;j++)T+=a[i]*b[j]*c[(6-i-j)%3];I val=I(q[0])*T;for(int j=0;j<3;j++)val+=I(q[1+2*j])*E2(cc[j])+I(q[2+2*j])*E3(cc[j]);for(auto f:fs){Tr t=order(cc[f.col]);val+=I(f.q)*f.tab[t[0]*46+t[1]];}if(target)for(auto t:ts){t=order(t);val-=phi[t[0]*113+t[1]];}if(val<K){cerr<<"FAIL "<<name<<" value="<<str(val)<<" K="<<K<<"\n";return 1;}mn=min(mn,val);}
assert(empty?count==0:count>0);total+=count;cout<<"PASS "<<name<<" preclash="<<preclash<<" count="<<count<<" min="<<(empty?"empty":str(mn))<<" K="<<K<<" bound_or_gap="<<B<<"\n";
}
assert(in);cout<<"ALL_PASS cases="<<nn<<" matrices="<<total<<"\n";}
