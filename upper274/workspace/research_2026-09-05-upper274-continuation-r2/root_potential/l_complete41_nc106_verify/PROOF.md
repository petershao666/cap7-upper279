# Independently verified universal NC106 histogram bound

**PASS.** For the function phi106 in the frozen candidate `compatibility/complete41_support_10610564/RESULT.json`, SHA256 `0fde44267b424bac9570b72813e8af4f0a44e0e7e87ba5ce9ae118af57881e97`, every NC106 cap satisfies

    sum over all 364 hyperplane directions of phi106(section-count type)
        <= -359979101924637.

The exact79-entry function, per-case calculations and source identities are retained in SOURCE_AND_SUPPORT_VERIFICATION.json and VERIFICATION.json. The three physical40 occurrences use the candidate's phi40 bound B40=-95858610055698, independently accepted by root. Ordinary six-dimensional restrictions and completion-forcing profiles, and the accepted published/classification inputs, remain explicit premises. This layer proves the stated universal NC106 bound; root separately verifies the40 layer and the seven-dimensional outer use. No outer/global conclusion is asserted by this component alone.

## Complete case cover and grid domain

For a106-cap let q(t)=E3(t)-39E2(t), where E2(a,b,c)=ab+ac+bc and E3(a,b,c)=abc. The six-dimensional moment identities give

    sum q = 81*C(106,3) -39*243*C(106,2) = -37112985.

There are364 directions, and364*(-101958)-(-37112985)=273>0. Hence some direction has q<-101958. Among all79 profiles left by the ordinary and NC-completion conditions there are exactly fourteen such types. They are the ordered anchors in the table below, independently regenerated in complete41_domain_audit/prepare_inputs.py. Choose the first anchor present in that declared order. No earlier anchor occurs in any transverse direction of this case. These prefix restrictions are conditional case restrictions, not ordinary prohibitions.

The independent domain proof is `root_potential/complete41_domain_audit/DOMAIN_DEFINITION.md`. For each fixed physical anchor, enumerate every ordered3x3 integer grid, cells0..20, with those column sums. All twelve affine grid lines represent5D sections and obey the frozen OLD five-dimensional profile predicate. The three transverse whole-cap profiles obey the accepted ordinary/NC-completion conditions and the case's earlier-anchor exclusion. L did not apply the newly known fourteen41-zero hard pruning. This verification likewise uses the complete old domain:1,120,785 ordered matrices, not only the95,343 discovery-cover rows.

The grid data were generated and frozen by P before reading H/L domain outputs. Each old raw file's SHA256 is checked again when compiling and finishing this replay. The independent generator also verified every18-element coordinate-label orbit and its stabilizer/cover multiplicities, so no equality of raw/cover counts is silently assumed. No physical-column permutation is used, including between the equal41 sections.

## Exact identities underlying a local certificate

Let a=(A0,A1,A2) be an anchor and let M be one refinement grid. Write t_j(M) for the sorted cell triple in physical column j, and u_s(M) for the whole-cap transverse type at slope s=0,1,2. Put T(M) equal to the sum of the nine products of the three cell counts on nonvertical affine grid lines. The seven exact local features are

    X0=T,
    X1=E2(t0), X2=E3(t0),
    X3=E2(t1), X4=E3(t1),
    X5=E2(t2), X6=E3(t2).

Summing over the121 projective lines through the anchor gives the exact vector

    F0=40*A0*A1*A2,
    F_(1+2j)=81*C(Aj,2),
    F_(2+2j)=27*C(Aj,3).

For the first identity, each triple with one point in each anchor section has nonzero sum because the set is a cap. The induced nonzero vector in the5D anchor kernel is annihilated by exactly40 of its121 projective covectors. For the other identities, restriction to a physical5D section runs through all121 of its directions exactly once; each pair contributes81 and each noncollinear triple contributes27. Thus the displayed values have the correct physical dimension and121 summation factor.

Append each declared exact43/44/45 profile indicator and its accepted spectrum multiplicity. Append each declared upper or new_upper function on its specified physical section and its declared121-direction bound. The exact feature coefficients may have either sign. Every upper/new_upper coefficient must be nonnegative; this audit checked all141 occurrences, including zeros and every new_upper entry. Their pointwise feature values and the complete sum/bound vector are independently reconstructed from the JSON descriptor and accepted sources. No discovery-centered or floating-point feature matrix is used.

There are six independently labeled physical41 support functions g_(a,j), two in the first case and one each in cases1,4,8,12. Each has

    B_(a,j) = max over all44 accepted41 histograms h of h dot g_(a,j).

