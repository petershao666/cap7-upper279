# Independent source and scope audit of the complete 5D41 histogram packet

**PASS_WITH_EXPLICIT_PUBLISHED_PREMISES.** The frozen candidate with SHA256 `9dc0610051533cdad6ad98ac05f9ef32c9d0bc1a787283b1aced1a650f7c2584` has a valid coverage chain for arbitrary 41-point caps in AG(5,3). Subject to the explicitly cited published classification and supplementary-list completeness, and the component numerical acceptances listed below, its 44 vectors are exactly the possible full-direction histograms. There is no unresolved coverage gap in this chain. This is recovery and verification of published finite inputs, not a new classification, a count of affine classes, or a new global bound.

This audit is separate from H's producer and root's numerical representative audit. It independently read the primary TeX statements and proof paragraphs, inspected the raw-file identities and companion-source semantics, and checked the static family union with new code. It did not rerun the author's search, execute Java, run an LP, or enumerate another geometric family.

## 1. Primary source and exact quantifiers

The primary source is H. R. Thackeray, arXiv:2206.09719v1, [primary article](https://arxiv.org/html/2206.09719v1). The independently downloaded local source is `root_potential/named41_45_source/CapSetProblem5S41.tex`; the accepted HTML is `hist105106/h13/source_article.html`, SHA256 `1382f2b23698b0aea3ec1ceeb4999e9ae46aeee5c542fd5f200ce98caeaa46d1`. Full source identities inspected by this audit are frozen in `STATIC_VERIFICATION.json`.

The beginning of Section 6, TeX line 405, declares C to be an arbitrary 41-cap 5-flat. There is no initial completeness assumption. Proposition 6.2, lines 438–443, assumes absence of directions (20,20,1) and (18,18,5). Part (b), under the additional presence of (18,17,6) or (18,16,7), gives the two deletion families, named F–I, or a complete cap with the specified saddled-cube intersection. Its parenthetical sentence explicitly says the supplementary lists cover all isomorphism classes for this last option, allowing more than one representative per class. These initial absence hypotheses must accompany a standalone use of Proposition 6.2(b); the global union instead invokes Theorem 6.3 directly.

Theorem 6.3, lines 555–559, covers every 41-cap with 13 alternatives and repeats the supplementary-list coverage in its proof for alternative 13 itself. The alternatives and their finite carriers are as follows. All carriers are accepted numerical inputs; the static audit independently confirmed that every carrier vector occurs with its source label in the frozen candidate.

| Alternative | Published scope | Complete finite carrier in this integration |
|---|---|---|
| 1 | A 45-cap minus four points | All 148,995 four-deletions of the accepted affine-unique 45-cap; 27 histograms |
| 2 | Delta686 minus one point | All 42 single deletions of the accepted named Delta686 representative; 2 histograms |
| 3 | 41A | Accepted named A point representative |
| 4 | 41B | Accepted named B point representative |
| 5 | 41C | Accepted named C point representative |
| 6 | 41D | Accepted named D point representative |
| 7 | 41E | Accepted named E point representative |
| 8 | 41F | Accepted H9 named F point representative |
| 9 | 41G | Accepted H9 named G point representative |
| 10 | 41H | Accepted H9 named H point representative |
| 11 | 41I | Accepted H9 named I point representative |
| 12 | A complete cap admitting (20,20,1) | Accepted enumeration of every cap admitting (20,20,1), complete or not; 1 histogram |
| 13 | A complete cap with no (18,18,5) direction, with a saddled cube shared by the indicated 18-section in an (18,17,6) or (18,16,7) direction and another section of size 18, 17 or 16 | All 34,345 actual positive raw outputs of the two specified ancillary searches; 41 histograms, including safe extra actual caps |

The theorem asserts unique membership among alternatives 1–12 only for caps outside alternative 13. It does not make alternative 13 disjoint from the others. The union retains overlaps and therefore does not need a disjointness claim. The named-cap remark preceding the theorem says A–I are pairwise nonisomorphic and complete; this is consistent with retaining each named alternative even when its histogram occurs in another source family.

## 2. Extendible caps are not lost

Completeness is a condition on alternatives 12 and 13, and a separately stated property of the nine named representatives; it is not a restriction on the theorem's universe. The packet does not apply a complete-cap filter to the two deletion families.

There is also a direct check using the 42-cap clause of the same theorem. If a 41-cap C is extendible, choose one point x making D=C union {x} a 42-cap. The theorem puts D either inside a 45-cap as a three-deletion, or in the affine orbit of Delta686. Removing x puts C in alternative 1 or 2. This argument uses all 42 deletions of Delta and all four-deletions of the 45-cap; no transitivity on deletion subsets is assumed. Thus the two finite deletion carriers cover every extendible 41-cap, including any extendible raw outputs or (20,20,1) outputs included redundantly elsewhere.

The static code checks that the two recorded Delta deletion-index groups form exactly a partition of 0 through 41, and that the four-deletion frequencies sum to 148,995. Their actual geometric completeness was already independently accepted; this audit does not substitute these arithmetic checks for that prior verification.

## 3. What affine uniqueness is, and is not, needed

Theorem 4.3, TeX lines 346–350, explicitly identifies every 45-cap with the representative in the paper. Therefore one accepted 45-point representative and all its four-deletions cover alternative 1: an affine isomorphism carries each four-subset to a four-subset.

The paper does not claim affine uniqueness of all 41-caps or of all 42-caps. We make neither assumption. Its 42-cap conclusion has two families, 45-minus-three and Delta686; it cannot be replaced by a single 42-point representative. Delta686 is defined at TeX line 175 as the affine orbit of the specified representative, as are A–E. F–I are similarly defined at line 417. These definitions justify using one point representative for each named orbit. The accepted (20,20,1) enumeration separately depends on the published affine uniqueness of the 4D20-cap and its full affine catalogue; that lower-dimensional classification is an explicit inherited premise of that component, not a claim that the 41-cap itself is unique.

Every 41-cap spans a 5-flat because a 4-flat has at most 20 cap points. Thus there is no hidden non-spanning case outside the stated 5-flat classification.

## 4. Raw outputs, summary, and reduction notes

The two raw carriers are identified by their content headers, not merely by filenames. They state the physical section cases {18,6,17} and {18,7,16}, respectively, which sort to the two directions in Proposition 6.2(b).

| Ancillary basename | Bytes | Lines | SHA256 |
|---|---:|---:|---|
| `Dim5_41_180617_SetDim5Cap43_9And8_ExclPtCounts_Data.txt` | 1,038,667 | 19,884 | `55e3a7eb2980c10096f38199e7834631d711a296a14826903afd7fc7e474641a` |
| `Dim5_41_180716_SetDim5Cap43_9And8_ExclPtCounts_Data.txt` | 878,638 | 17,142 | `fadaa04086ca80c94a4614e312cb94ff21eea81a142320e8e8d635133adaaedc` |

The primary URLs are recorded in `root_audit/exceptional41_raw/SOURCE_MANIFEST.json`. This audit independently recomputed both hashes, byte counts and line counts. The Section 5 method explains the data semantics: normalize two compatible 4D sections, retain the relevant shared-section symmetry possibilities, then fill the remaining four 3D cells. The proof of Proposition 6.2(b), TeX line 518, sends each count-matrix branch to contradiction, an earlier profile case, or one of its stated alternatives, and refers to the supplementary files for full search results. Theorem 6.3 then explicitly covers the final exceptional alternative by those lists.

`Dim5_41_CapsFound.txt` is a compressed summary of outputs, not a coordinate list to expand naively. In particular, its displayed ranges and some late containment descriptions need not have expansion cardinality equal to the number of actual caps. `Dim5_41_CapsFoundArguments.txt` contains reductions and named diagrams, not an additional exhaustive point catalogue. The 4D workbooks supply building blocks; they are not lists of 5D41-caps. The spreadsheet checks of list compression cannot replace the published full coverage assertion.

The accepted carrier correspondence is recorded in L's `RAW_SUMMARY_MATCH.json` and `RAW_AMENDMENT.md`: 49 positive saddled-cube blocks in the first raw file, containing 17,775 rows, and 28 in the second, containing 15,774 rows. The entire multiset of 77 pairs (count matrix, reported positive count), retaining repeated matrices, matches the 77 saddled-cube blocks of CapsFound. All raw footer counts match explicit output-row counts. This is the carrier bridge from the summary lists to the decoded raw records. These block and row checks are accepted shared finite inputs; this source audit did not rerun their point decoding.

The packet conservatively retains every positive raw format: 33,549 saddled-cube rows, 60 General9 rows, 432 cube rows, and 304 square-antiprism rows, totaling 34,345. General9 and the two other 8-cap shapes have their own catalogue/map semantics; they cannot be decoded as saddled cubes just because some column layouts agree. H/L independently implemented the complete decoding and compared all point payloads. Root accepted the complete source-row bijection and the representative histogram arithmetic. These numerical facts are explicitly inherited here.

The Arguments text excludes or identifies some already-handled families while discussing later cases; it eventually assigns remaining configurations to 45-minus-four or the complete saddled-cube option. Those reductions are not new global prohibitions. This integration applies none of those informal reductions as a filter on the accepted raw packet. In particular it retains cube and square-antiprism outputs, any earlier-case raw cap, and any overlap with named/deletion families. Hence it is not sensitive to a compressed summary expansion or to deciding which duplicate output should have been removed. Earlier cases are also covered by the other twelve alternatives. The {17,17,7} and {17,16,8} branches are reduced to (a) or (b) by Proposition 6.2(c); they are not an omitted fourteenth family.

The initial source audit's missing-raw-file obstacle was superseded by RAW_AMENDMENT and subsequent decoding acceptance. Its provisional grid convention must not be used in place of the accepted decoder convention: both raw coordinate axes have labels in the order (2,0,1). Root's accepted checks use the corrected convention and verify all recorded count matrices. This is resolved provenance history, not a remaining coverage condition.

Crucially, matching raw and summary records, even with all cap points checked, is not a fresh proof that the author's search found every required isomorphism class. The exhaustive-search/list assertion remains a published premise. The present conclusion intentionally states that premise rather than hiding it behind numerical agreement.

## 5. Accepted dependencies and independent static checks

The component acceptances used are:

- `root_audit/named41_pdf/ACCEPTED_POINTS.json`: independently reconstructed A–E and the 45-cap, including comparison with the EPS/orbit reconstructions.
- `root_audit/fortyfive/ACCEPTED_FOUR_DELETE_HISTOGRAMS.json`: all 148,995 four-deletions, independently computed by root and P using different occupancy algorithms.
- `root_audit/h9_named_independent.json`, together with the accepted H9 point/histogram files: F–I and all Delta single-deletion histograms.
- `root_audit/complete20201/ACCEPTED_HISTOGRAM.json`: the complete (20,20,1) family, using independent quadratic catalogue and lift computations.
- `root_audit/exceptional41_raw/ACCEPTED_RAW_HISTOGRAMS.json` and `ROOT_VERIFICATION.json`: all 34,345 raw records, their 41 spectra, H/L full point-row agreement and root source/representative checks.

`check_static.py` imports only the Python standard library. In 0.037 seconds it checked all 15 hashes in the candidate freeze, all 13 source hashes in its input snapshot, both raw-file identities, and a separately assembled set/multiset union from the accepted component tables. It compared the complete vector attached to every source family, not just the union cardinality. It obtained all 80 source occurrences and exactly 44 distinct vectors, with no lost alternatives or silently replaced family. It also reproduced all nine named-cap entries of the paper's three-row Table 2, and checked the two moment identities and total 121 for every component histogram. The test computes no new point family and does not import any producer, decoder, or root numerical kernel.

The arithmetic result is frozen in `STATIC_VERIFICATION.json`. Its candidate hash is the one stated at the beginning of this report. A future change to the candidate or source tables requires another identity/union check; this audit does not grant acceptance to an arbitrary later file with the same name.

## 6. Why this is the full histogram family

For a cap C, let h_C(t) count the 121 one-dimensional dual subspaces whose three parallel sections have sorted point-count triple t. The bound C4 <= 20 and the fixed total 41 give exactly 40 possible formal triples. If x maps to Ax+b under an invertible affine map, a dual form maps to its composition with A, and b only permutes its three levels. Thus the whole sorted-triple histogram is invariant under affine isomorphism.

Let U be the frozen 44-vector union. For any actual 41-cap, apply Theorem 6.3. Each of its 13 alternatives has the complete finite carrier established above; affine invariance puts its histogram in U. Conversely, every vector in U has an accepted explicit actual 41-point cap witness with its full-direction histogram. Therefore U equals the actual histogram family. Keeping extra actual caps in two of the carriers cannot invalidate this equality: their histograms already belong to the target universe.

Consequently the 14 types absent from every vector are ordinary all-direction exclusions for 5D41-caps once root integrates this accepted coverage proof and finite checks. They are not statements about only a selected minimum direction, and no seven-dimensional minimum-only exclusion has been promoted to an ordinary one. The number 44 counts histograms only; caps with one histogram may lie in several affine classes. No new global 7D bound follows from this source audit alone.

**Terminal classification:** PASS_WITH_EXPLICIT_PUBLISHED_PREMISES; no source/logic gap identified in the frozen packet. Published premises retained: 5D Theorems 4.3 and 6.3 including their supplementary-list completeness; the 4D cap bound; and the accepted lower-dimensional classification premises of the (20,20,1) input. Numerical premises retained: the named, deletion, raw-decoder, and 20201 component acceptances. Global-bound status is unchanged by this audit.
