# Exact-arithmetic checkpoint: 236 <= f(7,3) <= 275

## Result, status, and scope

This release excludes every 276-point cap in F_3^7, and therefore every larger cap by taking a subset. Together with the preserved explicit 236-point construction, the result is

    236 <= f(7,3) <= 275.

This is the step 276 -> 275 in the upper bound. It does NOT prove 274, 270, or the exact maximum. No publication-priority claim or independent mathematical peer review is asserted.

The complete C++ verifier passed with undefined-behavior sanitization. A separate standard-library Python implementation is included. Its independent execution was stopped during finalization before it reached every case. All 170 exact-result lines it had produced agree with C++; this is only a partial independent cross-check, not a second completed run. Full details are recorded in `VERIFICATION_STATUS.json`. The C++ run alone exhaustively verifies every additional finite claim used by this proof. The original published classification computations remain external mathematical inputs, not searches rerun by this package.

The original upper-276 archive is preserved byte-for-byte as `baseline276_certificate.zip`. The 70 underlying dependency files used here are preserved under `baseline277/`; `check_integrity.py` compares their bytes directly with that archive. `BASELINE276_PROOF.md` and `BASELINE276_TABLES.md` retain its written argument. The new proof is separate and does not modify those preserved sources.

## Reproduction

Run from this directory:

```sh
c++ -std=c++17 -O2 -Wall -Wextra \
  -fsanitize=undefined -fno-sanitize-recover=all verify.cpp -o verify
./verify

# Independent implementation; Python 3.10+ and its standard library:
python3 verify.py

# Integrity of the preceding release and preserved dependency files:
python3 check_integrity.py

# Regenerate the C++ data header from the JSON certificate:
python3 generate_cpp_data.py

# Explicit 236-point cap (also reconstructed in the complete verifiers):
python3 baseline277/baseline278/check_points.py
```

`compare_verifiers.py` compares the completed logs, when both full logs are present. It requires their full-pass lines; a partial log is not accepted as a full pass.

The proof data are `results/size276/proof.json` and `results/near_deleted2.json`, plus the preserved dependency certificates. C++ reads the generated integer transcription `results/size276/step_data.hpp`. Neither verifier imports a numerical optimizer or trusts its status. Python uses unbounded integers; C++ uses integer arithmetic and the recorded build is checked for undefined behavior.

The new ordinary and extremal calculations comprise 43,805,229 + 124,057,982 = 167,863,211 case-matrix evaluations. The five six-dimensional histogram checks comprise 681,237 further evaluations. The three 41-point histogram inequalities are checked on 138,621 configurations. Inherited representative, histogram, secant, Fourier, and lower-dimensional certificate checks are additional. The same matrix can occur in different branches, so these counts do not describe globally distinct matrices.

## 1. Mathematical inputs and the dependency boundary

The inherited inputs and their use are stated completely in `baseline277/README.md`, `baseline277/baseline278/README.md`, and `BASELINE276_PROOF.md`. They include the four-dimensional bound 20, the five-dimensional bound 45 and classification/completion results for sizes at least 42, the six-dimensional maximum 112 and uniqueness, the published completion theorem at size 110, and the stated reflected-slice propositions.

References:

* Aaron Potechin, *Maximal caps in AG(6,3)*, Designs, Codes and Cryptography 46 (2008), 243-259; DOI 10.1007/s10623-007-9132-z. Six-dimensional maximum and uniqueness.
* Henry (Maya) Robert Thackeray, *The cap set problem: 41-cap 5-flats*, arXiv:2206.09719v1 (2022), https://arxiv.org/html/2206.09719v1 . The additional published inputs used in this step are precisely Lemma 2.3 and Proposition 6.1, as stated below.
* Thackeray, *The cap set problem: Up to dimension 7*, arXiv:2206.09804v1 (2022), https://arxiv.org/html/2206.09804v1 . Theorem 2.1 and Table 1 give the large five-dimensional classification/histogram, Theorem 3.9 the 110-point completion result, and Propositions 3.5, 3.7 and 3.8 the reflected-slice inputs.

Derived lemmas rerun here include the 103-point extension-rigidity lemma for a subcap of a 112-cap, the 109-point completion theorem, all inherited six-dimensional exclusions and conditional completion patterns, the non-completable 108-cap histogram bound, and the large parallel-slice lemmas. None is silently attributed to a stronger published theorem.

In particular the previously established seven-dimensional impossible slice triples used as seeds are

    (112,112,29), (112,111,35), (112,110,45), (111,111,45).

