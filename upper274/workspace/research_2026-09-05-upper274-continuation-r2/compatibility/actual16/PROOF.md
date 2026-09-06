# Complete necessary4D16 histogram overcover

The frozen packet OVER_COVER.json contains376 distinct histograms realized by explicit16-caps with an8/9-point hyperplane section, and14 additional necessary small-only histograms. Its390 vectors form a complete necessary histogram overcover for all16-caps in F3^4. The additional14 vectors are not asserted realizable. This packet is therefore not a complete actual16 classification and is not a seven-dimensional cap bound.

## Coverage and normalization

Every direction of a16cap has decreasing profile with entries<=9. If any entry is8 or9, there is a direction in the nine families970,961,952,943,880,871,862,853,844. Relabel its levels as0,1,2 so their actual3D sections A,B,C have those ordered sizes. Every permutation of F3 is affine. Choose an affine automorphism z→Lz+v sending A to one of the accepted canonical orbit representatives:9 mask276138, or8 masks13851,13853,13902. The orbit input and actual7/8 catalogue hashes are recorded in INPUTS.json. Completeness of those3D inputs is independently accepted; it is not inferred merely from equal orbit counts.

For c0, the third section is empty. A mixed collinear triple would need all three distinct levels, because any nonconstant three-term zero sum in F3 uses0,1,2. Thus every actual B cap of the stated size is allowed, with no complement restriction. The search reads all126360 actual7caps for970 and all63180 actual8caps for each of the three880 representatives; every supplied mask is also checked for the3D cap condition by this implementation.

For c>0 choose a point z* of the third section. Extend the normalization by

    (t,z)→(t,Lz+v+t*w), with w=Lz*+v.

At level0 it preserves the chosen A representative. At level2 the chosen point maps to w+2w=0. For a cross-layer triple the transformed coordinate sum is L(a+b+c)+3v+(0+1+2)w=L(a+b+c), so the cap condition is preserved exactly. Because0 belongs to the normalized C, B must avoid−A. After choosing B, every C point must avoid−(A+B). Conversely these conditions together with A,B,C individually being caps suffice for the lifted set to be a cap: same-level triples are handled internally, and the only mixed triples use all three levels.

The search therefore enumerates every b-cap in complement(−A), then every c-cap in F3^3 minus−(A+B) containing0. It is a complete necessary normalized cover; choosing one normalization or one point z* does not assume a fixed orbit size. No first-prefix condition, stabilizer pruning or claimed affine-canonical4D representative is used. Families may overlap.

## Independent recursive kernel

For c>0, our B search is an ascending recursive cap augmentation over the allowed positions. After adding p it removes the completion point−p−q for every previously chosen q; every cap subset has exactly one increasing path and no legal path is pruned. The forbidden cross-layer set−(A+B) is accumulated incrementally from the chosen B points. The C search is a separate ascending recursion seeded by0, with the same exact internal-cap invariant and its complete free set. It imposes no extra geometric condition.

For c0 the full B catalogue is used directly. Every lifted set is distinct for its fixed anchor/A/B/C data; different such data may give affine-equivalent or identical histograms. All553678 emitted lifted sets are histogrammed. This number is a normalized anchored enumeration count, not a count of affine-isomorphism classes. The19 anchor/A cases, B counts, successful B counts, free-set-size frequencies and lift counts are recorded in LARGE_RAW.json and copied into the packet.

All40 projective directions are counted: the anchor functional, plus each of13 normalized nonzero3D functionals u and all three coefficients alpha in alpha*t+u·z. The occupancy is obtained directly from the three actual point masks. Duplicate histograms alone are merged; their multiplicities are retained, with one explicit representative.

The enumeration completed in0.312378 seconds under the600second gate, with UBSan enabled. The conservative pre-enumeration lift bound was17,338,272. No root actual16 result or output was read before this output was frozen. Root uses alternative equivalent A representatives and a full-B-catalogue filtering kernel; this implementation uses the accepted P canonical representatives and independent B/C recursion. Shared low-dimensional classification and cap-count inputs are disclosed rather than called independent implementations.

## Small-only branch

If no direction has an8/9 section, the only profiles are772,763,754,664,655. Over the40 directions, the exact totals are E2=3240 and E3=5040. On these five profiles,7E2−E3 takes values441,441,441,444,445, while the global total is441*40. Hence664 and655 have count0. The remaining moment equations give

    (h772,h763,h754,h664,h655)=(a,40−3a,2a,0,0), a=0,...,13.

All14 vectors are included as necessary-only entries. For a linear universal function bound, just their endpoints a0 and a13 suffice because all14 lie on the segment joining the endpoints. No actual representative is invented for this branch. Its proof is also independently audited by P and was established in the preceding Theta16 gate.

## Own point and histogram check

package_and_check.py independently decodes each saved actual representative as16 explicit F3^4 coordinates, checks all120 unordered pairs against third-point completion, and recomputes every histogram using direct dot products over all40 projective functionals. It checks376 representatives,45120 pairs, all histogram coordinates and total multiplicities. This verifier does not reuse the C++ histogram computation. Complete discovery/raw enumeration still requires root's independently frozen comparison before final acceptance; representative verification alone does not prove coverage.

No LP was run. The weaker local Theta16 support-dual model remains unrun and may be replaced by this stronger packet after independent acceptance. Any later small-only completion bridge requires a new amendment; this frozen packet retains the precise necessary-only status of its14 small vectors.
