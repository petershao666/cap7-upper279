# H20: complete (20,20,1) forty-one-cap histogram family

Root approved this new actual-geometry scope after the frozen theory gate in ../joint_geometry_gate/QUADRATIC20_GATE.md. Budget: <=600 seconds including author verification, one worker, <=2 GiB. No LP, no external Java, no edits to frozen earlier scopes. P independently enumerates polynomial coefficients with a different canonical cap, without reading H20 data before freezing; root independently audits coverage and representatives.

Object: ALL five-dimensional forty-one-caps admitting a (20,20,1) direction, including extendable caps. This is a conditional whole-branch family, not all forty-one-caps.

Premise: Thackeray 2021 Theorem 4.9, /private/tmp/upper274_thackeray2021.pdf, PDF page 25 (printed 24), proof continuing PDF page 26; affine uniqueness of a four-dimensional twenty-cap. The primary URL and elementary canonical-cap argument are recorded in the frozen theory gate. The source PDF hash is to be included in INPUT.json before enumeration.

Representation: canonical A is the twenty nonzero zeros of diag(1,1,1,2). Enumerate all 3^10 symmetric matrices over F3, including degenerate ones, select exactly twenty nonzero zeros, cap-check, and deduplicate actual point masks. Translate every retained centered mask by all 81 vectors. After normalizing A and shearing the third singleton to zero, an arbitrary twenty-cap B is compatible exactly when B is disjoint from -A=A. Retain all such B, cap-check their forty-one-point lifts, and compute all 121 directional histograms. Counts 8424 and 682344 are unverified proposed checks, never premises.

Coordinate convention: a four-dimensional point has ID x0+3*x1+9*x2+27*x3; the lifted five-dimensional point has ID t+3*x0+9*x1+27*x2+81*x3. Masks are unsigned 81-bit integers serialized as 21 lowercase hexadecimal digits. Symmetric-matrix coefficient order is (0,0),(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(2,2),(2,3),(3,3), and the polynomial has factor 2 on off-diagonal entries. Projective directions are normalized by first nonzero coordinate 1.

Terminal: complete centered and translated twenty-cap catalogues with witnesses and hashes, complete eligible-B ledger, every distinct forty-one histogram with an explicit point representative, exact pair and direction checks, coverage proof, and independent-audit-ready metadata. If any budget or correctness condition fails, a bounded stop replaces the completeness claim. No classification novelty, global upper-bound improvement, or ordinary profile ban is claimed from this enumeration.
