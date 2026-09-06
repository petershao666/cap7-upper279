# H13 model derivation and claim boundary

This document gives the validity argument for the finite relaxation. It is not itself a proof excluding the target. A positive exact terminal certificate and independent replay would be needed for that conclusion.

For a cap C in F_3^5 with 40 points, choose its first directional type in the frozen ordering of all 44 possible sorted triples summing to 40 with entries at most 20. Every subsequent two-dimensional quotient through this fixed direction has three physical columns, the fixed parallel four-flat sections. Each physical 18-point section has one of the 17 full directional histograms obtained from the complete published 20-class classification. Fix that histogram for each such column before enumerating refinements.

If the fixed type is (18,18,4), Table 1 of Thackeray arXiv:2206.09719v1 bounds the possible third section for every pair of actual affine classes of the two 18 sections. Two full histogram states are therefore allowed only when the maximum table capacity over all pairs of classes realizing those states is at least 4. The maximum is necessary to avoid identifying distinct affine classes that have the same histogram. The corrected primary table gives 267 ordered pairs. At (20,18,2), the analogous maximum capacity condition gives 16 states; (19,18,3) gives all 17. These are necessary conditions and do not assert that every retained pair is geometrically realizable.

There are 34 anchors without an 18 column, eight unrestricted single-18 anchors with 17 states each, one (20,18,2) anchor with 16 states, and one (18,18,4) anchor with 267 state pairs. The total is 453. For each state, every absent direction type is removed only in that physical column of that case. Every positive full-histogram entry is an exact feature. Taking the union over the complete states therefore covers all 40 caps. Emptiness uses both the first-anchor prefix and fixed states; none is an ordinary global directional ban.

For a five-dimensional cap and fixed direction, the 40 two-dimensional quotients containing that direction correspond bijectively to all 40 projective directions on each four-dimensional section. Thus a physical section's histogram indicator of type t sums exactly to its fixed count h(t). Each quotient also supplies three transverse directions, which together run once through the 120 directions other than the anchor. If, for every allowed local matrix,

    q*f + sum(parent directional values) - sum(transverse theta values) >= K,

then summation gives

    sum_C(theta) <= theta(anchor) + q*F + sum(parent bounds) - 40*K.

All exact-feature coefficients may have either sign. Coefficients of one-sided upper features are constrained to be nonnegative. The analogous NC106 inequality uses 121 quotients, 363 transverse directions, and factor 121 instead of 40. Maximizing each whole-direction upper bound over all cases yields a universal theta40, a universal theta41 using the retained complete H11 cover, and an NC106 bound Phi106.

In the final registered Q67-minimum (106,106,63) NC/NC branch, 364 quotient refinements in dimension seven yield an upper quantity U=q*F+2*B106. A finite local lower bound K would exclude that branch only if the exact integer gap 364*K-U is positive. No global upper bound of 274 follows from this branch alone.

All unknown lower functions enter with the fixed coefficient +1. State-specific histogram multipliers multiply known integer counts, so every constraint is linear. Discovery uses the shared finite enumerator and proposer from earlier scopes; reuse is disclosed and is not independent verification. Root independent replay is required for any positive result. A numerical failure to obtain positive gap is reported solely as a search null.
