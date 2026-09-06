#!/usr/bin/env python3
"""Compare all exact case outputs from the two complete implementations."""
import re
from pathlib import Path
D=Path(__file__).resolve().parent
pat=re.compile(r'^(n=|NEAR112 |NEW INNER |NEW BRANCH |LOWER INPUTS |RARE108 |HISTOGRAM108 |NEW ORDINARY |NEW ROOT |NEW COMPUTATIONS |FULL PASS:)')
a=[s for s in (D/'python_verification.txt').read_text().splitlines() if pat.match(s)]
b=[s for s in (D/'cpp_verification.txt').read_text().splitlines() if pat.match(s)]
if a!=b:
 for i,(x,y) in enumerate(zip(a,b)):
  if x!=y:raise AssertionError(f'Exact-output mismatch at {i}:\n{x}\n{y}')
 raise AssertionError(f'Output lengths differ: {len(a)} vs {len(b)}')
if not a or not a[-1].startswith('FULL PASS:'):raise AssertionError('Missing full pass')
print(f'PASS: all {len(a)} exact case/summary lines agree, including every local count, minimum, and gap.')
