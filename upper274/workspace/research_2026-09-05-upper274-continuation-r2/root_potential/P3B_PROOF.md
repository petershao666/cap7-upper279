# Exact exclusion of the Q67-minimum NC/NC state (108,106,61)

The certificate in this file has completed route-side and root independent exact replay and is accepted. It excludes one precisely specified extremal state; it is not an ordinary direction exclusion and does not alone lower the global bound275.

Assume a275-cap in F3^7 has a direction minimizing `Q67(a,b,c)=9abc−899(ab+ac+bc)+15730000`, with slice sizes `(108,106,61)`, and its108- and106-point slices are non-completable. Apply the complete marked cover and pointed moments proved and independently audited in P3 to NC107 caps S admitting an NC108 extension S union{x}.

The new full47-entry integer function phi is specified by `types` and `phi` in `pointed_joint_certificate.json`, frozen SHA256 `e0760693846143cf36a99d43a31aa7c7253cc39ebf1408bb92324a9c6256334b`. Its six exact local certificates prove conditional107 histogram bounds:

| Anchor of S | Marked column | Bound |
|---|---:|---:|
| (43,42,22) |1| −355846210849 |
| (43,43,21) |0| −355994410521 |
| (43,43,21) |1| −355994410521 |
| (43,43,21) |2| −355994433721 |
| (44,41,22) |0| −355994406227 |
| (44,42,21) |1| −355944415491 |

All other marked strata are excluded by the previously independently audited P3 cover. The local certificate identity is `q.X−sum(phi on three transverse S profiles)>=K`; summing121 directions gives `sum phi<=phi(anchor)+q.F−121K`. Thus the complete conditional family satisfies

`sum_(364 directions) phi <= B = −355846210849`.

As in P3, each of the108 deleted-point pairs from an arbitrary NC108 cap belongs to this conditional family. Hence the integer30-profile function

`Psi(t)=sum_i t_i phi(sort(t−e_i))`

satisfies the unconditional NC108 bound

`sum_(364 directions) Psi <=108B=−38431390771692`.

No rounding is involved here. One common integer scaling was used for the unknown function and every local/outer coefficient vector; the final B is the maximum of exact local expressions, not the numerical LP's bound.

The recovered proof has every restored-global108 histogram coefficient exactly zero in all six local certificates. Both reused P3 marked-branch exclusions also have zero coefficients on all such features. Therefore, although discovery included the H3/P2/fixedP3 restored108 functions, the final inequalities do not depend on them. Nonzero auxiliary inputs are exact43/44/45 spectra, two accepted42-point upper functions in the `(44,42,21)` marked stratum, and the accepted106-point histogram in the outer inequality. The marked geometry and exact restored predicates remain essential.

For each refinement of the assumed seven-dimensional root direction, let X be the usual seven moment features T,E2(alpha),E3(alpha),E2(beta),E3(beta),E2(gamma),E3(gamma). Here alpha is the108-point slice profile and beta the106-point slice profile. Let h106 be the accepted integer function `joint106_107_106_63_size276`. The exact outer inequality is

`16772577 T +699356293 E2(alpha) −18952959 E3(alpha)`

`−627556152 E2(beta) +12354611 E3(beta)`

`−234405693 E2(gamma) +4013462 E3(gamma)`

`+822 h106(sort(beta)) +Psi(sort(alpha)) >=3493400953736`.

The coefficient822 is nonnegative, as required for an upper histogram input. All other saved extra coefficients are zero. The ordinary forbidden directions and the condition that every transverse direction has Q67 at least Q67(108,106,61) are explicitly recorded in the certificate. No exclusion valid only at a different root minimum is used.

Summing364 refinements gives a left side at most

`1271595953973582`,

whereas the pointwise inequality forces it to be at least

`364*3493400953736`.

The difference is the strictly positive integer

`1993186322`.

This contradiction excludes the stated Q67-minimum NC/NC root state.

The standalone route-side local checker uses no discovery kernel and verifies85086 full ordered marked matrices, all six local minima and all30 transfer identities. A separately written C++ checker rebuilds the outer predicates from frozen lists and integer functions, retains every ordered alpha,beta,gamma, and verifies20980980 matrices with minimum3493400953736. Results are in `pointed_joint_local_verification.json` and `pointed_joint_outer_verification.json`. Root must independently reconstruct inputs and verify the mathematical domain before promoting this candidate.

The other registered P3b target `(108,107,60)` is deferred while root audits another agent's candidate for it, according to root's explicit priority change. No claim about that target follows from this certificate.

Root acceptance: independent standalone Ruby replay checked all21 strata and107217 full ordered marked matrices, including the reused two exclusions, and all30 induced table values. The frozen root C++ outer checker verified4203861 matrices with alpha sorted and all beta/gamma, attaining the same minimum3493400953736 and positive gap1993186322. Root explicitly accepted the mathematical domain and certificate. This is an internal verified extremal-state exclusion, without publication-priority claim.
