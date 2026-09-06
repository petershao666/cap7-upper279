# Exact-arithmetic proof package: 236 ≤ f(7,3) ≤ 277

## Result and scope

This package excludes **every 278-point cap in F₃⁷**. Every larger cap would contain a 278-point subcap. With the included 236-point construction, this proves

\[
                         \boxed{236\le f(7,3)\le277}.
\]

The upper bound improves the preceding release's 278 by one. This is **not an exact determination** of f(7,3), a claim that 277 is attainable, a publication-priority claim, or independent mathematical peer review.

The proof uses the published lower-dimensional results explicitly listed in Section 1. Their authors' original classification searches are not rerun. The preceding release's additional lower-dimensional lemmas **are rerun**, as are every new finite inequality and every representative computation required here. A floating-point optimizer proposed coefficients during discovery; no optimizer, failed cap search, or numerical infeasibility claim is part of verification.

The new argument does **not** prove that all forty previously targeted slice triples are universally impossible. Instead, it proves that none of the remaining possibilities can be a direction minimizing a specified polynomial over all directions. This distinction is essential to the proof and its noncircular implementation.

## Reproduction

Run either complete verifier from the extracted package directory:

```bash
python3 verify.py

c++ -std=c++17 -O2 verify.cpp -o verify
./verify
```

Python 3.10+ and its standard library suffice. C++17 and its standard library suffice. A more defensive compilation, also used for the recorded run, is:

```bash
c++ -std=c++17 -O2 -Wall -Wextra \
  -fsanitize=undefined -fno-sanitize-recover=all verify.cpp -o verify
./verify
```

Additional commands:

```bash
python3 compare_verifiers.py
python3 generate_cpp_data.py
python3 baseline278/check_points.py
python3 check_integrity.py
```

`generate_cpp_data.py` transcribes `certificate.json`; it does not discover coefficients. Python reads JSON; C++ reads the included integer transcription. Both rerun the necessary inherited lemmas before the new argument. They do not assume the previous seven-dimensional upper bound.

`baseline278_certificate.zip` is byte-identical to the preceding release. Its 33 source/data files are also preserved byte-for-byte under `baseline278/`. The auxiliary `baseline_kernel.hpp` is a separate copy of the preceding C++ functions with only its old entry point removed and its data-header include redirected. The original is unchanged. Python checks the archive hash and every preserved file. The new proof is in the new files, not injected into the baseline.

The new local calculations evaluate 32,388,316 ordinary seven-dimensional matrices, 48,372,154 extremal seven-dimensional matrices, and 6,546 inner six-dimensional matrices. The inherited lemmas evaluate 1,442,220 universal and 373,653 conditional six-dimensional matrices. Thus each complete verifier performs **82,582,889 case-matrix evaluations**. Numerical matrices can recur in different cases: this is not a count of globally distinct matrices.

There are **208 local inequalities**: 97 inherited universal, 22 inherited conditional, 62 new ordinary, 24 new extremal (including 20 completion-status branches), and three new inner inequalities. The twenty branches cover 36,916,842 labelled states; the verifiers minimize exactly over the permitted labels for each matrix instead of redundantly evaluating equal feature values. The auxiliary pair-of-large-slices lemmas check 2,022 inherited and 1,462 new integer state inequalities. Representative and deletion-histogram checks are additional.

`CERTIFICATE_TABLES.md` prints every new coefficient and spectral function. The inherited tables remain in `baseline278/`. Recorded execution logs and the comparison program are included. `research/` contains optional discovery helpers and their executed logs; discovery is not required to verify the result.

## 1. Published inputs and inherited derived lemmas

The external inputs are unchanged from the preceding release:

* A four-dimensional cap has at most 20 points.
* A five-dimensional cap has at most 45 points; the 45-cap is unique up to affine equivalence. Every cap of size at least 43 is contained in a 45-cap. A 42-cap is either a subcap of a 45-cap or the exceptional class Δ686, with its stated histogram.
* A six-dimensional cap has at most 112 points, and the 112-cap is unique up to affine equivalence.
* Every six-dimensional 110-cap is contained in a 112-cap.
* The reflected-slice results concerning parallel five-dimensional 45-, 44-, 43-, and 42-point slices used to justify the four completion seeds below.

