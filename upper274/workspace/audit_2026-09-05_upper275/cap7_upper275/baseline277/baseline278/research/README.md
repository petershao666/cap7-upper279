# Optional discovery helpers

The parent proof is reproduced with `python3 verify.py` or the C++ verifier, without these dependencies. This directory instead preserves a parameterized implementation of the local matrix and separating-inequality discovery step used in the improvement.

`engine.py` enumerates the relevant count matrices and uses linear programming with row generation to propose a separating functional. It converts candidate coefficients to integers and checks them on the full deduplicated feature family. This deduplication is a discovery optimization only: neither final verifier deduplicates matrices.

`rediscover.py` can propose ordinary seven-dimensional certificates, completion-status branch certificates, six-dimensional conditional completion certificates, and final seven-dimensional root inequalities. It uses the already proved restrictions in the parent certificate, and for a case already in that certificate it permits only completed **earlier** stages of its dimension.

Examples from the package root:

```bash
python3 -m pip install -r research/requirements.txt
python3 research/rediscover.py --case 108 108 63 --status 1 1
python3 research/rediscover.py --case 108 108 63 --status 0 0
python3 research/rediscover.py --dimension 6 --case 44 43 22
python3 research/rediscover.py --root 279
```

The requirements file records the versions used for these discovery-helper tests, not requirements for the mathematical verifier. There may be multiple valid separating vectors, so different optimizer versions need not choose identical coefficients. The correctness criterion is the exact exported inequality, not reproducing a specific optimizer path or decimal solution.

`base_certificate.json` preserves the preceding upper-279 certificate as the source of the inherited 97 universal six-dimensional restrictions and the five-dimensional histogram families. It is not a discovery program for those earlier 97 inequalities. The complete parent verifier repeats their exact verification, together with all added restrictions.

For later work the target size and candidate types can be varied. The current helpers are not a guarantee of further decreases and are not a complete automated search strategy: new constraints or geometric lemmas may be needed. Their built-in 109-completion restriction and conditional completion patterns are justified by the **completed parent proof**, not conjectural assumptions. In a six-dimensional completion search the lower-dimensional predicate is Adm5, so the 109 theorem is not used to prove itself.

An unsuccessful separation attempt means only that this attempt did not return an integer certificate. A feasible matrix-moment relaxation is not evidence that a cap with that size exists. Every proposed extension still needs a well-founded geometric reduction, a complete case split where used, an exhaustive exact check, and a new root contradiction.

The separate small auxiliary discovery can also be reproduced:

```bash
python3 research/discover_two112.py --output research/rediscovered_two112.json
python3 -c "import verify_hill; verify_hill.representative_checks(); verify_hill.inequality_checks('research/rediscovered_two112.json')"
```

This does not overwrite the accepted `hill_certificate.json`. It proposes a fresh set of 56 inequalities and the second command checks them against the same stated reduction.
