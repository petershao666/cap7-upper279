# Conditional exclusion certificate: minimum profile (108,107,60), NC/NC/*

Candidate frozen at SHA256 `d6b08cb03ee145fd7db5a539bcf8269bfd0edd200772910d43d15cabe41c31d3` for `EXACT_DUAL.json`. No mutation is permitted. Its 606 row descriptions are the complete row interface. The exact positive right-hand-side pairing is **21,167,272**. Root independently accepted full-domain verification and the mathematical incidence proof. A second fresh full-domain own verifier also passed; see ACCEPTED.md.

The precise claimed consequence is: a 275-point cap cannot have a globally Q67-minimizing hyperplane direction of profile (108,107,60) whose 108- and 107-point slices are both non-completable. Here Q67(a,b,c)=9abc-899(ab+ac+bc)+15730000. This is NOT an ordinary profile exclusion and cannot be inserted into an ordinary forbidden-profile list. It alone does not prove the seven-dimensional upper bound274.

## Exact input predicates and complete finite domains

Let OLD be every sorted triple named in `six_stages` of `audit_2026-09-05_upper275/cap7_upper275/baseline277/baseline278/certificate.json`. Let COMP be that certificate's `completion_seeds` together with every triple named in `completion_stages`. A triple avoids a list if its decreasing rearrangement does not coordinatewise dominate any member. Let completed(t) mean that its decreasing rearrangement (a,b,c) satisfies c<=22 or (a<=40 and b<=36).

Inner domain for N=108 or107: all nine-entry nonnegative integer tables, entries<=20, with sorted anchor column sums (A,B,C), A<=45, A+B+C=N, avoiding OLD+COMP. The first column entries are sorted decreasing. Every column and all nine affine transverse triples (a_r,b_(r+s),c_(r+2s)), r,s in F3, obey predicate P5 below. Each of the three transverse whole-N profiles (the three transverse sums for each s) has entries<=45 and avoids OLD+COMP. All orderings of the second and third columns are included.

P5: for decreasing (a,b,c), let n=a+b+c. Require n<=45 and either n<42, or (a<=18,b<=18,c<=9), or a<=15. At n=42 also permit exactly (20,16,6), (18,18,6), (18,17,7), (18,12,12), (16,15,11), (16,14,12), (15,15,12), (14,14,14). Finally exclude domination of any of (20,19,2), (20,18,3), (19,19,3), (19,18,4). These are frozen ordinary41 exclusions. **No H3 prefix-conditional empty branch is excluded.**

Outer domain: anchor sums (108,107,60), entries<=45, decreasing first column. Every column and all nine affine transverse triples obey P6: total<=112; if total>=109 require completed(t); and avoid OLD plus those COMP triples failing completed(t). The first two columns also avoid ALL COMP. All three transverse whole275 profiles have entries<=112, avoid ordinary BAN below, and satisfy Q67(profile)>=Q67(108,107,60). No further restrictions occur.

BAN is the four seeds (112,112,29), (112,111,35), (112,110,45), (111,111,45); the recovered ordinary seeds (112,109,51), (111,110,51); and all twelve ordinary stage triples from `research_2026-09-05-capset-round1-r1/root_audit/audited_certificate_snapshot.json`. In particular the newly closed minimum-only (105,105,65) branch is not used as an ordinary ban.

Every actual table has a domain representative. Permutations of the three anchor levels are affine maps over F3, so anchor sums can be decreasingly ordered. A common affine permutation of the three row levels sorts the first column. These transformations preserve every affine-line predicate and every feature used below. All six row permutations are allowed, including when entries tie. There is no paired-shear quotient in the raw domain and no assumption that orbit sizes are constant. The second and third column orderings remain unrestricted. For each actual dual line, choose one representative and place its weight there.

The discovery full raw counts are 565,824 inner108 (30 anchor profiles), 1,407,366 inner107 (47 profiles), and 3,050,715 outer. These counts are audit targets, not substitutes for domain coverage. Discovery merged only identical complete model feature columns, yielding31,505,80,583,817,764 respectively. Every inner column contains all four orientations simultaneously. Independent verification should enumerate the mathematical domains directly and need not trust these quotient counts or records.

## Incidence equations

For an N-point cap in F3^6, hyperplane directions are the364 points of dual PG(5,3). Each direction lies on121 projective lines; each line has4 directions; there are11011 lines. A dual line gives a3x3 cell-count table. Its four orientations are the forms x,y,x+y,x+2y. For each orientation let t be decreasing column sums; let T=sum_(i+j+k=0) a_i b_j c_k. For each DISTINCT size v in t in increasing order let E2_v and E3_v be the sums of elementary moments over ALL columns of that size. Equal-sized columns are grouped together, avoiding direction-dependent tie breaking.