Precise references:

1. Aaron Potechin, *Maximal caps in AG(6,3)*, Designs, Codes and Cryptography **46** (2008), 243–259, DOI `10.1007/s10623-007-9132-z`: six-dimensional maximum and uniqueness.
   https://link.springer.com/article/10.1007/s10623-007-9132-z
2. Henry (Maya) Robert Thackeray, *The cap set problem: 41-cap 5-flats*, arXiv:2206.09719v1: Lemma 2.3 and its proof recall the four-dimensional bound; Theorems 4.1, 4.3 and Proposition 4.2 supply the 45-cap facts; Theorem 6.3 supplies the large five-dimensional classification.
   https://arxiv.org/html/2206.09719v1
3. Thackeray, *The cap set problem: Up to dimension 7*, arXiv:2206.09804v1: Theorem 2.1 and Table 1 give the large five-dimensional classification and Δ686 histogram; Theorem 3.9 gives completion at size 110; Proposition 3.5(a,b) and Propositions 3.7–3.8 supply the reflected-slice inputs.
   https://arxiv.org/html/2206.09804v1

The full statements and their use in the reduction are preserved in `baseline278/README.md`, Sections 1–6. In particular, completion at size **109** is a derived lemma checked by this package, not something attributed to the cited 110-point theorem.

Call a six-dimensional cap **completable** precisely when it is contained in a 112-cap. This does not mean merely extendable by one point.

The complete verifiers rerun these consequences:

1. The explicit 112-cap S has 56 directions of type (45,45,22) and 308 of type (40,36,36). Every exterior point lies on at least ten disjoint secants. Thus any cap containing at least 103 points of S is contained in S (extension rigidity).
2. Each point of S belongs to eleven of the distinguished 22-point sections and 110 of the distinguished 40-point sections.
3. The 97 unconditional six-dimensional slice exclusions, with their frozen dependency stages.
4. The four completion seeds
   \[
   (45,45,7),\quad(45,43,15),\quad(44,44,15),\quad(45,42,20),
   \]
   and the 22 further conditional completion certificates. Every new conditional type has size at least 103, so extension rigidity justifies propagation to larger dominating triples. Twenty are incompatible with any subcap of a 112-cap and are therefore unconditional exclusions.
5. Every 109-point cap is completable, from the supplied exact root contradiction of −4,416.
6. Two parallel 112-point slices leave at most 28 available third-layer positions, from the Fourier/incidence argument and 56 exact certificates in `baseline278/HILL_PROOF.md`.
7. The histograms of all deletions of 0, 1, 2, or 3 points from the 45-cap representative. There is a unique histogram at sizes 43, 44, and 45; at size 42 the deleted subsets yield three histograms, supplemented by the published Δ686 histogram. All 1, 45, 990, and 14,190 deleted subsets are checked, not sampled.

All comparisons of slice triples are componentwise after decreasing sorting. An impossible triple excludes larger dominating triples by deleting points within parallel layers. A completion-forcing triple of size at least 103 also propagates upwards by extension rigidity. The low-size completion seed (45,45,7) has its own threshold argument in the inherited proof; its propagation is not attributed to the 103-point lemma.

Let `Adm5` and `Adm6` denote the necessary slice predicates implemented by the verifiers. `Adm5` has entries in 0..20, total ≤45, and the cited five-dimensional restrictions. `Adm6` has entries in 0..45, total ≤112, the 112-cap type restriction at total ≥109, and all proved universal six-dimensional exclusions. A non-completable column additionally avoids all completion-forcing patterns. A completable column must be componentwise bounded by (45,45,22) or (40,36,36).

## 2. Universal count identities and local matrices

For a triple t=(a,b,c), put

\[
E_2(t)=ab+ac+bc,\qquad E_3(t)=abc.
\]

For an s-point cap in F₃ⁿ, summing over all \((3^n-1)/2\) hyperplane directions gives

\[
\sum E_2=3^{n-1}\binom{s}{2},\qquad
\sum E_3=3^{n-2}\binom{s}{3}. \tag{1}
\]

