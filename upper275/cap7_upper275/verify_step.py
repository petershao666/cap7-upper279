#!/usr/bin/env python3
"""Independent unbounded-integer, standard-library verifier for one recorded step."""
from pathlib import Path
import sys,json,itertools,math,runpy,time
W=Path(__file__).resolve().parent
ns=runpy.run_path(str(W/'baseline277/verify.py'),run_name='preserved_baseline277')
v=ns['v'];b=ns['b'];require=ns['require'];matrices=ns['matrices'];features=ns['feats'];labels=ns['label_values'];BASE=ns['BASE']
from auxiliary41 import verify_cut as verify_aux41, prove_small_bound
AUXREG={};AUXDATA={}
def alltypes(S,upper):return [(a,b,S-a-b) for a in range(upper+1) for b in range(a+1) if 0<=S-a-b<=b]
def deleted2():
 R=json.loads((W/'results/near_deleted2.json').read_text());require([r['h'] for r in R]==list(range(1,52)),'two deletion coverage');count=0
 for r in R:
  h=r['h'];q=r.get('coeff',r.get('q'));rhs=[252+h,112-2*h,h,121*h,40*math.comb(h,2),13*math.comb(h,3),22*h,4*math.comb(h,2)];U=sum(a*z for a,z in zip(q,rhs))
  require(len(q)==8 and all(type(x) is int for x in q),'integer coefficient vector')
  for u in range(3):
   for p in range(21 if u==0 else 12):
    m=16+4*u+3*p-h
    if p>h or h-p>45 or m<0:continue
    f=(int(u==0),int(u==1),int(u==2),p,math.comb(p,2),math.comb(p,3),u*p,u*math.comb(p,2));value=sum(a*z for a,z in zip(q,f));count+=1
    require(value>=(r['K'] if r.get('infeasible') else r['L']*int(m<=2)),'two deletion local inequality')
  if r.get('infeasible'):require(U==r['forced'] and 364*r['K']-U==r['gap']>0,'two deletion infeasible gap')
  else:require(r['L']>0 and U==r['upper'] and 23*r['L']-U==r['gap']>0,'two deletion count gap')
 require(all(16+4*u-h>2 for h in (0,1) for u in range(3)),'small intersection nonzero counts');require(all(103<=2*h<112 for h in range(52,56)),'large intersection rigidity')
 print(f'DELETED2 PASS: {count} integer states; two deletions from two 112-caps leave at most44 positions.',flush=True)
