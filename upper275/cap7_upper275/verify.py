#!/usr/bin/env python3
"""Complete exact verifier for the upper bound 275."""
import sys
from verify_step import main
if __name__ == '__main__':
    if len(sys.argv)>1: raise SystemExit('Run without arguments; this release verifies target size 276.')
    sys.argv.append('276')
    main()