The local feature vector is f=(T,(E2_v,E3_v)_v). Its forced sum across the121 lines incident to a fixed direction is

    F6(t)=(40*t1*t2*t3,(r_v*81*C(v,2),r_v*27*C(v,3))_v),

where r_v is the multiplicity of size v in t. The mixed factor40 counts projective forms in five variables annihilating a nonzero vector: a zero vector would give a collinear triple crossing the three slices. The factors81 and27 come from annihilating a nonzero point difference and a two-dimensional span of differences of three distinct cap points. Thus these are exact identities.

Let h_t count directions of profile t, z_M count dual lines, k_t(M) count its orientations of type t, and f_t(M) sum their f. Then sum k_t z=121h_t, sum f_t z=F6(t)h_t, sum z=11011, sum h=364.

For the275-point cap's chosen direction, its364 refinements have weights w_R. Each fixed original slice's direction histogram is exactly h_(j,t)=sum_R [t_j(R)=t]w_R, j=0,1. Normalize W=w/364 and Z_j=z_j/11011. Both W and each Z sum1. The coupling gives sum k_t Z_j=4sum[t_j=t]W. Subtracting F6(t) times this marginal equation from the moment equation yields

    sum_M (121 f_t(M)-F6(t) k_t(M)) Z_j(M)=0.

Outer feature order is (T,E2(col0),E3(col0),E2(col1),E3(col1),E2(col2),E3(col2)). Its exact equation is 364 sum_R f7(R) W_R=F7, with

    F7=(121*108*107*60,
        243*C(108,2),81*C(108,3),
        243*C(107,2),81*C(107,3),
        243*C(60,2),81*C(60,3)).

## Universal theta40 input and inequality direction

Use ONLY the root-audited H3 universal function at `hist105106/h3/h3_result.json`, SHA256 `cbb4973544cf7e2388097bb333504dc0c53c943d1671605fa300996394dfd294`. Its44 values phi on40-point five-dimensional cap profiles satisfy sum_(121 directions) phi<=-1209524081280. Put theta=phi+10^10. Then sum theta<=B=475918720.

For any six-dimensional direction t with r40(t) occurrences of40, let theta_t(M) sum theta over its size40 columns across orientations of profile t. Incidence counting gives

    sum_M (121 theta_t(M)-r40(t)*B*k_t(M)) Z_j(M)<=0.

No prefix-conditional H3 empty case is an ordinary forbidden profile. The first invalid exploratory run using that interpretation was stopped and isolated under `invalid_prefix_scope/`; none of its pruned records enter this candidate. The corrected counts match the original unpruned finite domains.

## Certificate row convention and contradiction

Rows0,1,2 are normalizations of W,Z0,Z1 with RHS1. Rows3..9 are outer moment equations with coefficients364*f7 and RHSF7. Each `conditional,j,t,0` row is marginal: outer coefficient -4 if t_j=t and inner coefficient k_t. Each `conditional,j,t,k` for k>=1 has inner coefficient121*f_(k-1)-F6_(k-1)*k_t and RHS0. The twenty final `conditional_theta40,j,t` rows586..605 are the displayed upper inequalities with RHS0. Add one nonnegative slack with coefficient+1 in each such row.

For the frozen integer dual q, verification must prove q·column<=0 on every permitted raw outer/inner table and on every slack column (equivalently q_theta<=0). All variables are nonnegative. Nevertheless q·b=21,167,272>0. Multiplying all exact equations by q therefore gives a contradiction. This proof depends only on the domain coverage and exact integer checks, not any numerical LP status.

Discovery used int64 arithmetic with a verified absolute summand bound3,348,612,205,343, below2^62. An independent checker may use arbitrary integers or signed128-bit arithmetic to remove overflow concerns.

## Shared dependencies and independence limits

Discovery imports the frozen engine's P5/P6 predicate builders and uses one table generator throughout its optimization attempts. Theta feature records and sparse model assembly share discovery code, so checking that sparse matrix again is not independent mathematical coverage. Inputs OLD, COMP, ordinary41 exclusions, twelve prior ordinary275 exclusions, and universal theta40 are shared mathematical prerequisites. The new contribution is the all-orientation shared-marginal Farkas certificate for this conditional branch. A separate full-domain implementation and a separate proof-of-incidence audit are required for acceptance.
