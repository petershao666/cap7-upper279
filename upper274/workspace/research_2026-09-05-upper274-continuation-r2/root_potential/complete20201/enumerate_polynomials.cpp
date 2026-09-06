#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using Mask=__uint128_t;
using P4=std::array<int,4>;
using P5=std::array<int,5>;
using Profile=std::array<int,3>;
static P4 p4[81]; static P5 p5[243];
static int third4[81][81], plus4[81][81], third5[243][243], dots[243][243];
std::string hexmask(Mask m){std::string s(21,'0');for(int i=20;i>=0;i--){s[i]="0123456789abcdef"[unsigned(m&15)];m>>=4;}assert(m==0);return s;}
std::vector<int> points(Mask m){std::vector<int> r;for(int i=0;i<81;i++)if((m>>i)&1)r.push_back(i);return r;}
bool iscap4(Mask m){auto p=points(m);for(unsigned i=0;i<p.size();i++)for(unsigned j=0;j<i;j++)if((m>>third4[p[i]][p[j]])&1)return false;return true;}
void checkcap5(const std::vector<int>& p){bool hit[243]={};for(int x:p){assert(!hit[x]);hit[x]=true;}assert(p.size()==41);for(unsigned i=0;i<p.size();i++)for(unsigned j=0;j<i;j++)assert(!hit[third5[p[i]][p[j]]]);}
void jsonints(std::ostream&o,const std::vector<int>&v){o<<'[';for(unsigned i=0;i<v.size();i++){if(i)o<<',';o<<v[i];}o<<']';}
void jsonp4(std::ostream&o,const std::vector<int>&v){o<<'[';for(unsigned i=0;i<v.size();i++){if(i)o<<',';o<<'[';for(int k=0;k<4;k++){if(k)o<<',';o<<p4[v[i]][k];}o<<']';}o<<']';}
void jsonp5(std::ostream&o,const std::vector<int>&v){o<<'[';for(unsigned i=0;i<v.size();i++){if(i)o<<',';o<<'[';for(int k=0;k<5;k++){if(k)o<<',';o<<p5[v[i]][k];}o<<']';}o<<']';}
int main(int argc,char**argv){
 assert(argc==2);std::string dir=argv[1];auto start=std::chrono::steady_clock::now();
 auto guard=[&](){if(std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>580)throw std::runtime_error("bounded enumeration stop");};
 for(int i=0;i<81;i++){int v=i;for(int k=0;k<4;k++){p4[i][k]=v%3;v/=3;}}
 for(int i=0;i<243;i++){int v=i;for(int k=0;k<5;k++){p5[i][k]=v%3;v/=3;}}
 for(int i=0;i<81;i++)for(int j=0;j<81;j++){int plus=0,third=0,pow=1;for(int k=0;k<4;k++){plus+=pow*((p4[i][k]+p4[j][k])%3);third+=pow*((6-p4[i][k]-p4[j][k])%3);pow*=3;}plus4[i][j]=plus;third4[i][j]=third;}
 for(int i=0;i<243;i++)for(int j=0;j<243;j++){int third=0,pow=1,dot=0;for(int k=0;k<5;k++){third+=pow*((6-p5[i][k]-p5[j][k])%3);pow*=3;dot+=p5[i][k]*p5[j][k];}third5[i][j]=third;dots[i][j]=dot%3;}
 int monomials[81][10];for(int i=0;i<81;i++){int j=0;for(int k=0;k<4;k++)monomials[i][j++]=p4[i][k]*p4[i][k]%3;for(int k=0;k<4;k++)for(int l=k+1;l<4;l++)monomials[i][j++]=p4[i][k]*p4[i][l]%3;assert(j==10);}
 Mask A=0;for(int i=1;i<81;i++)if((p4[i][0]*p4[i][0]+p4[i][1]*p4[i][1]+p4[i][2]*p4[i][3])%3==0)A|=Mask(1)<<i;
 auto avec=points(A);assert(avec.size()==20&&iscap4(A));Mask minusA=0;for(int i:avec)minusA|=Mask(1)<<third4[i][0];assert(minusA==A);
 std::map<Mask,int> centered;std::map<int,long long> zero_sizes;long long with20=0,passed=0;
 for(int code=0;code<59049;code++){int v=code,coef[10];for(int j=0;j<10;j++){coef[j]=v%3;v/=3;}Mask m=0;int count=0;for(int x=1;x<81;x++){int val=0;for(int j=0;j<10;j++)val+=coef[j]*monomials[x][j];if(val%3==0){m|=Mask(1)<<x;count++;}}zero_sizes[count]++;if(count==20){with20++;if(iscap4(m)){passed++;centered.emplace(m,code);}}if(code%2048==0)guard();}
 assert(centered.count(A));std::ofstream cenout(dir+"/CENTERED20_MASKS_COEFFICIENTS.txt");for(auto[m,c]:centered)cenout<<hexmask(m)<<' '<<c<<'\n';cenout.close();
 std::vector<Mask> translated;translated.reserve(centered.size()*81);for(auto[m,code]:centered){auto pts=points(m);for(int v=0;v<81;v++){Mask translated_m=0;for(int x:pts)translated_m|=Mask(1)<<plus4[x][v];translated.push_back(translated_m);}guard();}
 long long translation_attempts=translated.size();std::sort(translated.begin(),translated.end());translated.erase(std::unique(translated.begin(),translated.end()),translated.end());std::ofstream allout(dir+"/ALL20_MASKS.txt");for(Mask m:translated)allout<<hexmask(m)<<'\n';allout.close();
 std::vector<int> normals;for(int d=1;d<243;d++){int first=0;for(int k=0;k<5;k++)if(p5[d][k]){first=p5[d][k];break;}if(first==1)normals.push_back(d);}assert(normals.size()==121);
 std::vector<Profile> types;std::map<Profile,int> type_index;for(int a=0;a<=20;a++)for(int b=0;b<=a;b++){int c=41-a-b;if(0<=c&&c<=b){type_index[{a,b,c}]=types.size();types.push_back({a,b,c});}}
 struct Entry{long long count=0;Mask firstB=0;};std::map<std::vector<int>,Entry> histograms;long long admissible=0;std::ofstream bout(dir+"/B20_DISJOINT_MASKS.txt");
 for(Mask B:translated){if(B&minusA)continue;assert(iscap4(B));admissible++;bout<<hexmask(B)<<'\n';std::vector<int> cap;for(int x:avec)cap.push_back(3*x);for(int x:points(B))cap.push_back(3*x+1);cap.push_back(2);std::sort(cap.begin(),cap.end());checkcap5(cap);
  std::vector<int> hist(types.size(),0);for(int d:normals){Profile t={0,0,0};for(int x:cap)t[dots[d][x]]++;std::sort(t.begin(),t.end(),std::greater<int>());assert(type_index.count(t));hist[type_index[t]]++;}
  long long total=0,e2=0,e3=0;for(unsigned j=0;j<types.size();j++){auto[a,b,c]=types[j];total+=hist[j];e2+=hist[j]*(a*b+a*c+b*c);e3+=hist[j]*a*b*c;}assert(total==121&&e2==81LL*41*40/2&&e3==27LL*41*40*39/6);auto &entry=histograms[hist];if(entry.count==0)entry.firstB=B;entry.count++;guard();}
 bout.close();std::ofstream hout(dir+"/HISTOGRAMS.json");hout<<"{\n\"status\":\"COMPLETE20201_POLYNOMIAL_ENUMERATION_FROZEN\",\n\"scope\":\"All 41-caps in AG(5,3) admitting a 20/20/1 direction, up to affine coverage only\",\n\"point_encoding\":\"4D i=x0+3*x1+9*x2+27*x3; 5D j=t+3*i; least significant base-3 digit first\",\n\"canonical_Q\":\"x0^2+x1^2+x2*x3\",\n\"canonical_A_mask\":\""<<hexmask(A)<<"\",\n\"canonical_A_points\":";jsonp4(hout,avec);hout<<",\n\"types\":[";for(unsigned i=0;i<types.size();i++){if(i)hout<<',';auto[a,b,c]=types[i];hout<<'['<<a<<','<<b<<','<<c<<']';}hout<<"],\n\"histograms\":[\n";bool first=true;for(auto &[hist,e]:histograms){if(!first)hout<<",\n";first=false;std::vector<int> cap;for(int x:avec)cap.push_back(3*x);for(int x:points(e.firstB))cap.push_back(3*x+1);cap.push_back(2);std::sort(cap.begin(),cap.end());hout<<"{\"counts\":";jsonints(hout,hist);hout<<",\"normalized_B_frequency\":"<<e.count<<",\"B_mask\":\""<<hexmask(e.firstB)<<"\",\"point_indices\":";jsonints(hout,cap);hout<<",\"points\":";jsonp5(hout,cap);hout<<'}';}hout<<"\n]}\n";hout.close();
 std::ofstream out(dir+"/RESULT.json");out<<"{\n\"status\":\"COMPLETE20201_POLYNOMIAL_ENUMERATION_PASS\",\n\"coefficient_vectors\":59049,\n\"zero_size_distribution\":{";first=true;for(auto [n,c]:zero_sizes){if(!first)out<<',';first=false;out<<'\"'<<n<<"\":"<<c;}out<<"},\n\"forms_with20_nonzero_zeros\":"<<with20<<",\n\"forms_with20_cap_nonzero_zeros\":"<<passed<<",\n\"distinct_centered20_caps\":"<<centered.size()<<",\n\"translation_attempts\":"<<translation_attempts<<",\n\"distinct_all20_caps\":"<<translated.size()<<",\n\"admissible_B20_disjoint_minusA\":"<<admissible<<",\n\"distinct_histograms\":"<<histograms.size()<<",\n\"canonical_pair_checks\":190,\n\"lifted_pair_checks\":"<<admissible*820<<",\n\"histogram_direction_evaluations\":"<<admissible*121<<",\n\"directions_per_histogram\":121,\n\"wall_seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<",\n\"read_H_generated_inputs\":false,\n\"expected_orbit_counts_used_as_filters\":false,\n\"LP_run\":false\n}\n";
 std::cout<<"PASS forms "<<passed<<" centered "<<centered.size()<<" all20 "<<translated.size()<<" B "<<admissible<<" histograms "<<histograms.size()<<'\n';
}
