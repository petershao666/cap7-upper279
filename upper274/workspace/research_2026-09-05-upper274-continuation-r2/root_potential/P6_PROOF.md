# Exact candidate for Q67-minimum NC/NC (107,106,62)

The certificate excludes the globally Q67-minimizing root profile `(107,106,62)` when the107- and106-point slices are non-completable. It is an extremal-state claim, not an ordinary profile exclusion. It does not independently establish the global upper bound274.

Frozen source: `incidence107_all5d_certificate_107_106_62.json`, SHA256 `3753f438b1021d1915d3c2d97a26f3be6a93899af6f69619e71ea76b3409ce6c`. The file specifies587 integer row descriptions and coefficients, all source functions, the ordinary bans and the target-specific Q67 minimum condition. All170 upper-row coefficients are nonpositive; equality coefficients are unrestricted.

The normalized distributions W and Z and shared107 marginals are exactly those derived in P5: W describes364 seven-dimensional refinements, Z describes11011 projective lines in the actual NC107 slice, with four orientations per line and121 lines through each direction. For every profile t, `sum k_t Z=4 sum 1_(alpha=t) W`; ordinary conditional moments give `sum(121f_t−F6(t)k_t)Z=0`.

P6 adds all33 accepted lower-dimensional functions from the root-audited schema `../compatibility/l2_all5d_10610663/FUNCTIONS.json`, SHA256 `92a0104c9db8bf04b55e503e2e71f523178dd134ca25045480ea55093a6f5336`:22 upper functions including theta40 and11 exact43/44/45 spectrum coordinates. Root independently matched every input to its accepted source in `../root_audit/all5d_input_independent.json`.

For a function h on size-v five-dimensional caps with bound B_h, group all size-v slices of each six-dimensional orientation of profile t. Let h_t(M) be their sum across every orientation of line M with profile t. Incidence counting gives

`sum_M [121 h_t(M)−r_v(t) B_h k_t(M)]Z_M <=0`,

with equality when h is an exact spectrum coordinate. The complete actual five-dimensional profiles are retained, including individually distinct profiles of equal-sized slices; grouped sums are used only when applying the theorem. The universal line domain contains every one of47 NC107 anchors, with no first-anchor prefix deletion.

All outer moments and upper histograms use the same centered rows as P5. The final normalization coefficients are

`q_W=687860485014`, `q_Z=−687403840428`,

whose sum is the strictly positive integer

`456644586`.

The integer row functional pairs to at most zero with every allowed outer table and every allowed inner line table. Each block's maximum is exactly zero. It also pairs nonpositively with every upper slack column because q is nonpositive on all170 upper rows. Therefore any nonnegative table distributions satisfying the exact normalization, marginal, moment and accepted histogram equations would force `q_W+q_Z<=0`, a contradiction.

Only one fixed outer histogram coefficient is nonzero:−30 on the accepted `joint106_107_106_63_size276` function of the106-point slice. Other saved fixed outer histogram coefficients are zero. The inner proof uses theta40, several accepted42-point functions and exact43/44/45 coordinates. It does not depend on the new universal41 research running in another route.

Discovery rebuilt all1407366 alpha-sorted raw NC107 line tables with all beta/gamma orderings and generated80583 complete60-entry feature records. The old40-entry cache was not used to derive the new features. Final independent route-side verification reconstructs the raw predicates and all33 function evaluations from accepted JSON in a separate C++ implementation, without the shared discovery generator or generated records. It checks6463458 all-ordered inner matrices and27457011 all-ordered outer matrices, attaining zero maxima and the stated positive RHS. Source/interface matching and signs are checked independently in Python. Results: `incidence107_all5d_interface_verification.json`, `incidence107_all5d_own_verification.json`.

Root independently accepted the certificate after checking6672783 raw matrices:1407366 inner and5265417 outer with alpha sorted and every beta/gamma ordering. Both maxima zero, all170 upper-row signs and RHS456644586 passed. The result is an accepted internal extremal-state exclusion; no publication-priority or standalone global-bound claim is made.