The last two follow from the upper-276 checkpoint's two-deletion lemma: removing at most two points in total from two completed 112-point layers leaves at most 44 available third-layer positions. The full Fourier/incidence proof, including small and large intersection cases and the origin, is in `BASELINE276_PROOF.md`. Its 51 finite certificates are rerun by both complete implementations.

A cap is called *completable* here only when it is contained in a 112-point cap. Completion status is a property of an entire six-dimensional slice, fixed across every direction. It does not mean merely extendable by one point.

## 2. Universal moments, local matrices, and exact certificates

Write E2(a,b,c)=ab+ac+bc and E3(a,b,c)=abc. For an s-point cap in F_3^n, summing over all (3^n-1)/2 hyperplane directions gives

    sum E2 = 3^(n-1) binom(s,2),
    sum E3 = 3^(n-2) binom(s,3).

A fixed pair occupies different slices in 3^(n-1) directions. A fixed triple is noncollinear, so its two independent differences take values (1,2) or (2,1) in 2*3^(n-2) nonzero linear functionals, hence 3^(n-2) projective directions. These prove the identities.

Fix a whole-cap direction with layer sizes t=(A,B,C). For a projective refinement direction [y] on F_3^(n-1), let M have ordered columns alpha,beta,gamma, each recording the three y-level counts inside one layer. Every column and all nine transverse triples

    (alpha_r,beta_(r+s),gamma_(r+2s)), r,s in F_3,

satisfy the lower-dimensional necessary admissibility predicate. Also

    t_s(M) = (alpha_r + beta_(r+s) + gamma_(r+2s))_(r=0,1,2)

is a whole-cap hyperplane profile in the direction y-sx. All subscripts are taken modulo three.

Set

    T(M) = sum_(i+j+k=0) alpha_i beta_j gamma_k,
    f(M) = (T,E2(alpha),E3(alpha),E2(beta),E3(beta),E2(gamma),E3(gamma)).

There are D_n=(3^(n-1)-1)/2 refinements and the exact feature sum is

    F_n(A,B,C) = ((3^(n-2)-1)/2 * ABC,
                 3^(n-2) binom(A,2), 3^(n-3) binom(A,3),
                 3^(n-2) binom(B,2), 3^(n-3) binom(B,3),
                 3^(n-2) binom(C,2), 3^(n-3) binom(C,3)).

For the first coordinate, one point from each original layer has a nonzero sum in F_3^(n-1), since otherwise the original points form a forbidden triple. Exactly (3^(n-2)-1)/2 projective functionals annihilate that nonzero vector. The other six coordinates are the within-layer moment identities.

If q.f(M)>=K for every admissible matrix and the exact identities and valid upper bounds give sum q.f(M)<=U, then

    D_n*K - U > 0

is a contradiction. Every multiplier of a summed upper bound is required to be nonnegative. Signed functions and negative bounds are permitted; the sign restriction concerns their multipliers.

Only the first column is sorted in exhaustive enumeration. Any permutation of the three row labels is affine over F_3, and simultaneous application to all columns preserves the constraints, the transverse families, and i+j+k=0. Completed-column labels travel with this permutation. The Python implementation uses bit-mask intersections; C++ tests the direct Cartesian product.

## 3. New finite histogram bounds for 41-point five-dimensional caps

This step does not assume that every 41-cap is a subset of a 45-cap, nor does it require a newly enumerated classification of all four-dimensional caps.

First, both new implementations establish the needed three-dimensional bound 9 by small exact counts. Every one of the 126 five-point subsets of F_3^2 contains a forbidden triple. Hence planar sections have size at most four. A hypothetical 10-cap in F_3^3 then has only profiles (4,4,2) and (4,3,3), whose E2 is at least 32. Its 13 directions would give sum E2>=416, contradicting 9*binom(10,2)=405.

Lemma 2.3 of the cited 41-cap paper implies that sorted profiles (a,b,c) in dimension four, with entries at most nine and total at most twenty, satisfy:

* (a,b) in {(9,9),(9,8),(9,7),(8,8)} implies c<=2;
* (a,b) in {(9,6),(8,7)} implies c<=3;
* (a,b) in {(9,5),(7,7)} implies c<=4.

The lemma's (9,4) case is redundant after decreasing sorting. These necessary conditions define `adm4` in `auxiliary41.py`; retaining additional unrealizable profiles only enlarges the relaxation.

Proposition 6.1 excludes the four 41-point profiles

    (20,19,2), (20,18,3), (19,19,3), (19,18,4),

leaving 36 candidate types. It also ensures that every 41-cap has at least one of the ten anchor profiles

    (20,20,1), (18,18,5), (20,17,4), (20,16,5), (19,17,5),
    (19,16,6), (18,17,6), (18,16,7), (17,17,7), (17,16,8).

