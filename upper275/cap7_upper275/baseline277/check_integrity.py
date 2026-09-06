#!/usr/bin/env python3
"""Check release hashes and the byte-for-byte preserved baseline."""
from pathlib import Path
import hashlib,json,zipfile
D=Path(__file__).resolve().parent
hashes=D/'SHA256SUMS.txt'
if not hashes.exists():raise SystemExit('SHA256SUMS.txt is missing')
count=0
for line in hashes.read_text().splitlines():
 digest,name=line.split('  ',1);p=D/name
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
  raise AssertionError('Missing or changed release file: '+name)
 count+=1
C=json.loads((D/'certificate.json').read_text())
p=D/'baseline278_certificate.zip'
assert hashlib.sha256(p.read_bytes()).hexdigest()==C['baseline_sha256']
with zipfile.ZipFile(p) as z:
 for name in z.namelist():
  rel=Path(name).relative_to('cap7_upper278')
  assert (D/'baseline278'/rel).read_bytes()==z.read(name),rel
print(f'INTEGRITY PASS: {count} release files and every preserved baseline file match their hashes/bytes.')
