# Independent acceptance of the seven-to-eight extension bridge

Every actual seven-point cap in AG(3,3) extends to an eight-point cap. More precisely, every one of the 126,360 actual seven-point caps has exactly four addable points. The complete accepted eight-cap affine representatives therefore give a complete affine seven-cap cover by their 24 single deletions, with duplicates allowed.

This is an exact finite input verification. It is not a classification into 24 affine orbits, an enumeration of sixteen-caps, or a new global bound.

## Frozen complete input and independent arithmetic

The complete seven-cap catalogue is `../small3d_actual_caps7.txt`, SHA256 `488211429dc1c2a6795859395914135e83990952ee2c109fcdd20956c8758db1`. It contains 126,360 sorted distinct masks. Its completeness was established by the previous exhaustive all-subset computation and independently accepted by the root's recursive augmentation audit. The complete eight-cap catalogue is `../h17_actual_caps8.txt`, SHA256 `01dcd9448bb1c4ad1232c97ec09e8d395c1167d630e0a31edbcdf68dfd4dfa4b`, containing 63,180 masks. Its independent all-subset and full affine-group checks were previously accepted. Neither catalogue is reenumerated here.

Point index i encodes `(i mod 3, floor(i/3) mod 3, floor(i/9))`; a mask's bit i records that point. For a cap S, a point q outside S is addable exactly when q is not `-a-b` for any distinct a,b in S. This follows because three distinct points are collinear over F3 exactly when their sum is zero. Any new forbidden triple after adjoining q must use q and two old points.

The new standalone `check_seven_extension.cpp` forms this forbidden union separately for every frozen seven-cap, using its own coordinate arithmetic. It checks nonempty complement and checks every resulting eight-mask against the complete accepted eight-cap set. It reads neither the root's witness file nor the root's extension implementation. Its shared dependencies are precisely the accepted complete mask catalogues and their cardinalities. The source performs no affine-orbit canonicalization and imports no root or L mathematical kernel.

The resulting exact degree distribution is `{4:126360}`. The total extension incidence count is 505,440, equal to `8*63180`, as also required by deleting each point from every actual eight-cap. The output `SEVEN_EXTENSION_WITNESSES_P.txt` has one line per seven-cap: `seven_mask added_point_index eight_mask`. It chooses the least addable point. `SEVEN_EXTENSION_RESULT.json` records the complete count and degree distribution. All arithmetic is integral.

## Why the 24 formal deletion entries cover every affine seven-cap

The previously accepted complete affine eight-cap representative masks are 13851, 13853, and 13902, with explicit coordinates in `../h17_representatives_explicit.json`. Given any seven-cap S, the verified extension property supplies an eight-cap T containing S. Completeness of the accepted eight-cap orbit cover gives an invertible affine map f taking T to one representative R. Since `|T minus S|=1`, its image satisfies `f(S)=R minus {p}` for one p in R. Thus S occurs up to affine equivalence among the eight single deletions of each of the three representatives.

`SEVEN_DELETION_COVER.json` exports all 24 formal entries, retaining any duplication. Every entry includes its source eight-mask, removed point, seven-mask, point indices and explicit coordinate array. `make_seven_cover.py` verifies the frozen source hashes and each entry's actual-cap membership and triple condition. No assertion is made that these 24 entries are pairwise inequivalent or a minimal cover.

## Consequence for complete small-only sixteen-cap enumeration

The previously audited moment argument in `PROOF.md` proves that every sixteen-cap in AG(4,3) whose three-dimensional sections all have size at most seven has histogram

`h772=a, h763=40-3a, h754=2a, h664=h655=0`,

with integer `0 <= a <= 13`. Consequently it has a 772 direction when a is positive. When a is zero, all its 40 directions have type 763. Hence the two anchor families 772 and 763 cover this entire branch. The first section A has seven points and can now be normalized to one of the 24 formal deletion entries.

After selecting a direction, any required ordering of its three levels is affine because AGL(1,3) is the full permutation group on those levels. Write the ordered sections as `(A at level 0, B at level 1, C at level 2)`. Normalize A by `x -> Lx+v`, with L invertible, and choose any z* in C. The ambient map

`(t,x) -> (t, Lx+v+t*(Lz*+v))`

is invertible, takes A to its chosen normalized seven-cap, and takes z* in level 2 to zero. This does not require C to be a singleton. The transformed three coordinates are `La+v`, `Lb+Lz*+2v`, and `Lc+2Lz*`; their sum is `L(a+b+c)`. Thus the signs preserve cross-layer collinearity exactly.

After normalization, B ranges over every actual seven-cap for 772, or every actual six-cap for 763, subject to `B intersect (-A)=empty`. For each B, let `F=AG(3,3) minus (-(A+B))`. The third section ranges over every actual two-cap for 772, or actual three-cap for 763, contained in F and containing zero. The complement condition on B is forced by the chosen zero of C and ensures zero lies in F. Within-layer cap tests together with `C subset F` are necessary and sufficient for the full union to be a cap: a nonconstant triple of layer labels summing to zero must use all three distinct levels.

Finally, retain only unions whose sections in every one of the 40 directions have size at most seven. The 772 family covers a>0. For a disjoint 763 family, additionally impose h772=0; omitting this additional filter retains possible duplicates but does not harm completeness or actual-cap validity. No condition on only the chosen anchor can substitute for the required all-direction maximum test.

This proves the exact coverage needed for a later complete actual small-only enumeration. It does not certify that such an enumeration has been executed. In particular, the fourteen formal moment vectors in the earlier necessary overcover may be replaced by actual histogram outputs only after that later computation and its independent verification are complete.

## Scope and terminal status

The declared extension audit used the frozen complete catalogues, one independent finite pass, and exact representative export within the 120-second gate. No seven/eight catalogue search, sixteen-cap enumeration, LP, or source-file mutation was performed. Status: `INDEPENDENT_EXTENSION_BRIDGE_ACCEPTED`. Publication priority and a new global bound are not claimed.
