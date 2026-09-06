# Two parallel 112-point slices leave at most 28 third-slice positions

This is an auxiliary lemma, not a classification of all pairs of 112-caps. It supplies the universally forbidden seven-dimensional slice type (112,112,29). The proof uses uniqueness of the six-dimensional 112-cap up to affine equivalence (Potechin, DOI `10.1007/s10623-007-9132-z`), an explicit representative checked by both programs, and 56 finite integer certificates in `hill_certificate.json`.

## 1. Normalization and integer Fourier data

Suppose two parallel layers of a cap in F₃⁷ contain 112 points each. Identify them with {0}×S and {1}×T in F₃×F₃⁶. By affine equivalence each of S,T has a center of symmetry. An affine shear and translation in the six remaining coordinates can send both centers to 0 independently. Thus S and T are linear images of the centered representative in README Section 2. The third layer undergoes a bijective affine coordinate change, so the number of possible positions there is unchanged.

Let ω be a primitive cube root of unity and use the unnormalized Fourier transform

\[
\widehat{1_S}(v)=\sum_{x\in S}\omega^{v\cdot x}.
\]

Central symmetry makes these Fourier coefficients integers: opposite nonzero character values contribute ω+ω²=−1. At v=0 the value is 112. At nonzero v the representative has value −23 when its centered hyperplane has 22 points and value 4 when that hyperplane has 40 points.

Let D be the set of nonzero v with value −23. The verifiers check on the representative that D is itself a central 112-cap, and that for x≠0,

\[
\widehat{1_S}(v)=4-27\mathbf1_D(v),\qquad
\widehat{1_D}(x)=4-27\mathbf1_S(x).
\tag{1}
\]

A linear change of coordinates transforms the dual by the inverse transpose, preserving these statements. The same holds for T and its corresponding dual 112-cap E.

Also, for every distinct projective pair [v],[w] in D/±,

\[
|S\cap v^\perp\cap w^\perp|=4.
\tag{2}
\]

Both programs check all 1,540 pairs for the representative. By linear equivalence, (2) holds for every S and its corresponding D, and likewise for T,E. The program does not assume that D and E are equal.

All representative checks use counts and modular arithmetic, not numerical complex arithmetic.

## 2. Cross-pair multiplicities

Set H=D∩E, and write |H|=2h with 0≤h≤56. For x∈F₃⁶ define

\[
m(x)=|\{(s,t)\in S\times T:s+t=x\}|.
\]

These are ordered pairs across two different layers. They include s=t when the six remaining coordinates coincide, because the full seven-dimensional vectors are still distinct.

For x≠0 put

\[
u(x)=\mathbf1_S(x)+\mathbf1_T(x)\in\{0,1,2\},
\qquad p(x)=|H\cap x^\perp|/2.
\]

Fourier inversion and (1) give

\[
\boxed{m(x)=16+4u(x)+3p(x)-h\quad(x\ne0),\qquad m(0)=2h.}
\tag{3}
\]

Here is the calculation explicitly. At nonzero frequency the product of transforms is

\[
16-108(\mathbf1_D+\mathbf1_E)+729\mathbf1_H.
\]

At x≠0, the constant-frequency contribution after inversion is

\[
\frac{112^2-16-108(4+4)}{729}=16,
\]

the membership contribution is 108·27/729=4 times u, and

\[
\sum_{v\in H}\omega^{v\cdot x}=2p-(h-p)=3p-h.
\]

At 0, the remaining constant is

\[
\frac{112^2+16\cdot728-108\cdot224}{729}=0,
\]

so m(0)=|H|=2h. Since S is central, m(0)=|S∩T| as well. Thus S/± and T/± have h common projective points.

A third-layer position z is allowed by the first two layers only if m(−z)=0. The set of zeros is central, so the number of such positions is the number of zeros of m. No assertion that all these positions form a cap is needed.

For h=0, (3) is positive for x≠0 and m(0)=0; there is only one zero. Hence assume h≥1. Then 0 is not a zero.

## 3. Projective state counts and exact moments

There are 364 projective nonzero points [x] in F₃⁶. Because S,T,H are central, u and p are well-defined on these points. Let g_{u,p} be the number of points with a given state.

