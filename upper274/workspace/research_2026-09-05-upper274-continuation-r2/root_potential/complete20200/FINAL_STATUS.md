# Complete 20/20/0 scoped input frozen

The full 682,344-choice actual family is enumerated. There are exactly eight directional histograms, with parameter values `r=0,1,2,3,4,5,6,10` and formula in `PROOF.md`. All are realized by explicit forty-point representatives. Histogram frequencies and the complete B-to-histogram assignment file are frozen in `FROZEN.json`; `HISTOGRAMS.json` has SHA256 `f3278815900918e48c0af51b7d88c8907c006b5451cd35fe52ee4b6ce198013d`.

Every actual lift passed all 780 pair completions, totaling 532,228,320 pairs. Every lift's 121 direction profiles were computed, totaling 82,563,624 profiles. A separate Ruby replay passed every representative, exact geometric parameter, and all assignment frequencies. The full polynomial catalogue was reused as an accepted shared input and was not reenumerated.

Status: `COMPLETE_SCOPED_FAMILY_INDEPENDENTLY_ACCEPTED_STOP_LINEAR_DUPLICATE`. Root's complete independent comparison passed, with all eight histogram vectors, all frequencies and 6,240 representative pairs matching; report `../../root_audit/complete20200/VERIFICATION.json`. L's exact old-constraint dual also confirmed that the linear input is already implied, so its linear research route is `STOP_LINEAR_DUPLICATE`. P read no root-generated 40-cap output before freezing. No LP or other family was executed.

Mathematical limitation: the eight vectors are collinear. Linear histogram optimization needs only the two realized endpoints r=0 and r=10, and their interval formula already follows from exact 20-section spectra. Thus finite exclusion of r=7,8,9 does not by itself provide a stronger linear constraint. Histogram count is not affine-class count; no complete classification of all 40-caps, new global upper bound, or publication-priority claim is made.
