# Seven-dimensional upper bound 274: proof and certificate dependency map

This is a research proof record, not a paper or a publication-priority claim. Acceptance is determined by `VERIFICATION.json` in this directory. The proof uses the published lower-dimensional classification and completion inputs listed below and the frozen, independently checked finite certificates.

## Statement

Every cap in the affine space \(\mathbb F_3^7\) has at most 274 points. With the previously verified 236-point construction, the resulting internally verified interval is

\[
236\leq f(7,3)\leq274.
\]

The existence of a 237-point cap remains unknown.

## Reduction to the last minimum state

Suppose that a 275-point cap \(A\) exists. For a projective direction \(D\), let \(t_D=(a,b,c)\) be its sorted parallel-hyperplane section sizes. There are 1093 directions. The published bound in dimension six gives \(a,b,c\leq112\), and \(a+b+c=275\).

Write \(E_2=ab+ac+bc\), \(E_3=abc\), and

\[
Q(a,b,c)=9E_3-899E_2+15730000.
\]

Each pair of distinct points is separated by 729 directions. Each triple of points in a cap is noncollinear and occupies all three sections in 243 directions. Hence

\[
\sum_D Q(t_D)
=9\cdot243\binom{275}{3}
-899\cdot729\binom{275}{2}
+1093\cdot15730000=-246950<0.
\]

Choose an actual direction minimizing \(Q\). Its value is negative. On every size-275 profile,

\[
4Q=(3c-275)^2(c-67)+(899-9c)(a-b)^2.
\]

The exact finite profile and whole-section completion partition is recorded in `../one_state_bridge/PROOF.md` and `../one_state_bridge/VERIFICATION.json`. It covers all 341 sorted profiles, including all 56 negative ones and every physical completion-state assignment; equal-sized sections are not identified. The original round-one 88 exact certificates were previously independently checked on 153,548,040 raw matrix rows. Those replays are inherited, not rerun or counted as new research.

After those certificates, the possible negative minimum states were precisely the following eight. In each row the two large whole six-dimensional sections have completion state NC, meaning not contained in a 112-cap; the third section has no additional completion hypothesis.

| Minimum profile | Independent accepted closure |
|---|---|
| (105,105,65) | H3-THETA40-PHI105-MIN10510565 |
| (108,107,60) | L-THETA40-INCIDENCE-MIN10810760 |
| (108,106,61) | P3B-POINTED107-TRANSFER108-MIN10810661 |
| (107,107,61) | L-THETA40-INCIDENCE-MIN10710761 |
| (107,105,63) | P5-SHARED107-MIN10710563 |
| (107,106,62) | P6-ALL5D-SHARED107-MIN10710662 |
| (106,105,64) | L-COMPLETE41-MIN10610564 |
| (106,106,63) | Last certificate proved below |

The first seven closures and their input hashes are bound by the one-state audit. All are minimum-only statements. The ordinary transverse exclusions remain exactly the 18 previously justified ordinary bans. Neither a minimum-only closure nor an empty conditional prefix case is inserted as an ordinary ban. Thus the last possible actual minimizing direction has profile (106,106,63), states (NC,NC,*), and \(Q=-7396\).

## The incidence identity used by the last certificate

For a cap in \(\mathbb F_3^d\) and a fixed direction with section sizes \(a_0,a_1,a_2\), put \(D=(3^{d-1}-1)/2\). The remaining projective directions split into triples on the \(D\) projective lines through the fixed direction. Each such line gives a 3 by 3 refinement matrix \(M\), whose physical column \(j\) sums to \(a_j\).

Let

\[
T(M)=\sum_{i,j\in\mathbb F_3}M_{i0}M_{j1}M_{-i-j,2}.
\]

Over the \(D\) refinements, the exact sums of
\(X=(T,E_{2,0},E_{3,0},E_{2,1},E_{3,1},E_{2,2},E_{3,2})\) are

\[
F_T=\frac{D-1}{3}a_0a_1a_2,
\quad F_{2,j}=3^{d-2}\binom{a_j}{2},
\quad F_{3,j}=3^{d-3}\binom{a_j}{3}.
\]

The first equality counts triples from the three parallel sections; the cap condition ensures their vector sum is nonzero. The other equalities count separated pairs and noncollinear triples inside a physical section. Restricting the refinements to one section visits every direction of that section once. These give the factors (13,27,9), (40,81,27), and (121,243,81) in dimensions 5, 6, and 7 respectively.

If a pointwise certificate has the form

\[
K\leq q\cdot X(M)+\sum_j g_j(t_j(M))
-\sum_{r=1}^3\Theta(s_r(M)),
\]

then summation yields

\[
\sum_{\text{all directions}}\Theta
\leq \Theta(a)+q\cdot F+\sum_j B_j-DK,
\]

provided \(\sum g_j\leq B_j\). Additional features with exact totals have unrestricted coefficients. Features with only an upper total require nonnegative coefficients; every such sign is checked. At the outer layer the three subtracted \(\Theta\) terms are absent.

## Three complete 40-point layers

The integer coefficient packet is
`../../compatibility/two_local_theta400_certificates/RESULT.json`, SHA-256
`78238a2e3f389f9c7a4f93e049ad56e678c09103151fb3bfed0adc6e1dcf14bf`.
Function identifiers 400, 401, and 402 all refer to mathematical size 40 in dimension five.

Every 40-point cap is covered by its first appearing anchor among the 44 possible sorted types, in descending order. Earlier anchors are excluded only conditionally within that case. Each layer has 43 nonempty cases and the last (14,13,13) conditional case, whose refinement domain is empty under the accepted grid exclusions. All 44 cases, including this boundary case, are independently checked.

