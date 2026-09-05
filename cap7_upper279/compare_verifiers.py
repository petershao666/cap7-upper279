#!/usr/bin/env python3
"""Compare recorded exact verification outputs, ignoring timing and line order.
This compares the supplied execution logs, not new verifier executions.
"""
from collections import Counter
from pathlib import Path

def main() -> None:
    root=Path(__file__).parent
    def read(name):
        return Counter(line for line in (root/name).read_text().splitlines()
                       if line and not line.startswith('Elapsed verification seconds:'))
    py=read('python_verification.txt'); cpp=read('cpp_verification.txt')
    if py!=cpp:
        raise AssertionError(f'Different records. Python only: {py-cpp}; C++ only: {cpp-py}')
    cases=sum(n for line,n in py.items() if line.startswith('n='))
    if cases!=155:
        raise AssertionError(f'Unexpected number of local cases: {cases}')
    print('PASS: both recorded outputs agree on all 155 cases, spectrum checks, stage counts, root contradiction, and matrix totals.')
if __name__=='__main__':
    main()
