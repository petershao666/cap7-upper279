"""Data-only normalization for the independently written Ruby pointed checker."""
from pathlib import Path
import json,hashlib,copy
W=Path(__file__).resolve().parent;R=W.parent;P=R/'root_potential'
d=json.loads((P/'pointed_joint_certificate.json').read_text());original=json.loads((P/'pointed_result.json').read_text())
assert hashlib.sha256((P/'pointed_joint_certificate.json').read_bytes()).hexdigest()=='e0760693846143cf36a99d43a31aa7c7253cc39ebf1408bb92324a9c6256334b'
assert d['cover_source_sha256']==hashlib.sha256((P/'pointed_result.json').read_bytes()).hexdigest()
newid='P3B_conditional107';normal=copy.deepcopy(original);normal['source_functions']=[newid]
normal['new_target']={'id':newid,'m':107,'types':d['types'],'phi':d['phi'],'bound':d['conditional_bound']}
extra=['P3_nested107_size276_to108','P3_nested107_size277_to108','P3_joint107_107_106_63_size276_to108']
normal['input_108_functions']+=extra
seen=[]
for r in normal['ledger']:
 if r['status']!='ENUMERATED':continue
 z=next(x for x in d['inner'] if x['anchor']==r['anchor107'] and x['marked_column']==r['marked_column'])
 assert z['count']==r['count'];seen.append((z['anchor'],z['marked_column']))
 for k in ['features','positive','forced']:r[k]=z[k]
 r['results']=[{'id':newid,'certificate':{'coeff':z['coeff'],'denominator':1,'K':z['K'],'bound_numerator':z['bound']}}]
assert len(seen)==len(d['inner'])==6
normal['conditional_bounds']=[{'id':newid,'numerator':d['conditional_bound'],'denominator':1}]
normal['original_joint_sha256']=hashlib.sha256((P/'pointed_joint_certificate.json').read_bytes()).hexdigest()
(W/'pointed_joint_audit_input.json').write_text(json.dumps(normal,indent=2)+'\n')
# Reuse the root's previously independent mathematical enumeration, explicitly
# recording this shared checker dependency rather than calling it a new kernel.
s=(W/'verify_pointed.rb').read_text()
s=s.replace("path=File.join(R,'root_potential/pointed_result.json');data=readj(path)","path=File.join(W,'pointed_joint_audit_input.json');data=readj(path)\nreadj(File.join(R,'root_potential/pointed_transfer_tables.json'))['functions'].each{|h|lookup[h['id']]=h.merge('lookup'=>h['types'].zip(h['phi']).to_h)}\nh=data['new_target'];lookup[h['id']]=h.merge('lookup'=>h['types'].zip(h['phi']).to_h)\nck(h['types']==lookup['nested107_size276']['types'],'new function full support')")
s=s.replace("anchors=targets.first['inner'].map{|c|c['type']}","anchors=lookup['nested107_size276']['inner'].map{|c|c['type']}")
s=s.replace("bounds[h['id']]<<[Rational(num,c['denominator']),h['bound']].min","bounds[h['id']]<<Rational(num,c['denominator'])")
s=s.replace("&&bd<lookup[r['id']]['bound']","&&bd==lookup[r['id']]['bound']")
s=s.replace("'pointed_independent.json'","'pointed_joint_independent.json'")
s=s.replace("Three improved bounds for NC107 caps admitting a common marked extension to NC108; not unconditional107 bounds, not a7D exclusion","New P3b histogram bound for NC107 caps admitting an NC108 extension; not an unconditional107 bound; outer exclusion checked separately")
s=s.replace("certificate_sha256:Digest::SHA256.file(path).hexdigest,","certificate_sha256:Digest::SHA256.file(path).hexdigest,original_joint_sha256:data['original_joint_sha256'],")
(W/'verify_pointed_joint.rb').write_text(s)
print('Prepared independent checker input for six new local bounds plus inherited21-stratum coverage.')
