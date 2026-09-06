// Independent full Cartesian matrix audit. No predecessor code is included.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
#include <stdexcept>
#include <limits>
using namespace std;using Tri=array<int,3>;using I=__int128_t;
void require(bool v,const char*s){if(!v)throw runtime_error(s);}
Tri sortt(Tri t){sort(t.begin(),t.end(),greater<int>());return t;}
bool dominates(Tri t,const vector<Tri>& bad){t=sortt(t);for(auto z:bad)if(t[0]>=z[0]&&t[1]>=z[1]&&t[2]>=z[2])return true;return false;}
bool completed(Tri t){t=sortt(t);return t[2]<=22||(t[0]<=40&&t[1]<=36);}
long long e2(Tri t){return t[0]*t[1]+t[0]*t[2]+t[1]*t[2];}
long long e3(Tri t){return t[0]*t[1]*t[2];}
long long choose(int n,int k){long long z=1;for(int i=1;i<=k;i++)z=z*(n-i+1)/i;return z;}
long long Q(Tri t){return 9*e3(t)-899*e2(t)+15730000;}
bool adm[46][46][46];
struct Hist {int size;long long bound;long long phi[46][46];bool valid[46][46];};
int main(){
 int no,nc,nh,ncases;cin>>no>>nc>>nh>>ncases;vector<Tri> old(no),comp(nc);for(auto &t:old)for(auto &x:t)cin>>x;for(auto&t:comp)for(auto&x:t)cin>>x;
 vector<Hist> hs(nh);for(auto &h:hs){int n;cin>>h.size>>h.bound>>n;for(auto &r:h.valid)for(auto &v:r)v=false;for(int j=0;j<n;j++){Tri t;long long val;cin>>t[0]>>t[1]>>t[2]>>val;require(t==sortt(t),"hist order");h.phi[t[0]][t[1]]=val;h.valid[t[0]][t[1]]=true;}}
 vector<Tri> unconditional=old;for(auto t:comp)if(!completed(t))unconditional.push_back(t);
 for(int a=0;a<=45;a++)for(int b=0;b<=45;b++)for(int c=0;c<=45;c++){Tri t={a,b,c};adm[a][b][c]=(a+b+c<=112)&&(a+b+c<109||completed(t))&&!dominates(t,unconditional);}
 long long grand=0;
 for(int idx=0;idx<ncases;idx++){
   Tri key,state;int mincase,empty,nb,ne,nq;cin>>key[0]>>key[1]>>key[2]>>mincase>>state[0]>>state[1]>>state[2]>>empty>>nb>>ne>>nq;
   vector<Tri> banned(nb);for(auto&t:banned)for(auto&x:t)cin>>x;
   vector<pair<int,int>>extra(ne);for(auto&[j,n]:extra)cin>>j>>n;
   vector<long long>q(nq);for(auto&v:q)cin>>v;long long K,forced,gap;cin>>K>>forced>>gap;
   require(key[0]+key[1]+key[2]==275&&key==sortt(key),"target");
   vector<I> sums={I(121)*key[0]*key[1]*key[2]};for(int N:key){sums.push_back(I(243)*choose(N,2));sums.push_back(I(81)*choose(N,3));}
   for(int j=0;j<3;j++){require(state[j]>=-1&&state[j]<=1,"state");if(state[j]>=0)require(key[j]>=103&&key[j]<=112&&(state[j]!=0||key[j]<109),"status scope");}
   for(auto[j,n]:extra){require(j>=0&&j<3,"extra column");if(n<0){require(state[j]==1,"completed feature");int d=112-key[j];sums.push_back(n==-1?56:n==-2?11*d:110*d);}else{require(n<nh&&state[j]==0&&hs[n].size==key[j],"hist scope");sums.push_back(hs[n].bound);require(q.at(sums.size()-1)>=0,"hist sign");}}
   if(!empty){require(q.size()==sums.size(),"feature count");I U=0;for(size_t j=0;j<q.size();j++)U+=I(q[j])*sums[j];require(U==forced&&I(364)*K-U==gap&&gap>0,"forced gap");}
   vector<Tri> cols[3];for(int j=0;j<3;j++)for(int a=0;a<=45;a++)for(int b=0;b<=45;b++){int c=key[j]-a-b;if(c<0||c>45||!adm[a][b][c])continue;Tri t={a,b,c};if(j==0&&t!=sortt(t))continue;if(state[j]==1&&!completed(t))continue;if(state[j]==0&&dominates(t,comp))continue;cols[j].push_back(t);}
   bool tops[113][113]={};for(int a=0;a<=112;a++)for(int b=0;b<=112;b++){int c=275-a-b;if(c<0||c>112)continue;Tri t={a,b,c};tops[a][b]=!dominates(t,banned)&&(!mincase||Q(t)>=Q(key));}
   long long count=0;I minimum=I(1)<<120;
   for(auto a:cols[0])for(auto b:cols[1])for(auto c:cols[2]){
      bool ok=true;
      // All nine affine transversals, then all three whole-cap profiles.
      for(int r=0;r<3&&ok;r++)for(int s=0;s<3;s++)if(!adm[a[r]][b[(r+s)%3]][c[(r+2*s)%3]]){ok=false;break;}
      if(!ok)continue;
      for(int s=0;s<3;s++){int x=a[0]+b[s]+c[(2*s)%3];int y=a[1]+b[(1+s)%3]+c[(1+2*s)%3];if(x>112||y>112||!tops[x][y]){ok=false;break;}}
      if(!ok)continue;require(!empty,"false empty certificate");
      long long T=0;for(int i=0;i<3;i++)for(int j=0;j<3;j++)T+=a[i]*b[j]*c[(6-i-j)%3];
      array<long long,7>f={T,e2(a),e3(a),e2(b),e3(b),e2(c),e3(c)};I value=0;for(int j=0;j<7;j++)value+=I(q[j])*f[j];array<Tri,3> cc={a,b,c};
      for(int j=0;j<ne;j++){auto[col,n]=extra[j];auto t=sortt(cc[col]);long long v=0,coeff=q[7+j];if(n==-1)v=t[2]<=22;else if(n==-2)v=t[2]<=22?22-t[2]:0;else if(n==-3){
        if(t[2]<=22)v=0;else{bool have=false;I best=I(1)<<120;for(int k=0;k<3;k++){bool fit=true;for(int l=0;l<3;l++)if(t[l]>(l==k?40:36))fit=false;if(fit){I z=I(coeff)*(40-t[k]);if(!have||z<best){have=true;best=z;}}}require(have,"completed label coverage");value+=best;continue;}
      }else{require(hs[n].valid[t[0]][t[1]],"hist support");v=hs[n].phi[t[0]][t[1]];}value+=I(coeff)*v;}
      require(value>=K,"inequality counterexample");minimum=min(minimum,value);count++;
   }
   require(empty?count==0:count>0,"nonempty requirement");require(minimum>=numeric_limits<long long>::min()&&(empty||minimum<=numeric_limits<long long>::max()),"output integer range");
   grand+=count;cout<<idx<<" "<<key[0]<<","<<key[1]<<","<<key[2]<<" mincase="<<mincase<<" state="<<state[0]<<","<<state[1]<<","<<state[2]<<" count="<<count<<" minimum="<<(empty?0:(long long)minimum)<<" gap="<<gap<<endl;
 }
 cout<<"PASS independent Cartesian audit cases="<<ncases<<" matrices="<<grand<<endl;
}
