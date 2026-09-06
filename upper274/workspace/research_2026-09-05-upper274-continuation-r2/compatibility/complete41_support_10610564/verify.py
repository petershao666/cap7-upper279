"""Exact arithmetic replay using the disclosed shared domain enumerator, no optimizer.
This is the author's checker. Independent root enumeration remains required.
"""
from pathlib import Path
import json,sys,time,signal
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W))
import run as D
np=D.np

def dot(a,b):return sum(int(x)*int(y)for x,y in zip(a,b))
def exact_values(X,q,terms):
 ceiling=dot(np.max(abs(X),axis=0),abs(q))+sum(max(map(abs,phi))*ids.shape[1]if ids.ndim==2 else max(map(abs,phi))for phi,ids in terms)
 assert ceiling<8*10**18,('int64_bound',ceiling)
 vv=X@q
 for phi,ids in terms:
  pp=np.array(phi,np.int64);vv+=pp[ids].sum(axis=1)if ids.ndim==2 else pp[ids]
 return vv

def main():
 signal.signal(signal.SIGALRM,D.limit);signal.alarm(590);started=time.monotonic()
 r=json.loads((W/'RESULT.json').read_text());assert r['claim']=='CANDIDATE_EXACT_CERTIFICATE'
 assert r['table1']==json.loads((D.H/'h13/table1_input_v2.json').read_text())
 assert r['histogram_pair_capacity']==D.CP
 assert r['input17']==D.INPUT17 and r['actual17']==D.ACTUAL17 and r['actual16']==D.ACTUAL16 and r['actual41']==D.ACTUAL41 and r['input41']==D.MODEL_INPUT
 hist={int(m):z for m,z in r['histograms'].items()};cf=r['conditional_functions'];cb=r['conditional_bounds']
 for m,z in hist.items():assert list(map(tuple,z['types']))==D.TS[m];assert all(type(v)is int for v in z['phi'])
 assert r['conditional_types']==list(map(list,D.T18))
 for fn in ['left18','right18','cond18']:assert len(cf[fn])==len(D.T18)and all(type(v)is int for v in cf[fn])
 assert cb['pair18']==max(dot(D.H18[a],cf['left18'])+dot(D.H18[b],cf['right18'])for a,b in D.PAIR)
 assert cb['cond18']==max(dot(D.H18[a],cf['cond18'])for a in D.COND)
 a40=[D.low40(t,i)for i,t in enumerate(D.ORDER40)];a41=[];ALL=a40
 INS=[z for z in ALL if not z['empty']]+[D.inner106(t,i)for i,t in enumerate(D.ANCH[106])]
 for z in INS:z.setdefault('deps',[]);z.setdefault('pairdeps',[])
 LEAF=D.localize_supports(INS);local=r['local_supports'];assert set(LEAF)==set(local)
 for name,l in LEAF.items():
  exact_meta=json.loads(json.dumps(l));f=local[name]
  for k,v in exact_meta.items():assert f[k]==v
  assert list(map(tuple,f['types']))==D.TS[l['m']]and all(type(v)is int for v in f['phi'])
  hh={16:D.H16,17:D.H17,18:D.H18,41:D.H41}[l['m']]
  assert f['bound']==max(dot(h,f['phi'])for h in hh)
 assert len(a40)==44 and len(a41)==0
 empty=[dict(m=z['m'],type=z['key'],class41=z.get('class41'),full18_state=z.get('full18_state'),state18=z.get('state18'),state8=z.get('state8'))for z in ALL if z['empty']]
 assert json.loads(json.dumps(empty))==r['empty_cases']
 rows=[]
 for m in[40,106]:
  cases=[z for z in INS if z['m']==m];assert len(cases)==len(hist[m]['inner']);bs=[]
  for z,c in zip(cases,hist[m]['inner']):
   assert list(z['key'])==c['type']and z.get('class41')==c['class41']and z.get('full18_state')==c['full18_state']
   assert json.loads(json.dumps(z['extra']))==c['extra']and z.get('state8')==c['state8']
   q=np.array(c['coeff'],np.int64);assert len(q)==z['X'].shape[1]and all(q[j]>=0 for j in z['pos'])
   expect_deps=[dict(m=parent,column=col,coefficient=1)for parent,ids,col in z['deps']]
   expect_cond=[dict(function=fn,column=col,coefficient=1)for fn,ids,col in z['pairdeps']]
   assert c['local_supports']==[dict(id=name,column=col,coefficient=1)for name,ids,col in z['leafdeps']]
   assert c['dependencies']==expect_deps and c['conditional_dependencies']==expect_cond and c['conditional_bound']==z.get('pairbound')
   terms=[([-v for v in hist[m]['phi']],z['tops'])]+[(hist[p]['phi'],ids)for p,ids,col in z['deps']]+[(cf[fn],ids)for fn,ids,col in z['pairdeps']]+[(local[name]['phi'],ids)for name,ids,col in z['leafdeps']]
   vv=exact_values(z['X'],q,terms);K=int(vv.min());B=hist[m]['phi'][z['anchor']]+dot(q,z['F'])+sum(hist[p]['bound']for p,ids,col in z['deps'])+sum(local[name]['bound']for name,ids,col in z['leafdeps'])+(cb[z['pairbound']]if z['pairdeps']else 0)-D.D[m]*K
   assert K==c['K']and B==c['bound']and len(vv)==c['count'];bs.append(B);rows.append(dict(m=m,type=z['key'],count=len(vv),K=K,bound=B))
  assert max(bs)==hist[m]['bound']
 old=json.loads((D.R/'certificates.json').read_text());ban=D.SEEDS+[(112,109,51),(111,110,51)]+[D.V.parse_key(k)for s in old['stages']for k in s]
 assert set(ban)==set(map(tuple,r['ordinary_bans']))==set(map(tuple,D.FIXED6['ordinary_bans'])) and len(ban)==18
 ban=list(map(tuple,D.FIXED6['ordinary_bans']))
 assert len(r['outer'])==1 and r['outer'][0]['type']==[106,105,64]
 for c in r['outer']:
  z=D.outer_new(tuple(c['type']),ban);assert z['fixed_functions']==r['fixed6_functions'];q=np.array(c['coeff'],np.int64);assert all(q[j]>=0 for j in z['pos'])
  vv=exact_values(z['X'],q,[(hist[m]['phi'],ids)for m,ids in z['ids']]);K=int(vv.min());U=dot(q,z['F'])+sum(hist[m]['bound']for m,ids in z['ids']);gap=364*K-U
  assert K==c['K']and U==c['forced']and gap==c['gap']and gap>0 and len(vv)==c['count'];rows.append(dict(m=275,type=c['type'],count=len(vv),K=K,forced=U,gap=gap))
 result=dict(status='AUTHOR_EXACT_REPLAY_PASS',shared_dependency='run.py domain enumerators; independent root replay still required',rows=rows,local_support_count=len(LEAF),local_support_sizes={m:sum(l['m']==m for l in LEAF.values())for m in[16,17,18,41]},finite_ordered_pairs=len(D.PAIR),finite_conditional_histograms=len(D.COND),elapsed=time.monotonic()-started)
 (W/'author_check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
