# Finite-support and summed-inequality audit

Status: `PASS_FRESH_STDLIB_FINITE_SUPPORT_AND_143_SUMMED_BOUNDS`.

This is an explicitly requested replication, not a new mathematical result. The
new Python implementation reads the frozen certificate and accepted histogram
tables directly and imports no research code. Existing checker sources were
read for their data schema and the summed-inequality convention.

The checks recomputed all 96 physical-column support maxima (15,885 total local
support and conditional evaluations), the 267 permitted ordered 18/18 state
pairs, the 16 permitted 20/18 states, and all used finite-spectrum upper bounds.
The actual 16-, 17-, 18-, 41-, and 42-point histogram families have respectively
376, 102, 17, 44, and 4 members. Their direction counts and second/third moment
identities pass. Embedded 17-point data have different type/member ordering and
additional point witnesses; equality holds after normalizing histogram maps.

The checker also recomputed all 143 local summed bounds, checked 171 nonnegative
upper coefficients and 258 exact indicator features, and checked parent anchors
and physical columns. It obtained

```
B400 = -9829345995830952
B401 = -9618859046048364
B402 = -10564264755104425
B106 = -35039780423844643
Kouter = 43471588119828
Uouter = 15823509458918317
364*Kouter - Uouter = 148616699075 > 0
```

All twelve fixed-function outer coefficients vanish. The certificate SHA-256 is
`78238a2e3f389f9c7a4f93e049ad56e678c09103151fb3bfed0adc6e1dcf14bf`.
Forty frozen-hash comparisons pass; repeated references are recorded rather
than claimed as independent files.

Scope limits: the pointwise raw-domain minima, the complete source
classification theorems, the older seven branch certificates, and the global
minimum-direction bridge were not re-proved here. Those are separate audit
components. The H3-derived centered 40-point function is checked by exact
centering of its accepted bound. Identical certificate coefficients and
histogram/classification inputs are shared dependencies.

Run: `python3 /private/tmp/cap274-review-20260906/support_audit.py`.
Full machine-readable details: `support_audit.json` in this directory.
