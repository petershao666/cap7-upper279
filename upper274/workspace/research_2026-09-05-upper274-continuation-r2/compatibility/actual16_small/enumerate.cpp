#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <vector>
using namespace std;
using Mask=uint32_t;using Hist=array<unsigned char,14>;
const Mask ALL=(Mask(1)<<27)-1;
int xyz[27][3],thirdpt[27][27],negative[27],dotval[13][27],ntypes;
array<array<int,3>,14> types;int profile_index[10][10];
int ac[13][3],bc[13][3],cc[13][3];Mask A,B,Across[27];int casea,caseb,casec;
struct Witness{Mask a,b,c;};struct HistInfo{long long multiplicity=0;Witness witness{};};map<Hist,HistInfo> found;
struct Count{array<int,3> anchor;Mask a;long long b=0,bwithc=0,lifts=0,constructed=0;array<long long,28> freecounts{};};vector<Count> counts;Count* current;
long long total_lifts=0,total_constructed=0;chrono::steady_clock::time_point start;bool complete=true;
int pc(Mask m){return __builtin_popcount(m);}int first(Mask m){return __builtin_ctz(m);}
void timecheck(){if(chrono::duration<double>(chrono::steady_clock::now()-start).count()>570){complete=false;throw 1;}}
array<int,3> sorted3(int a,int b,int c){array<int,3> t={a,b,c};sort(t.begin(),t.end(),greater<int>());return t;}
bool cap(Mask m){for(Mask x=m;x;){int a=first(x);x&=x-1;for(Mask y=x;y;){int b=first(y);y&=y-1;if(m&(Mask(1)<<thirdpt[a][b]))return false;}}return true;}
void init(){for(int p=0;p<27;p++){xyz[p][0]=p%3;xyz[p][1]=(p/3)%3;xyz[p][2]=p/9;negative[p]=0;int scale=1;for(int j=0;j<3;j++){negative[p]+=((3-xyz[p][j])%3)*scale;scale*=3;}}
 for(int p=0;p<27;p++)for(int q=0;q<27;q++){int z=0,s=1;for(int j=0;j<3;j++){z+=((6-xyz[p][j]-xyz[q][j])%3)*s;s*=3;}thirdpt[p][q]=z;}
 int u=0;for(int x=0;x<3;x++)for(int y=0;y<3;y++)for(int z=0;z<3;z++){int lead=x?x:y?y:z;if(lead!=1)continue;for(int p=0;p<27;p++)dotval[u][p]=(x*xyz[p][0]+y*xyz[p][1]+z*xyz[p][2])%3;u++;}assert(u==13);
 fill(&profile_index[0][0],&profile_index[0][0]+100,-1);ntypes=0;for(int a=0;a<=9;a++)for(int b=0;b<=a;b++){int c=16-a-b;if(c<0||c>b)continue;types[ntypes]={a,b,c};profile_index[a][b]=ntypes++;}assert(ntypes==14);}
void addcounts(int out[13][3],int p,int delta){for(int u=0;u<13;u++)out[u][dotval[u][p]]+=delta;}
void setcounts(int out[13][3],Mask m){fill(&out[0][0],&out[0][0]+39,0);while(m){int p=first(m);m&=m-1;addcounts(out,p,1);}}
void emit(Mask cmask){current->constructed++;total_constructed++;if((total_constructed&8191)==0)timecheck();Hist h{};auto anchor=sorted3(casea,caseb,casec);h[profile_index[anchor[0]][anchor[1]]]++;
 for(int u=0;u<13;u++)for(int alpha=0;alpha<3;alpha++){int v[3];for(int r=0;r<3;r++)v[r]=ac[u][r]+bc[u][(r-alpha+3)%3]+cc[u][(r-2*alpha+6)%3];auto t=sorted3(v[0],v[1],v[2]);assert(t[0]<=9&&t[2]>=0);if(t[0]>7)return;int k=profile_index[t[0]][t[1]];assert(k>=0);h[k]++;}
 auto[it,inserted]=found.try_emplace(h);it->second.multiplicity++;if(inserted)it->second.witness={A,B,cmask};current->lifts++;total_lifts++;if((total_lifts&8191)==0)timecheck();}
void crec(Mask candidates,Mask selected,int need){if(!need){emit(selected);return;}if(pc(candidates)<need)return;
 while(candidates){int p=first(candidates);candidates&=candidates-1;if(pc(candidates)+1<need)break;Mask next=candidates;
  for(Mask q=selected;q;){int j=first(q);q&=q-1;next&=~(Mask(1)<<thirdpt[p][j]);}
  addcounts(cc,p,1);crec(next,selected|(Mask(1)<<p),need-1);addcounts(cc,p,-1);}}