All264 exact support values were independently computed; each maximum equals its claimed integer bound. Functions belonging to different physical sections remain separate. The complete44-histogram family includes extendible41-caps and is accepted with its published coverage premises. Restriction to each actual41 section therefore bounds the sum of its own g by its own B. No compatibility or common-isomorphism assumption between41 sections is needed.

For each case the replay verifies on every raw matrix the exact inequality

    q_a dot X(M)
      + sum_(physical40 columns j) phi40(t_j(M))
      + sum_(physical41 columns j) g_(a,j)(t_j(M))
      - sum_(s=0,1,2) phi106(u_s(M)) >= K_a.

Summing the121 refinements gives

    sum_all364 phi106
      <= phi106(a) + q_a dot F
         + sum_(physical40 j) B40
         + sum_(physical41 j) B_(a,j) -121*K_a = B_a.

For upper-only features the inequality direction follows precisely from their nonnegative q coefficients. Taking the maximum over all fourteen first-anchor cases proves the universal bound.

## Independent full integer replay

`prepare_exact.py` uses only JSON and Python arbitrary-precision integers to validate descriptors, full spectrum bounds, physical interfaces and signs, and to compile the separately additive physical-column contributions. `replay_raw.cpp` reads the frozen independent9-cell grids. It computes the nine affine-line products and the three transverse profiles directly from those nine cells, then evaluates the compiled integer row using signed128 arithmetic. It does not read H/L domain caches or the discovery19-feature rows. Every finite minimum equals the frozen K, and an explicit minimizing9-cell grid is retained.

`finish_verification.py` then evaluates all fourteen witnesses again directly from the original candidate JSON coefficient vector, its uncompiled individual features, and child functions, using Python integers. It independently reconstructs q dot F and all child-bound sums, checks each B_a, and computes the maximum. The largest per-row conservative absolute-value bound is71,755,360,781,300, far below2^126. The C++ replay took0.080seconds and2.72MB peak RSS; the entire registered verification uses no LP and is well below600seconds/1GiB.

| Case | Anchor | Full ordered grids | Exact minimum K_a | Exact B_a |
|---:|---|---:|---:|---:|
|0|(41,41,24)|375138|-2805556705387|-359979366630494|
|1|(42,41,23)|210663|5983770610462|-359979359096561|
|2|(42,42,22)|121368|6873340120330|-359979296220136|
|3|(43,40,23)|87048|22897972172088|-359979367267198|
|4|(43,41,22)|84375|14245902736582|-359979367280727|
|5|(43,42,21)|49803|21414266600061|-359979101924637|
|6|(43,43,20)|22077|31740373605160|-359979367282625|
|7|(44,40,22)|45693|29011988533774|-359979367288210|
|8|(44,41,21)|44640|-22065503299143|-359979367021901|
|9|(44,42,20)|26379|26117568291712|-359979341827243|
|10|(44,43,19)|11709|37936851549648|-359979367286650|
|11|(45,40,21)|16350|-37591435062860|-359979367277088|
|12|(45,41,20)|16038|-50499033641184|-359979367271636|
|13|(45,42,19)|9504|-33044938213268|-359979345875460|

The maximum B_a is attained by case5, yielding B106=-359979101924637.

## Input checks and independence boundary

All23 applicable41/42 upper functions, including centered_theta41 and centered_theta42, were independently evaluated on their entire accepted spectrum families, giving an actual finite maximum no larger than the declared bound. The report preserves every spectrum value, maximizer, declared bound and coefficient occurrence. This avoids inheriting old41 optimization proofs merely to justify those fixed functions. Exact43/44/45 coordinate sums are checked against the unique accepted spectra. All centered_theta40/41/42 formula tables and bounds were also matched to their frozen transport sources with the exact common constant shift.

The sole40 fixed upper function centered_theta40 has coefficient zero in every one of its three NC106 occurrences. No actual full40 maximum is fabricated for it, and its unneeded bound is not used in the proof. The different child function phi40 occurs with coefficient+1 and uses root's separately independently verified B40; ACCEPTED_DEPENDENCY.md records this boundary.

Shared inputs are the candidate coefficients, complete41 spectra, baseline42--45 spectra, accepted ordinary/completion theorems, and root's accepted child40 theorem. The P domain generator is reused between P's domain and certificate tasks, explicitly disclosed. Neither task imports H/L/root computational kernels. This is independent certificate verification with shared mathematical/source premises; it is not an independent reproof of the published classifications.

Terminal artifacts: VERIFICATION.json for all fourteen minima and whole bound; SOURCE_AND_SUPPORT_VERIFICATION.json for coefficients, exact support values, source/sign checks and row-compilation tables; RAW_VERIFICATION.json for the complete raw replay and witnesses; and MANIFEST.json for file identities. Root's separate integration determines any seven-dimensional branch consequence.