def histogram(h,old,comp,a5,m5):
 m=h['m'];T=[t for t in alltypes(m,45) if v.downwards_allowed(t,old+comp)];require(T==list(map(tuple,h['types'])) and len(T)==len(h['phi']),'histogram type support');phi=dict(zip(T,h['phi']));require(all(type(x) is int for x in phi.values()),'integer histogram values');rare=[tuple(r['type']) for r in h['inner']];require(len(rare)==len(set(rare)),'duplicate rare case')
 root=h['root'];q=root['coeff'];require(len(q)==2,'rare polynomial dimension');U=q[0]*243*math.comb(m,2)+q[1]*81*math.comb(m,3);require(U==root['forced'] and 364*root['K']-U==root['gap']>0,'rare root gap')
 for t in T:
  if t not in rare:require(q[0]*v.e2(t)+q[1]*v.e3(t)>=root['K'],'rare type inequality')
 extra5=list(map(tuple,h.get('admissibility5_extra',[])))
 require(not extra5 or extra5==[(20,19,2),(20,18,3),(19,19,3),(19,18,4)],'published Proposition6.1 scope')
 if extra5:
  a5={t:ok and v.downwards_allowed(t,extra5) for t,ok in a5.items()}
  m5=v.make_masks(20,a5)
 bounds=[];count=0
 for ri,r in enumerate(h['inner']):
  absent=list(map(tuple,r.get('absent_types',[])))
  require(not absent or absent==rare[:ri],'first-occurring rare-direction ordering')

  key=tuple(r['type']);sums=list(v.forced(key,6));q=r['coeff'];spmaps=[]
  for col,t in r['extras']:
   data=BASE['spectrum5'][str(key[col])];require(key[col] in (43,44,45) and len(data['spectra'])==1,'fixed histogram scope');sums.append(data['spectra'][0][data['types'].index(t)])
  auxmaps=[]
  for ui,use in enumerate(r.get('uppercuts',[])):
   col=use['column'];name=use['id'];data=use['data']
   require(key[col]==41 and data['m']==41 and q[len(sums)]>=0,'41-cap upper-bound scope/sign')
   if name not in AUXREG:
    prove_small_bound();ph,bd,num=verify_aux41(data,name);AUXREG[name]=(ph,bd);AUXDATA[name]=data
   require(AUXDATA[name]==data,'auxiliary identifier data mismatch')
   ph,bd=AUXREG[name];sums.append(bd);auxmaps.append((col,ph))
  require(len(q)==len(sums) and all(type(x) is int for x in q),'inner coefficient length');U=sum(a*z for a,z in zip(q,sums))
  for sp in r['spectra']:
   col=sp['column'];N=key[col];require(N==42,'variable histogram scope');data=BASE['spectrum5'][str(N)];require(sp['types']==data['types'] and len(sp['phi'])==len(sp['types']),'spectral support')
   bound=max(sum(a*z for a,z in zip(hist,sp['phi'])) for hist in data['spectra']);require(bound==sp['bound'],'spectral bound');U+=bound;spmaps.append(dict(zip(map(tuple,sp['types']),sp['phi'])))
  bound=phi[key]+U-121*r['K'];require(bound==r['bound'],'inner full histogram bound');minimum=None;n=0
  for a,bb,cc,tops in matrices(key,6,a5,m5,old+comp+absent):
   cols=(a,bb,cc);f=list(features(a,bb,cc));f.extend(int(tuple(sorted(cols[j],reverse=True))==tuple(t)) for j,t in r['extras']);f.extend(ph[tuple(sorted(cols[col],reverse=True))] for col,ph in auxmaps);value=sum(x*y for x,y in zip(q,f))
   value+=sum(mp[tuple(sorted(cols[sp['column']],reverse=True))] for sp,mp in zip(r['spectra'],spmaps));value-=sum(phi[tuple(sorted(t,reverse=True))] for t in tops)
   require(value>=r['K'],'new histogram inner inequality');minimum=value if minimum is None else min(minimum,value);n+=1
  require(n>0,'empty inner family');count+=n;bounds.append(bound);print(f'STEP INNER {h["id"]} {key}: matrices={n}, minimum={minimum}, K={r["K"]}, bound={bound}',flush=True)
 require(max(bounds)==h['bound'],'uniform histogram bound');print(f'HISTOGRAM PASS {h["id"]}: types={len(T)}, rare={len(rare)}, bound={h["bound"]}, matrices={count}',flush=True);return phi,h['bound'],count

