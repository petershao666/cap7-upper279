import hashlib
import json
from pathlib import Path

here=Path(__file__).resolve().parent
source=here.parents[1]/'root_audit'/'fortyfive'/'ACCEPTED_POINTS.json'
raw=source.read_bytes()
packet=json.loads(raw)
points=sorted(tuple(p) for p in packet['points'])
assert len(points)==len(set(points))==45
assert all(len(p)==5 and all(x in (0,1,2) for x in p) for p in points)
(here/'COORDINATES.tsv').write_text(''.join('\t'.join(map(str,p))+'\n' for p in points))
out={'source_file':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),'point_order':'lexicographic five-coordinate tuple order','point_count':45,'coordinate_file':'COORDINATES.tsv','coordinate_file_sha256':hashlib.sha256((here/'COORDINATES.tsv').read_bytes()).hexdigest(),'source_status':packet['status'],'shared_dependency':'accepted 45-point coordinates and published affine uniqueness only'}
(here/'INPUT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
