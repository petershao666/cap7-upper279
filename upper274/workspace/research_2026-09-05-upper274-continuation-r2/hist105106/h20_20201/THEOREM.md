# Complete directional spectrum of the (20,20,1) branch

Subject to the published affine uniqueness theorem for twenty-caps in four dimensions, the finite enumeration and replay prove the following scoped statement.

Every forty-one-cap in F3^5 that has a hyperplane direction with section sizes (20,20,1) has exactly this complete 121-direction histogram:

| Sorted section sizes | Number of directions |
| --- | ---: |
| (14,14,13) | 40 |
| (15,15,11) | 20 |
| (17,12,12) | 20 |
| (17,16,8) | 40 |
| (20,20,1) | 1 |

All other direction types have count zero. An explicit forty-one-point representative is provided in REPRESENTATIVE_POINTS.tsv and histograms41.json. This is one histogram, not a claim of one affine isomorphism class. The 198 normalized cap pointsets are a complete cover up to the described normalizations, not the number of all labeled forty-one-caps.

## Coverage proof

The published input is Thackeray 2021, Theorem 4.9, PDF page 25 (printed 24), proof continuing PDF page 26. The locally read source /private/tmp/upper274_thackeray2021.pdf has SHA256 8b4e122e664f5138273dd0cae0793a9a3d968c51e6abdecd92c7e3dd0ecd6d9c. It states that every four-dimensional twenty-cap is affinely isomorphic to its displayed representative. No uniqueness of any larger cap is assumed.

Let A be the nonzero zeros of Q=x0^2+x1^2+x2^2+2*x3^2. Directly, Q has 9+12=21 zeros; A has twenty points. Its 190 point pairs are checked by exact coordinate arithmetic. The elementary determinant proof in ../joint_geometry_gate/QUADRATIC20_GATE.md also establishes that A is a cap. Consequently every twenty-cap is an affine image L(A)+c. It is therefore the translate by c of the nonzero zeros of the symmetric matrix L^{-T} diag(1,1,1,2) L^{-1}.

The enumerator visits every one of the 3^10 symmetric matrices. Off-diagonal matrix entries contribute twice in the quadratic polynomial, so every homogeneous quadratic form in characteristic three is represented. It retains precisely those with twenty nonzero zeros whose points pass a cap check, and deduplicates their exact masks. It then translates all retained centered sets by every vector of F3^4. This proves that the resulting catalogue contains every twenty-cap; conversely every entry is an affine translate of a checked cap. Thus the catalogue is exact and complete, without relying on an expected number of forms or caps.

Each centered zero set is closed under negation and has point sum zero. For a translated twenty-cap P+c, its point sum is 20c=-c. Its centre is therefore recovered as minus its point sum. This proves that different translations of different centered point masks are distinct, and independently checks the catalogue witnesses.

Now let S have a (20,20,1) direction. Choose that affine coordinate as t and put the two twenty-sections at t=0,1, the singleton at t=2. An invertible affine map z -> Lz+v puts the first section at A. If the original singleton is c, the map

(t,z) -> (t,Lz+v+t*(Lc+v))

sends it to (2,0), preserves the now-canonical first section, and sends the second section to an arbitrary twenty-cap B. This is invertible because its linear matrix is triangular with invertible diagonal blocks 1,L.

The union A at level zero, B at level one, and the origin at level two is a cap exactly when B does not intersect -A=A. Indeed a nonhorizontal affine line in characteristic three uses one point from each section and its three points sum to zero. All horizontal lines are already excluded by the cap properties of A and B. Filtering the complete twenty-cap catalogue by this exact disjointness test therefore produces a complete normalized cover of all S in the theorem.

Every retained lift is checked on all 820 point pairs. All 121 normalized nonzero normals in F3^5 are enumerated, their three level counts are calculated, and the resulting whole histogram is recorded. The computation finds a single vector, displayed above. Thus the equality holds for every cap in the scoped family.

## Exact artifacts and checks

enumerate.cpp is the complete C++ enumeration with exact integer coordinates and 81-bit masks; centered20.json supplies each centered set and its matrix-code witness. all20_catalogue.tsv supplies every translated mask, centre, and centered-set identifier; all20_masks.txt is the sorted complete mask list. eligible41_ledger.tsv records every compatible B and the resulting histogram identifier. histograms41.json records the full ordered type domain, the histogram, and an explicit five-dimensional point set.

The observed catalogue has 8424 centered masks and 682344 translated masks; exactly 198 B masks are compatible with the fixed canonical A. These values are outputs, not assumptions. verify_author.py separately reconstructs the matrix witnesses and every translated mask, checks the exact filter, and checks all 198 lifted caps and histograms using Python coordinate arithmetic. That author replay shares generated inputs and is not described as external independent verification. P separately enumerates all polynomial coefficients using a different canonical quadratic form; root separately audits the coverage and point representatives. Their acceptance is recorded separately in FINAL_STATUS.json when available.

For any real function phi on sorted forty-one section triples, this theorem gives the exact conditional sum

sum_d phi(type_d) = 40*phi(14,14,13) + 20*phi(15,15,11) + 20*phi(17,12,12) + 40*phi(17,16,8) + phi(20,20,1).

This may replace the first (20,20,1) whole-cap branch in a later, newly gated hierarchy. It is not an ordinary ban on any forty-one profile, does not cover the saddled-cube exceptional family, and does not by itself improve the seven-dimensional upper bound. No publication novelty claim is made for this finite input extraction.