void completeB(Mask bmask,Mask cross){B=bmask;current->b++;if((current->b&4095)==0)timecheck();Mask free=ALL^cross;assert(free&1);current->freecounts[pc(free)]++;if(pc(free)<casec)return;
 long long old=current->lifts;setcounts(cc,1);crec(free&~Mask(1),1,casec-1);if(current->lifts>old)current->bwithc++;}
void brec(Mask candidates,Mask selected,int need,Mask cross){if(!need){completeB(selected,cross);return;}if(pc(candidates)<need)return;
 while(candidates){int p=first(candidates);candidates&=candidates-1;if(pc(candidates)+1<need)break;Mask next=candidates;
  for(Mask q=selected;q;){int j=first(q);q&=q-1;next&=~(Mask(1)<<thirdpt[p][j]);}
  addcounts(bc,p,1);brec(next,selected|(Mask(1)<<p),need-1,cross|Across[p]);addcounts(bc,p,-1);}}
vector<Mask> readcatalog(string path,int size,long long expected){ifstream f(path);assert(f.good());vector<Mask> v;Mask m;while(f>>m){assert(pc(m)==size&&cap(m));v.push_back(m);}assert((long long)v.size()==expected);assert(is_sorted(v.begin(),v.end())&&adjacent_find(v.begin(),v.end())==v.end());return v;}
int main(int argc,char**argv){assert(argc==2);init();start=chrono::steady_clock::now();vector<Mask> cat7,cat8;
 const array<int,3> anchors[]={{7,7,2},{7,6,3}};counts.reserve(48);
 try{for(auto anchor:anchors){casea=anchor[0];caseb=anchor[1];casec=anchor[2];vector<Mask> reps=vector<Mask>{13850,13849,13843,13835,13339,12827,9755,5659,13852,13849,13845,13837,13341,12829,9757,5661,13900,13898,13894,13838,13390,12878,9806,5710};
  for(Mask rep:reps){A=rep;assert(cap(A)&&pc(A)==casea);counts.push_back({anchor,rep});current=&counts.back();setcounts(ac,A);fill(&bc[0][0],&bc[0][0]+39,0);fill(&cc[0][0],&cc[0][0]+39,0);
   if(casec==0){const auto& cat=caseb==7?cat7:cat8;for(Mask bm:cat){B=bm;setcounts(bc,B);emit(0);current->b++;current->bwithc++;}}
   else{Mask forbidden=0;for(Mask q=A;q;){int p=first(q);q&=q-1;forbidden|=Mask(1)<<negative[p];}for(int p=0;p<27;p++){Across[p]=0;for(Mask q=A;q;){int a=first(q);q&=q-1;Across[p]|=Mask(1)<<thirdpt[a][p];}}brec(ALL^forbidden,0,caseb,0);}
   cerr<<casea<<","<<caseb<<","<<casec<<" A="<<A<<" B="<<current->b<<" lifts="<<current->lifts<<" spectra="<<found.size()<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n";timecheck();}}
 }catch(int){complete=false;}
 ofstream out(argv[1]);out<<"{\"status\":\""<<(complete?"COMPLETE_SMALL_ONLY_ACTUAL_HISTOGRAMS":"INCOMPLETE_TIMEOUT")<<"\",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"total_lifts\":"<<total_lifts<<",\"total_constructed\":"<<total_constructed<<",\"types\":[";
 for(int i=0;i<14;i++){if(i)out<<",";out<<"["<<types[i][0]<<","<<types[i][1]<<","<<types[i][2]<<"]";}out<<"],\"cases\":[";
 for(size_t i=0;i<counts.size();i++){auto&r=counts[i];if(i)out<<",";out<<"{\"anchor\":["<<r.anchor[0]<<","<<r.anchor[1]<<","<<r.anchor[2]<<"],\"A_mask\":"<<r.a<<",\"B_caps\":"<<r.b<<",\"B_with_C\":"<<r.bwithc<<",\"lifted_caps\":"<<r.lifts<<",\"constructed_caps\":"<<r.constructed<<",\"free_size_counts\":[";for(int j=0;j<28;j++)out<<(j?",":"")<<r.freecounts[j];out<<"]}";}out<<"],\"histograms\":[";bool firstout=true;
 for(auto&[h,info]:found){if(!firstout)out<<",";firstout=false;out<<"{\"counts\":[";for(int i=0;i<14;i++)out<<(i?",":"")<<int(h[i]);out<<"],\"multiplicity\":"<<info.multiplicity<<",\"layer_masks\":["<<info.witness.a<<","<<info.witness.b<<","<<info.witness.c<<"]}";}out<<"]}\n";return complete?0:3;}
