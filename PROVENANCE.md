# Attribution, provenance, and version records

Project author and maintainer: **Heng Shao**. Please cite the exact release used, as specified in [CITATION.cff](CITATION.cff), and retain attribution to the original mathematical inputs.

The v1.2.0 result is an exact-arithmetic, computer-assisted exclusion of every 275-point cap in AG(7,3), giving `236 <= f(7,3) <= 274` under the stated lower-dimensional premises. It does not determine the exact maximum or establish whether a 237-point cap exists.

## Public checkpoints

| Version | Result | Public record |
|---|---|---|
| v1.0.0 | Upper bound 279 | [Release](https://github.com/petershao666/cap7-upper279/releases/tag/v1.0.0), published 2026-09-05 at 07:45:53 UTC |
| v1.1.0 | Upper bound 275 | [Release](https://github.com/petershao666/cap7-upper279/releases/tag/v1.1.0), published 2026-09-06 at 00:12:50 UTC |
| v1.2.0 | Upper bound 274 | [Release](https://github.com/petershao666/cap7-upper279/releases/tag/v1.2.0); consult the release page for its publication timestamp and fixed commit |

Release dates in citation metadata may use the author's local calendar date. GitHub publication timestamps are reported in UTC. A Git commit's author date, a tag date, and a server-recorded release publication time are distinct records.

The final upper-274 certificate is identified by SHA-256:

```text
78238a2e3f389f9c7a4f93e049ad56e678c09103151fb3bfed0adc6e1dcf14bf
```

Its final global verification record is identified by SHA-256:

```text
e7ff96ba398eabb3014ce06b3aef5210e78915aa92d3059cd164c657fdd2d4c4
```

Hashes identify exact bytes. They do not by themselves establish when those bytes were first created, mathematical correctness, or publication priority. The release bundles the statements, explicit premises, proof, coefficients, verification source, and execution evidence so the claim is inspectable.

## Contributions and shared inputs

Research, proof development, code generation, and computational audits used ChatGPT and Codex assistance. AI systems are not listed as scholarly authors. Separate verification programs and reviewers share frozen coefficients and explicitly cited mathematical inputs; the documentation states which components were independently implemented, freshly replayed, or inherited. No independent human peer review is claimed.

The low-dimensional classification and completion results are attributed to their cited original sources, including Potechin and Thackeray. Recovery and checking of published classification tables is not claimed as an original classification. The included 236-point lower-bound construction is an existing construction, not a new construction of this project.

## Citation and reuse

Use the release-specific citation and include the version when discussing numerical bounds or reproducing the certificate. The release record and complete evidence support attribution; this repository does not claim that a timestamp settles all questions of novelty or academic priority.

No repository-wide distribution license has been selected. Citation metadata is not a license. Third-party material retains its original attribution and applicable terms. A license choice for project code and explanatory text can be recorded in a later explicit update; no claim of exclusive ownership of mathematical facts is made.

No DOI, arXiv identifier, journal publication, affiliation, or ORCID is asserted unless explicitly linked in the citation metadata. A future archival DOI or manuscript should cite the exact version and preserve this provenance chain.
