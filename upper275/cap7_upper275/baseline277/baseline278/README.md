# A reproducible exact-arithmetic certificate: 236 ≤ f(7,3) ≤ 278

## Result and scope

This package excludes **every 279-point cap in F₃⁷**. Every larger cap would contain a 279-point subcap. Together with the explicitly included 236-point construction, the result is

\[
                         236\le f(7,3)\le278.
\]

This improves the preceding certificate's upper bound of 279 by one. It is **not an exact determination**: neither a cap larger than 236 nor the exclusion of all sizes 237 through 278 is supplied. No publication-priority claim or claim of independent mathematical peer review is made.

The proof uses published results specified in Section 1. Their original classification searches are not repeated. **Every additional finite assertion used here is reproduced by the two verifiers.** No unsuccessful construction search, optimization solver's infeasibility report, or floating-point tolerance is used as a proof.

The complete verification comprises 205 local matrix inequalities: 97 inherited universal six-dimensional exclusions, 22 conditional completion certificates, 62 ordinary seven-dimensional certificates, and 24 completion-status branches. It also checks 56 small auxiliary cases for pairs of 112-point slices. The programs agree on 64,400,303 case-matrix evaluations and all 2,022 auxiliary state inequalities. The same numerical matrix can occur in different branches; this is a count of **case-matrix evaluations**, not a count of globally distinct matrices.

## Reproduction

Python 3.10 or later, standard library only:

```bash
python3 verify.py
```

Independent direct-enumeration implementation, C++17 standard library only:

```bash
c++ -std=c++17 -O2 verify.cpp -o verify
./verify
```

Additional checks:

```bash
python3 check_points.py
python3 compare_verifiers.py
python3 generate_cpp_data.py
```

The last command regenerates the C++ data header from the JSON certificates. It is not a discovery optimizer. The Python verifier reads `certificate.json` and `hill_certificate.json`; C++ uses their included transcription `certificate_data.hpp`.

The recorded C++ run was additionally compiled with `-Wall -Wextra -fsanitize=undefined -fno-sanitize-recover=all`. The executed environment was Python 3.13.5 and GCC 14.2.0. These exact versions are not required by the mathematical certificate. No network access, third-party Python package, or optimizer is required for verification.

`CERTIFICATE_TABLES.md` prints all coefficients and auxiliary functions. `HILL_PROOF.md` gives the detailed two-112-slice argument. `research/` contains optional discovery helpers, clearly separated from the verifiers. Their numerical optimization proposes coefficients; only exact checking establishes an inequality.

## 1. Published mathematical inputs

The following statements are mathematical dependencies, not conjectures introduced here.

**D1.** A cap in dimension four has at most 20 points.

**D2.** A cap in dimension five has at most 45 points, and the 45-cap is unique up to affine equivalence. Every cap of size at least 43 is contained in a 45-cap. A 42-cap is either contained in a 45-cap or belongs to the exceptional class Δ686, with the histogram below.

**D3.** A cap in dimension six has at most 112 points, and the 112-cap is unique up to affine equivalence.

**D4.** Every six-dimensional 110-cap is contained in a 112-cap.

**D5.** For two parallel five-dimensional slices of a six-dimensional cap: two 45-caps that are not point reflections leave at most six points in the third slice. When their sizes have sum at least 88, if their 45-point completions are not point reflections, the third slice has at most 14 points.

**D6.** A 45-point slice and a 42-point Δ686 slice leave at most 18 points in the third slice. For slices of sizes 45, 42, and at least 20, when the 42-cap is contained in a 45-cap, the whole cap is contained in a 112-cap.

Sources and exact locations:

* Aaron Potechin, *Maximal caps in AG(6,3)*, Designs, Codes and Cryptography 46 (2008), 243–259, DOI `10.1007/s10623-007-9132-z`. Supplies D3. <https://link.springer.com/article/10.1007/s10623-007-9132-z>
* Henry (Maya) Robert Thackeray, *The cap set problem: 41-cap 5-flats*, arXiv `2206.09719v1` (2022). Lemma 2.3 and its proof recall D1; Theorems 4.1 and 4.3 and Proposition 4.2 give the 45-cap facts; Theorem 6.3 gives D2. <https://arxiv.org/html/2206.09719v1>
* Thackeray, *The cap set problem: Up to dimension 7*, arXiv `2206.09804v1` (2022). Theorem 2.1 and Table 1 give D2 and the Δ686 histogram; Theorem 3.9 gives D4; Proposition 3.5(a,b) gives D5; Propositions 3.7 and 3.8 give D6. <https://arxiv.org/html/2206.09804v1>

