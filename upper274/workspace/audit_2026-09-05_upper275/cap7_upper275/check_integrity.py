#!/usr/bin/env python3
from pathlib import Path
import hashlib,zipfile
D=Path(__file__).resolve().parent
archive=D/'baseline276_certificate.zip'
expected='a6fbdf4ec26711a0dce6fb5164a66da92f754b7b18350c45866ee57458e4f86e'
if hashlib.sha256(archive.read_bytes()).hexdigest()!=expected:raise AssertionError('Baseline276 archive was modified')
n=0
with zipfile.ZipFile(archive) as z:
    prefix='cap7_upper276/baseline277/'
    for name in z.namelist():
        if not name.startswith(prefix) or name.endswith('/'):continue
        dest=D/'baseline277'/name[len(prefix):]
        if dest.read_bytes()!=z.read(name):raise AssertionError(f'Baseline dependency changed: {name}')
        n+=1
if not n:raise AssertionError('No baseline files checked')
print(f'PASS: original276 archive hash and {n} preserved dependency files.')
