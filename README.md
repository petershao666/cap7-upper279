# An exact-arithmetic certificate for f(7,3) ≤ 275

**Latest release: [v1.1.0](https://github.com/petershao666/cap7-upper279/releases/tag/v1.1.0), establishing 236 ≤ f(7,3) ≤ 275.**

The certificate excludes every 276-point cap in AG(7,3), using explicitly cited low-dimensional classification theorems. An explicit 236-point cap is included. The exact maximum and the existence of a 237-point cap remain unknown.

Read the [mathematical proof](upper275/cap7_upper275/README.md), [certificate tables](upper275/cap7_upper275/CERTIFICATE_TABLES.md), [audit report](upper275/AUDIT.md), and [next steps](ROADMAP.md).

## What has been verified

- Both supplied complete implementations were freshly run locally: C++ with undefined-behavior sanitization, and standard-library Python with arbitrary-precision integers. All **448 non-timing result lines** match.
- The seven-dimensional ordinary and extremal cases cover **167,863,211 case-matrix evaluations**. The five additional six-dimensional histogram checks cover 681,237 evaluations.
- A separately written audit checker verifies the new 41-cap histogram lemmas on **599,436 fully ordered matrices**, including all 138,621 first-column-sorted configurations. All 30 local minima match the supplied implementations.
- Separate audit code checks the 112-cap geometry, Fourier and incidence identities, the final coverage of 17 minimum-direction alternatives by 50 branches, and all 27,730 point pairs in the 236-cap.

These are evaluations counted per certificate/branch; they are not distinct global caps. The smallest extremal contradiction gap is 1,259 and the final directional sum is −214,038.

The original package reported only a partial Python execution. **This release includes the completed local Python execution**, recorded separately in [AUDIT_RESULT.json](upper275/AUDIT_RESULT.json). The original package and its historical verification-status file remain unchanged. The audit report was written before this GitHub release, so its statement that GitHub had not yet been updated describes the audit's timestamp.

## Reproduce the proof

Python 3.10+ or a C++17 compiler is sufficient; no optimizer, network, randomness, or third-party mathematical library is needed.

```sh
cd upper275
python3 cap7_upper275/verify.py > python_replay.txt
c++ -std=c++17 -O2 -fsanitize=undefined -fno-sanitize-recover=all cap7_upper275/verify.cpp -o cpp_verify
./cpp_verify > cpp_replay.txt
```

On the audit machine, C++ took about 49 seconds and Python about 631 seconds; timings depend on hardware. The C++ build emits an inherited warning about an unused renamed historical entry point lacking an explicit return; the active verifier completes without sanitizer errors. The original source bytes are preserved.

## Reproduce the additional audit

From `upper275/`:

```sh
python3 prepare_audit.py
c++ -std=c++17 -O2 -fsanitize=undefined -fno-sanitize-recover=all independent_aux41.cpp -o independent_aux41
./independent_aux41 < aux41_input.txt > independent_aux41.txt
python3 independent_geometry.py > independent_geometry.txt
python3 final_checks.py
```

`prepare_audit.py` checks source integrity and regenerates C++ data in a separate directory. `final_checks.py` checks coverage and compares complete logs; it does not itself run either full verifier. The archived logs allow this comparison immediately after cloning.

The supplied Python/C++ implementations and the additional audit share certificate coefficients, representative data, external theorems, and mathematical reductions. The additional checker independently reimplements the stated subchecks, not a third complete seven-dimensional proof verifier. See the [audit trust boundary](upper275/AUDIT.md).

## Versions and citation

| Release | Certified interval | Materials |
|---|---|---|
| [v1.1.0](https://github.com/petershao666/cap7-upper279/releases/tag/v1.1.0) | 236 ≤ f(7,3) ≤ 275 | `upper275/` |
| [v1.0.0](https://github.com/petershao666/cap7-upper279/releases/tag/v1.0.0) | 236 ≤ f(7,3) ≤ 279 | `cap7_upper279/` and historical root audit files |

The repository retains its original name for continuity. The older certificate and release are preserved.

Heng Shao. *An exact-arithmetic certificate for f(7,3) ≤ 275*. Version 1.1.0 (2026-09-05). [GitHub release](https://github.com/petershao666/cap7-upper279/releases/tag/v1.1.0). Machine-readable metadata: [CITATION.cff](CITATION.cff).

## Provenance and mathematical inputs

The original upper-275 proof and certificate package came from the [supplied ChatGPT conversation](https://chatgpt.com/share/6a9ca714-e64c-83ea-a3d2-a6f0e53db44e). A separate Codex task reviewed the reduction, reran both complete implementations, and wrote additional audit code. AI assistance is disclosed; these checks are not independent human peer review.

The proof relies on Potechin's dimension-six maximum/uniqueness theorem and the specified Thackeray classification, completion, and reflected-slice results. Their historical classification computations are not rerun here. Precise references and derived-lemma proofs are in the package.

Original ZIP SHA-256: `6a7776fb65e8beeb962bce01b6a0f2050e37a0ebef641bf129d0dca1945f08f6`.

This release makes no publication-priority claim, no claim that a 275-point cap exists, and no novelty claim for the included 236-point construction. No distribution license has been assigned to this release. The next steps include resolving manuscript authorship, contribution statements, and release licensing before archival publication.
