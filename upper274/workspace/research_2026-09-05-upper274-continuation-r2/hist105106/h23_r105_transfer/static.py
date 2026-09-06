from pathlib import Path
from fractions import Fraction as F
import json,hashlib,math,time
W=Path(__file__).resolve().parent;R=W.parents[1];start=time.monotonic()
paths=['compatibility/fixed_nc106_outer_probe/FUNCTIONS.json','compatibility/r105_fixed_outer/FUNCTIONS.json','root_audit/r105_functions.json','compatibility/r105_fixed_outer/DELETION_CHECK.json','root_audit/complete41/ACCEPTED_HISTOGRAMS.json','hist105106/h22_complete41/h22_result.json']
docs={p:json.loads((R/p).read_text())for p in paths};old={z['id']:z for z in docs[paths[0]]['functions']if z['size']==106};new={z['id']:z for z in docs[paths[1]]['functions']if z['size']==106}
T=sorted(map(tuple,next(iter(old.values()))['types']));assert len(T)==79
maps={n:dict(zip(map(tuple,z['types']),z['values']))for n,z in new.items()};assert all(set(m)==set(T)for m in maps.values())
for n,z in old.items():assert dict(zip(map(tuple,z['types']),z['values']))==maps[n]and z['bound']==new[n]['bound']
name='R105_inner_to106_floor1000000';phi=[maps[name][t]for t in T]
# Independent exact rational row-reduction, preserving a pivot-column witness.
def rank(a):
 a=[[F(x)for x in row]for row in a];rank=0;piv=[]
 for j in range(len(a[0])):
  k=next((i for i in range(rank,len(a))if a[i][j]),None)
  if k is None:continue
  a[rank],a[k]=a[k],a[rank];v=a[rank][j];a[rank]=[x/v for x in a[rank]]
  for i in range(len(a)):
   if i!=rank and a[i][j]:v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[rank])]
  piv.append(j);rank+=1
  if rank==len(a):break
 return rank,piv
moment_rows=[[1]*79,[a*b+a*c+b*c for a,b,c in T],[a*b*c for a,b,c in T]];moment_bounds=[364,243*math.comb(106,2),81*math.comb(106,3)]
oldnames=list(old);base=moment_rows+[[maps[n][t]for t in T]for n in oldnames]
r0,p0=rank(base);r1,p1=rank(base+[phi]);bbase=[row+[bd]for row,bd in zip(base,moment_bounds+[new[n]['bound']for n in oldnames])];rb0,pb0=rank(bbase);rb1,pb1=rank(bbase+[phi+[new[name]['bound']]])
full=new['L4_fixed_inner_NC106'];floor=new['L4_fixed_inner_NC106_floor10000'];residual=[maps[full['id']][t]-10000*maps[floor['id']][t]for t in T];br=full['bound']-10000*floor['bound']
source_functions={z['id']:z for z in docs['root_audit/r105_functions.json']['functions']}
source105=source_functions['R105_inner'];source106=source_functions['R105_inner_to106'];lut105=dict(zip(map(tuple,source105['types']),source105['phi']));lut106=dict(zip(map(tuple,source106['types']),source106['phi']))
formula_rows=[]
for t in T:
 terms=[]
 for i,n in enumerate(t):
  if not n:continue
  u=list(t);u[i]-=1;u=tuple(sorted(u,reverse=True));assert u in lut105
  terms.append(dict(physical_section=i,multiplicity=n,profile105=u,value105=lut105[u]))
 value=sum(q['multiplicity']*q['value105']for q in terms);assert value==lut106[t]and value//1000000==maps[name][t]
 formula_rows.append(dict(profile106=t,terms=terms,unfloored=value,floor1000000=value//1000000))
assert source106['bound']==106*source105['bound']and source106['bound']//1000000==new[name]['bound']
def determinant(a):
 a=[list(map(int,r))for r in a];den=1;sign=1
 for k in range(len(a)-1):
  pivot=next(i for i in range(k,len(a))if a[i][k])
  if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sign=-sign
  q=a[k][k]
  for i in range(k+1,len(a)):
   for j in range(k+1,len(a)):
    v=a[i][j]*q-a[i][k]*a[k][j];assert v%den==0;a[i][j]=v//den
  for i in range(k+1,len(a)):a[i][k]=0
  den=q
 return sign*a[-1][-1]
minor=[[row[j]for j in p1]for row in base+[phi]];det=determinant(minor);assert det
(W/'TRANSFER_FORMULA.json').write_text(json.dumps(dict(status='PASS_DIRECT_WEIGHTED_DELETION_AND_INTEGER_FLOOR',source105_bound=source105['bound'],source106_bound=source106['bound'],floored106_bound=new[name]['bound'],rows=formula_rows,NC_preservation_premise='accepted103extensionrigidity'),indent=2)+'\n')
result={'status':'EXACT_STATIC_CORRESPONDENCE_NO_OPTIMIZATION','old106_function_ids':oldnames,'additional106_function_ids':[n for n in new if n not in old],'new_proposed_function':name,'new_bound':new[name]['bound'],'types':T,'new_values':phi,'old_values_and_bounds_match_exactly':True,'coefficient_rank':{'old_plus_exact_moments':r0,'with_R105_transfer':r1,'pivot_profile_indices':p1},'augmented_bound_rank':{'old_plus_exact_moments':rb0,'with_R105_transfer':rb1,'pivot_columns':pb1},'L4_full_floor':{'divisor':10000,'residual_values':residual,'residual_min':min(residual),'residual_max':max(residual),'bound_residual':br,'all_coefficients_exactly_scaled':all(v==0 for v in residual)},'nonzero_minor_witness':{'row_labels':['constant','E2','E3']+oldnames+[name],'profile_columns':[T[j]for j in p1],'matrix':minor,'determinant':str(det)},'limitation':'Rank nonmembership rules out exact linear recombination/rescaling; it does not establish non-implication from the full old inequality cone or the finite outer domain.','source_hashes':{p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in paths},'elapsed':time.monotonic()-start,'LP_runs':0}
(W/'STATIC_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['types','new_values','source_hashes','L4_full_floor']}));print('L4 residues',min(residual),max(residual),'bound residue',br)
print('r105_source_schema',docs['root_audit/r105_functions.json'].keys())
