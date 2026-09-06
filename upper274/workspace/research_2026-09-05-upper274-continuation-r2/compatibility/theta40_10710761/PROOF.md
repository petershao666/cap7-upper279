# Exact conditional exclusion of NC/NC/* minimum (107,107,61)

The frozen integer candidate is `EXACT_DUAL.json`, SHA256 c574f90aa862a7b94ed395cba567b4f4a2088fe96a515e7b55bde8ece140b4ec. Its exact RHS pairing is9,410,019,729>0. Both own and root full raw-domain exact checks have passed, and root accepted the averaging proof; see ACCEPTED.md. This is a Q67-minimum conditional branch exclusion, not an ordinary forbidden profile and not a standalone upper274 proof.

## Necessary averaged model

Assume a275-point cap has a globally Q67-minimizing direction with slice sizes107,107,61, the two107-point slices being non-completable. Each107-point slice has364 hyperplane directions and11011 dual projective lines, each with4 directions, each direction on121 lines. For each slice j=0,1 use its normalized line distribution Z_j, and use W for the original275-cap's normalized364 refinement tables. All these distributions are nonnegative and sum1.

For each decreasing profile t of a107-point NC slice, and every dual-line table M, let k_t(M) count its orientations with profile t. For each orientation of profile t let f be (T,(groupE2_v,groupE3_v)_v), where T is the mixed sum over triples of row values adding to0, distinct v are ordered increasingly, and equal-sized columns are summed together. Define

    F(t)=(40*t1*t2*t3,(r_v*81*C(v,2),r_v*27*C(v,3))_v).

Exact incidence and moment counting gives

    sum k_t Z_j=4 sum [t_j(R)=t] W_R,
    sum (121 f_t-F(t)k_t) Z_j=0.

Here f_t sums the features over all FOUR orientations of M with type t, rather than choosing a single favorable orientation. The counting proof and exact81/27/40 constants are in the accepted `../theta40/PROOF.md` and `../theta40/MOMENT_DETAIL.md`.

Define Z=(Z_0+Z_1)/2. It is a nonnegative distribution of total1 on the same full NC107 inner domain. Averaging the two marginal and moment equations yields

    sum k_t Z=2 sum ([t_0(R)=t]+[t_1(R)=t]) W_R,
    sum (121 f_t-F(t)k_t)Z=0.

This direct averaging proves necessity without any orbit multiplicity assertion or any claim that the two actual caps are isomorphic. The outer features used are

    g(R)=(T,E2col0+E2col1,E3col0+E3col1,E2col2,E3col2).

Their exact equation is

    364 sum g(R)W_R =
    (121*107*107*61,2*243*C(107,2),2*81*C(107,3),
     243*C(61,2),81*C(61,3)).

The universal H3 theta40 theorem is the same accepted input as before: theta=phi+10^10 on the44 decreasing total40 profiles, and its sum across121 directions of every40-point five-dimensional cap is<=B=475918720. For t containing40 this implies

    sum (121 theta_t-r40(t)*B*k_t)Z<=0.

The inequality survives averaging. No prefix-conditional H3 empty case is used as a local ban.

## Exact finite coverage

Inner domain is the same complete NC107 domain in accepted `../theta40/PROOF.md`: all sorted anchor profiles of total107, entries<=45 avoiding OLD+COMP; table entries<=20; first column decreasing; unrestricted orders of second and third columns; all12 columns/affine transversals satisfy P5 plus the four ordinary41 bans; all three transverse whole107 profiles avoid OLD+COMP and have entries<=45. There are47 anchor profiles and1,407,366 raw tables. Every inner table contributes all four forms x,y,x+y,x+2y.

Outer domain changes only the anchor to10710761 and the Q67 threshold toQ67(107,107,61). It otherwise has exactly the accepted P6 and OLD/COMP predicates and ordinary BAN list. Entries<=45; first column decreasing; all remaining column orders retained. First and second columns are NC. Every transverse whole275 profile has entries<=112, avoids ordinary BAN, and has Q67>=Q67(107,107,61). The domain includes3,772,668 raw tables.

The representative coverage proof is unchanged: every permutation of three levels is affine over F3; a common row relabelling sorts the first column while preserving line incidence and all used features. No fixed orbit size is used. The outer search quotient records its five features and the unordered pair of the two107 column profiles. Those are exactly all row coefficients; merging only identical records preserves the projected cone. Nevertheless the exact verifier enumerates every raw table and computes all scores directly, without NPZ or quotient input.

## Frozen row definitions

There are375 rows. Rows0,1 normalize W,Z with RHS1. Rows2..6 have coefficient364*g_k on outer tables and the five forced RHS coordinates above. For `conditional,t,0`, the outer coefficient is-2 times the number of its two107 columns of profile t; the inner coefficient is k_t(M). For `conditional,t,k`, k>=1, the inner coefficient is121*f_(k-1)-F_(k-1)*k_t and outer coefficient0. All conditional RHS coordinates vanish. The twelve upper rows363..374 are `conditional_theta40,t`, with coefficient121*theta_t-r40*B*k_t on inner columns and RHS0.

Add a nonnegative slack variable in each upper row. If the frozen dual q has nonpositive score on every full raw outer and inner column and q_upper<=0, every column of this equality model has nonpositive q score. Thus any nonnegative feasible model gives q·b<=0. Direct integer computation instead gives q·b=9,410,019,729. This contradiction closes exactly the stated minimum branch.

The discovery summand bound18,294,328,738,205,946 is below2^62. Fresh verification uses signed128-bit integers and undefined-behavior sanitizer.

## Independence and scope of evidence

Discovery reused the accepted all-orientation NC107 feature file, predicate builders, and table generator, and solved a375-row full-priced compact dual. This reuse is declared and is not independent verification. The own exact checker is separately compiled and does not read discovery kernels, NumPy, generated records, or any floating-point object; it reuses the previous accepted own checker helpers with the new375-row definition and target. Root supplies a separately implemented mathematical and full-domain audit. Shared mathematical inputs are OLD, COMP, frozen ordinary41 and275 exclusions, and universal theta40; there is no circular use of this new branch or other minimum-only closures as ordinary bans.
