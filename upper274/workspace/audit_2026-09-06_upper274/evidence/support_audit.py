"""Read-only, fresh integer audit of the frozen final certificate's support algebra.

No imports from the research tree; no coefficient discovery; no raw-domain replay.
The existing checker sources were read to understand the certificate schema.
"""
from pathlib import Path
from collections import Counter
from math import comb, prod
import hashlib, json, time

R = Path('/Users/hengshao/Desktop/math/research_2026-09-05-upper274-continuation-r2')
OUT = Path(__file__).resolve().parent
INPUTS = {}
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    p = p if isinstance(p, Path) else R/p
    INPUTS[str(p)] = digest(p)
    return json.loads(p.read_text())
def ensure(test, message):
    if not test: raise AssertionError(message)
def mapping(types, values):
    ensure(len(types) == len(values), 'vector length')
    ensure(all(type(x) is int for x in values), 'integer values')
    result = {tuple(t): v for t, v in zip(types, values)}
    ensure(len(result) == len(types), 'distinct types')
    return result
def dot(spectrum, function):
    ensure(all(t in function for t,v in spectrum.items() if v), 'function support')
    return sum(v * function[t] for t,v in spectrum.items() if v)
def dense_family(packet):
    return [mapping(packet['types'], v['counts'] if isinstance(v,dict) else v)
            for v in packet['histograms']]

start = time.monotonic()
C_PATH = R/'compatibility/two_local_theta400_certificates/RESULT.json'
C = read(C_PATH)
EXPECTED = '78238a2e3f389f9c7a4f93e049ad56e678c09103151fb3bfed0adc6e1dcf14bf'
ensure(digest(C_PATH) == EXPECTED, 'candidate digest')
base = read(R.parent/'audit_2026-09-05_upper275/cap7_upper275/baseline277/baseline278/certificate.json')
packets = {n:read(f'root_audit/{name}/ACCEPTED_HISTOGRAMS.json') for n,name in
           [(16,'actual16'),(17,'actual17'),(41,'complete41')]}
states = read('hist105106/h10/full18_states.json')
ensure(C['full18_states'] == states, '18 states source')
families = {n:dense_family(p) for n,p in packets.items()}
families[18] = [mapping(s['types'],s['histogram']) for s in states]
families[42] = [mapping(base['spectrum5']['42']['types'], s) for s in base['spectrum5']['42']['spectra']]
ensure(C['complete42'] == base['spectrum5']['42'], '42 embedded equality')
ensure(C['complete41'] == packets[41], '41 embedded equality')
for n in [16,17]:
    embedded=dense_family(C[f'actual{n}'])
    ensure({tuple(sorted(h.items())) for h in embedded} == {tuple(sorted(h.items())) for h in families[n]}, '16/17 embedded histogram equality ignoring order/metadata')
