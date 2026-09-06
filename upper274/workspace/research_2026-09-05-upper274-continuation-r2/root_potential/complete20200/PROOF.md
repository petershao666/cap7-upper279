# Complete 20/20/0 histogram family

Every 40-cap in AG(5,3) having a hyperplane direction with section sizes (20,20,0) has one of exactly eight possible 121-direction histograms. They are parameterized by

`r in {0,1,2,3,4,5,6,10}`

as follows; all omitted profiles have count zero.

| Section profile | Number of directions |
|---|---:|
| (14,14,12) | 40+2r |
| (15,15,10) | 20-2r |
| (16,12,12) | 20+r |
| (17,15,8) | 40-4r |
| (18,11,11) | 2r |
| (18,18,4) | r |
| (20,20,0) | 1 |

Every listed histogram is realized by the explicit forty-point representative in `HISTOGRAMS.json`. The eight histograms are not asserted to be eight affine isomorphism classes. This theorem covers the stated section family only, not all 40-caps and not the seven-dimensional upper-bound problem.

## Accepted input and complete normalization

The published input is Theorem 4.9 of Thackeray, *The cap set problem and standard diagrams* (2021): the four-dimensional 20-cap is unique up to affine equivalence and its forty hyperplane directions have types (9,9,2) ten times and (8,6,6) thirty times. The [primary accepted manuscript](https://repository.up.ac.za/bitstream/handle/2263/85152/Thackeray_Cap_2021.pdf?sequence=1), printed pages 24-25, was directly checked in the preceding complete20201 audit. The accepted full actual 20-cap catalogue is `../complete20201/ALL20_MASKS.txt`, SHA256 `66946f5ef9ea1e10164a5b3e56cf89dede2b85efc50d8a8eb1e392e5862d2f41`. Its 682,344 distinct masks were independently obtained through all homogeneous quadratic polynomial coefficients and all symmetric-matrix coefficients, followed by all translations. Its completeness proof is preserved in `../complete20201/PROOF.md`; no quadratic enumeration is repeated here.

Choose the verified canonical cap A consisting of the nonzero zeros of `x0^2+x1^2+x2*x3`. It has twenty points and its 190 pairs pass the cap condition. Given an arbitrary 40-cap with a (20,20,0) direction, choose coordinates (t,x) in which the first two levels have size twenty and the third is empty. Every required permutation of the three levels is affine. By affine uniqueness, an invertible affine map `x -> Lx+v` sends the first section to A. Extending this map to `(t,x) -> (t,Lx+v)` preserves the layers. The second section becomes an arbitrary actual 20-cap B and hence occurs in the complete accepted catalogue.

Conversely every catalogue B gives a cap `A@0 union B@1`: three points are collinear over F3 exactly when their vector sum is zero, and a triple of layer labels summing to zero is either constant or uses all three labels. The latter is impossible with the third layer empty. The former is ruled out because both sections are caps. Thus there is no additional cross-layer constraint. In particular, requiring `B intersect (-A)=empty` would be unjustified and incomplete. The enumeration applies no such filter. The complete 682,344 choices give a cover of every original cap in the declared family.

## Direction-count formula and the geometric parameter

The chosen t direction has profile (20,20,0). Every other projective normal has the form `(e,d)` where d is one of the forty projective nonzero normals of F3^4, normalized by first nonzero coordinate one, and e ranges independently over F3. This gives 120 distinct additional directions and covers them all: any normal with d nonzero can be scaled uniquely to this normalization.

For a fixed d, let a_s and b_s be the section point counts at d.x=s. The functional d.x+e*t has whole-cap counts `a_s+b_(s-e)`. The implementation counts the twenty actual B points to obtain b and uses this exact formula for all three e. No direction is omitted or weighted by a guessed multiplicity.

Let r be the number of common (9,9,2) directions of A and B in their shared four-dimensional coordinate space. There are r directions where both section types are (9,9,2), 10-r in each of the two mixed orders, and 20+r where both are (8,6,6). For each fixed d the three possible cyclic offsets exhaust all relative positions of the exceptional entries, regardless of their original labels:

* Two (9,9,2) sections yield one (18,18,4) and two (18,11,11) directions.
* One (9,9,2) and one (8,6,6) section yield one (15,15,10) and two (17,15,8) directions.
* Two (8,6,6) sections yield one (16,12,12) and two (14,14,12) directions.

Adding these contributions proves the displayed formula for any such actual pair. The finite full-catalogue enumeration determines the exact possible set of r; it does not assume that every integer from zero to ten occurs. In particular, r=7,8,9 do not occur, while every r in the stated set has an explicit point witness.

## Full finite computation and exact checks

The prerequisite check verifies the accepted catalogue hash before dispatch. `enumerate_layers.cpp` then reads every mask exactly once in strict increasing order and checks its size twenty. For each B it constructs all forty five-dimensional point indices and checks every one of the 780 unordered pairs by exact coordinate completion. Total checked pairs: 532,228,320. It computes all 121 profiles for each cap, totaling 82,563,624 profiles, and checks the exact histogram identities

`sum h=121`,

`sum E2*h=81*C(40,2)=63180`,

`sum E3*h=27*C(40,3)=266760`.

The normalized B frequencies, in increasing order r=0,1,2,3,4,5,6,10, are

`16038,118260,236925,174960,106920,14580,14580,81`.

They sum to 682,344. `HISTOGRAMS.json` records each histogram, its frequency, one B mask and all forty explicit point coordinates and indices. `B_HISTOGRAM_IDS.txt` records every assignment: line j corresponds to line j of the accepted sorted B catalogue, and contains the final histogram id. Thus the entire finite cover, not only representative witnesses, is preserved.

The separate Ruby replay `check_representatives.rb` verifies frozen hashes, assignment counts and frequencies, every representative's distinctness and all pairs, and recomputes each representative histogram through all 242 nonzero five-dimensional normals followed by exact division by two. It also verifies the geometric common-direction definition of r independently of the three-offset formula. The replay uses shared frozen output points but no C++ helper kernel; it does not recompute all 682,344 assignment histograms. The full independent enumeration belongs to root's different diagonal-Q, normal-mask implementation.

## Linear-bound limitation

The formula is affine in r, and `h(r)=(1-r/10)h(0)+(r/10)h(10)`. Both endpoints are realized. Consequently the maximum of any linear histogram functional on this exact actual family is the maximum of its two endpoint values. The simple interval `0<=r<=10` already follows from r being the intersection size of two ten-direction sets, and the displayed h(r) formula follows analytically from the exact section spectra and the three offsets. Therefore the finite computation's exclusion of r=7,8,9 does not strengthen a linear relaxation that already permits all h(r) for `0<=r<=10`. The output establishes exact actual support and point realizability; it must not be presented as a stronger linear input without checking the previous model's existing constraints.

## Independence and scope

P uses the cross-term canonical Q and direct residue counts; root uses a diagonal canonical Q and normal-mask popcounts. Both intentionally share the already accepted complete 20-cap catalogue and the published affine uniqueness theorem. P read no root-generated 40-cap output before hashing its complete output in `FROZEN.json`. No unproved symmetry quotient, guessed histogram count, or optimization was used.

The finite run completed within its 300-second/1-GiB gate with one worker. The result supplies a complete actual histogram family for the (20,20,0) branch only. It is an exact scoped input and carries no claim of publication priority or a new global upper bound.