A pair is separated into different slices in \(3^{n-1}\) directions. A triple of cap points is noncollinear; its two independent differences are sent to (1,2) or (2,1) by \(2\cdot3^{n-2}\) nonzero functionals, or \(3^{n-2}\) projective directions. This proves both identities.

Fix a direction x with slice sizes (A,B,C), and identify its slices with \(\{j\}\times U_j\) in \(F_3\times F_3^{n-1}\). For each projective direction [y] on the latter space, form a 3×3 matrix M with columns α,β,γ, where αᵢ counts points in U₀ with y-value i, and similarly for β,γ.

Each column satisfies the lower-dimensional admissibility predicate. Each of the nine transverse triples

\[
(\alpha_r,\beta_{r+s},\gamma_{r+2s}),\qquad r,s\in F_3, \tag{2}
\]

does too: these are the three parallel sections inside the hyperplane y−sx=r. Also

\[
t_s(M)=\bigl(\alpha_r+\beta_{r+s}+\gamma_{r+2s}\bigr)_{r=0,1,2} \tag{3}
\]

is the whole cap's slice triple in direction y−sx.

Define

\[
T(M)=\sum_{i+j+k=0}\alpha_i\beta_j\gamma_k,
\quad f(M)=(T,E_2(\alpha),E_3(\alpha),E_2(\beta),E_3(\beta),E_2(\gamma),E_3(\gamma)).
\]

There are \(D_n=(3^{n-1}-1)/2\) refinement directions, and the exact sum of f is

\[
F_n(A,B,C)=\left(\frac{3^{n-2}-1}{2}ABC,
3^{n-2}\binom A2,3^{n-3}\binom A3,
3^{n-2}\binom B2,3^{n-3}\binom B3,
3^{n-2}\binom C2,3^{n-3}\binom C3\right). \tag{4}
\]

For the first coordinate, any u∈U₀,v∈U₁,w∈U₂ has u+v+w≠0, or it would form a forbidden cross-layer triple. Exactly \((3^{n-2}-1)/2\) projective directions annihilate that nonzero vector. The other six coordinates follow from (1) within the layers.

An integer inequality \(q\cdot f(M)\ge K\) on every admissible matrix, together with a valid summed upper bound U, gives a contradiction whenever

\[
                         D_nK-U>0. \tag{5}
\]

Additional exact features are treated identically. Every coefficient multiplying an upper-bound feature must be nonnegative. The only new outer upper-bound features here are the two copies of ψ from Section 5, both with coefficient +1.

Every enumeration sorts only α and otherwise visits all ordered β,γ. This is safe: every permutation of three row labels is affine over F₃. Applying it to every column preserves (2), permutes the directions (3), and preserves T, since three copies of a translation add to zero. All other features depend on sorted triples or on labels carried with the row permutation. The two complete verifiers do not use the extra rotational reduction used in discovery.

## 3. New auxiliary seed: a 112-point slice and a 111-point slice

**Lemma.** A 112-point slice and a parallel 111-point slice leave at most 34 possible third-layer positions avoiding all cross-layer zero-sum triples. Thus (112,111,35) is universally impossible.

Complete the 111-point slice to a 112-cap. After an affine shear and translation, both full completions S,T can be centered at 0 independently. Their nonzero Fourier transforms have the form

\[
\widehat{1_S}=4-27\,1_D,\qquad \widehat{1_T}=4-27\,1_E,
\]

where D,E are central 112-caps. All representative Fourier and incidence assertions are rerun by both verifiers; the detailed inversion is in `baseline278/HILL_PROOF.md`.

Let H=D∩E, |H|=2h. For x≠0 put

\[
u=1_S(x)+1_T(x),\qquad p=|H\cap x^\perp|/2.
\]

The original ordered cross-pair multiplicity is

\[
m(x)=16+4u+3p-h,\qquad m(0)=2h=|S\cap T|. \tag{6}
\]

Removing one point from T decreases each multiplicity by at most one. A newly available position must therefore have original multiplicity at most one.

For h=1,...,51, let g_{u,p} count nonzero projective points in state (u,p). We require

