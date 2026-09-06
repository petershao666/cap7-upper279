# Pointed common-extension inequalities

This is an internal exact scoped result, with no publication-priority claim. All statements in this file concern a non-completable107-cap S in F3^6 together with one point x outside S for which C=S union{x} is a non-completable108-cap, or the resulting inequalities on NC108 caps. They do not assert any improved global seven-dimensional bound.

## Complete marked cover

Use the accepted rare-direction theorem for NC107 caps in `nested107_size276`: at least one of the ordered seven anchors

`(43,41,23),(43,42,22),(43,43,21),(44,41,22),(44,42,21),(44,43,20),(45,41,21)`

occurs. Choose the first one. Consequently all preceding anchors are absent in every other direction of S. Its three affine five-dimensional slices have sizes A=(A0,A1,A2). The extension point belongs to one fixed slice j. This j is fixed across the121 projective refinement directions in the five-dimensional kernel; it is never summed using a total from another j.

Each refinement gives a3x3 matrix M of four-dimensional cell sizes, with columns the three anchor slices. If x is in row r of column j, restoring x gives M+ by increasing just that entry by one. For fixed j, retain every r=0,1,2. Across the three j this covers all nine marked positions.

The discovery enumeration normalizes alpha and a coupled cyclic shear. The exact route-side verifier uses all ordered alpha,beta,gamma and all three row marks, so verification does not depend on the quotient. All original and updated columns and all nine original/updated mixed profiles `(M[i,0],M[k,1],M[−i−k,2])` satisfy the accepted five-dimensional cap predicate. All three transverse profiles of S lie in the complete47-element NC107 domain and avoid the preceding anchor prefix. The restored anchor and all three transverse C profiles lie in the complete30-element NC108 domain. Cell bounds are included. These conditions are necessary, not a claim of geometric realizability.

Thirteen of the21 anchor/j strata have an impossible restored anchor. Eight strata remain; the exact certificates exclude two of these and bound all six others. There is no omitted possible marked stratum.

## Exact pointed moments

For one refinement put `m=M[r,j]`, `p=M[r+1,j]M[r+2,j]` (row indices modulo3), and, writing a,b for the other columns,

`R = sum_(u+v+r=0 mod3) M[u,a] M[v,b]`.

The seven ordinary anchored moment features are T, then E2 and E3 of each column, where `T=sum_(i+k+l=0)M[i,0]M[k,1]M[l,2]`. Their sums over121 refinements for A are

`40 A0 A1 A2`, and, for each column n, `81 binom(n,2)`, `27 binom(n,3)`.

Apply the same identities to C, whose anchor sizes are A+e_j. Locally the differences are `Delta E2=A_j−m`, `Delta E3=p`, `Delta T=R`. Taking differences of the forced totals gives

`sum m=40 A_j`, `sum p=27 binom(A_j,2)`, `sum R=40 A_a A_b`.

This derivation uses the same extension point for every refinement. Equivalently the global pointed first and second binomial moments are121*107 and40*binom(107,2); removing the anchor subtracts A_j and binom(A_j,2), respectively. Those global totals are not incorrectly imposed separately on each marked-column stratum.

Exact43/44/45 five-dimensional spectra and accepted41/42 upper functions apply to original columns and the restored marked column. Each accepted108 histogram h with bound B_h contributes, on the three transverse restored profiles, a feature whose total is at most `B_h−h(sort(A+e_j))`. Inputs are the old direct psi108, three P2 transfers107→108, and root's audited H3_phi105_to108. No improved conditional107 bound is used as an input to its own proof.

## Certificate identity

For each retained stratum let X be the seven ordinary features followed, in the exact JSON order, by the indicated histogram and marked features, and let F be their exact equality totals or upper bounds. Upper-bound feature coefficients are nonnegative; equality coefficients are unrestricted.

For a fixed source histogram phi on NC107 direction profiles, each local certificate proves

`q.X − d sum_(three transverse S profiles t) phi(t) >= K`, with integer d>0.

Summing121 refinements proves

`d sum_(364 S directions) phi <= d phi(A)+q.F−121K`.

All coefficients, d, K, forced totals and numerators are in the frozen `pointed_result.json`, SHA256 `b232cf10117e0cd79eb1cdf7830c774934e146d48181c4ab54d92e624dfc78fd`. A separating certificate omits the phi term and has `121K−q.F>0`. The two separated strata are `(44,43,20),j=2` and `(45,41,21),j=2`. The full ordered replay checks107217 marked matrices and all local inequalities using Python integers. It imports no discovery kernels and rebuilds predicates, features, totals and prefix coverage from the accepted JSON inputs.

The resulting complete-family conditional bounds are:

Root independently replayed all107217 ordered marked matrices in standalone Ruby, all21 strata, all18 bound certificates and both exact exclusions: `../root_audit/pointed_independent.json`, PASS. The same source hash was frozen before the independent replay. The discovery and both verifiers share the accepted source theorem JSON and mathematical identities, but not executable kernels or generated enumeration inputs.

| Fixed107 function | Exact conditional upper bound | Safe integer upper bound | Old unconditional bound |
|---|---:|---:|---:|
| nested107_size276 | −322528231806731640051/1000000000000 | −322528232 | −321639387 |
| nested107_size277 | −173026594971255520621/500000000000 | −346053190 | −345314329 |
| joint107_107_106_63_size276 | −80909878377130558269/2500000000 | −32363951351 | −32290411632 |

The integer bound uses integrality of the histogram sum. These bounds are asserted only for NC107 caps that admit the specified NC108 extension.

## Induced108 inequalities

For any NC108 cap C, every deletion S_x=C minus{x} is NC107 by the accepted103-extension rigidity/heredity lemma. Thus all108 ordered pairs (S_x,x) satisfy the conditional theorem. For any profile t=(t0,t1,t2), define

`Psi(t)=sum_i t_i phi(sort(t−e_i))`.

Double counting deleted points and directions gives

`sum_(364 directions) Psi(t) = sum_(x in C) sum_(364 directions) phi(t(S_x)) <=108 floor(B_cond)`.

The saved tables retain the positive common divisor g of the corresponding audited P2 table. Their values are Psi/g and their safe integer bound is `floor(108 floor(B_cond)/g)`. The complete30-profile table has no missing deletion profile. This is an unconditional inequality on NC108 caps; it does not provide an unconditional inequality on arbitrary NC107 caps.

Both Q67-minimum NC/NC outer cases `(108,107,60)` and `(108,106,61)` were tested with these functions and all old/P2/H3 accepted cuts. Neither produced a positive dual certificate. This finite numerical result proves neither redundancy nor realizability. The global seven-dimensional upper bound remains275.
