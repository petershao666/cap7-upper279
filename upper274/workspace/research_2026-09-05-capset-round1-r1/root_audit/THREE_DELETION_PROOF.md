# Three deleted points: a recovered, scope-limited bridge

## Statement

Let S,T be arbitrary affine images of the six-dimensional 112-cap, placed in two parallel layers of F3^7. Delete D_S from S and D_T from T, where |D_S|+|D_T|<=3. At most **50** third-layer positions avoid every cross-layer zero-sum triple. Consequently the ordinary seven-dimensional types (112,109,51) and (111,110,51) are impossible, given the accepted completion theorem for sizes at least109.

This is a bound on possible third-layer positions, which need not themselves form a cap. It is not a global upper274 proof. A missing continuation archive was said to contain an auxiliary three-deletion lemma; this result must be treated as recovered/possibly overlapping prior work, with no novelty claim based solely on the missing source.

## Frozen mathematical inputs

Use the published uniqueness of the112-cap, the verified centered representative and Fourier/incidence reduction in the prior HILL_PROOF.md, the accepted103-point extension-rigidity lemma, and the verified two-deletion threshold certificate. No total275 or276 extremal exclusion is used.

After an affine shear, normalize both centers to0. If D,E are the dual central112-caps and |D intersect E|=2h, then for x!=0:

    m(x)=# {(s,t) in S x T : s+t=x}=16+4u(x)+3p(x)-h,
    u(x)=1_S(x)+1_T(x), p(x)=|(D intersect E) intersect x^perp|/2.

Also m(0)=2h. Allowed projective states obey 0<=p<=h, h-p<=45, p<=20 for u=0 and p<=11 otherwise, and m>=0. On the364 projective points the eight features

    X=(1_(u=0),1_(u=1),1_(u=2),p,C(p,2),C(p,3),u*p,u*C(p,2))

sum to

    R(h)=(252+h,112-2h,h,121h,40*C(h,2),13*C(h,3),22h,4*C(h,2)).

For a fixed x, cross-pair representations form a matching between S and T: each s determines t uniquely and conversely. Thus each deleted vertex destroys at most one representation, so a newly available x must have m(x)<=3. The allowed z in the third layer are negatives of these x.

## The additional deletion-incidence step

If h=0 modulo3 and m(x)=3, reduction of the multiplicity formula modulo3 yields 1+u(x)=0 modulo3; since u in {0,1,2}, u=2. Thus x belongs to both S and T, and centrality gives -x in both. The representation (-x,-x), whose sum is x in characteristic3, can be destroyed only by deleting coordinate -x from at least one layer. Different x require different deleted coordinates. Therefore at most three actual vectors x with m(x)=3 can become available. This is a count of vectors, not twice a projective count.

The old threshold<=2 certificate bounds all nonzero vectors with m<=2 by44 for 2<=h<=45 (its proof counts the threshold set, not just the points opened by a particular deletion). This does not assert the same bound at h=56, where diagonal multiplicities occur at112 vectors. Hence h=0 modulo3 with 3<=h<=45 leaves at most44+3=47 possible positions. The origin cannot open because2h>3.

## Remaining intersection parameters

For h=2..45 not divisible by3, every count record in deleted3_certificate.json provides integers q and L>0 with

    q.X(u,p) >= L*1_(m<=3),  q.R(h) < 26L.

The certificate is checked on every allowed state, so there are at most25 projective points with m<=3, hence at most50 nonzero vectors. The origin has2h>=4 and cannot open.

For h=46..51 each record supplies q.X>=0 and q.R(h)<0, excluding that intersection. For h=52..55 the two dual112-caps intersect in at least104 but fewer than112 points, contradicting103-point extension rigidity. At h=56, D=E and the Fourier identity gives S=T. For nonzero x in S the multiplicity is1; for nonzero x outside S it is20. Thus at most three diagonal representations can be destroyed, and0 cannot open.

At h=0,1 every nonzero multiplicity is at least15>3; only the origin can be available. These cases contribute at most1. These disjoint ranges cover h=0..56, giving the asserted maximum50.

## From the bound to ordinary seeds

A112-point slice and a109-point slice have respective completions with0 and3 deletions. Two slices of111 and110 points have1 and2 deletions. The whole109/110/111 slices are completable by the frozen theorem. In either situation, a third layer of51 points exceeds the50 possible cross-triple-free positions. Therefore both stated types, and every coordinatewise dominating type after decreasing sorting, are ordinary exclusions. No minimum-direction assumption is present.

## Certificate generation and independence

discover_deleted3.py creates rational duals using a numerical optimizer, then exact integer repair and inequality checks. Solver statuses alone are never proof. verify_deleted3.rb independently regenerates every finite state and exact total using Ruby integers, without importing discovery code, any predecessor kernel or an optimizer. Both share the new coefficient data and the old mathematical identities. A separate agent reviews the deletion-incidence and model-to-cap arguments before root promotes use of the seeds.
