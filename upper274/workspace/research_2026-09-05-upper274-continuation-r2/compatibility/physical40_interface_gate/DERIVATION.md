peter，Let P40 denote the histogram polytope specified by the entire retained44-case size40 proof layer: each case uses its complete finite refinement domain, forty refinement weights with total40, the exact/upper moments, and the accepted physical16/17/18 histogram constraints, including the267 ordered18 pairs and16 conditional18 states. The whole histogram is the anchor unit vector plus the sum of the three transverse unit vectors over the forty refinements. Take the convex hull over all44 first-anchor cases. Every actual size40 cap lies in P40; feasible points need not be actual caps.

All weights and auxiliary histogram mixtures live in bounded simplices. Linear programming duality for this finite polytope identifies its support epigraph with the complete certificate cone C40 of pairs (Theta,B) provable by the retained44-case hierarchy. In particular every actual40 cap satisfies sum_D Theta<=B. One proof layer uses a single Theta/B pair, while its case coefficients and every physical lower support function may vary independently across cases. This statement concerns the full exact finite cone; a bounded numerical search need not find its optimum.

There are exactly three parent occurrences of a physical40 section in the fourteen NC106 anchors: case3=(43,40,23), case7=(44,40,22), case11=(45,40,21), always physical column1. Case indices start at0. Each occurs once within its parent case. The two outer106 slices do not create six such universal proof tiers: one universal NC106 function is proved and then applied separately to both outer sections.

A shared pair (Theta,B) contracts at this interface against the sum of the three incoming marginal measures. If their nonnegative dual masses are alpha_j and their normalized121-direction histograms are z_j, the shared exact support condition is

    sum_j alpha_j*z_j in (sum_j alpha_j)*P40.

For positive total mass this says that the weighted mean belongs to P40. Other parent moments, predicates and constraints still constrain individual z_j; the statement does not say that the entire old model retains only this mean. It identifies precisely what the shared40 support cone itself can test.

Use instead three independent pairs (Theta_j,B_j) in C40, with three fully independent copies of its44-case proof tier. The corresponding interface requires

    alpha_j*z_j in alpha_j*P40, for each j.

When alpha_j=0, its physical marginal has zero mass and there is no division by zero. At positive mass each individual z_j must belong to P40. This is a strengthening because P40 is convex. In the certificate direction set all three pairs, all their case coefficients and every lower support copy equal to the old values: every old certificate embeds exactly. Thus the full new model is non-weaker, with no assumption that the actual sections are isomorphic.

Strictness at the histogram interface can be proved with a seven-coordinate rational witness, without an LP or cap enumeration. First observe that every40-cap satisfies h(20,20,0)<=1. Two distinct such hyperplane directions would each have an empty coset, leaving at most four nonempty intersections in their3-by-3 refinement. Each intersection is a3D cap of size at most9; hence the total would be at most36, contradicting40.

This bound is already exactly expressible inside C40. Set Theta to the indicator of (20,20,0), all local and lower coefficients zero and every local K=0. In the first case no transverse direction can be (20,20,0), by the same four-cell argument. In all later cases the first-anchor prefix excludes that profile. The resulting maximum whole bound is1. This is not a new previously unavailable lower theorem; it is used here to separate the interfaces.

The accepted complete (20,20,0) family realizes endpoints h0 and h10. Their midpoint hbar, on the ordered coordinates

    (20,20,0),(18,18,4),(18,11,11),(16,12,12),
    (14,14,12),(15,15,10),(17,15,8),

is (1,5,10,25,50,10,20). All other coordinates are zero. It belongs to P40 because it is the mean of two accepted actual histograms. Set

    v=(59136241,-154544760,151290368,-46118673,-9763176,0,0)/59136241.

The exact witness z1=hbar+v, z2=hbar-v, z3=hbar has nonnegative coordinates. Each has total121, E2 total63180 and E3 total266760. The three have exactly the same H3Theta40 total, -1209893448355, strictly below its accepted bound -1209524081280 by369367075. These equalities are checked by rational arithmetic in check_witness.py, which also binds h0/h10 to the already frozen root actual-histogram list.

The mean of z1,z2,z3 is hbar. Therefore every shared (Theta,B) in C40 accepts their equal-mass aggregate, and the fixed H3 bound accepts each separately. But z1 has h(20,20,0)=2, violating an inequality already in C40. Thus individual C40 membership is strictly stronger than aggregate C40 membership together with the fixed H3 bound. This is an exact interface separation. No lift of these three vectors to the complete parent NC106 matrix/moment system has been established; consequently strict improvement of the entire H23 feasible set or of its objective is not asserted.

This distinction also answers the absorption question. Adding one fixed H3Theta40 upper bound to the shared model cannot generally replace independent C40 constraints: the witness satisfies that fixed bound and still fails individual membership. After introducing independent C40 copies, however, explicitly adding that fixed bound is mathematically redundant. H3's proved pair (Theta0,B0) already belongs to C40, and C40 is a convex cone. Any nonnegative multiple of the fixed contribution can be absorbed into the relevant (Theta_j,B_j) and its copied proof coefficients. A positive uniform rescaling handles any homogeneous discovery coefficient box; it does not change the existence of a strict certificate.

The minimal interface uses44 values and one whole bound per j; each Theta_j appears at its sole physical40 parent occurrence with fixed coefficient+1. Never multiply two unknown coefficients. Its lower tier has40 refinements and whole-direction count121; the scalar representing B_j is B_j/121. The physical16/17/18 support scalars in that tier remain divided by40. At the NC106 parent the row contains Theta_j(profile)-B_j/121, with the whole NC106 scalar B106/364. The final outer contradiction remains364K_outer-q_outer*F_outer-2B106>0. The new40 bounds are already absorbed into B106 and are not added a second time at the outer layer.
