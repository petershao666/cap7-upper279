#!/usr/bin/env python3
"""Compare the complete recorded runs, excluding only elapsed-time reporting."""
from pathlib import Path
D=Path(__file__).resolve().parent

def normalized(path):
    lines=path.read_text().splitlines()
    assert any(line.startswith('FULL PASS:') for line in lines), f'Incomplete run: {path}'
    assert 'Under the published mathematical inputs in README.md, no 279-point cap exists; 236 <= f(7,3) <= 278.' in lines
    return [s for s in lines if not s.startswith('Elapsed verification seconds:')]
a=normalized(D/'python_verification.txt');b=normalized(D/'cpp_verification.txt')
assert a==b,'The runs disagree. Compare the logs before accepting the certificate.'
print(f'PASS: all {len(a)} non-timing output lines agree exactly.')