\[
u\in\{0,1,2\},\quad 0\le p\le h,\quad h-p\le45,
\quad p\le20\ (u=0),\quad p\le11\ (u>0),\quad m\ge0.
\]

The final inequality is simply nonnegativity of an actual count. The baseline incidence proof gives eight exact sums:

\[
\sum g_{u,p}X(u,p)=R(h),
\]

where

\[
X=(1_{u=0},1_{u=1},1_{u=2},p,\binom p2,\binom p3,up,u\binom p2),
\]

\[
R=(252+h,112-2h,h,121h,40\binom h2,13\binom h3,22h,4\binom h2).
\]

For every h the certificate either excludes the intersection parameter with a positive-gap integer inequality, or supplies integers q,L>0 such that

\[
q\cdot X\ge L\,1_{m\le1}\text{ on every state},\qquad q\cdot R<18L.
\]

Therefore fewer than eighteen projective points have m≤1, so at most seventeen do. They account for at most 34 nonzero vectors. At h≥1, the origin has m(0)≥2 and does not become available after one deletion.

All 51 cases and their 1,462 states are checked explicitly. For h=52,...,55, the overlap |S∩T|=2h≥104 forces S=T by extension rigidity, contradicting h<56. At h=56 the completions are identical: m=1 on S, m=20 on the other nonzero points, and m(0)=112. Each m=1 representation is the diagonal pair (−x,−x), by the cap property, so a single deletion exposes only one position. At h=0, only the origin has multiplicity at most one, because all nonzero multiplicities are at least sixteen. These cases complete the lemma.

## 4. Labelled completed-column identities

For a completed column of size N≥103, write d=112−N. Each direction is an original (45,45,22) direction or an original (40,36,36) direction. They remain distinguishable: the former has minimum at most 22, while the latter has minimum at least 36−d≥27.

Let t be the ordered remaining counts. In the second family, a permitted label j for the original 40-point section has

\[
t_j\le40,\qquad t_k\le36\quad(k\ne j).
\]

Its deletion count is \(d_0=40-t_j\). All compatible labels are retained, including ties. Nonnegative deletion counts then sum to d automatically. In the first family put this statistic equal to zero. Define

\[
f_0(t)=1_{\min t\le22},\qquad
f_1(t)=1_{\min t\le22}(22-\min t),\qquad
f_2(t,j)=\begin{cases}40-t_j&\min t>22,\\0&\min t\le22.\end{cases}
\]

For an actual completion, its original section identities induce permitted labels in every direction. The checked representative incidences give

\[
\sum f_0=56,\qquad\sum f_1=11d,\qquad\sum f_2=110d. \tag{7}
\]

This remains valid at N=106 or 107, when the original 40-point section need not be largest. In particular, f₂ is **not** replaced by 40−max(t) in those sizes.

Allowing labels that do not arise from one common completion only enlarges the family, so it is a safe relaxation. Every feature in a labelled state uses the same label. Since the polynomial is affine in the independent labels, checking its minimum over the permitted labels checks it for every labelled state exactly. Labels are carried by row permutations; they are not discarded during canonicalization.

A completion status belongs to an entire six-dimensional slice across all refinement directions. It is never chosen separately for individual directions. The completed-column restrictions apply only to the designated columns, not automatically to the transverse hyperplanes.

## 5. A new histogram bound for every non-completable 108-cap

Let C be a non-completable 108-point cap. The inherited unconditional and completion-forcing restrictions leave exactly thirty possible sorted hyperplane types. They, and an explicit nonnegative integer function ψ on them, are printed in `CERTIFICATE_TABLES.md`.

**Histogram lemma.** Every such C satisfies

\[
                \sum_{[x]}\psi(t_x)\le18\,044\,648. \tag{8}
\]

This assertion does not assume a classification of non-completable 108-caps.

### 5.1 Some rare direction must occur

Among the thirty possible types, designate

\[
(45,41,22),\qquad(44,43,21),\qquad(43,43,22). \tag{9}
\]

On all other twenty-seven types, the verifiers check

\[
E_3-39E_2\ge-105001.
\]

If no type in (9) occurred, summing would give a lower bound −38,220,364. But (1) forces

\[
81\binom{108}{3}-39\cdot243\binom{108}{2}=-38\,221\,470,
\]

