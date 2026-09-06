# Accepted exclusion of Q67-minimum NC/NC (107,105,63)

An assumed275-cap in F3^7 cannot have a globally Q67-minimizing direction with sizes `(107,105,63)` and both large slices non-completable. This is an extremal-state exclusion, not an ordinary forbidden profile. It does not alone establish the global upper bound274.

The complete integer certificate is `incidence107_certificate_107_105_63.json`, frozen SHA256 `aedb510abef5d4d1126f759d918f53e7fa4e9a8bc3e9947ffefc9ca8ad2dbc8a`. It contains386 exact row descriptions and coefficients. There are21 upper rows, whose coefficients are all nonpositive. The exact normalization coefficients are

`q_W=90644557772027`, `q_Z=−90605161297573`,

so their positive right-hand-side pairing is

`q_W+q_Z=39396474454`.

Here W is the normalized distribution of the364 seven-dimensional refinements of the chosen root direction. Z is the normalized distribution of the11011 dual projective lines of its actual NC107 slice. Each of the364 directions lies on121 lines, and each line has4 directions. For every one of47 NC107 profiles t the shared marginal is `sum k_t Z=4 sum 1_(alpha=t) W`. The four orientations of each inner line are retained simultaneously. Equal-sized slices are grouped in the conditional moment features.

The exact conditional moment and theta40 rows, complete P5/P6 matrix predicates, centering, inequality signs and source dependencies are specified in P5_SCOPE.md. In particular, conditional moment rows are `sum (121 f_t−F6(t)k_t)Z=0`; theta40 rows are `sum (121 theta_t−r40 Btheta k_t)Z<=0`; centered outer moments are `sum (364 f7−F7)W=0`. Every fixed upper histogram row is `sum (364h−B_h)W<=0`. The full ordinary ban list is in the frozen certificate and contains no minimum-only closures.

For every allowed inner matrix and every allowed outer matrix, the integer row functional pairs to at most zero. The maximum in each block is exactly zero. Adding one nonnegative slack with coefficient+1 to each upper row preserves this nonpositivity because the corresponding q is nonpositive. All table weights and slacks are nonnegative. Multiplying the exact equations by q would therefore imply `q_W+q_Z<=0`, contradicting the positive integer above.

Only two fixed outer upper functions have nonzero coefficients: coefficient−74 on the accepted `NC107_theta40_10710761_j0_floor10000` function, and coefficient−12 on the root-audited universal NC105 `H3_phi105`. The floor10000 function is the proved conservative inequality, not an arbitrary rounding. All other saved fixed outer upper coefficients are zero.

Independent route-side verification uses a fresh C++ implementation of the raw predicates, all four oriented moments, theta40 and shared marginals; it reads only accepted source lists/functions and the certificate. It does not use L's generated feature records. It checks6463458 all-ordered inner matrices and28471995 all-ordered outer matrices, with both maxima zero. The Python interface checker matches each saved function against the accepted JSON and checks the row signs and exact RHS. Records: `incidence107_interface_verification.json`, `incidence107_own_verification.json`.

Root independently accepted this result after checking6872231 raw matrices:1407366 inner and5464865 outer, with alpha sorted and every beta/gamma ordering. All21 upper signs, both maxima and RHS39396474454 passed, and all frozen source functions/hashes matched. Root's independent implementation is `../root_audit/verify_incidence_p5.cpp`. Its acceptance concerns this exact extremal state and makes no publication-priority claim.

The other P5 target `(107,106,62)` returned no positive certificate in the frozen cone. That numerical null proves no redundancy or feasibility statement and is not a completed family exclusion.
