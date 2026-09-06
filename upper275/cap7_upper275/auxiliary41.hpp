// Independent exact Cartesian-product check of the auxiliary 41-cap bound.
struct Aux41Inner{Triple key;std::vector<I>q;I K,bound,count;std::vector<Triple>absent;};
struct Aux41Cut{std::string id;std::vector<Triple>types;std::vector<I>phi;I bound;std::vector<Aux41Inner>inner;};
struct UpperCutUse{int column;std::string id;};
const std::vector<Triple> EXCLUDED41={{20,19,2},{20,18,3},{19,19,3},{19,18,4}};
std::map<std::string,std::map<Triple,I>> AUXPHI;
std::map<std::string,I> AUXBOUND;
void prove_small_bound(){
 int checked=0;
 for(int mask=0;mask<(1<<9);++mask){int k=0;for(int j=0;j<9;++j)k+=(mask>>j)&1;if(k!=5)continue;
  bool found=false;for(int x=0;x<9;++x)if(mask&(1<<x))for(int y=x+1;y<9;++y)if(mask&(1<<y)){int z=((6-x%3-y%3)%3)+3*((6-x/3-y/3)%3);if(mask&(1<<z))found=true;}
  check(found,"five-point subset of F3^2 contains a line");++checked;
 }
 check(checked==126,"small dimension enumeration");I lo=std::numeric_limits<I>::max();for(auto t:alltypes(10,4))lo=std::min(lo,e2(t));check(13*lo>9*c2(10),"dimension-three bound from pair moments");
}
bool adm4_step(Triple t){if(*std::min_element(t.begin(),t.end())<0||*std::max_element(t.begin(),t.end())>9||tsum(t)>20)return false;t=sort3(t);int a=t[0],b=t[1],c=t[2];if((a==9&&b>=7)||(a==8&&b==8))return c<=2;if((a==9&&b==6)||(a==8&&b==7))return c<=3;if((a==9&&b==5)||(a==7&&b==7))return c<=4;return true;}
I verify_aux41(const Aux41Cut&h){
 std::vector<Triple>T,required;for(auto t:alltypes(41,20))if(std::find(EXCLUDED41.begin(),EXCLUDED41.end(),t)==EXCLUDED41.end()){T.push_back(t);if(t==Triple{20,20,1}||t==Triple{18,18,5}||(t[0]>=17&&t[1]<=17&&t[1]>=16&&t[2]<=16))required.push_back(t);}
 check(T==h.types&&T.size()==h.phi.size(),"41-cap type support");std::map<Triple,I>phi;for(size_t i=0;i<T.size();++i)phi[T[i]]=h.phi[i];std::vector<Triple>anchors;for(auto&r:h.inner)anchors.push_back(r.key);auto tmp=anchors;std::sort(tmp.begin(),tmp.end());check(tmp==required,"41-cap Proposition6.1 coverage");
 Table adm(9);for(int a=0;a<10;++a)for(int b=0;b<10;++b)for(int c=0;c<10;++c)adm.set(a,b,c,adm4_step({a,b,c}));I count=0,bound=std::numeric_limits<I>::min();std::vector<Triple>earlier;
 for(const auto&r:h.inner){check(r.q.size()==7&&(r.absent.empty()||r.absent==earlier),"41-cap coefficient and first-anchor scope");earlier.push_back(r.key);std::vector<I>F{13LL*r.key[0]*r.key[1]*r.key[2],27*c2(r.key[0]),9*c3(r.key[0]),27*c2(r.key[1]),9*c3(r.key[1]),27*c2(r.key[2]),9*c3(r.key[2])};I B=phi.at(r.key)+scalar(r.q,F)-40*r.K;check(B==r.bound,"41-cap summed bound");std::vector<Triple>ban=EXCLUDED41;ban.insert(ban.end(),r.absent.begin(),r.absent.end());auto top=top_table(20,ban,41);I minimum=std::numeric_limits<I>::max();
  I n=enumerate_step(r.key,adm,top,{},Triple{-1,-1,-1},[&](const Triple&a,const Triple&b,const Triple&c,const std::array<Triple,3>&tops){I value=scalar(r.q,features(a,b,c));for(auto t:tops)value-=phi.at(sort3(t));check(value>=r.K,"41-cap exhaustive local inequality");minimum=std::min(minimum,value);});check(n==r.count&&n>0,"41-cap count");count+=n;bound=std::max(bound,B);std::cout<<"AUX41 INNER "<<h.id<<" "<<show(r.key)<<": matrices="<<n<<", minimum="<<minimum<<", K="<<r.K<<", bound="<<B<<"\n";
 }
 check(bound==h.bound,"41-cap bound maximum");AUXPHI[h.id]=phi;AUXBOUND[h.id]=h.bound;std::cout<<"AUX41 PASS "<<h.id<<": bound="<<bound<<", matrices="<<count<<"\n";return count;
}
