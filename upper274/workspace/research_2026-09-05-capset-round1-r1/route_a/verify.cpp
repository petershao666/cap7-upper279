#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std; using I=__int128_t; using Tr=array<int,3>;
struct Extra{int col,kind; long long bound; vector<long long> phi;};
Tr order(Tr a){sort(a.begin(),a.end(),greater<int>());return a;}
bool allowed(Tr a,const vector<Tr>& bans){a=order(a);for(auto t:bans)if(a[0]>=t[0]&&a[1]>=t[1]&&a[2]>=t[2])return false;return true;}
bool sub(Tr t){t=order(t);return t[2]<=22||(t[0]<=40&&t[1]<=36);}
long long e2(Tr t){return t[0]*t[1]+t[0]*t[2]+t[1]*t[2];}
long long e3(Tr t){return t[0]*t[1]*t[2];}
long long Q(Tr t){return 9*e3(t)-899*e2(t)+15730000;}
long long bin(int n,int k){long long v=1;for(int j=1;j<=k;++j)v=v*(n-j+1)/j;return v;}
string istr(I a){if(a==0)return "0";bool neg=a<0;if(neg)a=-a;string s;while(a){s+=char('0'+a%10);a/=10;}if(neg)s+='-';reverse(s.begin(),s.end());return s;}
bool adm[46][46][46]; bool tops[113][113];
int main(int argc,char**argv){ifstream in(argv[1]);int nn;in>>nn;vector<Tr> f6(nn);for(auto&t:f6)for(auto&x:t)in>>x;in>>nn;vector<Tr> comp(nn);for(auto&t:comp)for(auto&x:t)in>>x;
for(int a=0;a<=45;a++)for(int b=0;b<=45;b++)for(int c=0;c<=45;c++){Tr t={a,b,c};adm[a][b][c]=(a+b+c<=112)&&(a+b+c<109||sub(t))&&allowed(t,f6);}
in>>nn;long long totalcount=0;int passed=0;
for(int ri=0;ri<nn;ri++){string name;Tr key,status;int ismin,empty,nb,ne,nq;long long K,U,G;in>>name;for(auto&x:key)in>>x;for(auto&x:status)in>>x;in>>ismin>>empty>>K>>U>>G>>nb;vector<Tr>bans(nb);for(auto&t:bans)for(auto&x:t)in>>x;in>>ne;vector<Extra>extras;
for(int i=0;i<ne;i++){Extra e;in>>e.col>>e.kind>>e.bound;assert(0<=e.col&&e.col<=2);if(e.kind==3){e.phi.resize(46*46);for(auto&x:e.phi)in>>x;}extras.push_back(e);}
in>>nq;vector<long long>q(nq);for(auto&x:q)in>>x;
vector<long long> F={121LL*key[0]*key[1]*key[2]};for(int n:key){F.push_back(243*bin(n,2));F.push_back(81*bin(n,3));}for(auto e:extras)F.push_back(e.bound);
if(!empty){assert(q.size()==F.size());I sum=0;for(int j=0;j<nq;j++)sum+=I(q[j])*F[j];assert(sum==U&&I(364)*K-U==G&&G>0);}
for(int j=0;j<3;j++){assert(status[j]>=-1&&status[j]<=1);if(status[j]>=0)assert(key[j]>=103);if(status[j]==0)assert(key[j]<109);}
for(int j=0;j<ne;j++){auto e=extras[j];if(e.kind<3){assert(status[e.col]==1);assert(e.bound==(e.kind==0?56:(e.kind==1?11:110)*(112-key[e.col])));}else assert(status[e.col]==0&&q[7+j]>=0);}
for(int x=0;x<=112;x++)for(int y=0;y<=112;y++){int z=275-x-y;tops[x][y]=z>=0&&z<=112&&allowed({x,y,z},bans)&&(!ismin||Q({x,y,z})>=Q(key));}
vector<Tr> cols[3];for(int j=0;j<3;j++)for(int x=0;x<=45;x++)for(int y=0;y<=45;y++){int z=key[j]-x-y;if(z<0||z>45||(j==0&&!(x>=y&&y>=z)))continue;Tr t={x,y,z};if(!adm[x][y][z]||(status[j]==1&&!sub(t))||(status[j]==0&&!allowed(t,comp)))continue;cols[j].push_back(t);}
long long count=0;I mn=I(1)<<120;
for(auto a:cols[0])for(auto b:cols[1])for(auto c:cols[2]){bool ok=true;for(int i=0;i<3&&ok;i++)for(int j=0;j<3;j++)if(!adm[a[i]][b[j]][c[(6-i-j)%3]]){ok=false;break;}if(!ok)continue;
for(int s=0;s<3;s++){int x=a[0]+b[s]+c[2*s%3],y=a[1]+b[(1+s)%3]+c[(1+2*s)%3];if(x>112||y>112||!tops[x][y]){ok=false;break;}}if(!ok)continue;count++;assert(!empty);
Tr cc[3]={a,b,c};long long T=0;for(int i=0;i<3;i++)for(int j=0;j<3;j++)T+=a[i]*b[j]*c[(6-i-j)%3];I val=I(q[0])*T;for(int j=0;j<3;j++)val+=I(q[1+2*j])*e2(cc[j])+I(q[2+2*j])*e3(cc[j]);
for(int j=0;j<ne;j++){auto e=extras[j];Tr t=cc[e.col],s=order(t);I z=0;if(e.kind==0)z=I(q[7+j])*(s[2]<=22);if(e.kind==1)z=I(q[7+j])*(s[2]<=22?22-s[2]:0);if(e.kind==2&&s[2]>22){z=I(1)<<120;for(int k=0;k<3;k++){if(t[k]>40||t[(k+1)%3]>36||t[(k+2)%3]>36)continue;z=min(z,I(q[7+j])*(40-t[k]));}assert(z!=(I(1)<<120));}if(e.kind==3)z=I(q[7+j])*e.phi[s[0]*46+s[1]];val+=z;}
if(val<K){cerr<<"FAIL "<<name<<" value "<<istr(val)<<" K "<<K<<"\n";return 1;}mn=min(mn,val);
}
assert(empty?count==0:count>0);totalcount+=count;passed++;cout<<"PASS "<<name<<" count="<<count<<" minimum="<<(empty?"empty":istr(mn))<<" K="<<K<<" gap="<<G<<"\n";}
assert(in);cout<<"ALL_PASS certificates="<<passed<<" matrices="<<totalcount<<"\n";
}
