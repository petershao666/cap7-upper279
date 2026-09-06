# An exact-arithmetic certificate for f(7,3) ≤ 274

**Latest release: [v1.2.0](https://github.com/petershao666/cap7-upper279/releases/tag/v1.2.0), establishing 236 ≤ f(7,3) ≤ 274.**

The proof excludes every 275-point cap in AG(7,3), using explicitly cited low-dimensional classification and completion results. Every larger cap would contain a 275-point subcap. The included construction has 236 points; the exact maximum and the existence of a 237-point cap remain unknown.

Start with the [upper-274 package guide](upper274/README.md), [mathematical proof and dependency map](upper274/workspace/research_2026-09-05-upper274-continuation-r2/root_audit/global274/PROOF.md), [provenance record](PROVENANCE.md), and [next steps](ROADMAP.md). The new package preserves the proof's source dependencies and verification evidence under `upper274/workspace/`.

## What has been verified

- The complete direction-profile and completion-state cover reduces a hypothetical 275-cap to eight remaining minimum-direction branches. **All eight are now excluded.** Minimum-only exclusions remain distinct from ordinary forbidden profiles throughout the proof.
- The final certificate's independent integer checks pass on **8,807,118 raw matrix rows** and **15,885 finite-support evaluations**. These cover three universal 40-point histogram inequalities, all 14 NC106 anchor cases, and the final seven-dimensional inequality.
- The last branch, (106,106,63) with both large sections non-completable to a 112-cap, has a strict integer contradiction gap of **148,616,699,075**. The final global bridge checks the complete profile/status cover and its certificate dependencies.
- The earlier **88 certificates on 153,548,040 raw matrix rows** remain inherited verification evidence. The final-certificate replay does not rerun that entire history or the published classification searches.

Row counts refer to evaluations within declared certificate covers, not distinct caps or affine-equivalence classes. The method verifies inequalities on necessary count configurations; it does not infer nonexistence from unsuccessful point searches or solver timeouts.

## Reproduce the release

From the repository root:

```sh
python3 upper274/verify_release.py --mode quick
python3 upper274/verify_release.py --mode final
```

`quick` checks the packaged evidence and global integration. `final` additionally performs the final certificate's complete integer replay. **“Final” refers to the last certificate, not a new proof of every inherited theorem or a rerun of all historical classifications.** See the [package guide](upper274/README.md) for requirements, commands, and the precise boundary between fresh replay and inherited evidence. No discovery optimizer is needed for certificate verification.

## Mathematical premises and provenance

The proof inherits the audited upper-275 baseline, including the specified Potechin and Thackeray bounds, classification and completion results. Additional finite inputs include complete 16- and 17-point histogram families and the complete five-dimensional 41-point family. The latter explicitly depends on Thackeray's Theorem 6.3 and the ancillary-list completeness assertion in Proposition 6.2(b). Reconstructing and checking published point lists does not independently reprove the completeness of those classification searches. The [proof's premise section](upper274/workspace/research_2026-09-05-upper274-continuation-r2/root_audit/global274/PROOF.md#premises-and-independence) records this boundary.

This is AI-assisted research. ChatGPT contributed earlier proof and certificate material; Codex-assisted continuation, mathematical review, and separately implemented exact checkers produced and audited the upper-274 extension. Discovery and author replay share enumeration code and are not counted as independent verification. The independent checker implementations still share mathematical inputs, certificate coefficients, and stated external theorems. Shared inputs are not independent mathematical sources, and these checks are not human peer review.

This release makes no publication-priority claim, no claim that a 274-point cap exists, and no novelty claim for the included 236-point construction. No distribution license has been assigned. See the [provenance record](PROVENANCE.md) for release timestamps and certificate hashes.

## Versions and citation

| Release | Certified interval | Materials |
|---|---|---|
| [v1.2.0](https://github.com/petershao666/cap7-upper279/releases/tag/v1.2.0) | 236 ≤ f(7,3) ≤ 274 | `upper274/` |
| [v1.1.0](https://github.com/petershao666/cap7-upper279/releases/tag/v1.1.0) | 236 ≤ f(7,3) ≤ 275 | `upper275/` |
| [v1.0.0](https://github.com/petershao666/cap7-upper279/releases/tag/v1.0.0) | 236 ≤ f(7,3) ≤ 279 | `cap7_upper279/` and historical root audit files |

The repository retains its original name for continuity. The v1.0.0 and v1.1.0 releases and their assets are preserved.

Heng Shao. *An exact-arithmetic certificate for f(7,3) ≤ 274*. Version 1.2.0 (2026-09-06). [GitHub release](https://github.com/petershao666/cap7-upper279/releases/tag/v1.2.0). Machine-readable metadata: [CITATION.cff](CITATION.cff).
