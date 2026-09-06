# Verdict: a complete necessary histogram overcover

The proposed union is a complete necessary overcover of the40-direction histograms of all16-point caps in AG(4,3). The simultaneous-geometry large-anchor part consists of actual caps when its finite searches are carried out exactly. The appended fourteen small-only vectors are necessary moment solutions, and their realizability is not asserted. This distinction is essential: the proposal is not yet a complete family of realizable histograms.

This audit proves the cover and checks exact arithmetic only. It does not enumerate16caps, run an LP, or verify a later implementation's complete actual-family output. No root or L generation kernel is imported.

## Exhaustion by large anchors or the small-only branch

Every hyperplane section is a3D cap and has size at most9. The complete decreasing triples summing to16 with maximum8 or9 are exactly

`970,961,952,943,880,871,862,853,844`.

If a cap has any such direction, choose one and relabel the levels as0,1,2, with the first large section A at0. Any permutation of the three labels is affine because AGL(1,3)=S3. Equal-sized sections may remain ordered; no swap reduction is needed. If desired, selecting the first occurring anchor in the displayed order permits banning earlier anchors only inside that branch. Such prefix bans are unnecessary for an overcover obtained by taking the union of all nine families.

If no large anchor occurs, every direction has maximum at most7. That branch is addressed separately below. Thus the two parts exhaust all16caps.

## Normalization of A and exact singleton shear

At every large anchor, A has size8 or9. The independently accepted full3D catalogue gives all three affine8cap orbits and the single affine9cap orbit, with explicit representatives. Hence there is an affine map `x -> Lx+v`, with L invertible, taking A to one of these representatives. These data are frozen in `../h17_representatives_explicit.json`; their complete all-subset/full-group verification is recorded in `../H17_COVERAGE_PROOF.md`.

Suppose the third layer C is nonempty and choose any one of its points z*. Put

`w=Lz*+v`,

and apply the ambient affine map

`(t,x) -> (t,Lx+v+t*w)`.

Its linear part is block triangular with diagonal blocks1 and L, so it is invertible. It acts on A at level0 by precisely the chosen normalizing map. The chosen point in layer2 maps to `Lz*+v+2w=0`. Thus A is normalized and0 belongs to the transformed third layer simultaneously.

For original points a,b,c in levels0,1,2, their new coordinates are respectively

`a'=La+v`,

`b'=Lb+Lz*+2v`,

`c'=Lc+2Lz*`.

Consequently `a'+b'+c'=L(a+b+c)` overF3. The selected point c=z* maps to0. These formulas explicitly verify the signs and prove that cross-layer collinearity is preserved in both directions. The special case where A is already normalized is the shear `(t,x)->(t,x+t*z*)`, which fixes A pointwise.

## Exact restrictions on B and C

In F3, a triple of layer labels with sum zero is either all equal or all distinct. Indeed `2i+j=0` implies j=i. Therefore a triple involving multiple layers has one point in each of0,1,2. Its points are collinear exactly when their coordinate sum is zero.

All within-layer triples are handled by requiring A,B,C separately to be caps. If C contains0, the cross triples using that point force `B intersect(-A)=empty`. Thus B is an actual cap of its prescribed size in the complement of -A. This restriction also guarantees that0 is available in

`F=AG(3,3) minus (-(A+B))`,

where `A+B={a+b:a in A,b in B}`.

For arbitrary c in C, avoiding all cross triples is precisely the condition `c not in -(A+B)`. Therefore, after choosing A and B, taking every actual c-cap C contained in F and containing0 is both necessary and sufficient. There are no additional cross-layer conditions involving two points from one layer and one from another, because such layer labels cannot sum to zero.

If the third layer is empty, there are no cross triples at all. In the970 and880 families B must therefore range over all actual caps of size7 and8 respectively, with NO complement(-A) restriction. Imposing that restriction in these two families would discard valid members without justification.

This proves completeness: every original large-anchor16cap admits the described normalization, after which its B and C occur in the stated exhaustive choices. Conversely every retained triple of internal caps satisfying these exact restrictions gives a genuine16cap. No enumeration of B or C has been performed in this theory audit; later code must exhaust those declared choices and must not add unproved symmetry reductions.

## Complete small-only moment branch

The decreasing triples of sum16 with maximum at most7 are exactly

`772,763,754,664,655`.

There are40 projective hyperplane directions in AG(4,3). A pair is separated in27 directions, and an affinely independent triple is separated into three distinct levels in9 directions. Every triple of a cap is affinely independent. Hence its histogram h satisfies

`sum h=40`,

`sum E2*h=27*C(16,2)=3240`,

`sum E3*h=9*C(16,3)=5040`.

The values of `7E2-E3-441` on the five displayed profiles are `(0,0,0,3,4)`. The whole histogram has total value `7*3240-5040-441*40=0`. Since all counts are nonnegative, this gives `3h664+4h655=0`, and therefore `h664=h655=0`.

Write a=h772, b=h763, c=h754. The remaining normalization and centered E2 equation are `a+b+c=40` and `-4a+2c=0`. Thus all nonnegative integer solutions, with no omissions, are

`(h772,h763,h754,h664,h655)=(a,40-3a,2a,0,0)`,

where `a=0,1,...,13`. Every one of these fourteen vectors satisfies both moment identities exactly. Nonnegativity gives a<=40/3, and actual integral direction counts sharpen this to a<=13. No cap realizing every vector is presumed.

For a linear Theta16 bound, checking the two endpoints a=0 and a=13 is enough: the vector at a equals `(1-a/13)h(0)+(a/13)h(13)`. Keeping all fourteen vectors is also valid. The endpoint statement concerns linear inequalities, not realizability or a nonlinear classification.

## Relation to L's weaker table model and limits

L's `theta16_gate/PROOF_AND_MODEL.md` has the same nine-anchor/small-only cover, and `COVERAGE.json` matches all fourteen types, exact moments, fourteen residual vectors and the two linear endpoints. Its conceptual mixed-refinement total `4abc` is correct: for one point from each section, their sum is a nonzero vector in the anchor3-space, and exactly four of its thirteen projective normals annihilate that vector. Keeping separate complete histogram-state variables for separate physical sections is a valid relaxation. Its map `h=anchor+sum13pencils(three other profiles)` has the correct40-direction multiplicity.

This audit has not independently replayed the1314 raw-table inventory or certified its implementation. The stronger actual-geometry cover proved above is the priority of this gate. The accepted small-section packet used by both approaches has SHA256 `dc1d5f0578ca3df5d0cf6da03d9b097d9e818c8523451c261e92d07414465018`.

`ARITHMETIC_CHECK.json` records the independent coefficient and14-vector checks. Once a later actual large-family enumeration is independently complete, adjoining the fourteen small-only vectors gives the claimed necessary finite overcover for certifying a universal linear Theta16 function. It does not by itself imply a new global cap bound or any publication-priority claim.
