#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <unordered_set>
#include <vector>
using U=uint32_t;
int main(int argc,char**argv){assert(argc==4);std::string src7=argv[1],src8=argv[2],dir=argv[3];std::vector<U>seven;std::unordered_set<U>eight;U m;std::ifstream f7(src7),f8(src8);while(f7>>m){assert(__builtin_popcount(m)==7);if(!seven.empty())assert(seven.back()<m);seven.push_back(m);}while(f8>>m){assert(__builtin_popcount(m)==8);assert(eight.insert(m).second);}assert(seven.size()==126360&&eight.size()==63180);
 std::array<int,3>p[27];for(int i=0;i<27;i++)p[i]={i%3,i/3%3,i/9};int third[27][27];for(int a=0;a<27;a++)for(int b=0;b<27;b++)third[a][b]=((6-p[a][0]-p[b][0])%3)+3*((6-p[a][1]-p[b][1])%3)+9*((6-p[a][2]-p[b][2])%3);
 std::map<int,long long>degrees;long long count=0,total=0;std::ofstream witness(dir+"/SEVEN_EXTENSION_WITNESSES_P.txt");
 for(U s:seven){U forbidden=s,left=s;while(left){int a=__builtin_ctz(left);left&=left-1;U more=left;while(more){int b=__builtin_ctz(more);more&=more-1;forbidden|=U(1)<<third[a][b];}}U additions=((U(1)<<27)-1)&~forbidden;assert(additions);int first=__builtin_ctz(additions);witness<<s<<' '<<first<<' '<<(s|(U(1)<<first))<<'\n';int d=__builtin_popcount(additions);degrees[d]++;total+=d;count++;while(additions){int q=__builtin_ctz(additions);additions&=additions-1;assert(eight.count(s|(U(1)<<q)));}}
 assert(count==126360&&total==8LL*63180);std::ofstream out(dir+"/SEVEN_EXTENSION_RESULT.json");out<<"{\"status\":\"EVERY_ACTUAL3D7CAP_EXTENDS_TO8_INDEPENDENT_PASS\",\"seven_caps\":"<<count<<",\"eight_caps\":"<<eight.size()<<",\"all_extension_incidences\":"<<total<<",\"extension_degree_counts\":{";bool first=true;for(auto[d,n]:degrees){if(!first)out<<',';first=false;out<<'\"'<<d<<"\":"<<n;}out<<"},\"catalogue_reenumeration\":false,\"root_extension_witnesses_read\":false}\n";std::cout<<"PASS "<<count<<" seven-caps; "<<total<<" extension incidences\n";for(auto[d,n]:degrees)std::cout<<d<<' '<<n<<'\n';
}
