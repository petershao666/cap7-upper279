# H17 actual four-dimensional seventeen-cap histogram family

Written before code or enumeration. Root explicitly authorized this new actual-geometry object after H16's frozen null. Scope is hist105106/h17 only. H16's non-simultaneous local moment relaxation did not enumerate actual parallel sections; H17 does. No unchanged optimization is retried. No publication novelty or global bound is claimed from input extraction alone.

## Complete normalization and small orbit classification

Use exact F3 coordinates with point id x+3y+9z in three dimensions. A cap of size8 or9 spans dimension3 because C2<=4. It therefore contains an ordered affine basis. Normalize that basis to 0,e1,e2,e3. Enumerate EVERY cap extension of those four fixed points to size8 and9, checking all pair-generated third points. This requires at most C(23,4)=8855 and C(23,5)=33649 candidate extensions before cap pruning. No presumed orbit count or uniqueness is used.

For every normalized cap, enumerate every ordered affine basis it contains. Apply the exact invertible affine map taking that basis to the standard one; the minimum resulting bit mask is its canonical representative. This is a complete canonicalization: every affine equivalence sends affine bases to affine bases, so equivalent caps have exactly the same normalized images. Preserve every normalized cap, canonical representative and a witnessing basis/matrix/translation. Preserve explicit representative pointsets. Generate all invertible3x3 F3 matrices and all27 translations; generate every affine image of every discovered eight-cap representative to obtain the complete set of actual3D8 caps, retaining a representative-to-image witness for every distinct bit mask. No symmetry sampling or assumed number of orbits is permitted.

## Complete actual17 cover

Use the independently accepted primary Thackeray Lemma2.1(c) cover980/971/881.

* 980: place each complete3D9 representative A at level0 and EVERY actual3D8 cap B at level1, with level2 empty. There is no cross-level cap restriction when only two levels are occupied.
* 971: place each3D9 representative A at level0, singleton0 at level2, and enumerate EVERY cap7 subset B of complement(-A) at level1, at most C(18,7)=31824 candidates per A before cap pruning.
* 881: place each3D8 representative A at level0, singleton0 at level2, and enumerate EVERY cap8 subset B of complement(-A) at level1, at most C(19,8)=75582 candidates per A before cap pruning.

Completeness follows by first choosing a covered direction and normalizing A by an affine map on its three-flat. The shear (t,z)->(t,Lz+v+t*w) can then send the singleton at level2 to0 while preserving normalized A at level0. The cross-level cap condition is exactly B intersect(-A)=empty; internal cap conditions are checked separately. The equal eight-section case is covered for any chosen ordered assignment, without removing unproved symmetry cases.

For every generated17-point set, compute all40 projective-direction sorted triples exactly. Save the complete distinct histogram family, at least one explicit17-point table per histogram, counts/provenance per generating family, and the enumeration coverage ledger. Preserve sufficient generated-domain masks and witness mappings for independent replay. Histograms and representatives describe actual caps; their family is complete up to affine equivalence by the cover proof. They do not claim distinct affine17-cap classifications.

## Limits and terminal artifact

One worker, target memory<=2GiB, <=600seconds total enumeration; exact point bitsets and F3 arithmetic only. No external code execution beyond our own enumerator. Terminal full histograms and explicit point tables with coverage proof/hashes, or an explicit bounded incomplete result. Do not launch any coupled LP until root/P independently accept the small orbit domains, full coverage and actual17 histograms. P uses a different implementation for3D orbit/domain verification; root coordinates independent actual17 checking. Shared premises and source inputs must be recorded; agreement from shared code is not independent verification.