which is smaller by 1,106. Thus at least one rare direction occurs.

### 5.2 A refinement partitions all other directions

Fix any whole-cap direction x. For every refinement direction [y], the three directions [y−sx], s∈F₃, are the three other projective points in the two-dimensional dual subspace spanned by x and y. The refinement directions enumerate all such subspaces through [x]. Hence each whole-cap direction except [x] occurs exactly once among them.

Consequently, for any function ψ on slice types,

\[
\sum_{[z]}\psi(t_z)=\psi(t_x)+\sum_{[y]}\sum_{s=0}^2\psi(t_s(M_y)). \tag{10}
\]

This identity couples full histograms with the local refinement matrices. It is stronger than treating the three t_s only as individually admissible types.

### 5.3 The three inner certificates

For each rare type t, append to the seven features f the exact type indicators for its columns of size 43, 44, or 45. Their sums are known from the unique, exhaustively checked histograms. Call the resulting features g and their forced sum G_t.

The integer certificate checks, on every six-dimensional refinement matrix whose whole cap is non-completable,

\[
q_t\cdot g(M)-\sum_{s=0}^2\psi(t_s(M))\ge K_t. \tag{11}
\]

Summing (11) over its 121 refinement directions and using (10) gives

\[
\sum_{[z]}\psi(t_z)\le\psi(t)+q_t\cdot G_t-121K_t=B_t.
\]

The exact bounds are:

| Rare type t | K_t | B_t |
|---|---:|---:|
| (45,41,22) | 3,207,159 | 18,041,753 |
| (44,43,21) | 7,437,230 | 18,044,648 |
| (43,43,22) | 3,543,239 | 18,028,351 |

The three exhaustive computations inspect 6,546 matrices in total. The maximum of the three bounds proves (8), because at least one rare direction exists. There is no dependence on any seven-dimensional exclusion.

## 6. Ordinary exclusions and the globally minimizing direction

For the seven-dimensional target, set

\[
Q(a,b,c)=9abc-911(ab+ac+bc)+16\,306\,924.
\]

In a hypothetical 278-cap, each direction has sorted counts

\[
112\ge a\ge b\ge c\ge0,\qquad a+b+c=278.
\]

There are 310 basic integer types. The new ordinary certificates exclude 60 types in one stage and two in the next. Each stage freezes its earlier exclusions until all its inequalities are checked. Their matrices use `Adm6`, the universal count identities, and the existing two-112 seed. Only after those stages is the new (112,111,35) seed added. The ordinary calculations comprise 32,388,316 matrices.

Using (1), the sum of Q over all 1,093 directions would be

\[
9\cdot243\binom{278}{3}-911\cdot729\binom{278}{2}
+16\,306\,924\cdot1093=-148\,313. \tag{12}
\]

Therefore choose a direction x whose value of Q is a **global minimum**; it has Q<0. For each local refinement matrix at this direction, the additional necessary restriction is

\[
                        Q(t_s(M))\ge Q(t_x)\quad(s=0,1,2). \tag{13}
\]

This is legitimate because each t_s describes another direction of the same cap. It does not assume that those directions are globally impossible.

After the ordinary exclusions and two seeds, only nine negative-Q types can be the chosen minimum. The verifiers check this list exhaustively. The following table gives Q and the exact contradiction gaps of all their local cases. Status 0 means non-completable, status 1 means completable, and statuses concern the first and second large slices. A single gap means no status split was needed.

| Minimum-direction type | Q | Gap, 00 | Gap, 01 | Gap, 10 | Gap, 11 |
|---|---:|---:|---:|---:|---:|
| (106,106,66) | −1,600 | 11,047 | 1,116,497 | 1,116,497 | 287,779 |
| (107,105,66) | −1,283 | 502,031 (unsplit) | — | — | — |
| (107,106,65) | −3,363 | 331,505 (unsplit) | — | — | — |
| (107,107,64) | −5,547 | 217,648 | 532,542 | 532,542 | 316,618 |
| (108,104,66) | −332 | 193,644 (unsplit) | — | — | — |
| (108,105,65) | −2,711 | 166,138 (unsplit) | — | — | — |
| (108,106,64) | −5,212 | 266,669 | 51,062 | 23,914 | 212,520 |
| (108,107,63) | −7,835 | 114,639 | 229,056 | 8,247,346 | 73,578 |
| (108,108,62) | −10,580 | 1,864,274 | 74,659 | 74,659 | 3,406,910 |

