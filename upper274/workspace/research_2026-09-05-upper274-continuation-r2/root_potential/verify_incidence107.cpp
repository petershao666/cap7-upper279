#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <limits>
#include <string>
#include <vector>
using I=long long;using W=__int128_t;using T=std::array<int,3>;
T sort(T t){std::sort(t.begin(),t.end(),std::greater<int>());return t;}
I e2(T t){return I(t[0])*t[1]+I(t[0])*t[2]+I(t[1])*t[2];}I e3(T t){return I(t[0])*t[1]*t[2];}
I choose2(I n){return n*(n-1)/2;}I choose3(I n){return n*(n-1)*(n-2)/6;}
bool allowed(T t,const std::vector<T>&b){t=sort(t);for(T s:b)if(t[0]>=s[0]&&t[1]>=s[1]&&t[2]>=s[2])return false;return true;}
std::vector<T> readtypes(){int n;std::cin>>n;std::vector<T>x(n);for(T&t:x)std::cin>>t[0]>>t[1]>>t[2];return x;}
std::string str(W x){if(x==0)return"0";bool neg=x<0;if(neg)x=-x;std::string s;while(x){s+=char('0'+x%10);x/=10;}if(neg)s+='-';std::reverse(s.begin(),s.end());return s;}
struct C{bool set=false;I marg=0;int len=0;I co[7]={};I th=0;};C cc[46][46];I theta[21][21];
bool p5[21][21][21],p6[46][46][46],tp107[46][46],tp275[113][113];W extra[2][46][46];
I q67(T t){return 9*e3(t)-899*e2(t)+15730000;}
W oriented(T a,T b,T c){
 int m[3][3]={{a[0],a[1],a[2]},{b[0],b[1],b[2]},{c[0],c[1],c[2]}};int dirs[4][2]={{1,0},{0,1},{1,1},{1,2}};W total=0;
 for(auto&d:dirs){int ax=d[0],ay=d[1],bx=ax?0:1,by=ax?1:0,R[3][3]={};
  for(int x=0;x<3;x++)for(int y=0;y<3;y++)R[(ax*x+ay*y)%3][(bx*x+by*y)%3]=m[x][y];
  T su;for(int x=0;x<3;x++)su[x]=R[x][0]+R[x][1]+R[x][2];T t=sort(su);C q=cc[t[0]][t[1]];assert(q.set);I f[7]={},F[7]={};
  for(int u=0;u<3;u++)for(int v=0;v<3;v++)f[0]+=I(R[0][u])*R[1][v]*R[2][(6-u-v)%3];F[0]=40*e3(t);
  std::vector<int>vs={t[0],t[1],t[2]};std::sort(vs.begin(),vs.end());vs.erase(std::unique(vs.begin(),vs.end()),vs.end());int k=1;I th=0;int r40=0;
  for(int v:vs){int count=0;for(int x=0;x<3;x++)if(su[x]==v){T z={R[x][0],R[x][1],R[x][2]};f[k]+=e2(z);f[k+1]+=e3(z);count++;if(v==40){z=sort(z);th+=theta[z[0]][z[1]];r40++;}}
   F[k]=count*81*choose2(v);F[k+1]=count*27*choose3(v);k+=2;}
  assert(k==q.len);W val=q.marg;for(int i=0;i<k;i++)val+=W(q.co[i])*(121*f[i]-F[i]);val+=W(q.th)*(121*th-I(r40)*475918720);total+=val;
 }return total;
}
int main(){T base;std::cin>>base[0]>>base[1]>>base[2];I nW,nZ,q[7];std::cin>>nW>>nZ;for(I&v:q)std::cin>>v;auto old=readtypes(),comp=readtypes(),f6=readtypes(),ban=readtypes();
 int nt;std::cin>>nt;std::vector<T>anchors;
 for(int z=0;z<nt;z++){T t;int len;std::cin>>t[0]>>t[1]>>t[2]>>len;C&v=cc[t[0]][t[1]];v.set=true;v.len=len;std::cin>>v.marg;for(int k=0;k<len;k++)std::cin>>v.co[k];std::cin>>v.th;assert(v.th<=0);anchors.push_back(t);}
 I force[7]={121*e3(base),243*choose2(base[0]),81*choose3(base[0]),243*choose2(base[1]),81*choose3(base[1]),243*choose2(base[2]),81*choose3(base[2])};W constant=nW;for(int k=0;k<7;k++)constant-=W(q[k])*force[k];
 int nh;std::cin>>nh;for(int z=0;z<nh;z++){int j,n;I qc,B;std::cin>>j>>qc>>B>>n;assert(qc<=0);constant-=W(qc)*B;for(int k=0;k<n;k++){T t;I v;std::cin>>t[0]>>t[1]>>t[2]>>v;extra[j][t[0]][t[1]]+=W(364)*qc*v;}}
 int nth;std::cin>>nth;for(int z=0;z<nth;z++){int a,b,c;I v;std::cin>>a>>b>>c>>v;theta[a][b]=v;}
 std::vector<T>deltas={{20,16,6},{18,18,6},{18,17,7},{18,12,12},{16,15,11},{16,14,12},{15,15,12},{14,14,14}},bad41={{20,19,2},{20,18,3},{19,19,3},{19,18,4}};
 for(int a=0;a<=20;a++)for(int b=0;b<=20;b++)for(int c=0;c<=20;c++){T t=sort({a,b,c});int s=a+b+c;bool ok=s<=45&&(s<42||(t[0]<=18&&t[1]<=18&&t[2]<=9)||t[0]<=15);if(s==42&&std::find(deltas.begin(),deltas.end(),t)!=deltas.end())ok=true;p5[a][b][c]=ok&&allowed(t,bad41);}
 auto all=old;all.insert(all.end(),comp.begin(),comp.end());
 for(int a=0;a<=45;a++)for(int b=0;b<=45;b++){int c=107-a-b;if(c>=0&&c<=45)tp107[a][b]=allowed({a,b,c},all);}
 I ni=0;W maxi=-((W)1<<120);
 for(T A:anchors){std::vector<T>co[3];for(int j=0;j<3;j++)for(int a=0;a<=20;a++)for(int b=0;b<=20;b++){int c=A[j]-a-b;if(c>=0&&c<=20&&p5[a][b][c])co[j].push_back({a,b,c});}
  for(T a:co[0])for(T b:co[1])for(T c:co[2]){bool ok=true;for(int u=0;u<3&&ok;u++)for(int v=0;v<3;v++)if(!p5[a[u]][b[v]][c[(6-u-v)%3]]){ok=false;break;}if(!ok)continue;
   for(int s=0;s<3;s++){int x=a[0]+b[s]+c[2*s%3],y=a[1]+b[(1+s)%3]+c[(1+2*s)%3];if(x>45||y>45||!tp107[x][y]){ok=false;break;}}if(!ok)continue;W v=nZ+oriented(a,b,c);assert(v<=0);maxi=std::max(maxi,v);ni++;}
 }
 for(int a=0;a<=45;a++)for(int b=0;b<=45;b++)for(int c=0;c<=45;c++){T t=sort({a,b,c});int s=a+b+c;p6[a][b][c]=s<=112&&(s<109||t[2]<=22||(t[0]<=40&&t[1]<=36))&&allowed(t,f6);}
 for(int a=0;a<=112;a++)for(int b=0;b<=112;b++){int c=275-a-b;if(c>=0&&c<=112)tp275[a][b]=allowed({a,b,c},ban)&&q67({a,b,c})>=q67(base);}
 std::vector<T>co[3];for(int j=0;j<3;j++)for(int a=0;a<=45;a++)for(int b=0;b<=45;b++){int c=base[j]-a-b;if(c<0||c>45||!p6[a][b][c])continue;T t={a,b,c};if(j<2&&!allowed(t,comp))continue;co[j].push_back(t);}
 I no=0;W maxo=-((W)1<<120);
 for(T a:co[0])for(T b:co[1])for(T c:co[2]){bool ok=true;I mix=0;for(int u=0;u<3&&ok;u++)for(int v=0;v<3;v++){int w=(6-u-v)%3;if(!p6[a[u]][b[v]][c[w]]){ok=false;break;}mix+=I(a[u])*b[v]*c[w];}if(!ok)continue;
  for(int s=0;s<3;s++){int x=a[0]+b[s]+c[2*s%3],y=a[1]+b[(1+s)%3]+c[(1+2*s)%3];if(x>112||y>112||!tp275[x][y]){ok=false;break;}}if(!ok)continue;
  T as=sort(a),bs=sort(b);assert(cc[as[0]][as[1]].set);I f[7]={mix,e2(a),e3(a),e2(b),e3(b),e2(c),e3(c)};W v=constant+extra[0][as[0]][as[1]]+extra[1][bs[0]][bs[1]]-4*W(cc[as[0]][as[1]].marg);for(int k=0;k<7;k++)v+=W(364)*q[k]*f[k];assert(v<=0);maxo=std::max(maxo,v);no++;
 }
 assert(nW+nZ>0);std::cout<<"{\"status\":\"PASS_ALL_ORDERED_RAW_TABLES\",\"inner_count\":"<<ni<<",\"outer_count\":"<<no<<",\"inner_maximum\":\""<<str(maxi)<<"\",\"outer_maximum\":\""<<str(maxo)<<"\",\"rhs\":"<<nW+nZ<<"}\n";
}
