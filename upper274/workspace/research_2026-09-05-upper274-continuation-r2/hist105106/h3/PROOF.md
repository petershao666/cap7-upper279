# Verified histogram lemmas and exclusion of the(105,105,65) minimum branch

The result is conditional on the published and audited lower-dimensional inputs retained by the upper275 checkpoint, together with the additional published grid lemmas below. It is a scoped exact exclusion, not an upper274 proof. The global237-cap existence status remains UNKNOWN. No publication-priority claim is made.

## New published inputs and affine-grid coverage

We use Thackeray, *The cap set problem:41-cap5-flats*, [arXiv:2206.09719v1](https://arxiv.org/html/2206.09719v1), Lemmas2.2,2.4,2.5,2.6 and the19-/20-cap directional supports in the proof of Lemma2.3. The nine forbidden partial grids are transcribed in clashes.py. Stars place no restriction on a cell. Every grid is indexed by an affine quotientF3² of the ambient five-flat, so every affine coordinate change onF3² preserves impossibility. The432 maps in AGL(2,3) yield2664 distinct partial patterns, with nine orbit sizes216,432,432,432,432,216,216,72,216. Arbitrary cell permutations are not used. Root independently reconstructs the affine group by images of an affine basis and checks the resulting pattern set.

These are published exclusions; recovering and transcribing them is not itself claimed as new mathematics. They strengthen the earlier necessary grid model before any new histogram inequality is optimized.

## Exact19-/20-cap directional histograms

A19-cap inF3^4 has only the four types991,982,865,766 by the cited support theorem. Let their counts bex,y,z,w. Exact moments give

    x+y+z+w=40,
    21x+14y+2z=183,
    171x+108y+12z=1359.

Subtracting six times the second equation from the third gives15x+8y=87. Hencex≡1(mod8), while0<=x<=5, sox=1,y=9,z=18,w=12. No19-cap histogram is guessed.

For a20-cap, the two possible types are992 and866. TheirE2 values117 and132 and the forcedE2 sum5130 imply117x+132(40-x)=5130, hence the counts are10 and30. TheE3 identity also holds. These spectra are exact feature sums in the next level. Root independently enumerates the nonnegative integer solutions and confirms uniqueness.

## Universal40-cap histogram bound

Let theta be the integer function on all44 decreasing triples of total40 with entries<=20, given by histograms/40 in h3_result.json. For EVERY40-capD inF3^5,

    sum_[z] theta(profile_z(D)) <= B40=-1209524081280.

Proof: order the44 profiles as in the certificate and select the first that occurs. Earlier profiles are absent. For an anchor(A,B,C), enumerate all3x3 arrays of nonnegative entries<=9 such that every column and all nine transverse line triples satisfy the accepted four-dimensional predicate, all transverse whole-cap profiles avoid the earlier prefix, and no affine image of a published forbidden partial grid occurs.

The generic seven local featuresf=(T,E2(alpha),E3(alpha),E2(beta),E3(beta),E2(gamma),E3(gamma)) have forced sums

    F5=(13ABC,27C(A,2),9C(A,3),27C(B,2),9C(B,3),27C(C,2),9C(C,3))

across40 refinement directions. Append the proved19-/20-cap exact histogram features when a column has the indicated whole size. Every recorded local inequality is

    q·g(M)-sum_(s=0,1,2) theta(t_s(M)) >= K.

There are25 nonempty anchor branches and19 empty branches. Both complete verifiers check every branch. In a nonempty branch, summing its local inequality yields

    sum_[z]theta(profile_z(D)) <= theta(anchor)+q·F5-40K.

Taking the maximum over all25 recorded bounds gives exactlyB40. An empty branch cannot occur for a cap because it supplies no matrix for any refinement direction. No conclusion for one anchor is borrowed to prove another.

The independently verified enumeration retains EVERY ordered beta andgamma column after a common affine row relabelling sortsalpha. Across all44 branches,118944 matrices survive the inherited conditions; the published affine-grid exclusions leave117114. All local integer inequalities hold on that complete remaining domain. This proof neither assumes40-cap completion nor uses a41-cap classification.

## Universal non-completable105-cap histogram bound

Let phi be the integer function on the complete87-type non-completable105 profile support in histograms/105 of h3_result.json. For EVERY105-capE inF3^6 not contained in a112-cap,

    sum_[z]phi(profile_z(E)) <= B105=-3614141188092.

The support omits only audited universal six-dimensional forbidden profiles and completion-forcing profiles. The root inequalityq=(-77,2) on(E2,E3), recorded in selected_anchor_covers.json, forces one of17 rare anchor profiles. Choose the first occurring rare anchor and exclude exactly the complete preceding prefix.

At an anchor(A,B,C), the seven feature totals across121 refinements are

    F6=(40ABC,81C(A,2),27C(A,3),81C(B,2),27C(B,3),81C(C,2),27C(C,3)).

Append inherited exact43..45 column histograms and the audited41/42 histogram upper bounds. Every multiplier of a summed upper bound is nonnegative. For each40-point column, appendtheta of its directional profile with coefficient1 and use the independently provedB40 as its sum bound. Therefore the new40 lemma is established BEFORE this105 lemma; neither uses the seven-dimensional target.

Each recorded local inequality isq·g(M)+sum_(40-columns)theta(column)-sum_s phi(t_s(M))>=K. Its exact summed upper boundU gives the whole105 histogram boundphi(anchor)+U-121K. The maximum over the complete17-anchor cover equalsB105. Both independently written C++ programs check498731 matrices for this level with exact integer arithmetic. The full lower-dimensional function data and feature coefficients are retained in h3_result.json; inherited41/42 functions are matched against the frozen checkpoint by the root audit.

## Excluding one seven-dimensional minimum branch

Assume a275-cap inF3^7 has a globally minimizing direction for

    Q(a,b,c)=9abc-899(ab+ac+bc)+15730000

of type(105,105,65), with both105-point whole layers non-completable. For each refinement matrix, letalpha,beta,gamma be its three columns. The exact local inequality is

    573425 T
    -52910053 E2(alpha)+1265443 E3(alpha)
    -52910053 E2(beta) +1265443 E3(beta)
    -25735294 E2(gamma)+860383 E3(gamma)
    +phi(sort(alpha))+phi(sort(beta)) >= -190762786478.

Both verifiers check it on all7931724 admissible ordered matrices. The whole-cap transverse profiles obey the fixed ordinary exclusions andQ>=Q(105,105,65); this last condition is valid only at a globalQ minimum. The generic seven-dimensional moments and the twoB105 upper bounds give

    U=-69439581109599.

Summing the local lower bound over364 refinements instead gives

    364*(-190762786478)-U=1926831607>0,

a contradiction. Thus the(0,0,-1) whole-completion state of this minimum profile is excluded. It is NOT promoted to an ordinary exclusion of every(105,105,65) direction. Combined with the already verified other statuses, the profile is absent from the set of possible globalQ67 minimizers.

## Verification boundary and status

The route's standalone C++ verifier and root's independently written C++ verifier both use signed128-bit accumulation and undefined-behavior sanitization, retain all ordered beta/gamma columns, and agree on all62 cases:44 theta anchors including19 empty cases,17 phi anchors, and one outer case. Total matrix evaluations:8547569. They share published mathematical inputs and frozen coefficient data, but not enumeration implementation kernels. Root separately reconstructs the432 affine maps and19-/20-cap spectra in Ruby.

Frozen candidate file SHA-256:

    cbb4973544cf7e2388097bb333504dc0c53c943d1671605fa300996394dfd294

The accepted interval remains236<=f(7,3)<=275. The remaining sevenQ67 minimum states are(108,107,60),(108,106,61),(107,107,61),(107,106,62),(107,105,63),(106,106,63),(106,105,64), each with its two large whole slices non-completable. Further use oftheta orphi is permitted only through its proved universal scope; remaining cases are not assumed closed.