Four cases use ordinary seven-feature inequalities under (13). Five use all four completion statuses, giving twenty branches. Completed columns append (7). Non-completable columns avoid all completion patterns. The last case's 00 branch also uses (8), as detailed next.

Every table entry is a strictly positive gap of the form (5). **No conclusion in this table is inserted into the unconditional exclusion list, or used to eliminate another row.** Every row is an alternative for the same hypothetical globally minimizing direction, checked against the same previously established unconditional exclusions. This prevents circularity and avoids claiming a stronger type exclusion than was proved.

## 7. The final, previously unresolved branch

Suppose the globally minimizing direction has type (108,108,62), and both 108-point slices are non-completable. Define

\[
\begin{aligned}
F(M)={}&47T(M)-362\bigl(E_2(\alpha)+E_2(\beta)\bigr)
-6\bigl(E_3(\alpha)+E_3(\beta)\bigr)\\
&-146E_2(\gamma)-12E_3(\gamma)
+\psi(\operatorname{sort}\alpha)+\psi(\operatorname{sort}\beta).
\end{aligned}
\]

Both complete verifiers establish

\[
                         F(M)\ge7\,779\,630 \tag{14}
\]

on all **1,996,200** admissible matrices for this branch, including the global-minimum condition (13). The ordinary features have the forced sums (4); each copy of ψ has summed upper bound (8). Hence

\[
\sum F(M)\le2\,829\,921\,046.
\]

But summing (14) over 364 directions requires

\[
\sum F(M)\ge364\cdot7\,779\,630=2\,831\,785\,320.
\]

The difference is exactly **1,864,274**, a contradiction. Coefficients of both upper-bound features are +1, so there is no reversal of an inequality or use of an upper bound as an equality.

For another concrete example, (106,106,66) with both large slices non-completable uses

\[
10T-1178(E_2(\alpha)+E_2(\beta))+28(E_3(\alpha)+E_3(\beta))
-393E_2(\gamma)+13E_3(\gamma)\ge-4\,313\,912.
\]

Its 5,458,860 matrices all satisfy the inequality. The forced sum is −1,570,275,015, whereas 364 times the lower bound is −1,570,263,968; the gap is 11,047. The other three whole-slice statuses are separately checked, not inferred from this one.

## 8. Conclusion and exact verification boundary

Equation (12) forces a globally minimizing direction with Q<0. The ordinary exclusions and the two seeds reduce it to the nine rows above. Every row, and every required completion-status branch, contradicts an exhaustively verified integer inequality. Thus the hypothetical 278-cap does not exist. Taking subsets excludes every larger size:

\[
                              f(7,3)\le277.
\]

The identity

\[
4Q=(3c-278)^2(c-67)+(911-9c)(a-b)^2
\]

is also checked on all 310 types. The proof does not mistakenly assert Q≥0 on all basic types; it uses the global minimum and the certified case analysis to reach the contradiction.

The 236-point construction remains exactly the one in the preceding release, with two 112-point layers and a twelve-point layer. Its explicit list is `baseline278/cap236.txt`; both complete verifiers reconstruct it and check all 27,730 unordered distinct pairs. This proves the stated lower bound, not optimality of that construction.

The proof's trust boundary consists of the stated published mathematical inputs, the supplied geometric/counting reductions, and the exhaustive integer checks. Passing matrices form a superset of the matrices induced by caps. Independent label choices and possible incompatible directional choices enlarge that superset and cannot create a false exclusion when every retained case is tested.

The Python implementation uses bit-mask intersections for transverse constraints; C++ directly enumerates full Cartesian products. Neither uses feature deduplication or an optimization solver. C++ was run with undefined-behavior sanitization; Python uses unbounded integers. Agreement helps detect implementation mistakes, but is not a claim of independent mathematical review. The exact value of f(7,3) remains undetermined by this work.
