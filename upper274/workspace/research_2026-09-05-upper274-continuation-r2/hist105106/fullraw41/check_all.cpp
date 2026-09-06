#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
void ints(ostream&o,const vector<int>&v){o<<'[';for(size_t i=0;i<v.size();++i)o<<(i?",":"")<<v[i];o<<']';}
int main(int argc,char**argv){
 string dir=argc==2?argv[1]:"";int current=-1;
 try{
  if(argc!=2)throw runtime_error("output directory required");
  auto start=chrono::steady_clock::now();array<array<int,5>,243>c{};const int pow3[5]={81,27,9,3,1};
  for(int p=0;p<243;++p)for(int j=0;j<5;++j)c[p][j]=(p/pow3[j])%3;
  int third[243][243];for(int p=0;p<243;++p)for(int q=0;q<243;++q){int z=0;for(int j=0;j<5;++j)z+=pow3[j]*((6-c[p][j]-c[q][j])%3);third[p][q]=z;}
  vector<array<int,5>>normals;for(int p=1;p<243;++p){int first=0;for(int x:c[p])if(x){first=x;break;}if(first==1)normals.push_back(c[p]);}if(normals.size()!=121)throw runtime_error("normal count");
  int dot[121][243];for(int d=0;d<121;++d)for(int p=0;p<243;++p){int z=0;for(int j=0;j<5;++j)z+=normals[d][j]*c[p][j];dot[d][p]=z%3;}
  vector<array<int,3>>types;map<array<int,3>,int>idx;for(int a=0;a<=20;++a)for(int b=0;b<=a;++b){int k=41-a-b;if(k>=0&&k<=b){idx[{a,b,k}]=types.size();types.push_back({a,b,k});}}
  ifstream in(dir+"/point_rows.txt");int n;in>>n;if(n!=34345)throw runtime_error("record count");
  vector<vector<int>>hist,reps;vector<int>rep_row;map<vector<int>,int>hi;set<vector<int>>unique_points;long long pairs=0;
  ofstream ledger(dir+"/row_histogram_ids.tsv");const int levelidx[3]={1,2,0};
  for(int row=0;row<n;++row){current=row;int id,expected[9];vector<int>ps(41);in>>id;for(int&i:expected)in>>i;for(int&p:ps)in>>p;if(!in||id!=row)throw runtime_error("row parse/id failure");
   bool present[243]={};int grid[9]={};int last=-1;for(int p:ps){if(p<0||p>=243||p<=last)throw runtime_error("point range/order/duplicate");last=p;present[p]=true;++grid[3*levelidx[c[p][0]]+levelidx[c[p][1]]];}
   for(int j=0;j<9;++j)if(grid[j]!=expected[j])throw runtime_error("source grid mismatch");
   for(int i=0;i<41;++i)for(int j=i+1;j<41;++j){++pairs;if(present[third[ps[i]][ps[j]]])throw runtime_error("collinear triple");}
   vector<int>h(types.size());for(int d=0;d<121;++d){array<int,3>a{};for(int p:ps)++a[dot[d][p]];sort(a.begin(),a.end(),greater<int>());auto it=idx.find(a);if(it==idx.end())throw runtime_error("section type outside C4<=20");++h[it->second];}
   long long e2=0,e3=0;int sum=0;for(size_t i=0;i<types.size();++i){auto a=types[i];sum+=h[i];e2+=h[i]*(a[0]*a[1]+a[0]*a[2]+a[1]*a[2]);e3+=h[i]*a[0]*a[1]*a[2];}if(sum!=121||e2!=66420||e3!=287820)throw runtime_error("direction moments");
   int hid;auto it=hi.find(h);if(it==hi.end()){hid=hist.size();hi[h]=hid;hist.push_back(h);reps.push_back(ps);rep_row.push_back(row);}else hid=it->second;
   unique_points.insert(ps);ledger<<row<<'\t'<<hid<<'\n';
   if(row%256==0&&chrono::duration<double>(chrono::steady_clock::now()-start).count()>590)throw runtime_error("finite batch time limit");
  }
  int extra;if(in>>extra)throw runtime_error("extra unconsumed input");ledger.close();
  ofstream out(dir+"/HISTOGRAMS.json");out<<"{\"scope\":\"ALL_34345_DECLARED_PRIMARY_RAW_OUTPUT_RECORDS\",\"point_encoding\":\"81*x1+27*x2+9*x3+3*x4+x5\",\"types\":[";
  for(size_t i=0;i<types.size();++i){if(i)out<<',';ints(out,{types[i][0],types[i][1],types[i][2]});}out<<"],\"histograms\":[";
  for(size_t i=0;i<hist.size();++i){if(i)out<<',';out<<"{\"id\":"<<i<<",\"counts\":";ints(out,hist[i]);out<<",\"representative_row_id\":"<<rep_row[i]<<",\"point_ids\":";ints(out,reps[i]);out<<",\"points\":[";for(size_t j=0;j<reps[i].size();++j){if(j)out<<',';vector<int>p(c[reps[i][j]].begin(),c[reps[i][j]].end());ints(out,p);}out<<"]}";}out<<"]}\n";out.close();
  double seconds=chrono::duration<double>(chrono::steady_clock::now()-start).count();ofstream st(dir+"/CHECK_STATISTICS.json");st<<"{\"status\":\"FULL_DECLARED_RAW_POINT_AND_HISTOGRAM_CHECK_PASS\",\"records\":"<<n<<",\"point_pair_checks\":"<<pairs<<",\"direction_checks\":"<<121LL*n<<",\"distinct_histograms\":"<<hist.size()<<",\"distinct_normalized_pointsets\":"<<unique_points.size()<<",\"seconds\":"<<seconds<<"}\n";st.close();
  cout<<"FULL_CHECK_PASS records="<<n<<" pairs="<<pairs<<" histograms="<<hist.size()<<" pointsets="<<unique_points.size()<<" seconds="<<seconds<<'\n';
 }catch(const exception&e){ofstream f(dir+"/CHECK_FAILURE.json");f<<"{\"row_id\":"<<current<<",\"error\":\""<<e.what()<<"\"}\n";cerr<<"STOP row="<<current<<' '<<e.what()<<'\n';return 1;}
 return 0;
}