For a function psi on the 36 types and a chosen anchor direction x, refinement accounts for each other whole-cap direction exactly once:

    sum_[z] psi(t_z) = psi(t_x) + sum_[y] sum_(s=0,1,2) psi(t_s(M_y)).

The reason is that the refinement directions enumerate dual planes through [x], and the three other projective points in those planes partition the remaining projective directions.

Consequently, an exactly verified local inequality

    q.f(M) - sum_s psi(t_s(M)) >= K

implies

    sum_[z] psi(t_z) <= psi(t_x) + q.F_5(t_x) - 40*K.

The maximum of this expression across all possible anchor cases is a uniform bound. For two functions we choose the first occurring anchor in the recorded order. When processing its case, all earlier anchors are absent, and can be excluded from the transverse whole-cap directions. This is a case split on the same cap, not an unconditional exclusion of an anchor.

The three functions actually used in this proof are:

| Function | Uniform summed upper bound | Exhaustive matrices |
|---|---:|---:|
| hist5_41_0 | 58,774 | 52,299 |
| hist5_41_4 | 942,856 | 43,161 |
| hist5_41_5 | 701,006 | 43,161 |

All 36 function values, ten anchor inequalities per function, and their bounds are contained in `proof.json` and printed in `CERTIFICATE_TABLES.md`. Both implementations check every anchor and every local integer configuration; no numerical infeasibility claim is used.

## 4. Stronger full histograms for non-completable 106- and 107-caps

The inherited six-dimensional predicates and completion-forcing patterns leave 79 possible profiles for a non-completable 106-cap and 47 for a non-completable 107-cap. Each new histogram lemma first supplies a two-feature moment inequality showing that some profile in a listed rare family must occur. There are fourteen rare cases at size 106 and seven at size 107.

Choose the first rare profile that occurs, in the order stated by the certificate. In that branch every earlier rare profile is absent from the other whole-cap directions. The complete verifier requires the list of such absences to be either empty or exactly the preceding prefix, preventing arbitrary deletions of cases.

Append to the seven universal local features the fixed directional histograms of 43-,44-,45-point columns, the verified 42-point spectral upper bounds, and the new 41-point bounds when applicable. If g is the resulting vector, a local inequality

    q.g(M) - sum_s phi(t_s(M)) >= K

implies

    sum_[z] phi(t_z) <= phi(t_x) + U_t - 121*K,

where U_t is the exact forced sum or correctly signed upper bound for sum q.g. Taking the maximum over the rare cases yields a uniform upper bound. These lemmas are proved wholly in dimension six; they assume no seven-dimensional exclusion or outer branch conclusion.

The five histogram functions used in this release are:

| Certificate identifier | Size | Uniform upper bound | Inner matrices |
|---|---:|---:|---:|
| nested106_size276 | 106 | -3,591,640,984 | 282,135 |
| nested107_size276 | 107 | -321,639,387 | 38,598 |
| nested107_size277 | 107 | -345,314,329 | 39,771 |
| joint106_107_106_63_size276 | 106 | -33,592,598,595 | 282,135 |
| joint107_107_106_63_size276 | 107 | -32,290,411,632 | 38,598 |

The size-107 function bearing `size277` is an inherited checkpoint-276 histogram inequality that is rerun here. The names denote discovery targets, not the dimensions or sizes of the cap to which a function applies.

The last two functions were optimized together to help a mixed (107,106,63) outer branch, but their inner verification is independent: each is a separate inequality true for every non-completable cap of its indicated size. Joint numerical discovery does not make their proofs mutually dependent.

## 5. Ordinary exclusions and selection of the minimizing direction

Assume a 276-point seven-dimensional cap exists. Its sorted hyperplane profiles satisfy

    112 >= a >= b >= c >= 0,  a+b+c=276.

There are 331 basic integer types. Three stages prove 52,9,5 ordinary type exclusions respectively, using only the established lower-dimensional data and completed earlier ordinary stages. Within a stage the set of available exclusions is frozen. In these ordinary stages no completion-status assumption is imposed on a whole layer.

Define

    Q(a,b,c) = 9abc - 903(ab+ac+bc) + 15,920,784.

Its directional sum is

    9*243*binom(276,3) - 903*729*binom(276,2)
      + 15,920,784*1093 = -214,038.

Thus a direction globally minimizing Q has Q<0. In every refinement matrix at that chosen direction, its three other whole-cap profiles must satisfy

    Q(t_s(M)) >= Q(A,B,C),  s=0,1,2.

