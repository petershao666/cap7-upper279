# Exact-arithmetic certificate: 236 <= f(7,3) <= 279

## Result and scope

This package excludes every **280-point cap in F_3^7**, using the published
classification results stated below. A larger cap would contain a 280-point
subcap, so the exclusion proves

\[
                         f(7,3)\le279.
\]

The included explicit 236-point cap gives

\[
                         \boxed{236\le f(7,3)\le279}.
\]

This improves the preceding certificate's upper bound of 280 by one. It is not
an exact determination: no construction of size 279 is claimed, and sizes 237
through 279 have not all been excluded. No claim of publication priority or
independent external mathematical review is made.

The proof consists of an exhaustive mathematical reduction and integer
inequalities. All additional finite claims are reproduced by both included
verifiers. The cited classification results are inputs: the authors' original
classification searches are **not** rerun here. Neither an unsuccessful cap
search nor floating-point solver infeasibility is part of the proof.

## Reproduction and package contents

From the extracted directory, run either complete verifier:

```bash
python3 verify.py

c++ -std=c++17 -O2 verify.cpp -o verify
./verify
```

Python 3.10 or later uses only its standard library. C++17 also uses only its
standard library. Neither verifier requires an optimizer, network access,
randomness, or external data. Elapsed-time reporting is the only floating-point
arithmetic in the verifiers.

Python reads `certificate.json`. C++ reads the included `certificate_data.hpp`,
a transcription of the same data. To regenerate that header:

```bash
python3 generate_cpp_data.py
```

To check the point list separately and compare the supplied execution logs:

```bash
python3 check_points.py
python3 compare_verifiers.py
```

`CERTIFICATE_TABLES.md` prints every coefficient vector, spectral function,
lower bound, and positive contradiction gap. The execution logs additionally
record the matrix counts and computed minima. `SHA256SUMS.txt` records hashes.
The discovery optimizer is not needed to reproduce the certificate.

The final certificate has **97 six-dimensional and 58 seven-dimensional local
inequalities**, in ordered stages. Both verifiers enumerate **1,442,220** and
**53,811,193** admissible canonical matrices respectively, a total of
**55,253,413**. They also check all relevant deleted subsets of a 45-cap and
all 27,730 pairs of the 236-point construction.

## 1. Published mathematical inputs

We use the following statements over F_3.

D1. A cap in dimension four has at most 20 points.

D2. A cap in dimension five has at most 45 points; the 45-point cap is unique
up to affine equivalence. Every cap of size at least 43 is contained in a
45-point cap. Every 42-point cap is either contained in a 45-point cap or is
in the exceptional class Delta686, whose histogram is stated below.

D3. A cap in dimension six has at most 112 points, and the 112-point cap is
unique up to affine equivalence.

D4. Every 110-point cap in dimension six is contained in a 112-point cap.

References and exact locations:

* Aaron Potechin, *Maximal caps in AG(6,3)*, Designs, Codes and Cryptography
  46 (2008), 243-259, DOI `10.1007/s10623-007-9132-z`, supplies D3.
  <https://link.springer.com/article/10.1007/s10623-007-9132-z>
* Henry (Maya) Robert Thackeray, *The cap set problem: 41-cap 5-flats*,
  arXiv `2206.09719v1` (2022): Lemma 2.3 and its proof recall D1;
  Theorems 4.1 and 4.3 and Proposition 4.2 supply the 45-cap facts;
  Theorem 6.3 supplies the completion and 42-cap classification in D2.
  <https://arxiv.org/html/2206.09719v1>
* Thackeray, *The cap set problem: Up to dimension 7*,
  arXiv `2206.09804v1` (2022): Theorem 2.1 and Table 1 give the 42-cap
  classification and Delta686 histogram; Theorem 3.9 supplies D4.
  Lemma 3.1(a) states the 112-cap histogram also checked below.
  <https://arxiv.org/html/2206.09804v1>

Only these stated consequences are used. No classification of all 109-caps,
108-caps, or seven-dimensional caps is assumed.

## 2. Representatives, the 236-point cap, and initial admissibility

Write `123` for the subset {1,2,3} of {1,...,6}. Let

\[
\mathcal B_0=\{123,124,135,146,156,236,245,256,345,346\},
\qquad \mathcal B_1=\{[6]\setminus B:B\in\mathcal B_0\}.
\]

In F_3^6 set

