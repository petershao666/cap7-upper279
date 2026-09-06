#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <limits>
#include <vector>
using I=long long; using T=std::array<int,3>; using W=__int128_t;
T sorted(T x){std::sort(x.begin(),x.end(),std::greater<int>());return x;}
bool dominates(T x,T y){x=sorted(x);return x[0]>=y[0]&&x[1]>=y[1]&&x[2]>=y[2];}
bool permitted(T x,const std::vector<T>&b){for(T t:b)if(dominates(x,t))return false;return true;}
I e2(T t){return I(t[0])*t[1]+I(t[0])*t[2]+I(t[1])*t[2];}
I e3(T t){return I(t[0])*t[1]*t[2];}
I q67(T t){return 9*e3(t)-899*e2(t)+15730000;}
std::vector<T> readtypes(){int n;std::cin>>n;std::vector<T>v(n);for(auto&t:v)std::cin>>t[0]>>t[1]>>t[2];return v;}
bool adm[46][46][46],top[113][113];I ph[46][46],h106[46][46];
int main(){
 T base;std::cin>>base[0]>>base[1]>>base[2];I co[7],qh,K,U,gap;for(I &v:co)std::cin>>v;std::cin>>qh>>K>>U>>gap;
 auto f6=readtypes(),comp=readtypes(),ban=readtypes();
 const I absent=std::numeric_limits<I>::min();for(int a=0;a<46;a++)for(int b=0;b<46;b++)ph[a][b]=h106[a][b]=absent;
 for(int z=0;z<2;z++){int n;std::cin>>n;for(int k=0;k<n;k++){int a,b,c;I v;std::cin>>a>>b>>c>>v;(z?h106:ph)[a][b]=v;}}
 for(int a=0;a<=45;a++)for(int b=0;b<=45;b++)for(int c=0;c<=45;c++){
  T t=sorted({a,b,c});int s=a+b+c;adm[a][b][c]=s<=112&&(s<109||t[2]<=22||(t[0]<=40&&t[1]<=36))&&permitted(t,f6);
 }
 for(int a=0;a<=112;a++)for(int b=0;b<=112;b++){int c=275-a-b;if(c<0||c>112)continue;T t={a,b,c};top[a][b]=permitted(t,ban)&&q67(t)>=q67(base);}
 std::vector<T>col[3];
 for(int j=0;j<3;j++)for(int a=0;a<=45;a++)for(int b=0;b<=45;b++){
  int c=base[j]-a-b;if(c<0||c>45||!adm[a][b][c])continue;T t={a,b,c};if(j<2&&!permitted(t,comp))continue;col[j].push_back(t);
 }
 I count=0,mini=std::numeric_limits<I>::max();
 for(T a:col[0])for(T b:col[1])for(T c:col[2]){
  bool ok=true;I Tval=0;
  for(int u=0;u<3&&ok;u++)for(int v=0;v<3;v++){int w=(6-u-v)%3;if(!adm[a[u]][b[v]][c[w]]){ok=false;break;}Tval+=I(a[u])*b[v]*c[w];}
  if(!ok)continue;
  for(int s=0;s<3;s++){int x=a[0]+b[s]+c[2*s%3],y=a[1]+b[(1+s)%3]+c[(1+2*s)%3];if(x>112||y>112||!top[x][y]){ok=false;break;}}
  if(!ok)continue;T as=sorted(a),bs=sorted(b);I pv=ph[as[0]][as[1]],hv=h106[bs[0]][bs[1]];assert(pv!=absent&&hv!=absent);
  I f[7]={Tval,e2(a),e3(a),e2(b),e3(b),e2(c),e3(c)};W val=pv+W(qh)*hv;for(int i=0;i<7;i++)val+=W(co[i])*f[i];assert(val>=K&&val>=std::numeric_limits<I>::min()&&val<=std::numeric_limits<I>::max());mini=std::min(mini,I(val));count++;
 }
 assert(mini==K&&W(364)*K-U==gap&&gap>0);
 std::cout<<"{\"status\":\"PASS_ROUTE_SIDE_OUTER_ALL_ORDERED\",\"full_ordered_matrices\":"<<count<<",\"minimum\":"<<mini<<",\"forced\":"<<U<<",\"gap\":"<<gap<<"}\n";
}
