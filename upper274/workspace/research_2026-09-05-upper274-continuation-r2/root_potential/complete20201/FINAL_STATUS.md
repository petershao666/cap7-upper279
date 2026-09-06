# Complete scoped input verified

The declared independent polynomial enumeration is complete. Every 41-cap admitting a 20/20/1 direction has the single exact histogram recorded in `HISTOGRAMS.json`: 40 directions of type (14,14,13), 20 of type (15,15,11), 20 of type (17,12,12), 40 of type (17,16,8), and one of type (20,20,1). All other direction types have count zero. `PROOF.md` gives the complete connection from the original object to the finite search.

Derived inventory: 59,049 coefficient vectors, 16,848 cap-valued forms, 8,424 distinct centered masks, 682,344 distinct translated 20-caps, and 198 disjoint second sections. All 198 actual lifts were checked. Exact mask inventories, a coefficient witness for each centered mask, and explicit representative points are preserved.

The primary source uniqueness assumption was verified before enumeration. P's outputs were frozen before reading H's outputs. A separate Ruby arithmetic replay of every P lift passed. After both freezes, full mask and histogram comparison with H passed, and H's representative passed direct coordinate checks. H's execution timing disclosure is preserved in `H_COMPARISON.json`; the two implementations share the published theorem but no enumeration kernel or generated inputs before P's freeze.

Status: `COMPLETE20201_SCOPED_INPUT_INDEPENDENTLY_VERIFIED`. Parent/root retains authority for integration and any further acceptance. This is not the complete family of all 41-caps, not an affine classification of the 198 lifts, not a new seven-dimensional upper bound, and not a publication-priority claim. No LP or additional research campaign was started.
