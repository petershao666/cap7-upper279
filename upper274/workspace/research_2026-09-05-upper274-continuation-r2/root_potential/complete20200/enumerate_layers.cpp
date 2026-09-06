#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using M=__uint128_t;
using Triple=std::array<int,3>;
std::array<int,4> xyz[81];std::array<int,5> xyz5[243];
int third[243][243],residue[81][81],profile_id[21][21][21];
M readmask(const std::string&s){assert(s.size()==21);M m=0;for(char c:s){assert(('0'<=c&&c<='9')||('a'<=c&&c<='f'));m=(m<<4)+(c<='9'?c-'0':c-'a'+10);}assert((m>>81)==0);return m;}
std::string hex(M m){std::string s(21,'0');for(int i=20;i>=0;i--){s[i]="0123456789abcdef"[unsigned(m&15)];m>>=4;}assert(m==0);return s;}
std::vector<int> indices(M m){std::vector<int> v;for(int i=0;i<81;i++)if((m>>i)&1)v.push_back(i);return v;}
void sort3(Triple&t){if(t[0]<t[1])std::swap(t[0],t[1]);if(t[1]<t[2])std::swap(t[1],t[2]);if(t[0]<t[1])std::swap(t[0],t[1]);}
void jsonints(std::ostream&o,const std::vector<int>&v){o<<'[';for(size_t i=0;i<v.size();i++){if(i)o<<',';o<<v[i];}o<<']';}
int main(int argc,char**argv){assert(argc==3);std::string input=argv[1],dir=argv[2];auto start=std::chrono::steady_clock::now();
 for(int i=0;i<81;i++){int n=i;for(int k=0;k<4;k++){xyz[i][k]=n%3;n/=3;}}
 for(int i=0;i<243;i++){int n=i;for(int k=0;k<5;k++){xyz5[i][k]=n%3;n/=3;}}
 for(int i=0;i<243;i++)for(int j=0;j<243;j++){int t=0,pow=1;for(int k=0;k<5;k++){t+=((6-xyz5[i][k]-xyz5[j][k])%3)*pow;pow*=3;}third[i][j]=t;}
 for(int d=0;d<81;d++)for(int x=0;x<81;x++){int value=0;for(int k=0;k<4;k++)value+=xyz[d][k]*xyz[x][k];residue[d][x]=value%3;}
 std::vector<int> normals;for(int d=1;d<81;d++){int first=0;for(int k=0;k<4;k++)if(xyz[d][k]){first=xyz[d][k];break;}if(first==1)normals.push_back(d);}assert(normals.size()==40);
 M A=0;for(int i=1;i<81;i++)if((xyz[i][0]*xyz[i][0]+xyz[i][1]*xyz[i][1]+xyz[i][2]*xyz[i][3])%3==0)A|=M(1)<<i;auto av=indices(A);assert(av.size()==20);
 for(size_t i=0;i<av.size();i++)for(size_t j=0;j<i;j++)assert(!((A>>(third[3*av[i]][3*av[j]]/3))&1));
 std::array<Triple,40> acounts;for(int j=0;j<40;j++){acounts[j]={0,0,0};for(int a:av)acounts[j][residue[normals[j]][a]]++;}
 for(int a=0;a<=20;a++)for(int b=0;b<=20;b++)for(int c=0;c<=20;c++)profile_id[a][b][c]=-1;
 std::vector<Triple> types;for(int a=0;a<=20;a++)for(int b=0;b<=a;b++){int c=40-a-b;if(0<=c&&c<=b){profile_id[a][b][c]=types.size();types.push_back({a,b,c});}}
 struct Item{long long count=0;M firstB=0;int temporary_id=-1;};std::map<std::vector<int>,Item> families;std::vector<int> assignments;assignments.reserve(700000);
 std::ifstream in(input);std::string line;M previous=0;long long total=0,pairs=0,direction_evals=0;int next_id=0;
 while(in>>line){M B=readmask(line);assert(total==0||previous<B);previous=B;auto bv=indices(B);assert(bv.size()==20);std::vector<int> cap;cap.reserve(40);for(int a:av)cap.push_back(3*a);for(int b:bv)cap.push_back(3*b+1);bool hits[243]={};for(int p:cap){assert(!hits[p]);hits[p]=true;}
  for(int i=0;i<40;i++)for(int j=0;j<i;j++){assert(!hits[third[cap[i]][cap[j]]]);pairs++;}
  std::vector<int> hist(types.size(),0);hist[profile_id[20][20][0]]++;
  for(int j=0;j<40;j++){Triple bcounts={0,0,0};int d=normals[j];for(int b:bv)bcounts[residue[d][b]]++;for(int e=0;e<3;e++){Triple t;for(int s=0;s<3;s++)t[s]=acounts[j][s]+bcounts[(s-e+3)%3];sort3(t);assert(t[0]<=20&&profile_id[t[0]][t[1]][t[2]]>=0);hist[profile_id[t[0]][t[1]][t[2]]]++;}}
  long long sum=0,e2=0,e3=0;for(size_t j=0;j<types.size();j++){auto[a,b,c]=types[j];sum+=hist[j];e2+=hist[j]*(a*b+a*c+b*c);e3+=hist[j]*a*b*c;}assert(sum==121&&e2==63180&&e3==266760);
  auto &entry=families[hist];if(entry.count==0){entry.temporary_id=next_id++;entry.firstB=B;}entry.count++;assignments.push_back(entry.temporary_id);total++;direction_evals+=121;
  if(total%10000==0&&std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>280)throw std::runtime_error("280-second finite stop");
 }
 assert(in.eof());assert(total==682344);assert(pairs==780*total);std::vector<int> final_id(next_id);int id=0;for(auto &[hist,e]:families)final_id[e.temporary_id]=id++;
 std::ofstream assignout(dir+"/B_HISTOGRAM_IDS.txt");for(int old:assignments)assignout<<final_id[old]<<'\n';assignout.close();
 std::ofstream out(dir+"/HISTOGRAMS.json");out<<"{\n\"status\":\"COMPLETE20200_ACTUAL_FAMILY_FROZEN\",\n\"scope\":\"All 40-caps in AG(5,3) admitting a (20,20,0) direction, up to affine coverage only\",\n\"encoding\":\"4D i=x0+3*x1+9*x2+27*x3; 5D j=t+3*i; coordinates [t,x0,x1,x2,x3]\",\n\"source_catalogue_sha256\":\"66946f5ef9ea1e10164a5b3e56cf89dede2b85efc50d8a8eb1e392e5862d2f41\",\n\"canonical_A_mask\":\""<<hex(A)<<"\",\n\"types\":[";for(size_t j=0;j<types.size();j++){if(j)out<<',';auto[a,b,c]=types[j];out<<'['<<a<<','<<b<<','<<c<<']';}out<<"],\n\"histograms\":[\n";bool first=true;id=0;
 for(auto &[hist,e]:families){if(!first)out<<",\n";first=false;std::vector<int> cap;for(int a:av)cap.push_back(3*a);for(int b:indices(e.firstB))cap.push_back(3*b+1);std::sort(cap.begin(),cap.end());out<<"{\"id\":"<<id++<<",\"counts\":";jsonints(out,hist);out<<",\"normalized_B_frequency\":"<<e.count<<",\"B_mask\":\""<<hex(e.firstB)<<"\",\"point_indices\":";jsonints(out,cap);out<<",\"points\":[";for(size_t k=0;k<cap.size();k++){if(k)out<<',';out<<'[';for(int z=0;z<5;z++){if(z)out<<',';out<<xyz5[cap[k]][z];}out<<']';}out<<"]}";}out<<"\n]}\n";out.close();
 std::ofstream result(dir+"/RESULT.json");result<<"{\n\"status\":\"COMPLETE20200_ACTUAL_FAMILY_ENUMERATION_PASS\",\n\"all_catalogue_choices\":"<<total<<",\n\"distinct_histograms\":"<<families.size()<<",\n\"histogram_count_is_affine_class_count\":false,\n\"canonical_pair_checks\":190,\n\"all_lifted_pair_checks\":"<<pairs<<",\n\"all_direction_profiles_counted\":"<<direction_evals<<",\n\"normal_count_4D\":40,\n\"transverse_coefficients_per_normal\":3,\n\"third_layer_empty\":true,\n\"disjointness_filter_applied\":false,\n\"quadratic_catalogue_reenumerated\":false,\n\"root40_output_read_before_freeze\":false,\n\"worker_count\":1,\n\"LP_run\":false,\n\"wall_seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"\n}\n";
 std::cout<<"PASS B "<<total<<" histograms "<<families.size()<<" pairs "<<pairs<<" directions "<<direction_evals<<'\n';
}
