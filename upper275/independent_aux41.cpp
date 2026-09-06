// Audit implementation: no includes from the supplied certificate package.
// Enumerates all ordered first columns as well as a sorted subset for comparison.
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <vector>
#include <limits>
#include <stdexcept>
using T=std::array<int,3>; using Z=long long;
void need(bool v){if(!v)throw std::runtime_error("audit check failed");}
T ordered(T t){std::sort(t.rbegin(),t.rend());return t;}
Z p2(T t){Z a=0;for(int i=0;i<3;++i)for(int j=i+1;j<3;++j)a+=t[i]*t[j];return a;}
Z p3(T t){return Z(t[0])*t[1]*t[2];}
bool possible(T t){
 t=ordered(t); if(t[2]<0||t[0]>9||t[0]+t[1]+t[2]>20)return false;
 if(t[0]==9&&t[1]>=7&&t[2]>=3)return false;
 if(t[0]==8&&t[1]==8&&t[2]>=3)return false;
 if(((t[0]==9&&t[1]==6)||(t[0]==8&&t[1]==7))&&t[2]>=4)return false;
 if(((t[0]==9&&t[1]==5)||(t[0]==7&&t[1]==7))&&t[2]>=5)return false;
 return true;
}
T get(){T t;for(int&v:t)std::cin>>v;return t;}
int main(){
 int nh;std::cin>>nh;Z grand=0,canonical=0;
 for(int h=0;h<nh;++h){std::string id;int nt,nr;Z B;std::cin>>id>>nt>>nr>>B;
  std::map<T,Z> phi;for(int i=0;i<nt;++i){T t=get();Z v;std::cin>>v;phi[t]=v;}
  Z bestbound=std::numeric_limits<Z>::min();
  for(int r=0;r<nr;++r){T key=get();std::array<Z,7> q;for(Z&v:q)std::cin>>v;
   Z K,bound,nclaimed;int nabs;std::cin>>K>>bound>>nclaimed>>nabs;
   auto allowed=phi;for(int i=0;i<nabs;++i)allowed.erase(get());
   std::array<std::vector<T>,3> cs;
   for(int j=0;j<3;++j)for(int a=0;a<10;++a)for(int b=0;b<10;++b){T t{a,b,key[j]-a-b};if(possible(t))cs[j].push_back(t);}
   Z n=0,ncanonical=0,low=std::numeric_limits<Z>::max();
   for(T a:cs[0])for(T b:cs[1])for(T c:cs[2]){
    std::array<T,3> columns{a,b,c};Z cross=0,subtract=0;bool ok=true;
    for(int slope=0;slope<3&&ok;++slope){T sections{};
     for(int intercept=0;intercept<3;++intercept){T line{};
      for(int x=0;x<3;++x)line[x]=columns[x][(slope*x+intercept)%3];
      if(!possible(line)){ok=false;break;}
      cross+=p3(line);sections[intercept]=line[0]+line[1]+line[2];
     }
     if(ok){auto it=allowed.find(ordered(sections));if(it==allowed.end())ok=false;else subtract+=it->second;}
    }
    if(!ok)continue;
    Z value=q[0]*cross-subtract;
    for(int j=0;j<3;++j)value+=q[2*j+1]*p2(columns[j])+q[2*j+2]*p3(columns[j]);
    need(value>=K);low=std::min(low,value);++n;if(a==ordered(a))++ncanonical;
   }
   need(n>0&&ncanonical==nclaimed);
   Z U=q[0]*13*p3(key);
   for(int j=0;j<3;++j){Z s=key[j];U+=q[2*j+1]*27*s*(s-1)/2+q[2*j+2]*9*s*(s-1)*(s-2)/6;}
   need(phi.at(key)+U-40*K==bound);bestbound=std::max(bestbound,bound);
   std::cout<<id<<" ("<<key[0]<<","<<key[1]<<","<<key[2]<<") ordered="<<n<<" sorted="<<ncanonical<<" min="<<low<<" K="<<K<<" bound="<<bound<<"\n";
   grand+=n;canonical+=ncanonical;
  }need(bestbound==B);
 }
 need(bool(std::cin));std::cout<<"INDEPENDENT AUX41 PASS: ordered="<<grand<<" sorted="<<canonical<<"\n";
}