for n, family in families.items():
    D = 40 if n < 40 else 121
    ensure(len({tuple(sorted(h.items())) for h in family}) == len(family), 'distinct histograms')
    for h in family:
        ensure(all(type(v) is int and v >= 0 for v in h.values()), 'nonnegative counts')
        ensure(all(sum(t) == n and tuple(sorted(t,reverse=True)) == t for t in h), 'histogram type')
        ensure(sum(h.values()) == D, 'direction count')
        ensure(sum(v*sum(comb(x,2) for x in t) for t,v in h.items()) == ((D-1)//3)*comb(n,2), 'second moment')
        ensure(sum(v*sum(comb(x,3) for x in t) for t,v in h.items()) == ((D-4)//9)*comb(n,3), 'third moment')

capacity = read('hist105106/h13/table1_input_v2.json')
ensure(capacity == C['table1'], 'table 1 embedded equality')
labels = {s:i for i,s in enumerate(capacity['label_order'])}
table = capacity['symmetric_capacity_matrix']
ensure(all(table[i][j] == table[j][i] for i in range(len(table)) for j in range(len(table))), 'symmetric capacity')
pairs = [(i,j) for i,a in enumerate(states) for j,b in enumerate(states)
         if any(table[labels[x]][labels[y]] >= 4 for x in a['classes'] for y in b['classes'])]
conditional = [i for i,a in enumerate(states) if any(table[labels[x]][labels['20-cap']] >= 2 for x in a['classes'])]
ensure(pairs == [tuple(x) for x in C['histogram_pair_capacity']['allowed_18184_ordered_pairs']], 'pair capacity')
ensure(conditional == C['histogram_pair_capacity']['allowed_20182_full18_states'], 'conditional capacity')
cover = {(9,8,0),(9,7,1),(8,8,1)}
ensure(all(sum(h.get(t,0) for t in cover) >= 1 for h in families[17]), '17 direction cover')

supports = {}
support_evaluations = 0
for name,z in C['local_supports'].items():
    fn = mapping(z['types'],z['phi'])
    values = [dot(h,fn) for h in families[z['m']]]
    ensure(max(values) == z['bound'], f'local support maximum {name}')
    support_evaluations += len(values)
    supports[name] = {'maximum':max(values),'evaluations':len(values),'size':z['m']}
conditionals = {name:[dot(h,mapping(C['conditional_types'],v)) for h in families[18]]
                for name,v in C['conditional_functions'].items()}
for tier in [400,401,402]:
    left,right,cond = [f't{tier}_{s}' for s in ['left18','right18','cond18']]
    ensure(max(conditionals[left][i]+conditionals[right][j] for i,j in pairs) == C['conditional_bounds'][f't{tier}_pair18'], 'pair maximum')
    ensure(max(conditionals[cond][i] for i in conditional) == C['conditional_bounds'][cond], 'conditional maximum')
    support_evaluations += len(pairs)+len(conditional)

upper_audit = {}
h3 = read('hist105106/h3/h3_result.json')['histograms']['40']
for name,z in C['upper5'].items():
    fn = mapping(z['types'],z['phi'])
    if z['m'] == 40:
        old = mapping(h3['types'],h3['phi'])
        ensure(fn == {t:v+10**10 for t,v in old.items()}, '40 exact centering')
        ensure(z['bound'] == h3['bound']+121*10**10, '40 bound centering')
        upper_audit[name] = {'method':'exact centering of inherited H3 bound','bound':z['bound']}
    else:
        vals = [dot(h,fn) for h in families[z['m']]]
        ensure(max(vals) <= z['bound'], f'upper validity {name}')
        upper_audit[name] = {'method':'all accepted histograms','bound':z['bound'],'maximum':max(vals),'evaluations':len(vals)}

hist19_20 = read('hist105106/h3/hist19_20.json')
tiers = {400:[43,40,23],401:[44,40,22],402:[45,40,21]}
usage = Counter()
upper_signs = 0
exact_features = 0
derived = {}
case_rows = []
for key, obj in C['histograms'].items():
    n = obj['mathematical_size']; keyint = int(key)
    ensure(n == (106 if keyint==106 else 40), 'mathematical size')
    phi = mapping(obj['types'],obj['phi'])
    if keyint in tiers:
        ensure(C['tier_mapping'][key] == {'mathematical_size':40,'parent':tiers[keyint],'physical_column':1}, 'tier metadata')
        ensure(obj['tier_parent'] == tiers[keyint], 'tier parent')
        complete_types={(a,b,40-a-b) for a in range(21) for b in range(a+1) if 0<=40-a-b<=b}
        ensure(set(phi)==complete_types and len(complete_types)==44, 'complete40 type coverage')
        ensure({tuple(v['type']) for v in obj['inner']} == complete_types-{(14,13,13)} and len(obj['inner'])==43, '43 nonempty40 anchor cases')
    else:
        ensure(len(obj['inner'])==len({tuple(v['type']) for v in obj['inner']})==14, '14 distinct106 anchors')
    local_bounds = []
    for row in obj['inner']:
        anchor = row['type']; q = row['coeff']; extra = row['extra']
        ensure(sum(anchor)==n and len(q)==7+len(extra), 'row shape')
        ensure(all(type(x) is int for x in q), 'integer coefficients')
        fact = (13,27,9,40) if n==40 else (40,81,27,121)
        F = [fact[0]*prod(anchor)]
        for size in anchor: F.extend([fact[1]*comb(size,2),fact[2]*comb(size,3)])
        F.extend(e[3] for e in extra)
        for coeff,(col,kind,tag,bound) in zip(q[7:],extra):
            ensure(col in range(3), 'physical column index')
            if kind in ['exact','exact4']:
                packet = hist19_20[str(anchor[col])] if kind=='exact4' else base['spectrum5'][str(anchor[col])]
                counts = packet.get('histogram',packet.get('spectra',[None])[0])
                ensure(counts[packet['types'].index(tag)] == bound, 'exact feature value')
                if kind=='exact': ensure(len(packet['spectra'])==1, 'single exact spectrum')
                exact_features += 1
            else:
                ensure(coeff >= 0, 'upper coefficient sign'); upper_signs += 1
                if kind=='direction_cover':
                    ensure(anchor[col]==17 and set(map(tuple,tag))==cover and bound==-1, 'direction cover matching')
                else:
                    ensure(kind in ['upper','new_upper'], 'upper kind')
                    z=C['upper5'][tag]
                    ensure(z['m']==anchor[col] and z['bound']==bound, 'upper function physical size/bound')
        child = 0
        for term in row['local_supports']:
            z = C['local_supports'][term['id']]; col=term['column']
            ensure(term['coefficient']==1 and z['column']==col and z['m']==anchor[col], 'local physical scope')
            ensure(z['anchor']==anchor and z['case_dimension_size']==keyint, 'local anchor scope')
            child += z['bound']; usage[term['id']] += 1
        for term in row['dependencies']:
            tier=term['m'];col=term['column']
            ensure(term['coefficient']==1 and tier in tiers and tiers[tier]==anchor and col==1, 'tier physical scope')
            child += derived[str(tier)]
        conditional_terms = row['conditional_dependencies']
        if conditional_terms:
            expected = ([{'column':0,'function':f't{key}_left18','coefficient':1},{'column':1,'function':f't{key}_right18','coefficient':1}]
                        if anchor==[18,18,4] else [{'column':1,'function':f't{key}_cond18','coefficient':1}])
            ensure(conditional_terms==expected, 'conditional physical columns')
            boundname = f't{key}_pair18' if anchor==[18,18,4] else f't{key}_cond18'
            ensure(row['conditional_bound']==boundname, 'conditional bound mapping')
            child += C['conditional_bounds'][boundname]
        else: ensure(row['conditional_bound'] is None, 'unused conditional bound')
        value = phi[tuple(anchor)] + sum(a*b for a,b in zip(q,F)) + child - fact[3]*row['K']
        ensure(value==row['bound'], 'local summed upper identity')
        local_bounds.append(value)
        case_rows.append({'tier':keyint,'anchor':anchor,'q_dot_F':sum(a*b for a,b in zip(q,F)),'children':child,'bound':value})
    derived[key] = max(local_bounds)
    ensure(derived[key]==obj['bound'], 'universal maximum')
ensure(usage == Counter({name:1 for name in C['local_supports']}), 'every support used exactly once')
ensure(len(case_rows)==143, 'local bound count')
outer, = C['outer']; a=outer['type']; q=outer['coeff']
ensure(a==[106,106,63] and len(q)==19, 'outer shape')
ensure(all(v==0 for v in q[7:]), 'outer upper rows vanish')
F=[121*prod(a)]
for n in a: F.extend([243*comb(n,2),81*comb(n,3)])
U=sum(x*y for x,y in zip(q[:7],F))+2*derived['106']
gap=364*outer['K']-U
ensure(U==outer['forced'] and gap==outer['gap'] and gap>0, 'strict outer contradiction')

freeze_checks=[]
def hashes(packet, field, root):
    for name,value in packet[field].items():
        p=Path(name) if name.startswith('/') else root/name
        ensure(digest(p)==value, f'freeze mismatch {p}')
        freeze_checks.append(str(p))
candidate_freeze=read('compatibility/two_local_theta400_certificates/CANDIDATE_FROZEN.json')
ensure(candidate_freeze['result_sha256']==EXPECTED,'candidate freeze binding')
hashes(candidate_freeze,'source_hashes',C_PATH.parent)
raw=read('root_audit/three40_complete42/ROOT_RAW_VERIFICATION.json')
hashes(raw,'accepted_input_hashes',R);hashes(raw,'input_hashes',R)
logical=read('hist105106/final274_logic_audit/FROZEN.json')
ensure(logical['candidate_sha256']==EXPECTED,'logic freeze binding')
hashes(logical,'sha256',R/'hist105106/final274_logic_audit')
ncsource=read('root_potential/three40_complete42_nc106_verify/SOURCE_AND_SUPPORT_VERIFICATION.json')
hashes(ncsource,'source_hashes',R)

result={'status':'PASS_FRESH_STDLIB_FINITE_SUPPORT_AND_143_SUMMED_BOUNDS',
 'classification':'REPLICATION_NO_NEW_MATH','certificate_sha256':EXPECTED,
 'family_sizes':{n:len(v) for n,v in families.items()},'conditional_pair_count':len(pairs),
 'conditional_single_count':len(conditional),'local_support_count':len(supports),
 'local_support_and_conditional_evaluations':support_evaluations,
 'support_maxima':supports,'upper_functions':upper_audit,'upper_signs_checked':upper_signs,
 'exact_features_checked':exact_features,'summed_case_count':len(case_rows),'case_rows':case_rows,
 'universal_bounds':derived,'outer_K':outer['K'],'outer_forced':U,'positive_gap':gap,
 'zero_fixed_outer_coefficients':12,'freeze_hash_checks':len(freeze_checks),
 'distinct_frozen_files_checked':len(set(freeze_checks)),
 'frozen_files_checked':freeze_checks,'inputs':INPUTS,
 'shared_dependencies':['Same frozen RESULT.json coefficients and accepted histogram/classification inputs',
 'Existing checker source was read for schema and formula interpretation; no checker functions imported or run',
 'H3 centered-theta40 upper theorem inherited; final raw-domain replay delegated to root',
 'Classification completeness and global branch coverage are separate logical-audit premises'],
 'not_verified_here':['Raw pointwise minima / exhaustive domain generation',
 'Independent reconstruction or published completeness of low-dimensional classifications',
 'Global bridge and the seven earlier branch certificates'],
 'elapsed_seconds':time.monotonic()-start,'own_code_sha256':digest(Path(__file__))}
(OUT/'support_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['support_maxima','upper_functions','case_rows','inputs','frozen_files_checked']},indent=2))
