// Audit implementation: input parsed from user Markdown. Does not include original code/data header.
// Enumerates ALL ordered first columns, independently of the symmetry quotient.
#include <algorithm>
#include <array>
#include <cassert>
#include <climits>
#include <iostream>
#include <map>
#include <vector>
using Z=long long; using V=std::array<int,3>;
V order(V t){if(t[0]<t[1])std::swap(t[0],t[1]);if(t[1]<t[2])std::swap(t[1],t[2]);if(t[0]<t[1])std::swap(t[0],t[1]);return t;}
Z two(V t){return Z(t[0])*t[1]+Z(t[1])*t[2]+Z(t[2])*t[0];}
Z three(V t){return Z(t[0])*t[1]*t[2];}
struct Grid{
 int b;std::vector<unsigned char>a;
 Grid(int bound):b(bound+1),a(b*b*b,0){}
 int idx(V t)const{return (t[0]*b+t[1])*b+t[2];}
 bool get(V t)const{return t[0]>=0&&t[1]>=0&&t[2]>=0&&t[0]<b&&t[1]<b&&t[2]<b&&a[idx(t)];}
 void put(V t,bool v){a[idx(t)]=v;}
};
struct Cert{int n,s;V t;std::array<Z,7>q;Z K,U,gap,count,minimum;std::array<std::map<V,Z>,3>phi;};
Grid excluded(int bound,const std::vector<V>&keys){
 Grid out(bound);
 for(auto t:keys){std::sort(t.begin(),t.end());do{out.put(t,true);}while(std::next_permutation(t.begin(),t.end()));}
 // Upward closure, using three-dimensional cumulative OR, no sorted-key lookup kernel.
 for(int x=0;x<=bound;++x)for(int y=0;y<=bound;++y)for(int z=0;z<=bound;++z){V t{x,y,z};bool e=out.get(t);for(int j=0;j<3;++j){V prev=t;--prev[j];e=e||out.get(prev);}out.put(t,e);}
 return out;
}
std::vector<V> family(int total,const Grid&g){std::vector<V>v;for(int x=0;x<g.b;++x)for(int y=0;y<g.b;++y){V t{x,y,total-x-y};if(g.get(t))v.push_back(t);}return v;}
int main(){
 std::map<int,std::vector<V>>support;
 for(int j=0;j<4;++j){int n,k;std::cin>>n>>k;for(int l=0;l<k;++l){V t;for(int&x:t)std::cin>>x;support[n].push_back(t);}}
 int N;std::cin>>N;assert(N==155);std::vector<Cert> certs(N);
 for(auto&r:certs){std::cin>>r.n>>r.s;for(int&x:r.t)std::cin>>x;for(Z&x:r.q)std::cin>>x;std::cin>>r.K>>r.U>>r.gap>>r.count>>r.minimum;for(auto&p:r.phi){int k;std::cin>>k;for(int j=0;j<k;++j){V t;Z v;for(int&x:t)std::cin>>x;std::cin>>v;p[t]=v;}}assert(std::cin&&r.t==order(r.t));}
 Grid adm5(20);
 for(int x=0;x<=20;++x)for(int y=0;y<=20;++y)for(int z=0;z<=20;++z){int n=x+y+z;V t=order({x,y,z});bool ok=n<42;if(n>=42&&n<=45)ok=std::find(support[n].begin(),support[n].end(),t)!=support[n].end();adm5.put({x,y,z},ok);}
 std::vector<V>six,seven;Z totalCanonical=0,totalFull=0;int done=0;
 for(int dimension:{6,7}){
  Grid adm=adm5;
  if(dimension==7){adm=Grid(45);auto bad=excluded(45,six);for(int x=0;x<=45;++x)for(int y=0;y<=45;++y)for(int z=0;z<=45;++z){V t{x,y,z},u=order(t);int n=x+y+z;bool ok=n<=112;
    if(n>=110)ok=ok&&((u[0]<=45&&u[1]<=45&&u[2]<=22)||(u[0]<=40&&u[1]<=36&&u[2]<=36));adm.put(t,ok&&!bad.get(t));}}
  auto&proved=dimension==6?six:seven;int limit=dimension==6?45:112;
  for(int st=0;st<=(dimension==6?7:4);++st){
   const auto previous=excluded(limit,proved); // Frozen until the stage is complete.
   for(const auto&r:certs)if(r.n==dimension&&r.s==st){
    auto aa=family(r.t[0],adm),bb=family(r.t[1],adm),cc=family(r.t[2],adm);
    std::array<std::vector<Z>,3>cv;int col=0;
    for(const auto*familyPtr:{&aa,&bb,&cc}){for(V t:*familyPtr){Z f=r.q[1+2*col]*two(t)+r.q[2+2*col]*three(t);auto it=r.phi[col].find(order(t));if(it!=r.phi[col].end())f+=it->second;cv[col].push_back(f);}++col;}
    Z full=0,canonical=0,minimum=LLONG_MAX,canonicalMin=LLONG_MAX;V witness[3]{};
    for(size_t ia=0;ia<aa.size();++ia)for(size_t ib=0;ib<bb.size();++ib){auto a=aa[ia],b=bb[ib];
     // For each gamma coordinate, intersect its three transverse constraints directly.
     bool allowed[3][46]{};
     for(int k=0;k<3;++k)for(int v=0;v<adm.b;++v){bool ok=true;for(int i=0;i<3;++i){int j=(6-i-k)%3;ok=ok&&adm.get({a[i],b[j],v});}allowed[k][v]=ok;}
     for(size_t ic=0;ic<cc.size();++ic){auto c=cc[ic];if(!allowed[0][c[0]]||!allowed[1][c[1]]||!allowed[2][c[2]])continue;
      bool ok=true;for(int slope=0;slope<3;++slope){V sums{};for(int i=0;i<3;++i)sums[i]=a[i]+b[(i+slope)%3]+c[(i+2*slope)%3];if(sums[0]>limit||sums[1]>limit||sums[2]>limit||previous.get(sums)){ok=false;break;}}if(!ok)continue;
      Z T=0;for(int i=0;i<3;++i)for(int j=0;j<3;++j)T+=Z(a[i])*b[j]*c[(6-i-j)%3];
      Z value=r.q[0]*T+cv[0][ia]+cv[1][ib]+cv[2][ic];assert(value>=r.K);++full;
      if(value<minimum){minimum=value;witness[0]=a;witness[1]=b;witness[2]=c;}
      if(a==order(a)){++canonical;canonicalMin=std::min(canonicalMin,value);}
     }
    }
    assert(canonical==r.count&&minimum==r.minimum&&canonicalMin==minimum);
    assert((dimension==6?121:364)*r.K-r.U==r.gap&&r.gap>0);
    std::cout<<dimension<<' '<<st<<' '<<r.t[0]<<' '<<r.t[1]<<' '<<r.t[2]<<" canonical="<<canonical<<" full="<<full<<" min="<<minimum<<" witness=";
    for(auto t:witness)std::cout<<'['<<t[0]<<','<<t[1]<<','<<t[2]<<']';std::cout<<std::endl;
    totalCanonical+=canonical;totalFull+=full;++done;
   }
   for(const auto&r:certs)if(r.n==dimension&&r.s==st)proved.push_back(r.t);
  }
 }
 auto bad=excluded(112,seven);int excludedN=0,remaining=0;Z minRoot=LLONG_MAX;
 for(int a=0;a<=112;++a)for(int b=0;b<=a;++b){int c=280-a-b;if(c<0||c>b)continue;V t{a,b,c};if(bad.get(t)){++excludedN;continue;}Z value=6*three(t)-613*two(t)+11141493;assert(value>=0);minRoot=std::min(minRoot,value);++remaining;}
 Z C2=280LL*279/2,C3=280LL*279*278/6;Z root=6*243*C3-613*729*C2+11141493LL*1093;
 assert(root==-45291&&remaining==232&&excludedN==58&&done==155&&totalCanonical==55253413);
 std::cout<<"PASS cases="<<done<<" canonical="<<totalCanonical<<" full="<<totalFull<<" root_remaining="<<remaining<<" excluded="<<excludedN<<" min_root="<<minRoot<<" root_sum="<<root<<std::endl;
}