The support functions on physical 16-, 17-, and 18-point four-dimensional sections use the accepted complete families of 376, 102, and 17 directional histograms. The 17-point direction-cover feature and the unique 19- and 20-point marginal histograms keep their exact scope. The coupled (18,18,4) support uses the 267 admissible ordered histogram pairs reconstructed from the accepted primary capacity table. The (20,18,2) support uses the 16 applicable histogram states. These are physical-column conditions, not unrestricted marginal assumptions.

Only two local moment vectors were changed from the frozen integer discovery checkpoint: those for anchors (20,17,3) and (20,15,5) in layer 400. The exact local coefficients and forced vectors are displayed in `../../compatibility/two_local_theta400_certificates/PROOF.md`. Their case bounds are respectively -9977029449239280 and -9931932768117975. All function tables and other case coefficients stayed fixed. The independent full-domain checks give

| Function | Bound on its sum over all 121 directions |
|---|---:|
| \(\Theta_{400}\) | -9829345995830952 |
| \(\Theta_{401}\) | -9618859046048364 |
| \(\Theta_{402}\) | -10564264755104425 |

Root checks 106,239 raw matrices per layer, with all ordered second and third columns. Sorting the first column uses one common affine permutation of the three refinement levels and loses no matrix. No physical-column permutation is used. There are 36,455 cyclic-normalized cover rows per layer; this count is a cover comparison, not a count of geometric objects or disjoint orbits.

## The universal NC106 layer

For a six-dimensional 106-point NC cap, let \(R=E_3-39E_2\). Its total over 364 directions is -37112985, less than \(364(-101958)=-37112712\). Thus some direction has \(R<-101958\). Applying the accepted ordinary and whole-NC restrictions leaves exactly 14 such anchor types:

```
(41,41,24), (42,41,23), (42,42,22), (43,40,23),
(43,41,22), (43,42,21), (43,43,20), (44,40,22),
(44,41,21), (44,42,20), (44,43,19), (45,40,21),
(45,41,20), (45,42,19).
```

Taking the first occurring anchor covers every NC106 cap. The functions \(\Theta_{400},\Theta_{401},\Theta_{402}\) apply respectively at physical column 1 of (43,40,23), (44,40,22), and (45,40,21). Each of the six physical 41-point and six physical 42-point sections has its own support function. Its bound is the exact maximum on the complete accepted 44-member or 4-member histogram family. In particular all 41-point sections are covered, whether or not they can be extended. The 14 zero coordinates of the complete 41-point family are used only in their valid five-dimensional scope.

The original 14 NC106 domains and the full 42-point support family are retained. No later whole42 state disjunction is required. Independent NC106 replay checks every one of the 1,106,094 fully ordered raw matrices and recomputes all 14 case sums, yielding

\[
\sum_{364\text{ directions}}\Phi_{106}\leq
B_{106}=-35039780423844643.
\]

This bound is universal for the stated NC106 class, independent of the seven-dimensional minimum-direction condition. P's generator and row compiler are separate from the discovery implementation and from root's lower/outer enumerator.

## Contradiction in the last seven-dimensional state

Apply the frozen outer inequality at the actual minimizing direction (106,106,63). The domain includes all ordinary admissibility restrictions, both whole-section NC predicates, the 18 ordinary bans, and \(Q(t)\geq-7396\) for every transverse direction.

Root's independent wide-integer checker verifies every one of its 7,382,307 raw matrices and obtains

\[
K_{\rm out}=43471588119828.
\]

The 12 extra fixed upper-function coefficients at this outer layer are all zero. Therefore summation uses only the seven moment totals and the two copies of the newly proved \(B_{106}\), and requires

\[
364K_{\rm out}\leq U_{\rm out}
=15823509458918317.
\]

But exact integer arithmetic gives

\[
364K_{\rm out}-U_{\rm out}
=148616699075>0,
\]

a contradiction. This excludes the last possible actual minimum state. The negative total of \(Q\) required a minimum state, so a 275-point cap cannot exist. Any larger cap contains a 275-point subset, also a cap. Consequently \(f(7,3)\leq274\).

## Premises and independence

The published cap bounds, classifications, and completion results in the audited upper-275 baseline remain premises. Additional finite inputs include the actual 16/17-point histogram families established by complete finite enumeration and independently checked in this campaign. The primary 18-point capacity table and the complete 41-point histogram family are recovered published inputs; the latter uses Thackeray's Theorem 6.3 and the explicitly asserted ancillary-list completeness in Proposition 6.2(b). Recovery of those published inputs is not a new classification. See `../complete41/PROOF.md` and its component audits.

The original upper-275 full C++/Python audit and the round-one 88 certificate replays remain inherited evidence. The new final-certificate replay uses root's own standard-library data/support checks and standalone C++ lower/outer kernel, plus P's independently generated fully ordered NC106 domains and row compiler. Discovery and author replay share a kernel and are not counted as independent verification. Root's earlier checker is reused and that reuse is explicit. All implementations share the published mathematical premises and frozen coefficient/input data.

The new lower/NC106/outer checks comprise 8,807,118 raw matrix rows and 15,885 finite support checks. These are exhaustive checks within complete declared covers, not sampling. C++ products and sums use signed 128-bit integers with magnitude checks and undefined-behavior sanitization; Python uses arbitrary-precision integers. Final acceptance and hashes are recorded in `VERIFICATION.json`, with no claim of independent reproof of the published classification searches.
