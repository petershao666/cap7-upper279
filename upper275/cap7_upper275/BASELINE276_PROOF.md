# Recorded reduction 277 -> 276: an exact-arithmetic cap certificate

## Result and trust boundary

Under the published mathematical inputs and the explicitly verified derived lemmas
in `baseline277/README.md`, this package excludes every 277-point cap in F_3^7.
Consequently **236 <= f(7,3) <= 276**. It does not establish 275 or 270, does not
assert that 276 is attainable, and is not a claim of publication priority or
independent mathematical peer review.

The preceding upper-277 ZIP is preserved byte-for-byte. The required inherited
lower-dimensional lemmas are rerun by both verifiers. The old seven-dimensional
bound is not assumed in the new proof. Published original classifications remain
external mathematical inputs, not computations rerun here.

## Reproduce

From this directory:

```sh
python3 verify_step.py 277
c++ -std=c++17 -O2 verify_step.cpp -o verify_step
./verify_step
python3 compare_verifiers.py
python3 check_integrity.py
python3 baseline277/baseline278/check_points.py
```

Python 3.10+ uses only its standard library. C++17 uses integer arithmetic.
The actual checks used Python 3.13.5 and GCC 14.2.0. No numerical solver is used
in verification. `results/size277/proof.json` is the complete certificate;
`step_data.hpp` is its integer C++ transcription. The recorded source versions
are the ones that passed both complete runs, not later research modifications.

Each verifier checks 38,040,573 new ordinary matrices, 77,458,499 new extremal
matrices, and 39,771 new inner matrices. The original lower-dimensional checks
are additional. These are case-matrix evaluations, not globally distinct caps.
The 109 new case and summary lines agree between implementations.

## 1. Imported lemmas and the matrix method

See `baseline277/README.md` Sections 1--4, including precise citations to
Potechin (2008), DOI 10.1007/s10623-007-9132-z, and Thackeray arXiv:2206.09719v1
and arXiv:2206.09804v1. The imports include f(6,3)=112 and uniqueness, completion
at size 110, the lower-dimensional classification and reflected-slice results.
Completion at size109 is a separately verified *derived* lemma. Completableness
here means containment in a 112-point cap, not just the ability to add a point.

For a triple t=(a,b,c), set E2=ab+ac+bc and E3=abc. An s-point cap in dimension n
satisfies, over (3^n-1)/2 hyperplane directions,

    sum E2 = 3^(n-1) binom(s,2),
    sum E3 = 3^(n-2) binom(s,3).

Pairs contribute to the first count when separated. Three cap points are
noncollinear and occupy all three slices in exactly 3^(n-2) directions.

For a fixed direction with layer sizes (A,B,C), refine by a functional on the
(n-1)-dimensional layer space. The three columns alpha,beta,gamma of its 3x3
matrix count the three values in each layer. Columns and every transverse triple
(alpha_r,beta_(r+s),gamma_(r+2s)) satisfy the lower-dimensional restrictions.
The three triples t_s=(alpha_r+beta_(r+s)+gamma_(r+2s))_r are other whole-cap
directions.

Let T=sum_(i+j+k=0) alpha_i beta_j gamma_k. The seven features are

    f=(T,E2(alpha),E3(alpha),E2(beta),E3(beta),E2(gamma),E3(gamma)).

Their exact summed vector is

    F_n=((3^(n-2)-1)/2 *ABC,
         3^(n-2)binom(A,2),3^(n-3)binom(A,3), ... B ..., ... C ...).

For T, one point from each layer has nonzero sum in the remaining coordinates,
otherwise the three original points violate the cap condition. Exactly
(3^(n-2)-1)/2 functional directions annihilate that nonzero sum.
There are D_n=(3^(n-1)-1)/2 refinements. Thus q.f>=K on every necessary matrix
and a valid summed upper bound U exclude the situation whenever D_n K-U>0.

All enumerations allow extra matrices not induced by caps, which is safe.
Sorting the first column is justified because every permutation of F_3 is
affine and preserves the statistics and transverse lines. The complete verifiers
do not use discovery's additional cyclic reduction of the second column.

## 2. New two-deletion lemma

**Two 112-point completions with at most two deleted points in total leave at
most44 third-layer positions avoiding cross-layer triples.** Hence the types
(112,110,45) and (111,111,45) are impossible.

The proof reuses the Fourier/incidence reduction in
`baseline277/baseline278/HILL_PROOF.md`. Normalize the two completion centers to0.
For projective intersection parameter h, the ordered cross-pair multiplicity is

    m(x)=16+4u+3p-h (x nonzero),    m(0)=2h.

Each deletion removes at most one representation of a fixed sum, so a newly
available point must have original multiplicity at most2. The eight state features
X and forced sums R(h) are precisely those in the inherited proof. For h=1..51
our integer certificate either excludes h, or verifies

    q.X >= L*1_(m<=2)   for every allowed state,
    q.R(h) < 23 L,      L>0.

Thus at most22 projective points qualify, giving at most44 nonzero vectors.
For h>=2 the origin has multiplicity at least4 and cannot open after two deletions.
For h=0 or1, all nonzero multiplicities are at least15, so only the origin can
possibly open. For h=52..55, overlap2h>=104 and the inherited 103-point extension
rigidity force identical completions, a contradiction. At h=56 they are identical:
only the multiplicity-one diagonal representations can be destroyed by two
deletions; at most two positions open. This covers every parameter.