This is a condition on a minimum direction, NOT an unconditional exclusion of a type. After the ordinary exclusions and inherited seeds, exactly seventeen negative-Q alternatives remain. They are exhaustively listed in the next section. No extremal-case conclusion is added to the universal type exclusions or used to eliminate a different alternative.

As an additional exact algebraic check,

    4Q = (3c-276)^2(c-67) + (903-9c)(a-b)^2

holds on every basic type. The proof relies on the negative total and the minimum-direction case analysis, not on incorrectly asserting that Q is nonnegative on every basic profile.

## 6. The seventeen exact extremal exclusions

Status 0 means the entire six-dimensional layer is non-completable; status 1 means it is contained in a 112-cap. Sizes at least 109 are automatically completable by the inherited derived theorem. Sizes 103 through 108 are split into both statuses when a split is used. In a completed layer of size N=112-d the retained labels give exact totals 56,11d,110d for the original family and distinguished-section deletion statistics. Every compatible label is tested, including ties; the original 40-point section need not remain largest.

All entries below are exactly computed positive gaps 364*K-U. “Unsplit” means the inequality applies without either completion assumption. For the final two rows only status11 is possible, so other entries are not applicable.

| Minimum-direction type | Status 00 | Status 01 | Status 10 | Status 11 |
|---|---:|---:|---:|---:|
| (105,105,66) | 533,106 | 46,168 | 46,168 | 55,400 |
| (106,104,66) | 1,629,299 (unsplit) | — | — | — |
| (106,105,65) | 273,601 | 674,960 | 452,219 | 1,259 |
| (106,106,64) | 2,195,770 | 77,650 | 77,650 | 122,220 |
| (107,103,66) | 35,079 (unsplit) | — | — | — |
| (107,104,65) | 566,919 (unsplit) | — | — | — |
| (107,105,64) | 126,138 | 957,223 | 229,963 | 1,008,030 |
| (107,106,63) | 2,265,557 | 1,801,738 | 19,221,002 | 172,258 |
| (107,107,62) | 23,628 | 538,787 | 538,787 | 543,821 |
| (108,103,65) | 4,771 (unsplit) | — | — | — |
| (108,104,64) | 119,394 | 1,079,850 | 1,499,342 | 440,910 |
| (108,105,63) | 143,953 | 527,377 | 19,917 | 453,181 |
| (108,106,62) | 312,590 | 1,228,393 | 120,489 | 566,582 |
| (108,107,61) | 3,216,348 | 1,350,309 | 821,970 | 1,314,754 |
| (108,108,60) | 675,522 | 1,374,972 | 1,374,972 | 1,632,818 |
| (111,110,55) | not applicable | not applicable | not applicable | 96,858 |
| (112,109,55) | not applicable | not applicable | not applicable | 120,516 |

There are 50 extremal local certificates: four unsplit, forty-four in eleven four-way splits, and two automatically-completed cases. Their coefficients, feature order, K, U, and gaps are printed in `CERTIFICATE_TABLES.md`. Their complete matrix counts and minima are in the execution logs.

For a concrete mixed-slice example, the non-completable/non-completable branch (107,106,63) has the inequality

    13147*T - 649942*E2(alpha) + 12610*E3(alpha)
      - 581071*E2(beta) + 11875*E3(beta)
      - 128339*E2(gamma) + 1078*E3(gamma)
      + 8*nested107_size276(sort(alpha))
      + joint106_107_106_63_size276(sort(beta))
      + joint107_107_106_63_size276(sort(alpha))
      >= -775,651,987.

The exact moments and previously proved histogram upper bounds imply a summed upper bound -282,339,588,825. Summing the local lower bound over 364 refinements instead requires at least -282,337,323,268. The positive difference is 2,265,557.

Every negative-Q alternative for a globally minimizing direction is excluded. Yet the negative global sum forces such a minimum. This contradiction proves that no 276-point cap exists, hence f(7,3)<=275.

## 7. Verification boundary and preserved continuation work

The complete verification does not search for caps or rely on a search failing. It enumerates a finite superset of all locally possible cap-induced count matrices and checks the integer inequality on every member. Extra incompatible labels or directional choices enlarge that superset; they are not assumed realizable.

The trust boundary includes the explicitly cited published theorems, the geometric/counting reductions above and in the preserved proofs, and these finite computations. Successful verifiers are not independent peer review. The lower bound is still the same explicit 236-cap, not a larger construction.

The separate continuation-research archive contains proposals toward upper274 and an auxiliary three-deletion lemma. It is NOT part of this upper275 certificate and does not prove 274 or 270. In particular, there are still unclosed minimum-direction branches for total275. No numerical solver report in that archive is presented as an exact feasible witness or a nonexistence proof.
