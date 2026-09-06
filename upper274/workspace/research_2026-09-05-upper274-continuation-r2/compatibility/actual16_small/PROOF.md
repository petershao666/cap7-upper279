# Completion of the actual 4D 16-cap histogram family

## Precise conclusion and verification status

Subject to independent enumeration comparison, the producer has exhaustively obtained exactly 376 distinct direction histograms of 16-caps in AG(4,3), with an explicit cap representative for each. The nine large-anchor enumeration is frozen separately in `../actual16/FROZEN.json`. The new small-only enumeration has zero retained caps. Consequently every 16-cap has an affine hyperplane section of size at least 8. This is a classification of direction histograms, not a classification up to affine isomorphism, and gives no seven-dimensional upper bound by itself.

## Coverage of the residual small-only family

An AG(4,3) cap has 40 projective directions. Its section profile in a direction is the decreasing triple t=(a,b,c). Assume all hyperplane sections have size at most 7. Since a+b+c=16, the complete possible type list is 772, 763, 754, 664, 655. Put E2(t)=ab+ac+bc and E3(t)=abc.

Every unordered pair of cap points lies in different hyperplanes in exactly 27 projective directions. Every unordered triple, being noncollinear, meets all three hyperplanes in exactly 9 directions. Hence

    sum E2 = 27*C(16,2) = 3240,
    sum E3 = 9*C(16,3) = 5040.

For the five types in the listed order, 7*E2-E3 is 441,441,441,444,445. Its global sum is 17640=441*40, so the last two types have count zero. The first three E2 values are 77,81,83. The two remaining equations therefore give histogram (a,40-3a,2a,0,0), with integer 0<=a<=13. If a>0 a 772 direction exists; if a=0 a 763 direction exists. Enumerating both anchors without a prefix restriction is a complete cover; duplication causes no exclusion error.

## Complete 7-cap affine overcover

The accepted complete affine 8-cap orbit representatives are masks 13851,13853,13902, using point index x+3y+9z. Root and P independently checked the complete actual 7-cap catalogue: all 126360 members have exactly four addable points, with 505440 extension incidences. Therefore any 7-cap is an 8-cap with one point removed. An affine map taking its 8-cap extension to one of these three representatives takes the original 7-cap to one of their 24 labeled single-point deletions. These 24 entries are an affine overcover; duplicates and any equivalences between deletions are retained.

The source result hash and all 24 labeled deletions are frozen in INPUTS.json. This bridge is shared accepted mathematical input. Our producer does not read root enumeration results or extension witnesses.

## Normalization and exact recursive search

Choose one of the two anchors and one of its 7-point first layers A. First apply an affine change in AG(3,3) taking A to a listed representative. On the full coordinates (t,z), all transformations of the form (t,z)->(t,Lz+v+t*w) preserve the layer coordinate and are affine bijections. If z* is a selected point of the nonempty third layer C, choose w=Lz*+v. At t=2 its image is w+2w=0, while the first layer remains L*A+v. For a triple with one point from each layer, the transformed inner-coordinate sum is L(a+b+c)+3v+3w=L(a+b+c).

Thus the exact conditions after normalization are:

* A, B and C individually are caps;
* B is contained in the complement of -A, since 0 belongs to C;
* C contains 0 and is contained in F=AG(3,3) minus (-(A+B)).

A triple crossing layers must use all three layers, so these conditions also suffice for the lifted set to be a cap. The large-family c=0 branches used no restriction B subset complement(-A); no such branch occurs here.

For each of the 48 labeled anchor/A cases, the producer recursively enumerates every cap B of the required size in complement(-A). An increasing-index cap recursion removes the point -p-q whenever a new point p joins an earlier q; this is both necessary and sufficient and enumerates each subset once. The same recursion enumerates all required caps C in F seeded with 0. No stabilizer, prefix or heuristic pruning is used. Counts are accumulated before the final small-only filter.

For each lift, all 40 profiles are computed. Besides the layer direction, the other directions are (alpha,u) for each of 13 normalized nonzero u in AG(3,3)* and each alpha in F3. Counts are formed by shifted sums of the three layer dot-product distributions. A lift is retained exactly when every profile has maximum at most 7. Early rejection upon seeing a larger section implements this same predicate.

## Exhaustive result and final point witnesses

The run completed all 48 cases in 0.180875 seconds under the registered 600-second gate and UBSan. The 772 anchor constructed 352440 cross-valid lifts; 763 constructed 732132. Their total is 1084572. Every lift was rejected by the maximum-section-7 predicate. There are therefore no small-only actual histograms to append to the 376 large-anchor histograms.

`SMALL_RAW.json` records all per-case B counts, free-set size counts, constructed counts and retained counts. `B_with_C` counts B states that yield at least one retained small-only cap; it is zero in every case. Constructed counts include all valid C before the filter, even when another direction has a large section.

`COMPLETE_ACTUAL16.json` contains the final 376 histograms in the common 14-type order, with 16 explicit four-coordinate points for every histogram. A separate Python routine recomputed all 45120 unordered point pairs and the 40 direct dot-product direction profiles of all 376 representatives. This confirms the realization half. Completeness follows from the two exhaustive covers and the normalization argument, subject to root's independent replay agreement.

## Shared dependencies and independent verification boundary

Our large and small recursive enumeration kernels share implementation lineage. Our point verifier independently uses coordinate pairs and direct four-dimensional dot products, but consumes our emitted representatives. Root independently uses alternative affine representatives and a full B-catalogue filter followed by C-subset enumeration; no root result was read before our FROZEN.json. Both enumerations share the accepted complete 3D 8/9 orbit input and the independently checked 7-extension bridge. P supplies a separate proof audit of normalization and residual coverage. Agreement is claimed only after root compares the frozen outputs.
