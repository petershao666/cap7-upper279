# Complete histogram theorem for the 20/20/1 family

Every 41-cap in AG(5,3) having a hyperplane direction of type (20,20,1) has exactly the following histogram over its 121 hyperplane directions:

| Section profile | Number of directions |
|---|---:|
| (14,14,13) | 40 |
| (15,15,11) | 20 |
| (17,12,12) | 20 |
| (17,16,8) | 40 |
| (20,20,1) | 1 |

Every other profile has count zero. This is a theorem for the stated family only. It makes no assertion about 41-caps without a (20,20,1) direction, affine equivalence of caps sharing a histogram, or publication priority.

## Published input and canonical point certificate

The only classification input is affine uniqueness of the four-dimensional 20-cap, from Theorem 4.9 of Thackeray, *The cap set problem and standard diagrams*, Discrete Mathematics 344 (2021), 112558. The [primary accepted manuscript](https://repository.up.ac.za/bitstream/handle/2263/85152/Thackeray_Cap_2021.pdf?sequence=1) states the theorem on printed page 24, with proof continuing on page 25. Its definition of isomorphism is affine equivalence. This source was checked directly before enumeration. No list of quadratic-form classes is imported.

Take Q(x)=x0^2+x1^2+x2*x3 over F3, and let A be its nonzero zero set. The values of x0^2+x1^2 have multiplicities 1,4,4 at 0,1,2. The product x2*x3 has multiplicities 5,2,2. Thus Q has `1*5+4*2+4*2=21` zeros, including the origin, so |A|=20. `HISTOGRAMS.json` gives all twenty explicit coordinates. The checker evaluates all 190 unordered pairs and verifies that their distinct-line third point is outside A. Hence A is an actual 20-cap, and affine uniqueness applies to this separately verified representative. Also Q(-x)=Q(x), so -A=A, verified directly by masks.

## Completeness of the polynomial and translation enumeration

All homogeneous quadratic polynomials in four coordinates are enumerated through the ten monomials

`x0^2,x1^2,x2^2,x3^2,x0*x1,x0*x2,x0*x3,x1*x2,x1*x3,x2*x3`.

Each coefficient independently ranges over F3; base-three coefficient codes 0 through 59048 enumerate all 59,049 vectors exactly once. For each vector the implementation evaluates all 80 nonzero coordinate points, retains the zero set only when its size is twenty and its 190-pair cap check passes, and deduplicates by exact 81-bit masks. It does not filter by rank, determinant, nonsingularity, a conjectured form class, or an expected orbit size. All retained sets are actual 20-caps by the point test.

For completeness, any actual 20-cap T is an affine image `L(A)+v`, with L invertible, by the published uniqueness theorem. The set L(A) is exactly the nonzero zero set of `Q composed with L^{-1}`, which is a homogeneous quadratic polynomial among the enumerated ten-coefficient vectors. It passes the size and cap tests. Translating each retained mask by every vector v in F3^4 therefore includes T. Conversely all translations of the retained caps are caps. Exact mask deduplication cannot lose an actual set. Thus the translated inventory is the complete actual 20-cap family, not a symmetry sample or a conditional collection of form types.

The exact output is 16,848 retained coefficient vectors, 8,424 distinct centered zero sets and 682,344 distinct translated 20-caps. These numbers were derived by the loops, not imposed as assertions. `CENTERED20_MASKS_COEFFICIENTS.txt` records each centered mask and a coefficient code. `ALL20_MASKS.txt` records every actual 20-cap mask in increasing order, as fixed-width 21-digit hexadecimal text. Bit i corresponds to `i=x0+3*x1+9*x2+27*x3`.

## Complete normalization of a 20/20/1 cap

Given a 41-cap with a (20,20,1) direction, choose affine coordinates `(t,x)` with the two 20-sections in levels 0 and 1 and the singleton in level 2. This ordering is always possible since every permutation of F3 is affine. Call the sections A0,B0,{z}. Choose an invertible affine map `x -> Lx+v` sending A0 to the fixed A. Put `w=Lz+v` and apply

`(t,x) -> (t, Lx+v+t*w)`.

Its block triangular linear part has invertible diagonal blocks 1 and L. It acts on level zero by the chosen normalizing map and sends z in level two to `Lz+v+2w=0`. Thus both normalizations hold simultaneously. It sends coordinates from the three original levels to `La+v`, `Lb+Lz+2v`, and `Lc+2Lz`; their sum is `L(a+b+c)`. This also verifies the signs of the shear directly.

The transformed second section B is an actual 20-cap, hence occurs in the complete translated catalogue. A triple of layer labels over F3 whose sum is zero is either constant or consists of all three labels. Therefore, once A and B are caps internally, the union `A@0 union B@1 union {0}@2` is a cap if and only if there are no a in A and b in B with a+b=0, equivalently `B intersect (-A)=empty`. This is an exact condition, not just a necessary relaxation.

Testing this condition on every translated mask leaves exactly 198 possibilities for B. Thus the 198 normalized lifts form a complete affine cover of the stated 41-cap family. No claim is made that they are distinct affine orbits. `B20_DISJOINT_MASKS.txt` preserves the entire normalized B list.

## Exact direction histograms and point verification

The five-dimensional index of a lifted point is `t+3*x0+9*x1+27*x2+81*x3`. For each of the 198 lifts, the C++ implementation checks all 820 unordered pair completions directly in five coordinates. It then runs over every projective nonzero normal, choosing first nonzero coordinate one; these are exactly (3^5-1)/2=121 directions. Counting points at the three values of the normal and sorting those counts gives the direction profile. All 198 lifts produce the single histogram displayed above. The explicit representative in `HISTOGRAMS.json` contains 41 distinct coordinate arrays and their matching indices.

The exact moment checks are `sum h=121`, `sum E2*h=81*C(41,2)=66420`, and `sum E3*h=27*C(41,3)=287820`. These are consistency checks in addition to, not substitutes for, the complete actual-point enumeration and direction counts.

The separate Ruby artifact checker `check_frozen_points.rb` reads the frozen output and verifies its hashes, recomputes the canonical zeros and all canonical pairs, independently refilters the complete translated inventory, checks every lifted pair with direct coordinate arithmetic, and recomputes histograms using all 242 nonzero normals before exact division by two. It also verifies the explicit coordinate and index encodings and every exact moment. This is an independent arithmetic replay of shared generated point data, not a second independent enumeration of all polynomials; that limitation is recorded in `POINT_REPLAY.json`.

## Independence, freeze and terminal limitation

This polynomial implementation uses a different canonical quadratic form and a ten-monomial coefficient loop, not H's symmetric-matrix generation kernel. No H generated input or output was read before the complete counts, masks and histogram were hashed in `FROZEN.json`. Shared dependencies with H are the published uniqueness theorem and finite-field mathematics. Parent/root comparison of the two complete families is separate from this producer's own arithmetic replay.

The complete finite pass used one worker and far less than the declared 600-second/2-GiB gate. No LP or seven-dimensional certificate was run. The result is an exact scoped histogram input; the global upper-bound problem is unchanged by this artifact alone.

After both outputs were frozen, `compare_H_frozen.py` checked equality of all 8,424 centered masks, byte identity of all 682,344 translated masks, and equality of the complete histogram sets. It separately checked H's explicit representative, all 820 pairs and all directions. The comparison passed and is recorded in `H_COMPARISON.json`. H transparently reports that its source was completed and compiled before receiving P's result, but execution followed that message after resource-wrapper failures; H reports no subsequent kernel modification or P generated-file import. P's own enumeration and freeze preceded any H output read. Thus implementation and generated-input independence are explicit, while H's final run was not blind to P's reported counts.