Every inequality is in `results/near_deleted2.json` and is checked in both runs.
No numerical zero-count estimate is used as a proof.

## 3. New full-histogram bound for non-completable107-caps

The inherited universal and completion-forcing restrictions leave47 possible
hyperplane types for a non-completable107-point cap in F_3^6. Let phi be the
47-entry integer function listed in the coefficient tables. The new lemma is

    sum_[x] phi(t_x) <= -345314329.

Negative values cause no problem. Equivalently replace phi by phi+1000000;
the summed upper bound becomes 18685671.

First, at least one of the seven types

    (43,41,23), (43,42,22), (43,43,21), (44,41,22),
    (44,42,21), (44,43,20), (45,41,21)

must occur. On every other allowed type the verifiers check

    100 E3 -3953 E2 >= -10548667.

Its forced sum at size107 is -3839715009, whereas364 times the stated lower
bound is -3839714788, a contradiction gap of221.

Fix a direction x of one of those seven types. Its121 refinements, with their
three other directions each, partition all363 whole-cap directions other than x.
For any phi this gives the exact identity

    sum_[z] phi(t_z) = phi(t_x) + sum_[y] sum_s phi(t_s(M_y)).

For each of the seven possibilities, append to the seven universal features
fixed histogram indicators for five-dimensional columns of size43,44,45 and
spectral upper bounds for columns of size42. The inherited representative
computations justify these fixed histograms and the four possible42 histograms.
Each inner certificate verifies

    q.g(M) + spectral_terms - sum_s phi(t_s(M)) >= K.

If U is the justified sum of the first two terms, the full histogram is bounded
by phi(t_x)+U-121K. The maximum of the seven exactly checked bounds is
-345314329. There are39771 full canonical inner matrices in aggregate.
All inner coefficients, functions, sign conventions and bounds are in the JSON
and readable tables. No seven-dimensional conclusion is used in this lemma.

## 4. The global minimizing direction at size277

Assume a277-point cap exists. Its sorted whole-cap profiles satisfy
112>=a>=b>=c>=0 and a+b+c=277. Put

    P=9abc-907 E2+16113090.

The exact identity is

    4P=(3c-277)^2(c-67)+(907-9c)(a-b)^2.

The directional moment identities force

    sum P=9*243*binom(277,3)-907*729*binom(277,2)
          +16113090*1093 = -181158.

Choose a globally minimizing direction. Its P is negative. In each refinement,
P(t_s(M))>=P(chosen profile) is then a necessary additional condition.

Two frozen ordinary stages exclude61 and3 profiles, respectively. They use only
previously completed unconditional exclusions; their own stage is never available
as an assumption within that stage. The two new seeds from Section2 are added
after these stages. Eleven negative-P minimum-direction possibilities remain.
The certificate exhaustively verifies each unsplit case or all four statuses of
the two large slices, using the new107 histogram bound when needed.
Completion statuses concern entire slices across every direction. The inherited
labelled deletion statistics retain every compatible identity of the original
40-point section, with sums56,11d,110d (d=112-N). No incorrect substitution
40-max(column) is used when the original section need not remain largest.

Every extremal gap is strictly positive; the complete table follows below.
Crucially these are exclusions *as globally minimizing directions*. They are
not inserted into the unconditional exclusion set or used to eliminate another
extremal alternative.

## 5. The decisive new branch

For the minimum direction (107,107,63), with both107-point slices non-completable,
the new certificate verifies on every retained matrix

    76 T -3464(E2(alpha)+E2(beta)) +70(E3(alpha)+E3(beta))
      +261 E2(gamma)-33 E3(gamma)+phi(alpha)+phi(beta) >= -3670928.

The exact moments and two histogram upper bounds force its sum at most
-1336287074. The local lower bounds require at least364*(-3670928)=-1336217792.
The strictly positive difference is69282. Each histogram upper bound has
coefficient+1, so the inequality direction is preserved.

## 6. Conclusion

The negative summed polynomial forces a negative global minimum. Every one of
its eleven possible profiles, and every required whole-slice completion status,
has a positive-gap exact certificate. This contradiction excludes all277-point
caps. Taking subsets excludes every larger cap, proving f(7,3)<=276.
The unchanged explicit236-cap is checked independently, proving the lower bound.
This checkpoint makes no claim about f(7,3)<=275 or f(7,3)<=270.

## 7. Discovery and verification

The optional research scripts document the numerical discovery approach but are
not part of the proof's trust boundary. The complete verifiers regenerate the
necessary configurations and use exact arithmetic. Missing or failed discovery
outcomes are not treated as exclusions. Independent implementations help detect
programming mistakes but do not replace independent review of the reductions
or of the cited classification theorems.

### Exact minimum-direction gaps

| Type | Gaps (00,01,10,11, or unsplit) |
|---|---|
| 106,105,66 | 143622, 170348, 19839, 312566 |
| 106,106,65 | 11158, 987165, 987165, 158792 |
| 107,104,66 | 1217092 (unsplit) |
| 107,105,65 | 252526 (unsplit) |
| 107,106,64 | 11453, 109409, 38853, 245749 |
| 107,107,63 | 69282, 32713, 32713, 279591 |
| 108,104,65 | 17404 (unsplit) |
| 108,105,64 | 1670914, 892520, 1202850, 419728 |
| 108,106,63 | 88205, 2382761, 177505, 692961 |
| 108,107,62 | 150176, 1782224, 651328, 742011 |
| 108,108,61 | 3643254, 844830, 844830, 12126464 |