A necessary state domain is

\[
\begin{gathered}
u\in\{0,1,2\},\quad0\le p\le h,\quad h-p\le45,\\
p\le20\text{ when }u=0,\qquad p\le11\text{ when }u=1\text{ or }2.
\end{gathered}\tag{4}
\]

Indeed H⊆D,E. If x is in S, D∩x^⊥ has 22 points, or 11 projective points; if x is not in S, it has 40 points, or 20 projective points, by (1). The same statement holds for T,E. The number of projective points of D outside any such hyperplane is at most 45. These prove (4). States impossible for other reasons are harmlessly retained.

The following eight sums are exact:

\[
\begin{aligned}
\sum g_{0,p}&=252+h,&\quad\sum g_{1,p}&=112-2h,&\quad\sum g_{2,p}&=h,\\
\sum p\,g_{u,p}&=121h,\\
\sum\binom p2g_{u,p}&=40\binom h2,\\
\sum\binom p3g_{u,p}&=13\binom h3,\\
\sum u p\,g_{u,p}&=22h,\\
\sum u\binom p2g_{u,p}&=4\binom h2.
\end{aligned}\tag{5}
\]

Unspecified sums range over all states. The first three follow from |S/±|=|T/±|=56 and their h-point overlap.

For the next three, H/± has no collinear projective triple. If three distinct projective points were linearly dependent, their relation would have three nonzero coefficients, each ±1, and centrality of H would turn it into a forbidden affine zero-sum triple in H⊆D. Consequently a projective point, pair, or triple of H is annihilated by respectively 121, 40, or 13 projective dual directions. Counting incidences proves the three binomial moments.

For the up sum, each [v]∈H/± is orthogonal to 11 projective points in S/± and 11 in T/±. For the u·binomial(p,2) sum, each pair of H is orthogonal to two points in S/± and two in T/±, by (2). Membership in both S and T is correctly counted twice by u.

Write

\[
X(u,p)=\left(\mathbf1_{u=0},\mathbf1_{u=1},\mathbf1_{u=2},p,\binom p2,\binom p3,up,u\binom p2\right),
\]

and

\[
R(h)=\left(252+h,112-2h,h,121h,40\binom h2,13\binom h3,22h,4\binom h2\right).
\]

Equation (5) is \(\sum g_{u,p}X(u,p)=R(h)\).

## 4. The 56 integer certificates

For each h=1,...,56, the supplied certificate is one of the following two forms.

**Zero-count certificate.** It supplies integers q and L>0 and exhaustively checks

\[
q\cdot X(u,p)\ge L\,\mathbf1_{16+4u+3p-h=0}
\]

for every state in (4), together with

\[
                       q\cdot R(h)<15L.
\]

After summing, the number of projective points with zero multiplicity is strictly less than 15. That count is an integer, hence at most 14.

**Impossible-intersection certificate.** It supplies integers q,K and checks

\[
q\cdot X(u,p)\ge K\quad\text{for all states},\qquad
                       364K-q\cdot R(h)>0.
\]

That excludes this h entirely. The program accepts neither a solver's infeasibility statement nor an omitted case: it checks the full sequence of all 56 h values and every integer inequality.

The complete coefficient tables, exact totals, and positive gaps are printed in `CERTIFICATE_TABLES.md`. In aggregate there are 2,022 states to check. The Python and C++ implementations evaluate them separately and agree on every total and gap.

For h≥1 each zero projective point accounts for its two opposite nonzero vectors, and 0 is not a zero. Thus at most 2·14=28 vectors have zero multiplicity. The h=0 case has only one zero. In every case there are at most 28 possible third-layer positions, proving the lemma.

## 5. Reproduction and trust boundary

The lemma alone may be checked with

```bash
python3 verify_hill.py
```

The complete `verify.py` and `verify.cpp` both perform the lemma's representative and finite-inequality checks. The original proof of uniqueness of the 112-cap remains the stated published input. The Fourier inversion, incidence counts, and connection between zeros and forbidden triples are the mathematical reduction, supplied above for inspection.
