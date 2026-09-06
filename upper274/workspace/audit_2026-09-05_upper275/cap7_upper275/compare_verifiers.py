#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
D=Path(__file__).resolve().parent
prefix=('DELETED2','STEP ','HISTOGRAM ','AUX41 ')
def lines(name):
    return Counter(x.strip() for x in (D/name).read_text().splitlines() if x.startswith(prefix))
if not (D/'python_verification.txt').is_file():
    raise SystemExit('No completed Python log is included. Run python3 verify.py > python_verification.txt before full comparison; the supplied partial log is not a full pass.')
a,b=lines('python_verification.txt'),lines('cpp_verification.txt')
if a!=b: raise AssertionError(f'Verifier disagreement: Python-only={a-b}; C++-only={b-a}')
if not any(x.startswith('STEP FULL PASS: no 276-point cap;') for x in a):raise AssertionError('Missing full-pass line')
print(f'PASS: {sum(a.values())} matching exact computation lines.')