\[
\begin{aligned}
R&=\{v\in\{1,2\}^6:\#\{i:v_i=2\}\text{ is even}\},\\
D_j&=\{v:\operatorname{supp}(v)\in\mathcal B_j\},\\
U&=\{\pm e_i:1\le i\le6\}.
\end{aligned}
\]

The representative 112-cap is S=R union D_0. The lower-bound construction is

\[
A=(\{0\}\times(R\cup D_0))\cup
  (\{1\}\times(R\cup D_1))\cup(\{2\}\times U).
\]

Its size is (32+80)+(32+80)+12=236. Each complete verifier reconstructs it and
checks all 27,730 unordered distinct pairs x,y, confirming that -x-y is absent.
In characteristic three this third point is automatically distinct from both
x and y. The explicit point list is `cap236.txt`.

For a direct cap-property proof, each block family has no complementary pair
and exactly two blocks in every four-element set, as one checks from its ten
listed triples. Three R vectors summing to zero must be identical. Two R
vectors and one D_j vector would require the R vectors to differ in exactly
three coordinates, contrary to their even parity. One R vector and two D_j
vectors would require complementary supports. For three D_j vectors, a
coordinate cannot occur in exactly one support. Three identical supports
force identical vectors; exactly two equal supports leave a singleton
coordinate; three distinct supports would fit in a four-element set, which
contains only two blocks. Thus R union D_j is a cap. The weight-one set U is
also a cap. A cross-layer zero-sum triple would require x+y to have weight one
for x in R union D_0 and y in R union D_1. Two R vectors have a sum of even
weight; an R and D_j vector have a sum of weight at least three; D_0 and D_1
vectors have distinct three-element supports and a sum of weight at least two.
This excludes the cross-layer case.

Both verifiers also check that S has hyperplane histogram

\[
56\,(45,45,22)+308\,(40,36,36).
\]

Every exterior point lies on at least ten secants: 616 exterior points have ten
each and the remaining exterior point has 56. For a fixed exterior p, its
secant pairs are disjoint because x determines y=-p-x. Removing two points
leaves at least eight secants through every exterior point. By D4, a 111-cap
also lies in a 112-cap: complete 110 of its points, and its remaining point
cannot be exterior to that completion. Hence all 110-, 111-, and 112-caps
are subcaps of the representative, up to affine coordinates.

All comparisons of triples below are componentwise after sorting decreasingly.
Define Adm5(t) as follows. Its entries are integers in 0,...,20 and sum to at
most 45. If the sum is at least 43, require

\[
t\le(18,18,9)\quad\text{or}\quad t\le(15,15,15).
\]

If the sum is 42, additionally allow the types in the Delta686 histogram:

| Type | Multiplicity | Type | Multiplicity |
|---|---:|---|---:|
| (20,16,6) | 3 | (16,15,11) | 24 |
| (18,18,6) | 4 | (16,14,12) | 36 |
| (18,17,7) | 18 | (15,15,12) | 3 |
| (18,12,12) | 6 | (14,14,14) | 27 |

Below total 42, impose no further restrictions. D1-D2 justify Adm5.
The Delta686 histogram is a cited input, not independently reclassified.

Initially define Adm6(t) by entries in 0,...,45 and sum at most 112; for a sum
at least 110 also require

\[
t\le(45,45,22)\quad\text{or}\quad t\le(40,36,36).
\]

This follows from D3-D4 and the verified representative facts. The proven
six-dimensional exclusions will strengthen Adm6 by downward closure.

## 3. The strengthened ingredient: upper bounds from full histograms

Both verifiers find a 45-point hyperplane section of S and identify its
hyperplane with F_3^5 by deleting a coordinate with nonzero coefficient in its
equation. They verify the resulting cap and enumerate every removal of zero,
one, two, or three points. Thus they examine 1, 45, 990, and 14,190 deleted
subsets, respectively, computing all 121 hyperplane directions for each.

For sizes 45, 44, and 43, there is one histogram each. For size 42, the
three-point deletions yield three histograms; the Delta686 histogram gives a
fourth. The complete four histograms are in `CERTIFICATE_TABLES.md` and are
checked by both programs, not accepted solely from that table.

Let H_m be this finite set of histograms for size m in {42,43,44,45}. By D2,
every m-cap in dimension five has a histogram in H_m. For any integer-valued
function phi on the allowed sorted slice types, define

\[
B(\phi)=\max_{h\in H_m}\sum_t h(t)\phi(t).
\]

Every such cap therefore satisfies the exact integer upper bound

\[
                  \sum_{[y]}\phi(t_y)\le B(\phi). \tag{1}
\]

Some certificate functions instead have the same sum L on every histogram;
these supply an equality. The preceding upper-280 certificate used such
common equalities. **The additional seven six-dimensional exclusions here
also use (1), allowing unequal sums on the four size-42 histograms.**
This retains restrictions lost by keeping common equalities alone.

Every function and bound used is explicitly listed. Python checks it on every
deleted subset and, at size 42, on Delta686. C++ independently performs the
same checks. Sizes 44 and 45 are verified too, even though their fixed
histograms follow already from the ordinary moments and their type supports.

## 4. Counting identities and the local matrix lemma

Write E2(a,b,c)=ab+ac+bc and E3(a,b,c)=abc. For an s-point cap in F_3^n,
summing over all (3^n-1)/2 hyperplane directions gives

\[
\sum E_2=3^{n-1}\binom{s}{2},\qquad
\sum E_3=3^{n-2}\binom{s}{3}. \tag{2}
\]

A fixed distinct pair occupies different slices for 3^{n-1} directions.
A fixed triple is noncollinear: its two independent difference vectors are
sent to (1,2) or (2,1) by 2*3^{n-2} nonzero functionals, or 3^{n-2} projective
directions. This proves (2).

Fix a whole-cap direction with sorted slice sizes (A,B,C). Choose affine
coordinates so the three slices are {0} x U_0, {1} x U_1, {2} x U_2, with
U_j subsets of F_3^{n-1}. For each nonzero functional direction [y] in that
slice space, form the matrix

\[
M=\begin{pmatrix}
\alpha_0&\beta_0&\gamma_0\\
\alpha_1&\beta_1&\gamma_1\\
\alpha_2&\beta_2&\gamma_2
\end{pmatrix}.
\]

The entries count the y-values in U_0, U_1, U_2. Each column must satisfy the
appropriate lower-dimensional admissibility condition. In addition, all nine
transverse triples

\[
            (\alpha_r,\beta_{r+s},\gamma_{r+2s}),\qquad r,s\in F_3, \tag{3}
\]

must satisfy it: these are the parallel (n-2)-flat counts inside the
(n-1)-flat y-sx=r.

Put

\[
T(M)=\sum_{i+j+k=0}\alpha_i\beta_j\gamma_k,
\quad f(M)=(T,E_2(\alpha),E_3(\alpha),E_2(\beta),E_3(\beta),E_2(\gamma),E_3(\gamma)).
\]

There are D_n=(3^{n-1}-1)/2 such matrices, with multiplicity by directions.
Their exact feature sums are

\[
\begin{aligned}
F_n(A,B,C)=\big(&\tfrac{3^{n-2}-1}{2}ABC,
3^{n-2}\tbinom A2,3^{n-3}\tbinom A3,\\
&3^{n-2}\tbinom B2,3^{n-3}\tbinom B3,
3^{n-2}\tbinom C2,3^{n-3}\tbinom C3\big). \tag{4}
\end{aligned}
\]

For the T identity, choose u in U_0, v in U_1, w in U_2. The vector u+v+w is
nonzero, or the original cap would have a forbidden cross-layer triple.
Exactly (3^{n-2}-1)/2 projective directions annihilate that nonzero vector.
Summing over the ABC choices proves the first coordinate of (4). The other
coordinates follow from (2) within the layers.

At n=6, a column sum in {42,43,44,45} also permits the spectral functions from
Section 3. Append their values to f. In the upper bound on its sum, append
either the exact known sum or the bound B(phi).

## 5. Integer separation certificates and noncircular propagation

For each local case the certificate supplies integer coefficients q and K,
and exhaustively verifies

\[
                            q\cdot f(M)\ge K \tag{5}
\]

on every admissible matrix. Ordinary feature sums and spectral equalities are
exact. The coefficient multiplying a spectral upper bound is required to be
nonnegative. Thus the data supply an exact integer U such that

\[
                     \sum_{[y]}q\cdot f(M)\le U.
\]

If

\[
                            D_nK-U>0, \tag{6}
\]

then (5) contradicts this upper bound and excludes the whole-cap slice triple.
For cases with only equality features, U is the exact forced sum.

In `certificate.json`, an extra function is stored under the legacy key
`identity`; `bound: "upper"` distinguishes an upper bound from an equality.
The field `sum` stores its bound and `forced` stores U. The latter is not
claimed to be an equality when an upper-bound function occurs. Every such
multiplier is checked for its required sign.

Two propagation rules are used. An excluded sorted triple t also excludes any
sorted u >= t: deleting points separately from the layers would otherwise
produce t. Furthermore, for each s in F_3,

\[
t_s(M)=\bigl(\alpha_r+\beta_{r+s}+\gamma_{r+2s}\bigr)_{r=0,1,2} \tag{7}
\]

is the whole cap's slice triple in direction y-sx. It must not dominate an
already excluded triple of the same dimension.

The stages are ordered. A stage uses only completed earlier stages of its own
dimension in (7). Its own exclusions are not available within that stage.
Dimension seven uses all completed six-dimensional exclusions to strengthen
Adm6 in the column and transverse-line tests. This is not circular.

| Dimension | Stage | Newly excluded triples |
|---:|---:|---:|
| 6 | 0 | 68 |
| 6 | 1 | 1 |
| 6 | 2 | 1 |
| 6 | 3 | 1 |
| 6 | 4 | 19 |
| 6 | 5 | 4 |
| 6 | 6 | 2 |
| 6 | 7 | 1 |
| 7 | 0 | 46 |
| 7 | 1 | 2 |
| 7 | 2 | 2 |
| 7 | 3 | 7 |
| 7 | 4 | 1 |

The seven additional six-dimensional exclusions, all of total 108, are:

* Stage 5: (42,41,25), (42,39,27), (42,35,31), (42,33,33).
* Stage 6: (44,41,23), (42,36,30).
* Stage 7: (45,39,24).

All 58 seven-dimensional exclusions have total 280. The coefficient tables
contain the complete lists, not just these new examples.

## 6. Exhaustiveness of the matrix computations

For each fixed (A,B,C), list every admissible sorted first column alpha,
every admissible ordered second column beta, and every admissible ordered
third column gamma. Test every combination against all nine conditions (3)
and, when applicable, all three conditions (7). Evaluate the polynomial with
integer arithmetic on each surviving matrix and check (5). Calculate U and
the positive gap (6) independently of the enumeration.

Sorting alpha loses no case. Every permutation of F_3 is affine, z -> az+b
with a nonzero. Applying it to all three row labels preserves the column
tests, permutes the transverse lines and the directions in (7), preserves
sorted histogram functions, and preserves i+j+k=0 since 3b=0. Thus it
preserves T and all the certificate features.

Python accelerates the transverse tests using bit-mask intersections, still
visiting every surviving matrix. C++ directly enumerates the Cartesian product
of the three column families and tests the nine lines. Neither verifier uses
feature-vector deduplication or the optimizer used in discovery.

Passing matrices need not arise from caps. They form a finite **superset** of
all possibilities for a cap, and proving the inequalities on that superset
is sufficient. The enumeration is not a search for large caps.

## 7. A final local example: (107,107,66)

The last seven-dimensional stage excludes just (107,107,66). Its coefficients,
in the order of f above, are

\[
q=(200,-18913,443,-18913,443,-11388,377),
\qquad K=-66301244.
\]

Both implementations check the inequality on all **3,681,540** admissible
canonical matrices at that stage. The moment identities force

\[
q\cdot F_7=-24133866528,
\]

whereas summing the local lower bound requires

\[
q\cdot F_7\ge364K=-24133652816.
\]

The contradiction gap is **213,712**. The preceding stages have already
excluded the other cases needed for the root inequality.

## 8. Final contradiction excluding 280 points

A hypothetical 280-point cap has, in every hyperplane direction, a sorted
triple satisfying

\[
               a+b+c=280,\qquad112\ge a\ge b\ge c\ge0.
\]

There are **290** such integer triples. The local certificates exclude **58**.
For every one of the **232** remaining triples both verifiers check

\[
                 6abc-613(ab+ac+bc)+11141493\ge0. \tag{8}
\]

Summing (8) over the 1,093 hyperplane directions and using (2) would give a
nonnegative result. Its forced value is instead

\[
\begin{aligned}
6\cdot243\binom{280}{3}
-613\cdot729\binom{280}{2}
+11141493\cdot1093
=\boxed{-45291}<0.
\end{aligned}
\]

This contradiction excludes every 280-point cap. Taking subsets excludes all
larger sizes as well, proving f(7,3) <= 279.

The terminal output of both complete verifiers, apart from elapsed time, is:

```text
Root: 232 allowed types, 58 excluded types, K=-11141493, forced=-12177697140, gap=45291.
FULL PASS: 1442220 dimension-six matrices; 53811193 dimension-seven matrices.
Under the published classification inputs in README.md, no 280-point cap exists; 236 <= f(7,3) <= 279.
```

## 9. Trust boundary and remaining gap

The package supplies every additional finite inequality, its exhaustive
verification, its mathematical connection to cap geometry, and an explicit
236-point construction. Agreement of two implementations is a useful check,
not a substitute for examining those reductions or the cited classification
theorems. Those authors' original classifications are not certified anew.

The proof uses upper bounds on spectral sums where marked, not unjustified
equalities. Stage ordering prevents circular exclusion. No unsuccessful
construction search is used as evidence of nonexistence.

The certified change is **280 -> 279 in the upper bound**. The lower bound
remains 236, and a matching upper and lower bound has not been established.