def main():
 start=time.monotonic();S=int(sys.argv[1]);folder=W/'results'/f'size{S}';C=json.loads((folder/'proof.json').read_text());k=C['k'];require(C['size']==S,'target size')
 ns['baseline_integrity']();old,comp,a5,m5,a6,m6=ns['lower_inputs']();ns['near112']();phi,B,n=ns['histogram_bound'](old,comp,a5,m5);deleted2();registry={'psi108':(phi,B)};inner=0
 for h in C['new_histograms']:
  ph,bd,num=histogram(h,old,comp,a5,m5);registry[h['id']]=(ph,bd);inner+=num
 def Q(t):return 9*v.e3(t)-(4*S-3*k)*v.e2(t)+S*S*(S-k)
 ts=alltypes(S,112)
 def case(key,r,banned,extremal):
  state=tuple(r.get('status',[-1,-1,-1]));pred=[]
  for j,s in enumerate(state):
   require(s in (-1,0,1),'status domain')
   if s>=0:require(103<=key[j]<=112 and (s==1 or key[j]<109),'status scope')
   pred.append(b.sub112 if s==1 else (lambda t:v.downwards_allowed(t,comp)) if s==0 else None)
  extra=r.get('extra_features',[]);sums=list(v.forced(key,7));q=r.get('coeff',[])
  for i,(j,name) in enumerate(extra):
   require(j in (0,1,2),'extra column');d=112-key[j]
   if name in ('fam','small','label40'):
    require(state[j]==1 and 0<=d<=9,'completed feature scope');sums.append({'fam':56,'small':11*d,'label40':110*d}[name])
   else:
    require(state[j]==0 and name in registry and q[7+i]>=0,'histogram feature scope/sign');ph,bd=registry[name];require(all(sum(t)==key[j] for t in ph),'histogram dimension');sums.append(bd)
  if not r.get('empty'):
   require(len(q)==len(sums) and all(type(x) is int for x in q),'step coefficient dimension');U=sum(x*y for x,y in zip(q,sums));require(U==r['forced'] and 364*r['K']-U==r['gap']>0,'step exact gap')
  ban=list(banned)+([t for t in ts if Q(t)<Q(key)] if extremal else []);minimum=None;n=0
  for a,bb,cc,_ in matrices(key,7,a6,m6,ban,tuple(pred)):
   require(not r.get('empty'),'empty claim has witness');fs=features(a,bb,cc);value=sum(x*y for x,y in zip(q[:7],fs));cols=(a,bb,cc)
   for i,(j,name) in enumerate(extra):
    t=cols[j];ss=tuple(sorted(t,reverse=True));qq=q[7+i]
    if name=='fam':value+=qq*int(ss[2]<=22)
    elif name=='small':value+=qq*(22-ss[2] if ss[2]<=22 else 0)
    elif name=='label40':value+=min(qq*d for d in labels(t))
    else:value+=qq*registry[name][0][ss]
   require(value>=r['K'],'step local inequality');minimum=value if minimum is None else min(minimum,value);n+=1
  require(n==0 if r.get('empty') else n>0,'step empty/nonempty family');print(f'STEP {"EXTREMAL" if extremal else "ORDINARY"} {key} status={state}: matrices={n}, minimum={minimum or 0}, K={r.get("K",0)}, gap={r.get("gap",0)}',flush=True);return n
 require(C['initial_seeds']==[[112,112,29],[112,111,35]],'initial seeds');require(C['seeds']==[[112,112,29],[112,111,35],[112,110,45],[111,111,45]],'all seeds')
 ban=list(map(tuple,C['initial_seeds']));ordinary=0;extremal=0
 for stage in C['stages']:
  snap=list(ban)
  for key,r in sorted(stage.items()):
   t=v.parse_key(key);require(sum(t)==S and v.downwards_allowed(t,ban),'ordinary type');require('status' not in r and not r.get('extra_features'),'ordinary scope');ordinary+=case(t,r,snap,False)
  ban.extend(v.parse_key(key) for key in stage)
 ban.extend([(112,110,45),(111,111,45)]);expected={t for t in ts if Q(t)<0 and v.downwards_allowed(t,ban)};require(expected=={v.parse_key(key) for key in C['extremal']},'minimum type coverage')
 for key,r in sorted(C['extremal'].items()):
  t=v.parse_key(key)
  if 'branches' not in r:extremal+=case(t,r,ban,True)
  else:
   elig=[j for j,N in enumerate(t) if 103<=N<109];want={tuple(bits[elig.index(j)] if j in elig else (1 if t[j]>=109 else -1) for j in range(3)) for bits in itertools.product((0,1),repeat=len(elig))};have=[tuple(rr['status']) for rr in r['branches']];require(len(have)==len(want) and set(have)==want,'completion split coverage')
   for rr in r['branches']:extremal+=case(t,rr,ban,True)
 for a,bb,c in ts:require(4*Q((a,bb,c))==(3*c-S)**2*(c-k)+(4*S-3*k-9*c)*(a-bb)**2,'root identity')
 total=9*243*math.comb(S,3)-(4*S-3*k)*729*math.comb(S,2)+S*S*(S-k)*1093;require(total==C['root_sum']<0,'global negative sum')
 print(f'STEP FULL PASS: no {S}-point cap; f(7,3) <= {S-1}; ordinary_matrices={ordinary}; extremal_matrices={extremal}; new_inner_matrices={inner}; minimum_cases={len(expected)}; global_sum={total}.',flush=True)
 print(f'Elapsed seconds: {time.monotonic()-start}',flush=True)
if __name__=='__main__':main()
