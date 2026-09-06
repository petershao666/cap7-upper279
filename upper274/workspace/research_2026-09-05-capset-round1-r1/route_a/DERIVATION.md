# Exact reduction of the 275-point target

This is a scoped research result, not a proof of the upper bound 274. All statements retain the published and audited lower-dimensional inputs of the upper-275 checkpoint. Existence of a 237-cap remains UNKNOWN. Novelty beyond the available checkpoint is not claimed: the unavailable continuation archive may overlap this reduction.

## Root identities and complete type coverage

An s-point cap in F3^n has directional moments sum E2=3^(n-1) C(s,2), sum E3=3^(n-2) C(s,3). Point pairs and noncollinear point triples give these identities exactly, as in the accepted baseline. The profile entries for a 275-cap in dimension seven are at most112. Enumerating a=0..112, b=0..a, c=275-a-b with 0<=c<=b gives exactly341 types.

Take Q=9abc-899(ab+ac+bc)+15730000. On a+b+c=275,

    4Q=(3c-275)^2(c-67)+(899-9c)(a-b)^2.

Substituting 4ab=(275-c)^2-(a-b)^2 proves the identity by expansion. The exact global moment sum is

    9*243*C(275,3)-899*729*C(275,2)+15730000*1093=-246950.

Thus a global Q-minimum direction has Q<0. There are56 such basic types. Every transverse direction at that minimum must have Q at least its value. The 275 root and all resulting totals are derived for this target; no276 contradiction is imported.

## Local matrix inequalities

Fix a direction with layer sizes (A,B,C). A refinement produces columns alpha,beta,gamma, with their entries summing to A,B,C, respectively. Every column and every triple (alpha_i,beta_j,gamma_(-i-j)) satisfy the six-dimensional necessary profile predicate. Each of the three transverse whole-cap profiles is (alpha_r+beta_(r+s)+gamma_(r+2s)) for r=0,1,2. Its entries are at most112 and it avoids the fixed ordinary exclusions; only a minimum-direction certificate also imposes Q>=Q(A,B,C).

For T=sum_(i+j+k=0) alpha_i beta_j gamma_k and f=(T,E2(alpha),E3(alpha),E2(beta),E3(beta),E2(gamma),E3(gamma)), the364 refinement directions obey

    sum f=(121ABC,243C(A,2),81C(A,3),243C(B,2),81C(B,3),243C(C,2),81C(C,3)).

Additional upper bounds are the frozen non-completable106/107/108 whole-cap histogram functions. Their multipliers are nonnegative. In a whole slice contained in a112-cap, the completed-section features fam,small,label40 have exact sums56,11d,110d for d=112-N. If the original40-section label is ambiguous, the checker uses the smallest signed contribution over EVERY compatible label, including ties. These are the inherited interfaces; the statement concerns an entire six-dimensional slice, never one numerical profile's apparent completion.

A certificate q.g>=K on every allowed matrix, together with sum q.g<=U and364K-U>0, excludes the corresponding type or fixed-status minimum branch. Every quantity in the accepted records is integral. In C++, accumulation uses signed128-bit integers and the execution enables undefined-behavior sanitization.

## Frozen stages and exact verification

Four inherited ordinary seeds are (112,112,29),(112,111,35),(112,110,45),(111,111,45). Stage0 proves12 new ordinary exclusions using ONLY these seeds; stage1 found no new certificate and is empty. All minimum certificates use the same four seeds plus the completed stage0. No minimum certificate is reused as an ordinary exclusion or as a dependency of another minimum certificate.

The new ordinary types are

    (111,108,56), (110,109,56), (109,109,57),
    (112,105,58), (111,106,58), (112,104,59), (111,105,59),
    (112,103,60), (111,104,60), (112,102,61),
    (111,103,61), (111,102,62).

The recorded coefficients and integer gaps are in certificates.json. After these exclusions,40 negative types remain. There are76 successful minimum-direction certificates. Unsplit certificates cover all completion statuses; split certificates enumerate the two possible statuses for every layer of size103..108, require completion at size>=109, and leave layers below103 unrestricted. This closes30 whole minimum types and every branch except ten fixed states. The route's standalone checker verifies all88 certificates on153,548,040 matrices. It retains all ordered beta and gamma columns, rather than depending on discovery's paired-shear quotient. Root wrote another direct Cartesian checker from the raw JSON, without importing either discovery or route verifier kernels; it also checks all88 and the same total. These checks share the certificate coefficients and accepted mathematical lower-dimensional inputs.

The independently audited recovered three-deletion lemma proves at most50 third-layer positions after a total of three deletions from two112-caps. Therefore the two ordinary seeds (112,109,51),(111,110,51) close the remaining completed states (112,109,54),(111,110,54). This is a root-owned recovered scoped input with prior-overlap warning; it is not counted as new Route A mathematics.

## Verified remaining-case lemma

Consequently, if a275-point seven-dimensional cap exists, every global Q-minimizing direction has one of the following eight profiles, and its two large whole six-dimensional slices are both non-completable:

| Profile | Q |
|---|---:|
| (108,107,60) | -15704 |
| (108,106,61) | -12346 |
| (107,107,61) | -12696 |
| (107,106,62) | -9816 |
| (107,105,63) | -7064 |
| (106,106,63) | -7396 |
| (106,105,64) | -5086 |
| (105,105,65) | -3200 |

Proof: the negative global sum forces a negative minimum; the341-type ledger lists every possibility. Inherited seeds,12 ordinary certificates,76 minimum certificates and the recovered three-deletion seeds exclude every other possibility. Each surviving state is exactly(0,0,-1). This is a necessary-condition reduction, not existence of a cap or a proof that any surviving matrix is realizable.

## Common histogram attempt and stop

COMMON107_GATE.md registers one common107-cap histogram function, optimized jointly for the open pairs(108,107,60),(107,107,61),(107,106,62). Its inner proof family contains all47 admissible types and seven exhaustive first-occurring rare anchors, uses all three verified41-cap bounds jointly and all distinct existing42-cap functions, and imports no seven-dimensional assumption. The numerical search performed11 row-generation iterations in about15.1 seconds and produced no positive joint dual gap. It produced no exact new histogram certificate and proves no impossibility or exact feasibility. The declared common family attempt stops here; there is no unchanged per-branch restart.

The eight states remain unresolved. A further global improvement requires a constraint that excludes them with full model coverage; a numerical aggregate alone cannot supply that bridge.
