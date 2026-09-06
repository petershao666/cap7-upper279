import time,signal,resource,os,sys
START=time.monotonic()
def timeout(*args):raise TimeoutError('600-second arithmetic scope exhausted')
signal.signal(signal.SIGALRM,timeout);signal.alarm(590)
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[name]='1'
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;R=W.parents[1]
import domain as D
np=D.np
SCALE=10**14
def save(n,x):(W/n).write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dot(a,b):return sum(int(x)*int(y)for x,y in zip(a,b))
def guard():
 assert time.monotonic()-START<590
 assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<2**31
def norm(x):return json.loads(json.dumps(x))
def arrhash(x):return hashlib.sha256(np.asarray(x,dtype='<i8').tobytes()).hexdigest()
CEILINGS=[]
def values(z,q,terms):
 ceiling=dot(np.max(abs(z['X']),axis=0),abs(q))
 for ph,ids in terms:ceiling+=max(map(abs,ph))*(ids.shape[1]if ids.ndim==2 else 1)
 assert ceiling<8*10**18,ceiling
 CEILINGS.append(int(ceiling))
 vv=z['X']@q
 for ph,ids in terms:
  p=np.array(ph,np.int64);vv+=p[ids].sum(axis=1)if ids.ndim==2 else p[ids]
 return vv
