# Next steps after the certified upper bound 275

Planning date: 2026-09-05. This is a proposed sequence, not a report of additional results. The established interval is 236 ≤ f(7,3) ≤ 275; existence of a 237-cap is still unknown.

## 1. Make the present result a readable, citable paper

The priority is to explain and preserve the 275 theorem without waiting for another numerical improvement.

1. Build a theorem-dependency table: exact external theorem statement and version, where it is used, which lemma is derived here, and which checker certifies each finite claim. Recheck the current and historical literature before describing 275 as a record or claiming a new theorem. A short web search is not a novelty audit.
2. Write a self-contained manuscript, tentatively *An exact-arithmetic upper bound of 275 for caps in AG(7,3)*. Suggested order: statement and literature; directional moments and local certificates; completion and large parallel slices; nested histogram bounds; the minimum-direction contradiction; reproducibility and limitations. Include one fully worked certificate in the text and put the full coefficient tables in the archived supplement.
3. Explain the reusable method. The contribution should be judged on the mathematical reduction, completion information, histogram inequalities and exact certificates; the raw evaluation count alone is not the scientific contribution. A useful additional deliverable is a dependency/ablation table stating which exclusions each ingredient actually proves, without treating failure of a weaker relaxation as proof of necessity.
4. Prepare a focused human-review packet, emphasizing the external theorem uses, the 109-point completion derivation, the one/two-deletion Fourier bounds, first-occurring-anchor case splits, and signed labelled features. A human mathematical review is a separate task from rerunning the supplied code. Contacting reviewers requires an explicit outreach instruction; no contacts have been made.
5. Resolve the author/contribution statement, affiliations and license, then archive the exact release with a DOI and prepare an arXiv submission. GitHub publication is already useful public disclosure, but neither a GitHub timestamp nor a DOI establishes novelty or constitutes peer review.

Zenodo can archive enabled GitHub repositories when releases are created, or accept a manual software upload. Existing v1.1.0 should be archived intentionally rather than assuming a subsequently enabled integration will retroactively capture it. See [Zenodo's release guide](https://help.zenodo.org/docs/github/archive-software/github-upload/) and [manual upload guide](https://help.zenodo.org/docs/github/archive-software/).

For arXiv, prepare a refereeable manuscript and TeX source. Registration and, for a new user or subject category, endorsement may be needed; submission remains subject to moderation. See the [official submission guidance](https://info.arxiv.org/help/submit/index.html) and [endorsement guidance](https://info.arxiv.org/help/endorsement.html). No arXiv or journal submission has been made. Select a journal after the novelty and human-review pass, rather than making an acceptance prediction from the bound alone.

**Completion artifacts:** manuscript TeX/PDF; dependency table; reviewed references; human-review issue log; versioned DOI record; submission-ready source archive.

## 2. Investigate upper 274 through a declared set of unresolved cases

The next numerical target is to exclude size 275. It is not established by v1.1.0. The source package mentions a separate `cap7_toward274_research.zip`; that continuation archive was not present among the audited inputs. Its contents and claimed progress must be recovered and checked before reusing them.

Before computation, register the exact target, admissibility predicates, symmetry convention, external inputs, candidate features, and finite resource limits. Compare each proposed domain with established results so that already-covered work is classified as replication.

The first deliverable should be a complete **case ledger**, not another long unconstrained search:

- Recompute the whole-cap direction types at total 275 from the stated hypotheses.
- Separate ordinary exclusions, minimum-direction conditions, and fixed completion-status branches.
- For every surviving branch, record either a checkable exact certificate or an explicit unresolved status. Keep heuristic/solver statuses separate from proof statuses.
- Identify the mathematical obstruction in the remaining branches and test a declared new family of constraints. Candidates include stronger bounds for non-completable six-dimensional slices, additional five-dimensional histogram information, or a three-deletion parallel-slice lemma. These are proposals; none is currently promoted to a theorem.

**Success gate:** every branch closed, all dependencies checked, integer certificates replayed by both full implementations, and the model-to-cap implication reviewed.

**Stop gate:** the declared feature family and finite compute budget are exhausted without a certificate. Record the unresolved cases and the limitation of that relaxation. Do not respond by only adding tokens, extending unchanged solver timeouts, or declaring a cap exists from feasible aggregate counts.

Aim for a lemma or parameterized family that removes several cases when possible. If only one further bound is obtained, release it as a new checkpoint while keeping the 275 manuscript stable until the stronger proof has passed the same audit standard. Do not promise 270 as an automatic consequence of the recent sequence of improvements.

**Completion artifacts:** preregistration; `case_ledger.json`; new lemma statements/proofs; exact coefficients; complete replay logs; either a fully audited 274 result or a bounded report of remaining cases.

## 3. Keep construction of a 237-cap as a separate objective

Improving an upper bound does not construct a larger cap. Any construction result must provide 237 explicit, distinct vectors in F3^7 and pass two independently implemented all-pairs checks. There are 27,966 pairs to check.

Only resume construction work after declaring a new mathematical object or bridge beyond already excluded families. Closed local replacement shells and bounded-degree graph families should not be rerun with cosmetic changes. Shared kernels and inputs must be disclosed when describing verification independence.

This route should not delay publication of the upper-bound theorem. Failure to construct a cap, solver timeout, or a feasible directional histogram leaves global existence unresolved.

## Immediate working order

1. Freeze and publish v1.1.0 with the complete audit evidence.
2. Produce the dependency table and manuscript outline, then the first readable manuscript.
3. Recover and audit the continuation materials; build the total-275 case ledger before launching a new bounded campaign.
4. Arrange human review and archival/submission preparation for the established result while assessing whether the unresolved branches suggest a useful general lemma.

The next recommended work session is **the theorem-dependency table plus the manuscript outline**. It directly improves the reviewability of the result already obtained and also exposes the most useful targets for further upper-bound work.
