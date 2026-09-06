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
using Point=std::array<int,5>;
using Profile=std::array<int,3>;
using Deletion=std::array<int,4>;
void sort3(Profile&t){if(t[0]<t[1])std::swap(t[0],t[1]);if(t[1]<t[2])std::swap(t[1],t[2]);if(t[0]<t[1])std::swap(t[0],t[1]);}
void ints(std::ostream&o,const std::vector<int>&v){o<<'[';for(size_t i=0;i<v.size();i++){if(i)o<<',';o<<v[i];}o<<']';}
int main(int argc,char**argv){assert(argc==2);std::string dir=argv[1];auto start=std::chrono::steady_clock::now();
 std::ifstream in(dir+"/COORDINATES.tsv");std::vector<Point> points;Point p;
 while(in>>p[0]>>p[1]>>p[2]>>p[3]>>p[4]){for(int x:p)assert(0<=x&&x<=2);assert(points.empty()||points.back()<p);points.push_back(p);}assert(in.eof()&&points.size()==45);
 for(int i=0;i<45;i++)for(int j=0;j<i;j++){Point third;for(int k=0;k<5;k++)third[k]=(6-points[i][k]-points[j][k])%3;assert(!std::binary_search(points.begin(),points.end(),third));}
 unsigned char value[242][45];for(int code=1;code<243;code++){int z=code;Point normal;for(int k=0;k<5;k++){normal[k]=z%3;z/=3;}for(int j=0;j<45;j++){int dot=0;for(int k=0;k<5;k++)dot+=normal[k]*points[j][k];value[code-1][j]=dot%3;}}
 int type_id[21][21][21];for(int a=0;a<=20;a++)for(int b=0;b<=20;b++)for(int c=0;c<=20;c++)type_id[a][b][c]=-1;
 std::vector<Profile> types;for(int a=0;a<=20;a++)for(int b=0;b<=a;b++){int c=41-a-b;if(0<=c&&c<=b){type_id[a][b][c]=types.size();types.push_back({a,b,c});}}
 struct Entry{long long frequency=0;Deletion deleted{};int temp_id=-1;};std::map<std::vector<int>,Entry> families;
 std::vector<Deletion> deleted_all;std::vector<int> temporary_ids;deleted_all.reserve(148995);temporary_ids.reserve(148995);long long total=0;int next_id=0;
 for(int a=0;a<42;a++)for(int b=a+1;b<43;b++)for(int c=b+1;c<44;c++)for(int d=c+1;d<45;d++){
  Deletion deletion={a,b,c,d};int retained[41],n=0;for(int i=0;i<45;i++)if(i!=a&&i!=b&&i!=c&&i!=d)retained[n++]=i;assert(n==41);
  std::vector<int> histogram(types.size(),0);
  for(int normal=0;normal<242;normal++){Profile counts={0,0,0};for(int j=0;j<41;j++)counts[value[normal][retained[j]]]++;sort3(counts);assert(counts[0]<=20);int id=type_id[counts[0]][counts[1]][counts[2]];assert(id>=0);histogram[id]++;}
  long long sum=0,e2=0,e3=0;for(size_t k=0;k<types.size();k++){assert(histogram[k]%2==0);histogram[k]/=2;auto[x,y,z]=types[k];sum+=histogram[k];e2+=histogram[k]*(x*y+x*z+y*z);e3+=histogram[k]*x*y*z;}assert(sum==121&&e2==66420&&e3==287820);
  auto &entry=families[histogram];if(entry.frequency==0){entry.deleted=deletion;entry.temp_id=next_id++;}entry.frequency++;deleted_all.push_back(deletion);temporary_ids.push_back(entry.temp_id);total++;
  if(total%1024==0&&std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>110)throw std::runtime_error("110-second incomplete finite stop");
 }
 assert(total==45LL*44*43*42/24&&total==148995);std::vector<int> final_id(next_id);int id=0;for(auto &[h,e]:families)final_id[e.temp_id]=id++;
 std::ofstream assignments(dir+"/SUBSET_HISTOGRAM_IDS.txt");for(size_t i=0;i<deleted_all.size();i++){auto[a,b,c,d]=deleted_all[i];assignments<<a<<' '<<b<<' '<<c<<' '<<d<<' '<<final_id[temporary_ids[i]]<<'\n';}assignments.close();
 std::ofstream out(dir+"/HISTOGRAMS.json");out<<"{\n\"status\":\"COMPLETE45_MINUS4_RETAINED_POINT_ENUMERATION_FROZEN\",\n\"scope\":\"All 41-caps obtained by four-point deletion from a 45-cap, up to published affine uniqueness\",\n\"point_order\":\"Lexicographic coordinate order of the accepted 45-point input\",\n\"types\":[";for(size_t i=0;i<types.size();i++){if(i)out<<',';auto[a,b,c]=types[i];out<<'['<<a<<','<<b<<','<<c<<']';}out<<"],\n\"histograms\":[\n";id=0;bool first=true;
 for(auto &[h,e]:families){if(!first)out<<",\n";first=false;auto[a,b,c,d]=e.deleted;std::vector<int> retained,indices;for(int i=0;i<45;i++)if(i!=a&&i!=b&&i!=c&&i!=d){retained.push_back(i);int encoded=0,power=1;for(int x:points[i]){encoded+=power*x;power*=3;}indices.push_back(encoded);}
  out<<"{\"id\":"<<id++<<",\"counts\":";ints(out,h);out<<",\"frequency\":"<<e.frequency<<",\"deleted_input_indices\":["<<a<<','<<b<<','<<c<<','<<d<<"],\"retained_input_indices\":";ints(out,retained);out<<",\"point_indices\":";ints(out,indices);out<<",\"points\":[";for(size_t k=0;k<retained.size();k++){if(k)out<<',';out<<'[';for(int j=0;j<5;j++){if(j)out<<',';out<<points[retained[k]][j];}out<<']';}out<<"]}";
 }
 out<<"\n]}\n";out.close();std::ofstream result(dir+"/RESULT.json");result<<"{\n\"status\":\"COMPLETE45_MINUS4_RETAINED_POINT_ENUMERATION_PASS\",\n\"subsets\":"<<total<<",\n\"histograms\":"<<families.size()<<",\n\"input_pair_checks\":990,\n\"normals_per_subset\":242,\n\"nonzero_normal_profiles_computed\":"<<242*total<<",\n\"retained_point_residues_counted\":"<<242*41*total<<",\n\"normalized_directions_per_subset\":121,\n\"used_deleted_occupancy_subtraction\":false,\n\"root_generated_outputs_read_before_freeze\":false,\n\"worker_count\":1,\n\"wall_seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<",\n\"LP_run\":false\n}\n";
 std::cout<<"PASS subsets "<<total<<" histograms "<<families.size()<<" direct normal profiles "<<242*total<<'\n';
}