The 109-cap completion statement proved below is **not** being attributed to D4. No classification of all 108-caps or all 107-caps is assumed. The original computational proofs underlying D1–D6 remain external dependencies.

The Δ686 histogram, counted over 121 hyperplane directions, is

| Sorted type | Multiplicity | Sorted type | Multiplicity |
|---|---:|---|---:|
| (20,16,6) | 3 | (16,15,11) | 24 |
| (18,18,6) | 4 | (16,14,12) | 36 |
| (18,17,7) | 18 | (15,15,12) | 3 |
| (18,12,12) | 6 | (14,14,14) | 27 |

## 2. Representatives, the lower bound, and extension rigidity

Write `123` for the subset {1,2,3} of {1,...,6}, and set

\[
\mathcal B_0=\{123,124,135,146,156,236,245,256,345,346\},
\qquad \mathcal B_1=\{[6]\setminus B:B\in\mathcal B_0\}.
\]

Define subsets of F₃⁶ by

\[
\begin{aligned}
R&=\{v\in\{1,2\}^6:\#\{i:v_i=2\}\text{ is even}\},\\
D_j&=\{v:\operatorname{supp}(v)\in\mathcal B_j\},\\
U&=\{\pm e_i:1\le i\le6\}.
\end{aligned}
\]

The representative 112-cap is \(S=R\cup D_0\). The explicit 236-cap is

\[
(\{0\}\times(R\cup D_0))\cup
(\{1\}\times(R\cup D_1))\cup(\{2\}\times U).
\]

Its size is \(2(32+80)+12=236\). Both verifiers reconstruct it and check all 27,730 unordered distinct pairs, confirming that their negative sum is absent. The point list is `cap236.txt`.

A direct proof is available from the displayed supports. In each block family there are no complementary blocks, and each four-element subset contains exactly two blocks. For a zero-sum triple in \(R\cup D_j\), three R vectors must be identical coordinatewise; two R vectors and one D vector would force an odd Hamming distance between the R vectors; one R vector and two D vectors require complementary supports. With three D vectors, no coordinate may appear in exactly one support. Three distinct supports would therefore fit in a four-element set, which contains only two blocks; equal-support cases force equality or a singleton coordinate. These exhaust the cases. The weight-one layer U is a cap. A cross-layer triple would require a sum of weight one from the first two six-dimensional layers, impossible by the same support and parity conditions.

The programs verify that S is central about 0, excludes 0, and has 56 hyperplane directions of type (45,45,22) and 308 of type (40,36,36). In the centered representative the hyperplane through 0 is the 22-point or 40-point section respectively.

They also verify that 616 exterior points each lie on exactly ten secants of S and the remaining exterior point lies on 56. For a fixed exterior point p, the corresponding pairs x,y with x+y+p=0 are disjoint: x determines y. Removing at most nine points from S therefore leaves at least one such pair through every exterior p.

**Extension-rigidity lemma.** If a six-dimensional cap contains at least 103 points of a 112-cap, it is contained in that 112-cap.

This follows immediately from the preceding secant computation. It is used when extending a conditional completion conclusion from a smaller cap to a larger one. It also shows, using D4, that every 111-cap is contained in a 112-cap: complete 110 of its points and exclude an exterior final point.

## 3. Initial admissibility and spectral bounds

All triples used for componentwise comparisons are sorted decreasingly.

A necessary predicate Adm5(t) for three four-dimensional slices of a five-dimensional cap is:

* entries between 0 and 20 and total at most 45;
* at total at least 43, componentwise domination by (18,18,9) or (15,15,15);
* at total 42, the preceding possibilities or a Δ686 type from Section 1.

At smaller totals no extra restriction is imposed. D1–D2 justify this predicate.

Initially, Adm6(t) requires entries between 0 and 45 and total at most 112; at totals 110–112 it additionally requires domination by (45,45,22) or (40,36,36). D3–D4 and Section 2 justify this. It is strengthened only by subsequently proved statements.

Both verifiers find a 45-point hyperplane section of S and identify that affine hyperplane with F₃⁵ by removing a coordinate whose coefficient in its equation is nonzero. They verify the 45-cap and enumerate every deletion of 0, 1, 2, or 3 points: respectively 1, 45, 990, and 14,190 subsets. All 121 directional histograms are computed for each subset.

There is one histogram each for sizes 45, 44, and 43. Three histograms occur among the 42-point subcaps; adjoining the Δ686 histogram gives four. These exhaust all possibilities by D2.

For any integer function φ on sorted slice types of such an m-cap,

\[
\sum_{[y]}\phi(t_y)\le B(\phi):=\max_{h\in\mathcal H_m}\sum_t h(t)\phi(t).
\tag{1}
\]

An equality may be used when all histograms have the same sum. Every function in the certificate is checked on every deleted subset and, where relevant, on Δ686. The tables and JSON give the exact functions and bounds.

## 4. Counting identities and the matrix certificate

For \(t=(a,b,c)\), let \(E_2(t)=ab+ac+bc\) and \(E_3(t)=abc\). An s-point cap in F₃ⁿ has

\[
\sum_{[x]}E_2=3^{n-1}\binom{s}{2},\qquad
\sum_{[x]}E_3=3^{n-2}\binom{s}{3}.
\tag{2}
\]

A fixed pair is separated into different slices in \(3^{n-1}\) projective dual directions. A triple of distinct cap points is noncollinear; its two independent differences are sent to (1,2) or (2,1) by \(2\cdot3^{n-2}\) linear functionals, giving \(3^{n-2}\) directions. These counts prove (2), even if the cap has smaller affine span.

Fix a direction with slice sizes (A,B,C), identified with layers \(\{j\}\times U_j\). For each nonzero functional direction [y] in F₃ⁿ⁻¹ form a matrix with columns α,β,γ, whose entries count the three y-values on the layers. Every column satisfies lower-dimensional admissibility. So do all nine triples

\[
(\alpha_r,\beta_{r+s},\gamma_{r+2s}),\qquad r,s\in\mathbb F_3,
\tag{3}
\]

because these are the three parallel sections within the hyperplane y−sx=r.

Define

\[
T(M)=\sum_{i+j+k=0}\alpha_i\beta_j\gamma_k,
\quad f(M)=(T,E_2(\alpha),E_3(\alpha),E_2(\beta),E_3(\beta),E_2(\gamma),E_3(\gamma)).
\]

There are \(D_n=(3^{n-1}-1)/2\) refinement directions. The forced sum of f is

\[
\begin{aligned}
F_n(A,B,C)=\big(&\tfrac{3^{n-2}-1}{2}ABC,
3^{n-2}\tbinom A2,3^{n-3}\tbinom A3,\\
&3^{n-2}\tbinom B2,3^{n-3}\tbinom B3,
3^{n-2}\tbinom C2,3^{n-3}\tbinom C3\big).
\end{aligned}\tag{4}
\]

For the T identity, a choice u∈U₀, v∈U₁, w∈U₂ has u+v+w≠0, or the original cap would have a forbidden triple. Exactly \((3^{n-2}-1)/2\) projective dual directions annihilate that nonzero vector. The other coordinates follow from (2).

A local certificate specifies integers q,K and checks

\[
q\cdot f(M)\ge K
\tag{5}
\]

on **every admissible integer matrix**, with spectral functions appended when appropriate. The forced feature sums, together with any spectral upper bounds multiplied by nonnegative coefficients, give an upper bound U for the sum of the left side. Thus

\[
                         D_nK-U>0
\tag{6}
\]

is a contradiction. For equality-only certificates U is exactly q·Fₙ. The verifiers independently compute U and the positive integer gap.

Two consistency rules strengthen this finite family. A universally excluded type t excludes every componentwise larger type by point deletion. Also

\[
t_s(M)=\big(\alpha_r+\beta_{r+s}+\gamma_{r+2s}\big)_{r=0,1,2}
\tag{7}
\]

is the whole cap's slice type in direction y−sx; it cannot dominate an already excluded whole-cap type.

Both implementations freeze the set of available exclusions during each stage. **No case in a stage uses the conclusion of another case in that same stage.**

## 5. Conditional completion certificates and all 109-caps

Call a six-dimensional cap *completable* here if it is contained in a 112-cap. This does not mean merely that it can be enlarged by one point.

### Four completion seeds

Any cap with a sorted slice type dominating one of

\[
(45,45,7),\quad(45,43,15),\quad(44,44,15),\quad(45,42,20)
\tag{8}
\]

is completable.

For the first three, D5 forces the two 45-point completions to be point reflections. The programs verify, for a 45-cap P in F₃⁵, that the multiplicity of each difference p−q is 9 at 220 vectors, 0 at 22 vectors, and 45 at 0. The two reflected layers P,−P and the 22 zero-multiplicity points together form a 112-cap, also checked directly. Deleting at most two points from the first two layers cannot make any positive multiplicity vanish. Hence every third-layer point remains in that 22-point set and the whole cap is a subcap of the verified completion. At the fourth seed, D2 and D6 either exclude the Δ686 case or directly give completion. The same threshold arguments cover componentwise larger triples.

### The conditional stages

Assume a cap is **not** completable. None of its directions can satisfy (8). The matrix lemma may therefore use these additional forbidden types in (7), alongside the inherited 97 universal exclusions.

The certificate proves 20 further conditional types in one stage and two in the next. A conditional type means: every cap with that type is completable. All these types have total at least 103. If a larger type dominates a previously proved conditional type, point deletion yields a completable subcap of size at least 103; the extension-rigidity lemma then completes the entire cap. Thus the propagation is sound.

Twenty of the 22 conditional types are **incompatible** with the two possible slice types of a 112-cap. They are therefore universally impossible, not merely impossible under a noncompletion assumption. The two compatible conditional types are (44,43,22) and (44,42,22). All lists and coefficients are printed in the tables.

For clarity, the (44,43,22) conditional certificate has the small seven-feature vector

\[
q=(59,-825,20,-616,35,117,-23),\qquad K=82706.
\]

Its exhaustive family has 852 canonical matrices. Formula (4) gives q·F₆=10,006,954, while 121K=10,007,426. The gap is 472.

### The 109-cap completion theorem obtained here

Suppose a 109-cap is not completable. Remove from consideration the four seeds, the inherited 97 universal exclusions, and the newly established conditional type (44,43,22). Exactly 24 sorted types remain. The programs check

\[
                       abc-39E_2(a,b,c)+106518\ge0
\]

on all 24. Summing over 364 directions forces

\[
81\binom{109}{3}-39\cdot243\binom{109}{2}+106518\cdot364
                         =-4416<0.
\]

This contradiction proves that **every 109-point cap in F₃⁶ is contained in a 112-cap**. Consequently the 112-cap type restriction is valid already at total 109, not just at 110–112. This new theorem and the 20 new universal exclusions strengthen Adm6 used below.

## 6. A separate seed: two 112-point slices

`HILL_PROOF.md` proves the following auxiliary lemma using only D3 and the representative computations, together with 56 explicit integer certificates:

> Two parallel 112-point slices leave at most 28 points in the third slice that avoid all cross-slice forbidden triples.

In fact this bounds all available third-layer positions without imposing that they form a cap. Thus the whole-cap type (112,112,29) is impossible. Its upward consequences may be used in the seven-dimensional matrix tests.

The proof normalizes both centers to zero, uses the two Fourier levels of the 112-cap to express cross-pair multiplicities, and bounds the number of zero multiplicities by projective incidence moments. It examines all intersection parameters h=1,...,56 and separately handles h=0. The finite check consists of 2,022 state inequalities; both full verifiers reconstruct all representative facts and verify these inequalities.

## 7. Completed-column identities and the final six case splits

A completed six-dimensional slice of size N≥103 is a 112-cap with d=112−N points removed. Its 364 directions split into 56 directions originally of type (45,45,22) and 308 originally of type (40,36,36).

These two families remain distinguishable from the sorted remaining type t=(a,b,c): the first has c≤22; the second has c≥36−d≥27. Each point of the 112-cap lies in exactly 11 of the 22-point sections through its center and in exactly 110 of the 40-point sections through its center. Both verifiers check this individually for all 112 representative points; affine equivalence transfers it to every completion.

Therefore a completed slice satisfies the exact identities

\[
\begin{aligned}
\sum_{[y]}\mathbf1_{c\le22}&=56,\\
\sum_{[y]}\mathbf1_{c\le22}(22-c)&=11d.
\end{aligned}\tag{9}
\]

For N≥108, also

\[
\sum_{[y]}\mathbf1_{c>22}(40-a)=110d.
\tag{10}
\]

Indeed d≤4, so in the second family the original 40-point section still has at least 36 points and is a largest section, including ties. Thus its deletion count is exactly 40−a. Formula (10) is **not used for N<108**.

The final six types that need this distinction are

\[
(108,108,63),\ (108,107,64),\ (107,107,65),\
(108,106,65),\ (108,105,66),\ (107,106,66).
\]

For each, the two large slices are split into all four statuses: neither completable, only the second, only the first, or both. A completable column has a type dominated by a 112-cap type and may use (9)–(10). A non-completable column cannot dominate any established completion pattern. **The four statuses concern entire slices, not a status chosen independently for each refinement direction.** This makes their directional identities legitimate.

Each status has its own integer inequality and positive gap. There are 24 branch certificates in total. For example, for (108,108,63) with neither large slice completable, the polynomial is

\[
18T-4040(E_2(\alpha)+E_2(\beta))+97(E_3(\alpha)+E_3(\beta))
+147E_2(\gamma)-10E_3(\gamma)\ge-17852940.
\]

Its forced sum is −6,498,587,637 and the summed lower bound is 364·(−17,852,940)=−6,498,470,160, a gap of 117,477. The other three branches additionally use the completed-column identities as specified in the tables.

The seven-dimensional stages contain 55 ordinary types, then seven ordinary types, then one branched type, then two branched types, then three branched types. Every stage uses only earlier seven-dimensional exclusions, the separately proved two-112 seed, and the previously completed six-dimensional lemmas.

## 8. Final contradiction: no 279-point cap

A hypothetical 279-point cap has sorted slice counts

\[
                   a+b+c=279,\qquad112\ge a\ge b\ge c\ge0.
\]

There are 300 such integer triples. The two-112 seed and the 68 target-size slice exclusions remove 69 types. These include **all 42 possibilities with c≤66**; the other 27 exclusions are useful supporting restrictions in the preceding stages.

All 231 remaining types therefore have 67≤c≤93. Since a+b+c=279, the exact identity

\[
\begin{aligned}
4\big(3abc-305E_2(a,b,c)+5500764\big)
={}&3(c-93)^2(c-67)\\
&+(305-3c)(a-b)^2
\end{aligned}\tag{11}
\]

shows that the expression in parentheses is nonnegative. The programs check the identity and the range on every remaining type, but (11) itself is an algebraic nonnegativity proof.

Summing this nonnegative expression over all 1,093 directions and applying (2) gives instead

\[
3\cdot243\binom{279}{3}
-305\cdot729\binom{279}{2}
+5500764\cdot1093
                         =-38502<0.
\]

This contradiction excludes every 279-point cap. Taking subsets excludes all larger sizes. Therefore f(7,3)≤278.

## 9. Exhaustiveness and verification boundary

The enumeration is of finite **necessary count configurations**, not a heuristic search for caps. Matrices that pass the tests need not be realizable by any cap; verifying the inequalities on this larger family is sufficient.

For each local case, all admissible first columns in sorted order and all admissible ordered second and third columns are generated. All nine transverse tests and the applicable whole-cap direction tests are enforced. Branches additionally restrict only their designated columns. In particular, a completed-column restriction is **not** erroneously imposed on all transverse hyperplanes.

Sorting the first column loses no cases: every permutation of F₃ is an affine map z↦uz+v with u≠0. Applied to all row labels it preserves the transverse lines, permutes the other direction families, preserves all sorted type functions, and preserves i+j+k=0 because 3v=0. Thus it preserves every statistic and every necessary condition used here. Different refinement directions may use different canonicalizing row permutations because these quantities are individually invariant.

Python uses bit-mask intersections for the transverse constraints. C++ instead enumerates the direct Cartesian product of the column families, testing all nine lines explicitly. Neither verifier uses feature deduplication or numerical optimization. The two implementations agree on each case's exact count, computed minimum, certificate threshold, and gap. In a few inherited cases the new stronger restrictions make the computed minimum exceed the recorded threshold; that strengthens the certificate, and the recorded positive gap still uses the lower threshold.

The stage dependency order is checked, as are the completeness of each four-way status split and the signs of all spectral-upper-bound multipliers. The representative, histogram, Fourier, secant, and point-list checks are performed afresh in both complete runs.

The final output is:

```text
Root: 231 allowed types, 69 excluded types, K=-5500764, forced=-6012373554, gap=38502.
FULL PASS: 1442220 original six-dimensional matrices; 373653 conditional six-dimensional matrices; 62584430 seven-dimensional case-matrix evaluations; 24 completion-status branches; 2022 two-112-slice state inequalities.
Under the published mathematical inputs in README.md, no 279-point cap exists; 236 <= f(7,3) <= 278.
```

The counts total 64,400,303 matrix evaluations. Successful independent implementations reduce the risk of an implementation mistake; they do not replace mathematical inspection of the reductions or independent review of the cited papers. The exact value of f(7,3) remains undetermined by this package.
