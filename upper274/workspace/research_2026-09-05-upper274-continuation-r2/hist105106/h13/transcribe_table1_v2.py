# Corrected 981H / 990A3 from primary HTML S3.T1.1.12.4, math S3.T1.m211, alttext 3.
from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent
labels=['990A1','990A2','990A3','990B']+['981'+c for c in 'ABCDEFGHIJ']+['972A','963A','963B','954A','882A1','882A2','19-cap','20-cap']
rows=[
[5],
[2,4],
[3,3,4],
[4,3,3,4],
[4,3,3,4,5],
[4,4,4,4,4,4],
[4,3,3,4,4,4,4],
[4,3,4,4,4,4,4,4],
[4,3,3,4,4,4,4,4,4],
[4,4,3,4,4,4,4,4,4,4],
[4,3,3,3,4,3,4,4,4,4,4],
[4,4,3,4,4,4,4,4,4,4,4,4],
[3,4,3,4,4,4,4,4,4,4,4,4,4],
[3,3,3,3,4,3,3,4,4,4,4,4,4,4],
[4,3,4,4,4,4,4,4,4,4,4,4,4,4,5],
[4,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
[4,3,4,4,4,3,4,4,4,4,4,4,4,4,4,4,6],
[4,4,4,4,4,4,3,3,4,3,4,4,4,4,4,4,4,4],
[4,3,4,3,4,3,3,3,3,3,3,3,3,3,4,4,4,5,9],
[4,5,4,4,3,4,4,4,4,4,4,4,5,3,4,4,3,4,3,9],
[2,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,2],
[2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,1,1]]
assert len(rows)==22 and all(len(r)==i+1 for i,r in enumerate(rows));mat=[[rows[max(i,j)][min(i,j)]for j in range(22)]for i in range(22)]
z={'source_url':'https://arxiv.org/html/2206.09719v1#S3.T1','source_table':'Table1, proof ofLemma3.1(a,b)','semantics':'Maximum size of a middle4-flat cap given the affineclasses of two parallelouter4-flat caps; allplacements/linearorientations checked inpublishedsource. Uppercapacity is sufficient; no newclassification claim.','label_order':labels,'lower_triangular_rows':rows,'symmetric_capacity_matrix':mat,'independent_entries':253,'row_sizes':[18]*20+[19,20]}
(W/'table1_input_v2.json').write_text(json.dumps(z,indent=2)+'\n');print('Table1',len(labels),'labels',sum(map(len,rows)),'entries',hashlib.sha256((W/'table1_input_v2.json').read_bytes()).hexdigest())
ST=json.loads((W.parent/'h10/full18_states.json').read_text());ix={s:i for i,s in enumerate(labels)}
M=[[max(mat[ix[a]][ix[b]]for a in x['classes']for b in y['classes'])for y in ST]for x in ST]
HP={'histogram_states':ST,'max_capacity_by_full18_histogram_pair':M,'allowed_18184_ordered_pairs':[[i,j]for i in range(17)for j in range(17)if M[i][j]>=4],'allowed_19183_full18_states':[i for i,h in enumerate(ST)if max(mat[ix[a]][20]for a in h['classes'])>=3],'allowed_20182_full18_states':[i for i,h in enumerate(ST)if max(mat[ix[a]][21]for a in h['classes'])>=2]}
(W/'histogram_pair_capacity_v2.json').write_text(json.dumps(HP,indent=2)+'\n');print('allowed18184',len(HP['allowed_18184_ordered_pairs']),'of289;19183',len(HP['allowed_19183_full18_states']),'20182',len(HP['allowed_20182_full18_states']))
