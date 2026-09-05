# An exact-arithmetic certificate for f(7,3) ≤ 279

The certificate excludes every 280-point cap in the seven-dimensional affine space over F3, using the cited low-dimensional classification theorems. An explicit 236-point cap is included, giving **236 ≤ f(7,3) ≤ 279**. The exact value remains unknown.

Read the [complete mathematical proof](cap7_upper279/README.md), [all certificate tables](cap7_upper279/CERTIFICATE_TABLES.md), and [audit report](AUDIT.md).

## Reproduce the certificate

Python 3.10+ or a C++17 compiler is sufficient. No optimizer, network, randomness or third-party mathematical library is required.

```sh
python3 cap7_upper279/verify.py
c++ -std=c++17 -O2 cap7_upper279/verify.cpp -o verify
./verify
python3 cap7_upper279/check_points.py
```

Both complete verifiers have been freshly executed. Their 155 local cases cover 55,253,413 canonical matrices and finish with the root contradiction −45,291.

## Reproduce the separate audit

```sh
python3 parse_tables.py
c++ -std=c++17 -O2 -fsanitize=undefined -fno-sanitize-recover=all independent.cpp -o independent
./independent < audit_data.txt
python3 final_checks.py
```

The audit checker reads coefficients parsed directly from the supplied Markdown table. It enumerates all ordered first columns, checking 262,070,710 matrices. Every local minimum matches. `final_checks.py` compares archived fresh execution logs, checks the point file, and compares spectra with an earlier independent enumeration; it does not launch the full verifiers itself.

## Cite this version

Heng Shao. *An exact-arithmetic certificate for f(7,3) ≤ 279*. Version 1.0.0 (2026-09-05). [GitHub release](https://github.com/petershao666/cap7-upper279/releases/tag/v1.0.0).

## Sources and provenance

The original proof and certificate package came from a [ChatGPT conversation](https://chatgpt.com/share/6a9bb8ef-55a8-83ea-b66c-93d843e4e334). A separate Codex task reviewed the reduction, reran both included verifiers, and wrote the additional parser/checker. These are programmatic checks by AI-assisted workflows, not independent human peer review. The original package is preserved unmodified in `cap7_upper279/` with its own checksums.

The proof relies on Potechin's dimension-six maximum/uniqueness theorem and Thackeray's dimension-five classification and dimension-six 110-cap completion theorem. Exact citations and the trust boundary are stated in the proof and audit report. Their historical classification computations are not rerun here.

This release makes no publication-priority claim, no claim that a 279-point cap exists, and no novelty claim for the included 236-point construction. Released by Heng Shao (GitHub: [petershao666](https://github.com/petershao666)). See `CITATION.cff` for citation metadata. No distribution license has been assigned to this release.
