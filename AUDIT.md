# Audit: 236 ≤ f(7,3) ≤ 279

Verdict: **PASS under the explicitly cited dimension 4/5/6 classification theorems.** No error was found in the reduction or the complete additional finite certificate. This audit does not certify publication priority or rerun the historical classification computations. Existence of a 237-cap remains UNKNOWN.

The audited artifact excludes every 280-point cap in AG(7,3). Every larger cap has a 280-point subset, so this is a global upper bound of 279, not a claim that a 279-point cap exists. The included 236-point example verifies the lower bound; no novelty or affine-equivalence claim is made for that example.

## Inputs and reproducibility

- User's shared conversation: https://chatgpt.com/share/6a9bb8ef-55a8-83ea-b66c-93d843e4e334
- Original archive preserved as `source.zip` in the workspace audit directory.
- User-provided `CERTIFICATE_TABLES.md` is byte-identical to the archive's table.
- All 16 entries of the original SHA256SUMS.txt were checked.
- Original package remains unmodified in `cap7_upper279/`.
- Fresh replay environment: Apple clang 15.0.0, Python 3.14.5. Both C++ executions used `-O2 -fsanitize=undefined -fno-sanitize-recover=all` and exited successfully.

## Actual executions

| Check | Result |
|---|---|
| Original Python full verifier, freshly executed | PASS; all 155 local cases |
| Original C++ full verifier, freshly compiled and executed | PASS; all 155 local cases; no sanitizer error |
| Fresh logs versus supplied logs | Every exact output line matches, ignoring elapsed time and order |
| Separate Markdown parser | All 155 coefficient rows and 17 spectral functions parsed; all U values, gaps, function bounds and multiplier signs verified |
| New audit C++ implementation | PASS on all 155 cases, using coefficients parsed directly from the user's Markdown |
| Canonical matrices | 1,442,220 in dimension six + 53,811,193 in dimension seven = 55,253,413 |
| Unquotiented matrices in new checker | 262,070,710; every ordered first column included |
| Local minima | Every minimum matches the displayed table, including three conservative K values strictly below the minimum |
| Final example (107,107,66) | 3,681,540 canonical matrices; minimum −66,301,244; gap 213,712 |
| Final root | 290 candidate triples; 58 excluded; 232 remain; minimum shifted polynomial 0; forced sum −45,291 |
| Explicit point file | 236 distinct ternary vectors; all 27,730 pairs checked separately |
| Spectra | Original replays checked 1, 45, 990, and 14,190 deleted subsets; size-42/43 spectra also match our earlier independent enumeration |

The new checker (`independent.cpp`) does not use `verify.cpp`, `verify.py`, their matrix kernels, or `certificate_data.hpp`. It parses a separate plain-text data file emitted from the Markdown. It builds exclusions by a three-dimensional cumulative OR on all permutations and enumerates all ordered first columns, independently checking the symmetry reduction numerically. Minimum witnesses are retained for every local case.

Shared dependencies are the numerical certificates, the mathematical reduction, and the cited classification inputs. All audit work was performed by the same Codex assistant in one task; multiple programs are not multiple independent human referees or independent classification proofs.

## Mathematical bridge review

1. The ordinary directional moments follow by counting pairs and noncollinear triples. Their factors are 3^(n−1) and 3^(n−2), respectively.
2. For fixed slices U0,U1,U2, a cross-layer zero sum would violate the cap property. Thus u+v+w is nonzero, and the projective annihilator count is (3^(n−2)−1)/2. This gives the stated T moment.
3. A codimension-two count matrix must satisfy all column and all nine transverse-line admissibility constraints. Passing matrices form a superset of geometrically realizable matrices, which is sufficient for a lower bound on the certificate polynomial.
4. The size-42 histogram alternatives are the three deletion histograms plus the cited Delta686 histogram. A maximum over the four gives a valid spectral sum upper bound. Every multiplier of an upper-bound function is nonnegative; exact identities can have either sign.
5. An excluded slice triple excludes every componentwise dominating triple after sorting, by deleting points within each layer. Whole-cap transverse directions use only completed earlier stages. No same-stage circular dependency was found.
6. The extension from the cited 110-cap completion theorem to 111-caps is justified: every exterior point has at least ten disjoint secant pairs in the 112-cap, so deleting two points cannot admit an exterior point.
7. Sorting the first column is justified because every permutation of F3 is affine; the constraints and T are invariant under applying the same permutation to all three rows. The new checker additionally removes this quotient entirely.
8. Each local inequality sums to D_n K ≤ sum F ≤ U, contradicting D_n K−U>0. Finally, all remaining root triples satisfy the shifted polynomial, but its forced directional sum is negative.

The final contradiction is

6·243·binom(280,3) − 613·729·binom(280,2) + 11141493·1093 = −45291.

## Verified source dependencies

- [Potechin, Maximal caps in AG(6,3)](https://link.springer.com/article/10.1007/s10623-007-9132-z): dimension-six maximum 112 and uniqueness up to affine equivalence, confirmed in the publisher's abstract. The original full classification was not replayed.
- [Thackeray, 41-cap 5-flats, v1](https://arxiv.org/html/2206.09719v1): Lemma 2.3 proof recalls the dimension-four bound; Theorems 4.1 and 4.3 give the dimension-five bound and uniqueness; Theorem 6.3 gives the completion/classification consequences.
- [Thackeray, Up to dimension 7, v1](https://arxiv.org/html/2206.09804v1): Theorem 2.1 and Table 1 give the size-42 alternatives and Delta686 histogram; Theorem 3.9 gives 110-cap completion. The statements and table were checked against the primary source.

These source results are accepted mathematical inputs, not hypothetical new conjectures. Calling the upper bound established relative to them is the normal dependency structure of a theorem.

## Interpretation for release

This is suitable for public release as a reproducible exact-arithmetic upper-bound certificate. The mathematical work is a structural reduction using classification, directional moments, histogram inequalities and staged exclusions, followed by finite exhaustive verification. It does not enumerate all point subsets of F3^7.

Correctness, novelty and publication suitability are separate questions. This audit supports correctness of the stated bound. It does not establish first discovery, journal acceptance, a matching 279-point construction, or the exact value of f(7,3). A public release should disclose AI assistance and credit the mathematical inputs. The 236-point lower bound must not be advertised as new without a separate historical and equivalence audit.
