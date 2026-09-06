# Complete histogram family of four-point deletions from a 45-cap

The complete family has exactly 27 distinct directional histogram vectors. Each vector is a histogram over all 121 hyperplane directions of a 41-point cap in AG(5,3). Every vector is realized by the explicit retained point table in `HISTOGRAMS.json`, and its recorded frequency counts the unordered four-point deletions of the fixed accepted 45-cap that produce it. These frequencies sum to 148,995. Histogram count is not a count of affine isomorphism classes.

This is a scoped theorem: it covers every 41-cap obtainable by deleting four points from a 45-cap, and no other class of 41-caps is asserted covered. It supplies no new global upper bound or literature-priority claim.

## Complete reduction to the finite domain

The accepted input is `../../root_audit/fortyfive/ACCEPTED_POINTS.json`, SHA256 `f6d8bad31f3250d88f65e326e68e2e5404a11a1d2d93ca90a0fad352aab26980`. Its 45 points were independently reconstructed and verified by root and P using the published T/R maps. The input's affine uniqueness is the published Theorem 4.3 of Thackeray, [The cap set problem: 41-cap 5-flats, arXiv:2206.09719v1](https://arxiv.org/html/2206.09719v1#S4.Thmtheorem3).

If C is a 41-cap obtained by removing four points from an arbitrary 45-cap K, affine uniqueness gives an invertible affine map f taking K to the accepted representative A. The image f(C) is A with the four distinct image points removed. Conversely every four-point deletion from A is a cap by heredity. An invertible affine map bijects hyperplane directions and preserves each sorted three-section profile, so it preserves the whole direction histogram. Therefore enumerating all unordered four-subsets of A is both sufficient and complete for the declared histogram family.

P first orders the accepted coordinate tuples lexicographically; it does not preserve or assume root's enumeration order. The finite domain consists of all indices `0<=a<b<c<d<45`, counted by

`C(45,4)=45*44*43*42/24=148995`.

The four nested loops explicitly visit each increasing tuple exactly once. `SUBSET_HISTOGRAM_IDS.txt` preserves every tuple and its assigned final histogram id. The separate checker verifies that this entire file agrees line-for-line with an independently generated combinations iterator, with no skipped, duplicated or out-of-order subset, and checks every resulting histogram frequency.

## Direct retained-point directional computation

`enumerate_retained.cpp` reads only the lexicographically sorted point data exported by `prepare_input.py`. It independently checks that the input has 45 distinct field points and verifies all 990 pair completions. For each deletion tuple it explicitly assembles the 41 retained point indices.

For every one of the 242 nonzero normals d in F3^5, it starts three zero counters and increments the counter at d.p for each of the 41 retained points p. Precomputed individual point residues are used only as lookup values. It does not subtract the deleted points' occupancy from a whole-45 histogram and does not import root's subtraction kernel.

Sorting the three counters gives the directional profile. The only two nonzero scalars in F3 are 1 and -1; d and -d define the same hyperplane direction and simply permute its level counts. Thus each projective direction is counted exactly twice. Every profile count is checked even before exact division by two. The resulting histogram has 121 directions.

The finite run computed 36,056,790 nonzero-normal profiles directly, totaling 1,478,328,390 retained-point residue increments. For every normalized histogram it checked the exact moment identities

`sum h=121`,

`sum E2*h=81*C(41,2)=66420`,

`sum E3*h=27*C(41,3)=287820`.

The moments are consistency checks, not substitutes for the full point-level count. Deduplication uses the entire vector of counts indexed by every sorted triple summing to 41 with maximum at most 20. The upper support bound is valid because every section is a four-dimensional cap; every actually observed profile is required to occur in that full type list. No presumed 41-cap exclusions or expected histogram count is used to filter the finite domain.

## Exact output and witnesses

`HISTOGRAMS.json`, SHA256 `c7a6c7b338e8df3185b3e5a72949c40be310c7b65d8eace0d902e4d07e83c02e`, contains all 27 complete vectors, their frequencies, the four deleted input indices, all retained input indices, encoded points and explicit five-coordinate arrays. In vector order the frequencies are

`990,13680,9000,3960,19440,15120,1440,180,10800,1980,8640,720,1080,45,1980,6840,22680,9720,360,9000,2520,2880,2160,360,2880,360,180`.

`RESULT.json` records the complete loop totals. The finite enumeration completed in one batch within the declared 120-second and 512-MiB limits; no algorithm change or retry was needed. The C++ source SHA256 is `ab161c6ef272208a9828b7b41bb452681340c2e45f5162a5535ef32d50673dbb`.

## Independent verification and full root comparison

P's generated input, source, binary, full output and assignments were hashed in `FROZEN.json` before reading any root four-deletion result. Only afterward did `verify_and_compare.py` open root's frozen `FOUR_DELETE_HISTOGRAMS.json`. It compares all full histogram vectors after aligning their profile labels and compares every corresponding frequency. All 27 vectors and all frequencies agree exactly, with total 148,995 in both implementations.

The checker directly revalidates each P and root representative as exactly the complement of its declared four source indices. It recomputes all point pairs and all 121 directions, using normals normalized by their last nonzero coordinate rather than the enumerator's all-242-normal approach. For each of the two representative sets, 22,140 pairs and 3,267 projective directions pass. The P assignment file also passes the complete independent subset-order and frequency audit.

`INDEPENDENT_COMPARISON.json` preserves these results and both output/source hashes. Root's generator source was neither read nor imported. The implementations share the accepted 45-point coordinates and the published affine uniqueness theorem, as declared. They use different complete directional arithmetic: root subtracts deleted occupancies; P explicitly counts retained points. The point tables are a deliberately shared accepted input, so this is not claimed to be independence from every source dependency.

The result is an independently matching complete actual histogram input for one published classification alternative. Whether this support sharpens an older linear relaxation is a separate mathematical dominance question; no stronger linear cone or seven-dimensional exclusion is inferred merely from computing the finite family.