def main():
 inp=json.loads((W/'INPUTS.json').read_text())
 for name,h in inp['source_hashes'].items():assert sha(R/name)==h
 source=json.loads((R/'compatibility/physical40_complete42_10610663/INPUTS.json').read_text())
 for name,h in source['source_hashes'].items():assert sha(R/name)==h
 checkpoint_path=R/'compatibility/physical40_complete42_10610663/LAST_FLOAT_CHECKPOINT.json'
 assert sha(checkpoint_path)=='522aeaba0fcb802be76437c564183e62260deeab2e0764f3d216f7367452cc3f'
 checkpoint=json.loads(checkpoint_path.read_text())
 repair=json.loads((R/'compatibility/physical40_complete42_exact_repair/RESULT.json').read_text())
 expected=next(z for z in repair['repairs']if z['scale']==SCALE)
 cover=json.loads((R/'hist105106/whole42_state_gate/STATE_COVER.json').read_text())
 assert cover['formal_state_case_count']==41 and cover['known_empty_count']==3
 assert cover['types']==norm(D.T42)and cover['states'][3]['counts']==D.H42[3].tolist()
 base40=[D.low40(t,i)for i,t in enumerate(D.ORDER40)]
 lower=[D.clone40(z,tier)for tier in D.TIERS for z in base40]
 nc=[D.inner106(t,i)for i,t in enumerate(D.ANCH[106])]
 ALL=lower+nc;INS=[z for z in ALL if not z['empty']]
 for z in INS:z.setdefault('deps',[]);z.setdefault('pairdeps',[])
 LEAF=D.localize_supports(INS)
 assert len(LEAF)==96
 assert norm(LEAF)==json.loads((R/'compatibility/physical40_complete42_10610663/PLANNED_COPY_LAYOUT.json').read_text())['leaf_functions']
 old=json.loads((D.R/'certificates.json').read_text())
 ban=D.SEEDS+[(112,109,51),(111,110,51)]+[D.V.parse_key(k)for s in old['stages']for k in s]
 outer=D.outer_new((106,106,63),ban)
 assert len(outer['X'])==2460769 and sum(len(z['X'])for z in nc)==94242
 assert all(sum(len(z['X'])for z in INS if z['m']==m)==36455 for m in D.TIERS)
 assert len(outer['fixed_functions'])==12
 guard();print('DOMAINS_READY',time.monotonic()-START,flush=True)
 pofs={};bofs={};off=0
 for m in D.TIERS+[106]:pofs[m]=off;off+=len(D.TS[m]);bofs[m]=off;off+=1
 for n in D.COND_FUNCTIONS:pofs[n]=off;off+=len(D.T18)
 for n in D.COND_BOUNDS:bofs[n]=off;off+=1
 for n,l in LEAF.items():pofs[n]=off;off+=len(D.TS[l['m']]);bofs[n]=off;off+=1
 for z in INS+[outer]:z['offset']=off;off+=z['X'].shape[1]
 assert off+1==3291
 layout=json.loads((R/'compatibility/physical40_complete42_10610663/REALIZED_COPY_LAYOUT.json').read_text())
 assert {str(m):[pofs[m],bofs[m]]for m in D.TIERS+[106]}==layout['main_offsets']
 assert [dict(function=z['m'],anchor=list(z['key']),offset=z['offset'],width=z['X'].shape[1])for z in INS]==layout['case_coefficients']
 floats=np.array(checkpoint['values'],float)
 assert len(floats)==off+1 and np.isfinite(floats).all()
 for z in INS+[outer]:floats[z['offset']:z['offset']+z['X'].shape[1]]/=z['scale']
 for i in bofs.values():floats[i]=0
 floats[-1]=0
 assert np.max(abs(floats))*SCALE<8*10**18
 qi=np.rint(floats*SCALE).astype(np.int64)
 PH={m:list(map(int,qi[pofs[m]:bofs[m]]))for m in D.TIERS+[106]}
 cf={n:list(map(int,qi[pofs[n]:pofs[n]+len(D.T18)]))for n in D.COND_FUNCTIONS}
 local={}
 HH={16:D.H16,17:D.H17,18:D.H18,41:D.H41,42:D.H42}
 for n,l in LEAF.items():
  ph=list(map(int,qi[pofs[n]:bofs[n]]));scores=[dot(h,ph)for h in HH[l['m']]]
  local[n]=dict(l,mathematical_size=l['m'],types=D.TS[l['m']],phi=ph,bound=max(scores),support_values=scores)
 cb={};cv={}
 for tier in D.TIERS:
  left=f't{tier}_left18';right=f't{tier}_right18';cond=f't{tier}_cond18';pair=f't{tier}_pair18'
  cv[pair]=[dot(D.H18[a],cf[left])+dot(D.H18[b],cf[right])for a,b in D.PAIR]
  cv[cond]=[dot(D.H18[a],cf[cond])for a in D.COND]
  cb[pair]=max(cv[pair]);cb[cond]=max(cv[cond])
 upper={n:dict(size=m,types=list(phi),values=list(phi.values()),bound=bd)for n,(m,phi,bd)in(D.O.U5|D.R106.H4.NEW).items()}
 cases=[]
 for i,z in enumerate(INS+[outer]):
  q=qi[z['offset']:z['offset']+z['X'].shape[1]];assert all(q[j]>=0 for j in z['pos'])
  z['q']=q;z['packet_index']=i
  cases.append(dict(index=i,function_id=z.get('m','outer'),mathematical_size=40 if z.get('m')in D.TIERS else z.get('m',275),anchor=z['key'],offset=z['offset'],coeff=list(map(int,q)),forced=list(map(int,z['F'])),upper_indices=z['pos'],extra=z['extra'],count=len(z['X']),X_sha256=arrhash(z['X']),tops_sha256=arrhash(z['tops'])if'tops'in z else None,dependencies=[dict(function_id=p,column=j,ids_sha256=arrhash(ids))for p,ids,j in z.get('deps',[])],local_supports=[dict(id=n,column=j,ids_sha256=arrhash(ids))for n,ids,j in z.get('leafdeps',[])],conditional_dependencies=[dict(id=n,column=j,ids_sha256=arrhash(ids))for n,ids,j in z.get('pairdeps',[])],conditional_bound=z.get('pairbound')))
 packet=dict(status='FROZEN_INTEGER_COEFFICIENTS_BEFORE_STATE_EVALUATION',scale=SCALE,checkpoint_sha256=sha(checkpoint_path),checkpoint_iteration=checkpoint['iteration'],integer_rounding='Same numpy rint after original feature scaling; all bound slots and gap slot set to zero as in L repair; no alternative scales',integer_vector=list(map(int,qi)),main_functions={m:dict(mathematical_size=40 if m in D.TIERS else m,types=D.TS[m],phi=ph)for m,ph in PH.items()},conditional_types=D.T18,conditional_functions=cf,conditional_bounds=cb,conditional_support_values=cv,local_supports=local,cases=cases,finite_histograms={m:dict(types=D.TS[m],histograms=h.tolist())for m,h in HH.items()},pair18_domain=D.PAIR,conditional18_domain=D.COND,upper5_functions=upper,fixed6=D.FIXED6,first_anchor_order40=D.ORDER40,first_anchor_order106=D.ANCH[106],whole42_state_cover=cover,source_inputs=source,activation_inputs=inp,base_empty_cases=[dict(function_id=z['m'],mathematical_size=40,anchor=z['key'])for z in lower if z['empty']],shared_dependency='Copied L repair domain kernel; author replay only; root independent verification required for any positive claim')
 save('INTEGER_PACKET.json',packet);save('INTEGER_PACKET_FROZEN.json',dict(sha256=sha(W/'INTEGER_PACKET.json'),elapsed=time.monotonic()-START))
 print('INTEGER_PACKET_FROZEN',sha(W/'INTEGER_PACKET.json'),flush=True)
 bounds={};oldrows=[];cache={}
 for m in D.TIERS+[106]:
  bs=[]
  for z in [a for a in INS if a['m']==m]:
   terms=[([-v for v in PH[m]],z['tops'])]+[(PH[p],ids)for p,ids,col in z['deps']]+[(local[n]['phi'],ids)for n,ids,col in z['leafdeps']]+[(cf[n],ids)for n,ids,col in z['pairdeps']]
   vv=values(z,z['q'],terms);K=int(vv.min())
   forced=int(PH[m][z['anchor']])+dot(z['q'],z['F'])+sum(bounds[p]for p,ids,col in z['deps'])+sum(local[n]['bound']for n,ids,col in z['leafdeps'])+(cb[z['pairbound']]if z['pairdeps']else 0)
   B=forced-D.D[m]*K;bs.append(B)
   row=dict(packet_case=z['packet_index'],function_id=m,mathematical_size=40 if m in D.TIERS else m,anchor=z['key'],count=len(vv),K=K,forced=forced,bound=B,min_index=int(np.argmin(vv)))
   oldrows.append(row)
   if m==106:cache[z['key']]=(vv,row)
  bounds[m]=max(bs)
  assert bounds[m]==expected['main_bounds'][str(m)],(m,bounds[m],expected['main_bounds'][str(m)])
  guard()
 outervv=values(outer,outer['q'],[(PH[m],ids)for m,ids in outer['ids']])
 outerK=int(outervv.min());outerbase=dot(outer['q'],outer['F']);oldforced=outerbase+2*bounds[106];oldgap=364*outerK-oldforced
 assert list(map(int,outer['q']))==expected['outer'][0]['coeff']and outerK==expected['outer'][0]['K']and oldgap==expected['gaps'][0]
 save('OLD_EXACT_REPRODUCTION.json',dict(main_bounds=bounds,rows=oldrows,outer_K=outerK,outer_min_index=int(np.argmin(outervv)),outer_base_forced=outerbase,old_outer_forced=oldforced,old_gap=oldgap,matched_L_scale=SCALE))
 del outervv
 print('OLD_EXACT_MATCH',bounds,'old_gap',oldgap,flush=True)
 state_rows=[];newbs=[]
 state_dir=W/'state_indices';state_dir.mkdir(exist_ok=True)
 for c in cover['cases']:
  guard();z=nc[c['original_anchor_index']];assert list(z['key'])==c['anchor']
  assignments={v['column']:v['state']for v in c['physical42_states']}
  metadata=dict(state_case=c['id'],original_anchor_index=c['original_anchor_index'],anchor=c['anchor'],physical42_states=c['physical42_states'],packet_case=z['packet_index'],original_count=len(z['X']))
  if c['status']=='KNOWN_ROW_DOMAIN_IMPLICATION_EMPTY':
   state_rows.append(dict(metadata,status=c['status'],count=None,K=None,bound=None,source=c['known_empty_audit']));continue
  vv,oldrow=cache[z['key']];mask=np.ones(len(vv),bool);physical=[];F=z['F'].copy();changed=[]
  for name,ids,col in z['leafdeps']:
   if local[name]['m']!=42:continue
   s=assignments[col];h=D.H42[s];mask&=(h[ids]>0)
   exact=dot(h,local[name]['phi']);assert exact<=local[name]['bound']
   physical.append(dict(column=col,state=s,support_id=name,old_bound=local[name]['bound'],exact_bound=exact))
   nfixed=0
   for k,e in enumerate(z['extra'],start=7):
    if e[0]!=col or e[1]not in('upper','new_upper'):continue
    fn=e[2];u=upper[fn];assert u['size']==42 and k in z['pos']and z['q'][k]>=0
    lut=dict(zip(map(tuple,u['types']),u['values']));p=np.array([lut[t]for t in D.T42],np.int64)
    assert np.array_equal(z['X'][:,k],p[ids]);assert F[k]==e[3]==u['bound']
    exactfixed=dot(h,p);assert exactfixed<=int(F[k])
    changed.append(dict(index=k,column=col,function=fn,old_forced=int(F[k]),exact_forced=exactfixed,coefficient=int(z['q'][k]),weighted_change=int(z['q'][k])*(exactfixed-int(F[k]))))
    F[k]=exactfixed;nfixed+=1
   assert nfixed==19
  assert len(physical)==len(assignments)
  indices=np.flatnonzero(mask)
  payload=(''.join(str(int(i))+'\n'for i in indices)).encode();path=state_dir/f"state_{c['id']:02d}.txt";path.write_bytes(payload)
  common=dict(metadata,count=len(indices),indices_file=str(path.relative_to(W)),indices_sha256=sha(path),exact42_contributions=physical,exact42_fixed_features=changed)
  if not len(indices):state_rows.append(dict(common,status='EMPTY_CONDITIONAL_ZERO_FILTER_DOMAIN',K=None,bound=None));continue
  sub=vv[indices];K=int(sub.min());assert K>=oldrow['K']
  supportchange=sum(p['exact_bound']-p['old_bound']for p in physical)
  fixedchange=dot(z['q'],F)-dot(z['q'],z['F'])
  forced=oldrow['forced']+supportchange+fixedchange;B=forced-121*K
  assert B<=oldrow['bound']
  row=dict(common,status='EXACT_COMPLETE_STATE_MINIMUM',K=K,forced=forced,bound=B,old_bound=oldrow['bound'],minimum_parent_index=int(indices[int(np.argmin(sub))]),support_bound_change=supportchange,fixed_forced_change=fixedchange,forced_vector=list(map(int,F)))
  state_rows.append(row);newbs.append(B)
 assert len(state_rows)==41 and len(newbs)>0
 newB=max(newbs);newforced=outerbase+2*newB;gap=364*outerK-newforced
 result=dict(status='CANDIDATE_EXACT_POSITIVE_GAP_PENDING_INDEPENDENT_AUDIT'if gap>0 else'DETERMINISTIC_FIXED_COEFFICIENT_NULL_STOP',target=[106,106,63],minimum_scope='Q67-global-minimum NC/NC/* only',scale=SCALE,integer_packet_sha256=sha(W/'INTEGER_PACKET.json'),old_main_bounds=bounds,new_B106=newB,old_B106=bounds[106],old_gap=oldgap,gap=gap,outer_K=outerK,outer_base_forced=outerbase,outer_forced=newforced,outer_count=len(outer['X']),state_rows=state_rows,formal_state_count=41,known_old_empty_count=3,new_conditional_empty_count=sum(r['status']=='EMPTY_CONDITIONAL_ZERO_FILTER_DOMAIN'for r in state_rows),nonempty_state_count=len(newbs),state_row_total=sum(r['count']or 0 for r in state_rows),maximizing_state_cases=[r['state_case']for r in state_rows if r.get('bound')==newB],integer_product_ceiling=max(CEILINGS),optimizer_calls=0,number_of_scale_evaluations=1,elapsed=time.monotonic()-START,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 save('RESULT.json',result)
 for name,h in inp['source_hashes'].items():assert sha(R/name)==h
 for name,h in source['source_hashes'].items():assert sha(R/name)==h
 guard();print('FINAL',json.dumps({k:result[k]for k in ['status','new_B106','old_B106','old_gap','gap','new_conditional_empty_count','nonempty_state_count','state_row_total','maximizing_state_cases','elapsed','peak_rss_bytes']}),flush=True)
 signal.alarm(0)
if __name__=='__main__':main()
