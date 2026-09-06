# Candidate complete 5D41 histogram family: source coverage and exact union

This is a finite recovery of published classification inputs. It is not a new classification or a global upper-bound improvement. Each component input has been independently accepted by root. The complete union and source-coverage inference remain pending root's final audit and P's independent coverage confirmation at this freeze.

## Scope and source reading

The primary source is Thackeray, arXiv:2206.09719v1, local `hist105106/h13/source_article.html`, SHA256 `1382f2b23698b0aea3ec1ceeb4999e9ae46aeee5c542fd5f200ce98caeaa46d1`. The statement at `S6.Thmtheorem3.p1.1`, Proposition6.2(b) at `S6.I1.ix2.p1.1`, and the theorem proof at `S6.p10.1` were read directly from this source. This proof paraphrases their precise logical scope; `SOURCE_ALTERNATIVES.json` maps all thirteen alternatives to finite inputs. No completeness assumption on the cap being classified is added to the theorem's opening universal quantifier.

The thirteen options are: (1) a 45-cap minus four points; (2) Delta686 minus one point; (3)-(11) the nine named caps 41A through41I; (12) a complete cap admitting a direction with section counts (20,20,1); (13) a complete cap with no (18,18,5) direction and with the stated saddled-cube intersection between an18-section in an (18,17,6) or (18,16,7) direction and another section of size18,17 or16. The theorem asserts unique membership among the first twelve only for caps outside the thirteenth alternative. We neither infer disjointness of alternative13 nor discard overlaps.

Proposition6.2(b) starts with the presence of an (18,17,6) or (18,16,7) direction. Its possibilities are 45-minus-four, Delta-minus-one, F,G,H,I, and a complete cap with the specified saddled-cube intersection. Its parenthetical statement says the supplementary lists cover every isomorphism class in that last option, with duplicate representatives permitted. Independently of an inference through that proposition, the proof of Theorem6.3 explicitly restates supplementary-list coverage for alternative13. That stated completeness of the published lists is a literature premise. Replaying output coordinates does not itself prove the published search complete.

The remark at `Thmremarkx5.p1.1` states that the nine named caps are complete, pairwise nonisomorphic, and have no (20,20,1) direction. Those are source statements; we do not need to test completeness to use their accepted point representatives. Section4, especially `S4.p1.1`, records the affine uniqueness of the45-cap and reproves it. This premise is necessary to cover every45-minus-four alternative using one45-point representative.

## Coverage of the finite components

Alternative1 is covered by all C(45,4)=148995 deletions of four points from the accepted unique45 representative. The root/P independent enumeration yields27 spectra and representative point tables. Alternative2 is covered by all42 single deletions from the accepted named Delta686 representative, giving two spectra. Deletion indices in the two recorded groups partition0..41; this merge uses the already accepted complete deletion computation and rechecks one representative per resulting spectrum. Both alternatives contain extendable41-caps, so an attempted restriction of the whole classification to complete caps would be incorrect.

Alternatives3-7 use root's accepted independent PDF reconstruction of A-E, compared with P's EPS reconstruction. Alternatives8-11 use the already accepted H9 F-I primary point inputs. Every named representative is explicitly present in the union, regardless of whether its spectrum occurs elsewhere.

Alternative12 is covered by the accepted complete enumeration of **all**41-caps admitting (20,20,1), not merely complete ones. It has one spectrum. Including any extra extendable members is safe. Its separate proof normalizes one20-section and the singleton, uses the published unique20-cap input, and enumerates the entire affine20 catalogue. That proof is not rerun here.

Alternative13 is covered by the accepted decoding of all34345 positive raw output rows:33549 saddled-cube,60 General9,432 cube and304 square-antiprism outputs. The raw-source mapping is a checked bijection, including every positive record of all four formats. Their41 spectra are retained without applying a completeness test or removing caps with an (18,18,5) direction. The source theorem requires coverage of a subclass, and using a larger family of actual41-caps is safe. The earlier SC-only fixture is disclosed as shared; the two complete producer implementations froze independently before comparing all raw point payloads. Root additionally audited all source/row mappings and the shape formulas.

## Why the union is the exact histogram family after acceptance

A histogram records, for each sorted triple(a,b,c) with a+b+c=41 and20>=a>=b>=c>=0, the number of one-dimensional subspaces of the dual whose three parallel4-flats meet the cap in those sizes. There are40 formal triples and (3^5-1)/2=121 directions. The bound C4<=20 makes this domain exhaustive. A41-cap necessarily spans the5-flat because a4-flat contains at most20cap points.

An invertible affine map permutes the121 dual directions and permutes the three levels of each direction. Thus the sorted-triple histogram is an affine-isomorphism invariant. The source classification and component coverage imply that every41-cap has a histogram in the candidate union. Conversely, every union vector has an explicit41-point representative, and every representative has passed the cap and histogram checks below. Therefore, once the final coverage and union audit are accepted, the union is exactly the set of possible histograms, not merely a convex relaxation. This statement concerns44 histograms, not44 affine-isomorphism classes.

The static union contains44 vectors from80 source occurrences:41raw +1all20201 +4F-I +2Delta-deletion +5A-E +27four-deletion. Multiple provenance labels remain attached to the same vector. The only vectors absent from the raw41-spectrum set are those supplied by all20201,41B and41C. Sharing a vector does not replace a proof that an entire classification alternative is covered.

## Exact representative verification and outputs

For each of the80 source occurrences, `merge.py` verifies41 distinct points in F3^5, all820 unordered pairs (the third point -p-q is absent), and all121 normalized dual vectors with first nonzero coordinate1. Every full40-coordinate vector equals its expected source histogram where that source stores one. The moment checks are sum(h)=121, sum(h(ab+ac+bc))=66420 and sum(habc)=287820. The total representative checks are65600 pairs and9680 directions. This is a small input merge, not a repeated34345-row replay. Its implementations reuse basic histogram arithmetic from prior work and are not claimed to be an independent audit of those same source inputs.

`CANDIDATE_UNION.json` retains every source label, source hash, source-specific representative point table and histogram index. `REPRESENTATIVE_POINTS.tsv` gives one explicit table per union vector. `INPUT_SNAPSHOT.json`, `SOURCE_ALTERNATIVES.json`, and `DEPENDENCY_DAG.json` state the dependencies. Files prefixed `PRE_ACCEPTANCE_` preserve the initial candidate state before the two pending component acceptances arrived. The final frozen candidate has no pending component family; final union and source audits remain explicit.

## Ordinary five-dimensional zero-support corollary

Across the44 vectors,26 of the40 types occur and14 never occur. The zero types are:

(19,11,11), (19,12,10), (19,13,9), (19,14,8), (19,15,7), (19,18,4), (19,19,3), (20,11,10), (20,12,9), (20,13,8), (20,14,7), (20,17,4), (20,18,3), (20,19,2).

After complete-family acceptance, each is excluded for every direction of every5D41-cap. This follows because a nonnegative count is zero in every possible histogram. These are ordinary **5D41** profile exclusions; no condition involving a seven-dimensional minimum direction is being removed. This corollary recovers information from the complete published family; no claim of a new global bound or publication novelty is made.
